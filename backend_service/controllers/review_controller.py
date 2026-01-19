from database.db import SessionLocal
from database.models import Review, Product
import time
import json
import hashlib

# In-memory store (persists while server is running)
request_store = {}

LIMIT = 2          # max same payload
WINDOW = 60        # seconds

def hash_payload(payload: dict) -> str:
    payload_str = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(payload_str.encode()).hexdigest()


def get_client_ip(request):
    return request.remote_addr

def check_duplicate(ip: str, payload: dict):
    payload_hash = hash_payload(payload)
    key = f"{ip}:{payload_hash}"
    now = time.time()

    if key not in request_store:
        request_store[key] = []

    # remove expired timestamps
    request_store[key] = [
        t for t in request_store[key] if now - t < WINDOW
    ]

    if len(request_store[key]) >= LIMIT:
        raise ValueError("Duplicate review detected from same IP")

    request_store[key].append(now)


def add_review(product_id, data, ip):
    if not data.get("review") or not data["review"].strip():
        raise ValueError("Review text is required")

    rating = data.get("rating")
    if rating is None or not (1 <= rating <= 5):
        raise ValueError("Rating must be between 1 and 5")

    payload = {
        "product_id": product_id,
        "reviewer": data.get("reviewer", "").strip(),
        "rating": rating,
        "review": data["review"].strip(),
    }

    # 🔒 SAME AS YOUR NEXT.JS LOGIC
    check_duplicate(ip, payload)

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
