
from database.db import SessionLocal
from database.models import Review, Product, ReviewPrediction, ReviewFeature
import time
import json
import hashlib
from ml.inference import predict_review


# ---------------- CONFIG ----------------
WINDOW = 60  # seconds
MAX_SAME_PRODUCT = 2  # reviews per IP per minute
MAX_SAME_PAYLOAD = 2  # identical payload allowed

# In-memory store
request_store = {}


def to_float(x):
    return float(x) if x is not None else None


# ---------------- UTILS ----------------
def hash_payload(payload: dict) -> str:
    payload_str = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(payload_str.encode()).hexdigest()


def clean_store(key):
    now = time.time()
    request_store[key] = [t for t in request_store.get(key, []) if now - t < WINDOW]


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
    
    db = SessionLocal()
    try:
        # 🔍 Get product
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError("Product not found")
        
        payload = {
            "product_id": product_id,
            "reviewer": data.get("reviewer", "").strip(),
            "rating": rating,
            "review": data["review"].strip(),
        }

        check_limits(ip, payload)

        # 🤖 ML Prediction FIRST
        ml_result = predict_review(
            review=payload["review"],
            rating=payload["rating"],
            category=product.category,
        )
        
        # Save Prediction (ALWAYS)
        prediction = ReviewPrediction(
            review_id=None,  # will be set ONLY if genuine
            reviewer=payload["reviewer"],
            rating=rating,
            review_text=payload["review"],
            label=ml_result["prediction"],
            probability=ml_result["probability"],
            model_version="v1.0",
        )
        db.add(prediction)
        db.flush()
        
        # 🧪 Save Features (ALWAYS)
        features = ReviewFeature(
            prediction_id=prediction.id,
            text_length=len(payload["review"]),
            capital_ratio=to_float(ml_result["features"]["capital_ratio"]),
            punctuation_ratio=to_float(ml_result["features"]["punctuation_ratio"]),
            repetition_score=to_float(ml_result["features"]["repetition_score"]),
            sentiment_score=to_float(ml_result["features"]["sentiment_score"]),
            adjective_ratio=to_float(ml_result["features"]["adjective_ratio"]),
            rating_sentiment_mismatch=to_float(
                ml_result["features"]["rating_sentiment_mismatch"]
            ),
            is_extreme_rating=to_float(ml_result["features"]["is_extreme_rating"]),
            raw_review_similarity=to_float(
                ml_result["features"]["raw_review_similarity"]
            ),
            review_similarity_score=to_float(
                ml_result["features"]["review_similarity_score"]
            ),
            category_consistency_score=to_float(
                ml_result["features"]["category_consistency_score"]
            ),
        )
        db.add(features)
        
        
        # Save Review ONLY if Genuine
        if ml_result["prediction"] == "Genuine":
            review = Review(
                product_id=product_id,
                reviewer=payload["reviewer"],
                rating=rating,
                review=payload["review"],
            )
            db.add(review)
            db.flush()
            prediction.review_id = review.review_id
            db.commit()
            return {
                "review_id": review.review_id,
                "status": "Genuine",
                "confidence": round(ml_result["probability"] * 100, 2),
            }
        
        # Fake review: DO NOT store in reviews table
        db.commit()

        raise ValueError(
            f"Fake review detected."
        )
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
