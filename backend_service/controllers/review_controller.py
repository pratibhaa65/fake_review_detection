from database.db import SessionLocal
from database.models import Review, Product


def add_review(product_id, data):
    if not data.get("review") or not data["review"].strip():
        raise ValueError("Review text is required")

    rating = data.get("rating")
    if rating is None or not (1 <= rating <= 5):
        raise ValueError("Rating must be between 1 and 5")

    db = SessionLocal()

    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError("Product not found")

        review = Review(
            product_id=product_id,
            reviewer=data.get("reviewer", "").strip(),
            rating=rating,
            review=data["review"].strip()
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
