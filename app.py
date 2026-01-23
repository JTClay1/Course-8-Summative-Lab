from flask import Flask, jsonify, request, 
from data import products

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return {"status": "ok"}

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products), 200


@app.route("/products/<int:id>", methods=["GET"])
def get_product_by_id(id):
    product = next(
        (product for product in products if product["id"] == id),
        None
    )
    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(product), 200

if __name__ == "__main__":
    app.run()