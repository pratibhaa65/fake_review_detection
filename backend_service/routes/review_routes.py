from flask import Blueprint, request, jsonify
from controllers.review_controller import add_review, delete_review

review_bp = Blueprint("review_bp", __name__)


@review_bp.route("/products/<int:product_id>/reviews", methods=["POST"])
def add(product_id):
    try:
        ip = (
            request.headers.get("X-Forwarded-For", "").split(",")[0]
            or request.remote_addr
        )

        review = add_review(product_id, request.json, ip)
        return jsonify({"review_id":  review["review_id"], "message": "Review added successfully"}), 201

    except ValueError as e:
        if "fake" in str(e).lower():
            return jsonify({
                "message": str(e),
                "type": "fake_review"
            }), 403
        else:
            return jsonify({
                "message": str(e),
                "type": "duplicate_review"
            }), 429
        


@review_bp.route("/reviews/<int:review_id>", methods=["DELETE"])
def remove(review_id):
    try:
        delete_review(review_id)
        return jsonify({"message": "Review deleted"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404