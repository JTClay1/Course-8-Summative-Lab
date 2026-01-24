from flask import Flask, jsonify, request
from data import products
from services.openfoodfacts import fetch_by_barcode, fetch_by_name

# Main Flask app for the inventory API
app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health_check():
    # Super simple heartbeat endpoint so tests / humans can confirm the server is up
    return {"status": "ok"}


@app.route("/products", methods=["GET"])
def get_products():
    # Return the full in-memory "database"
    return jsonify(products), 200


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    # Find the product with a matching id (None if it doesn't exist)
    product = next((product for product in products if product["id"] == product_id), None)

    if product is None:
        # Keep errors consistent and readable
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product), 200


@app.route("/products", methods=["POST"])
def add_product():
    # Incoming JSON payload from the client / CLI
    data = request.get_json()

    # No JSON body at all (or empty)
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    # Name is the one required field for a product
    if "name" not in data:
        return jsonify({"error": "Product name is required"}), 400

    # Auto-increment id based on current max id in the list
    new_id = max(product["id"] for product in products) + 1

    # Create the new product, defaulting missing fields to sane values
    new_product = {
        "id": new_id,
        "name": data["name"],
        "barcode": data.get("barcode", None),
        "price": data.get("price", 0.0),
        "stock": data.get("stock", 0),
        "details": data.get("details", {}),
    }

    # Since this is in-memory storage, append is basically our "INSERT"
    products.append(new_product)

    return jsonify(new_product), 201


@app.route("/products/<int:product_id>", methods=["PATCH"])
def update_product(product_id):
    # PATCH = partial update, so we only update fields the client actually sends
    data = request.get_json()

    product = next((product for product in products if product["id"] == product_id), None)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    # Update each field if it was provided in the payload
    if "name" in data:
        product["name"] = data["name"]

    if "barcode" in data:
        product["barcode"] = data["barcode"]

    if "price" in data:
        product["price"] = data["price"]

    if "stock" in data:
        product["stock"] = data["stock"]

    if "details" in data:
        # Allow manually setting/replacing details (useful for testing or admin work)
        product["details"] = data["details"]

    return jsonify(product), 200


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    # Find product by id, then remove it from the list
    product = next((p for p in products if p["id"] == product_id), None)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    # List remove is our "DELETE FROM products WHERE id = ?"
    products.remove(product)

    return jsonify({"message": "Product deleted"}), 200


@app.route("/products/search", methods=["GET"])
def search_products():
    # Support searching by barcode OR name (barcode wins if both are sent)
    barcode = request.args.get("barcode")
    name = request.args.get("name")

    if not barcode and not name:
        return jsonify({"error": "barcode or name query param is required"}), 400

    # Prefer barcode lookup because it's more exact
    if barcode:
        details = fetch_by_barcode(barcode)
    else:
        details = fetch_by_name(name)

    if details is None:
        # Clean "not found" instead of leaking random external API behavior
        return jsonify({"error": "Product not found"}), 404

    return jsonify(details), 200


@app.route("/products/<int:product_id>/enrich", methods=["PATCH"])
def enrich_product(product_id):
    # Enrich = take an existing inventory item and fill its details via OpenFoodFacts
    product = next((p for p in products if p["id"] == product_id), None)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    barcode = product.get("barcode")
    if not barcode:
        # If the product doesn't have a barcode, we can't enrich it
        return jsonify({"error": "Barcode required to enrich product"}), 400

    # Pull external product details (wrap in try so we can return a proper 502)
    try:
        details = fetch_by_barcode(barcode)
    except Exception:
        return jsonify({"error": "External API request failed"}), 502

    if details is None:
        return jsonify({"error": "External product not found"}), 404

    # Store the clean subset in our inventory item
    product["details"] = details
    return jsonify(product), 200


if __name__ == "__main__":
    # Local dev run (production would use gunicorn/etc)
    app.run()
