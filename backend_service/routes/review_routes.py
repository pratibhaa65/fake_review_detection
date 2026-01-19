from flask import Blueprint, request, jsonify
from controllers.review_controller import add_review, delete_review

review_bp = Blueprint("review_bp", __name__)


@review_bp.route("/products/<int:product_id>/reviews", methods=["POST"])
def add(product_id):
    try:
        review = add_review(product_id, request.json)
        return jsonify({"review_id": review.review_id, "message": "Review added"}), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400




@review_bp.route("/reviews/<int:review_id>", methods=["DELETE"])
def remove(review_id):
    try:
        delete_review(review_id)
        return jsonify({"message": "Review deleted"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404