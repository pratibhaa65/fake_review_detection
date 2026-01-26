from flask import Blueprint, request, jsonify
from controllers.product_controller import (
    create_product,
    get_product_with_reviews,
    delete_product,
    get_categories,
    get_all_products
)

product_bp = Blueprint("product_bp", __name__)


@product_bp.route("/products", methods=["GET"])
def list_products():
    return jsonify(get_all_products()), 200


@product_bp.route("/products", methods=["POST"])
def create():
    try:
        product = create_product(request.json)
        return jsonify({
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "price": product.price,
            "description": product.description
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@product_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = get_product_with_reviews(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200


@product_bp.route("/products/<int:product_id>", methods=["DELETE"])
def remove(product_id):
    try:
        delete_product(product_id)
        return jsonify({"message": "Product deleted"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@product_bp.route("/categories", methods=["GET"])
def categories():
    return jsonify(get_categories()), 200
