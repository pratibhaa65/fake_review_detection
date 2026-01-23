from database.db import SessionLocal
from database.models import Product


def create_product(data):
    # Product name validation
    if not data.get("name") or not data["name"].strip():
        raise ValueError("Product name is required")

    # Category validation
    if not data.get("category") or not data["category"].strip():
        raise ValueError("Product category is required")

    # Price validation
    price = int(data.get("price", 0))
    if price < 0:
        raise ValueError("Price cannot be negative")

    db = SessionLocal()

    try:
        product = Product(
            name=data["name"].strip(),
            description=data.get("description", "").strip(),
            category=data["category"].strip(),
            price=price
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


def get_product_with_reviews(product_id):
    db = SessionLocal()

    try:
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise ValueError("Product not found")

        return [{
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "price": product.price,
            "reviews": [
                {
                    "review_id": r.review_id,
                    "reviewer": r.reviewer,
                    "rating": r.rating,
                    "review": r.review
                }
                for r in product.reviews
            ]
        }]

    finally:
        db.close()


def delete_product(product_id):
    db = SessionLocal()

    try:
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise ValueError("Product not found")

        db.delete(product)
        db.commit()

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()
        
        
        
        


def get_categories():
    db = SessionLocal()
    try:
        categories = (
            db.query(Product.category)
            .distinct()
            .filter(Product.category.isnot(None))
            .all()
        )

        # Convert list of tuples → list of strings
        return [c[0] for c in categories]

    finally:
        db.close()


def get_all_products():
    db = SessionLocal()
    try:
        products = db.query(Product).all()

        return [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "category": p.category,
                "price": p.price,
            }
            for p in products
        ]

    finally:
        db.close()

