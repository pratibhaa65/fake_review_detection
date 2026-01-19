from flask import Flask, render_template, jsonify
from routes.product_routes import product_bp
from routes.review_routes import review_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    # Register Blueprints
    app.register_blueprint(product_bp)
    app.register_blueprint(review_bp)

    # Home Page (Visual)
    @app.route("/", methods=["GET"])
    def home():
        return render_template("index.html")

    # -------------------------
    # Global Error Handlers
    # -------------------------

    # 404 - Route Not Found
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Not Found",
            "message": "The requested route does not exist"
        }), 404

    # 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": "Bad Request",
            "message": "Invalid request data"
        }), 400

    # 500 - Internal Server Error
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "error": "Internal Server Error",
            "message": "Something went wrong on the server"
        }), 500

    return app


if __name__ == "__main__":
    app = create_app()
    CORS(app)
    app.run(debug=True)
