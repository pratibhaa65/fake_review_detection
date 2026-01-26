from database.db import SessionLocal
from database.models import Product


def create_product(data):
    if not data:
        raise ValueError("No data provided")

    name = data.get("name", "").strip()
    category = data.get("category", "").strip()
    description = data.get("description", "").strip()
    price = data.get("price")

    if not name:
        raise ValueError("Product name is required")

    if not category:
        raise ValueError("Product category is required")

    if price is None or str(price).strip() == "":
        raise ValueError("Price is required")

    try:
        price = int(price)
    except:
        raise ValueError("Price must be a valid number")

    if price < 0:
        raise ValueError("Price cannot be negative")

    db = SessionLocal()
    try:
        product = Product(
            name=name,
            description=description,
            category=category,
            price=price
        )

        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    except Exception as e:
        db.rollback()
        raise ValueError(str(e))

    finally:
        db.close()



def get_product_with_reviews(product_id):
    db = SessionLocal()

    try:
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise ValueError("Product not found")

        return {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "price": product.price,
            "description": product.description,
            "reviews": [
                {
                    "review_id": r.review_id,
                    "reviewer": r.reviewer,
                    "rating": r.rating,
                    "review": r.review
                }
                for r in product.reviews
            ]
        }

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
                "category": p.category,
                "price": p.price,
                "description": p.description
            }
            for p in products
        ]
    finally:
        db.close()

