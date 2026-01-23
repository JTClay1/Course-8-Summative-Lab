from flask import Flask, jsonify, request
from data import products

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return {"status": "ok"}

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products), 200


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    product = next(
        (product for product in products if product["id"] == product_id),
        None
    )
    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(product), 200

@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    if "name" not in data:
        return jsonify({"error": "Product name is required"}), 400

    new_id = max(product["id"] for product in products) + 1

    new_product = {
        "id": new_id,
        "name": data["name"],
        "barcode": data.get("barcode", None),
        "price": data.get("price", 0.0),
        "stock": data.get("stock", 0),
        "details": data.get("details", {})
    }

    products.append(new_product)

    return jsonify(new_product), 201



if __name__ == "__main__":
    app.run()