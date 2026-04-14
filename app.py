from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Using a list as temporary storage (db)
inventory = [
    {"id": 1, "name": "Apple Juice", "price": 2.99, "stock": 50, "barcode": "0048500005347"},
    {"id": 2, "name": "Whole Milk", "price": 3.49, "stock": 30, "barcode": "0041303004616"},
]

# Helper to find an item by id
def find_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None


# GET all items
@app.route("/inventory", methods=["GET"])
def get_all_items():
    return jsonify(inventory), 200


# GET single item
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


# POST - add new item
@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400

    # generate a new id
    new_id = max(item["id"] for item in inventory) + 1 if inventory else 1

    new_item = {
        "id": new_id,
        "name": data["name"],
        "price": data.get("price", 0.0),
        "stock": data.get("stock", 0),
        "barcode": data.get("barcode", ""),
    }

    inventory.append(new_item)
    return jsonify(new_item), 201


# PATCH - update an item
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()

    # only update fields that were sent
    if "name" in data:
        item["name"] = data["name"]
    if "price" in data:
        item["price"] = data["price"]
    if "stock" in data:
        item["stock"] = data["stock"]

    return jsonify(item), 200


# DELETE - remove an item
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    inventory.remove(item)
    return jsonify({"message": f"Item {item_id} deleted"}), 200


# External API to fetch product by barcode from OpenFoodFacts
@app.route("/product/<barcode>", methods=["GET"])
def get_product_from_api(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("status") == 1:
            product = data["product"]
            # pull out just the info we want
            result = {
                "name": product.get("product_name", "Unknown"),
                "brand": product.get("brands", "Unknown"),
                "barcode": barcode,
                "image": product.get("image_url", ""),
            }
            return jsonify(result), 200
        else:
            return jsonify({"error": "Product not found"}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Could not reach external API", "details": str(e)}), 500


# Route to fetch product from API and add to inventory
@app.route("/product/<barcode>/add", methods=["POST"])
def add_product_from_api(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("status") == 1:
            product = data["product"]
            new_id = max(item["id"] for item in inventory) + 1 if inventory else 1

            new_item = {
                "id": new_id,
                "name": product.get("product_name", "Unknown Product"),
                "price": 0.0,  # price not available from API
                "stock": 0,
                "barcode": barcode,
            }
            inventory.append(new_item)
            return jsonify(new_item), 201
        else:
            return jsonify({"error": "Product not found in OpenFoodFacts"}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "API error", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)