import requests

BASE_URL = "http://127.0.0.1:5000"


def view_all_items():
    response = requests.get(f"{BASE_URL}/inventory")
    items = response.json()

    if not items:
        print("No items in inventory.")
        return

    print("\n--- Inventory ---")
    for item in items:
        print(f"ID: {item['id']} | {item['name']} | Price: ${item['price']} | Stock: {item['stock']}")
    print("-----------------\n")


def view_single_item():
    item_id = input("Enter item ID: ").strip()

    try:
        item_id = int(item_id)
    except ValueError:
        print("Error: ID must be a number.")
        return

    response = requests.get(f"{BASE_URL}/inventory/{item_id}")

    if response.status_code == 404:
        print("Item not found.")
    else:
        item = response.json()
        print(f"\nID: {item['id']}")
        print(f"Name: {item['name']}")
        print(f"Price: ${item['price']}")
        print(f"Stock: {item['stock']}")
        print(f"Barcode: {item.get('barcode', 'N/A')}\n")


def add_item():
    name = input("Product name: ").strip()
    if not name:
        print("Error: name cannot be empty.")
        return

    price_input = input("Price (e.g. 2.99): ").strip()
    stock_input = input("Stock quantity: ").strip()

    try:
        price = float(price_input)
        stock = int(stock_input)
    except ValueError:
        print("Error: price must be a number and stock must be a whole number.")
        return

    barcode = input("Barcode (optional, press Enter to skip): ").strip()

    payload = {"name": name, "price": price, "stock": stock, "barcode": barcode}

    response = requests.post(f"{BASE_URL}/inventory", json=payload)

    if response.status_code == 201:
        item = response.json()
        print(f"Added: {item['name']} with ID {item['id']}")
    else:
        print("Failed to add item:", response.json())


def update_item():
    item_id = input("Enter item ID to update: ").strip()

    try:
        item_id = int(item_id)
    except ValueError:
        print("Error: ID must be a number.")
        return

    print("Leave blank to keep current value.")
    new_price = input("New price: ").strip()
    new_stock = input("New stock: ").strip()
    new_name = input("New name: ").strip()

    payload = {}
    if new_price:
        try:
            payload["price"] = float(new_price)
        except ValueError:
            print("Invalid price, skipping.")
    if new_stock:
        try:
            payload["stock"] = int(new_stock)
        except ValueError:
            print("Invalid stock, skipping.")
    if new_name:
        payload["name"] = new_name

    if not payload:
        print("Nothing to update.")
        return

    response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=payload)

    if response.status_code == 200:
        print("Item updated successfully.")
    elif response.status_code == 404:
        print("Item not found.")
    else:
        print("Something went wrong:", response.json())


def delete_item():
    item_id = input("Enter item ID to delete: ").strip()

    try:
        item_id = int(item_id)
    except ValueError:
        print("Error: ID must be a number.")
        return

    confirm = input(f"Are you sure you want to delete item {item_id}? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return

    response = requests.delete(f"{BASE_URL}/inventory/{item_id}")

    if response.status_code == 200:
        print("Item deleted.")
    elif response.status_code == 404:
        print("Item not found.")


def search_by_barcode():
    barcode = input("Enter barcode to search: ").strip()
    if not barcode:
        print("Error: barcode cannot be empty.")
        return

    response = requests.get(f"{BASE_URL}/product/{barcode}")

    if response.status_code == 200:
        product = response.json()
        print(f"\nFound: {product['name']} by {product['brand']}")

        add = input("Add this product to inventory? (y/n): ").strip().lower()
        if add == "y":
            add_response = requests.post(f"{BASE_URL}/product/{barcode}/add")
            if add_response.status_code == 201:
                print("Product added to inventory!")
            else:
                print("Could not add product.")
    elif response.status_code == 404:
        print("Product not found in OpenFoodFacts.")
    else:
        print("Error contacting external API.")


def main():
    print("=== Inventory Management CLI ===")

    while True:
        print("\nOptions:")
        print("1. View all items")
        print("2. View single item")
        print("3. Add item manually")
        print("4. Update item")
        print("5. Delete item")
        print("6. Search product by barcode (OpenFoodFacts)")
        print("0. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            view_all_items()
        elif choice == "2":
            view_single_item()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            search_by_barcode()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()