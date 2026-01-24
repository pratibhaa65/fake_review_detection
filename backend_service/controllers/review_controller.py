from database.db import SessionLocal
from database.models import Review, Product
import time
import json
import hashlib

# ---------------- CONFIG ----------------
WINDOW = 60          # seconds
MAX_SAME_PRODUCT = 2 # reviews per IP per minute
MAX_SAME_PAYLOAD = 2 # identical payload allowed

# In-memory store
request_store = {}

# ---------------- UTILS ----------------
def hash_payload(payload: dict) -> str:
    payload_str = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(payload_str.encode()).hexdigest()


def clean_store(key):
    now = time.time()
    request_store[key] = [
        t for t in request_store.get(key, []) if now - t < WINDOW
    ]


def track(key):
    clean_store(key)
    request_store.setdefault(key, []).append(time.time())


def check_limits(ip: str, payload: dict):
    ip = f"{ip}"
    payload_key = f"{ip}:payload:{hash_payload(payload)}"

    clean_store(ip)
    clean_store(payload_key)

    # 🚫 Three review per ip per minute
    if len(request_store.get(ip, [])) >= MAX_SAME_PRODUCT:
        raise ValueError("Mutiple reviews detected . Please try again later!")

    # 🚫 Copy-paste spam
    if len(request_store.get(payload_key, [])) >= MAX_SAME_PAYLOAD:
        raise ValueError("Duplicate review detected")

    track(ip)
    track(payload_key)


# ---------------- MAIN LOGIC ----------------
def add_review(product_id, data, ip):
    if not data.get("review") or not data["review"].strip():
        raise ValueError("Review text is required")

    rating = int(data.get("rating", 0))
    if not (1 <= rating <= 5):
        raise ValueError("Rating must be between 1 and 5")

    payload = {
        "product_id": product_id,
        "reviewer": data.get("reviewer", "").strip(),
        "rating": rating,
        "review": data["review"].strip(),
    }

    check_limits(ip, payload)

    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError("Product not found")

        review = Review(
            product_id=product_id,
            reviewer=payload["reviewer"],
            rating=rating,
            review=payload["review"],
        )

        db.add(review)
        db.commit()
        db.refresh(review)
        return review

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()



def delete_review(review_id):
    db = SessionLocal()

    try:
        review = db.query(Review).filter(Review.review_id == review_id).first()

        if not review:
            raise ValueError("Review not found")

        db.delete(review)
        db.commit()

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()
