Inventory Management System

A simple Flask-based inventory management system with CLI and external API integration.
Project Structure

Flask-API-inventory-Management-Project/
├── app.py          # Flask REST API
├── cli.py          # CLI frontend
├── test_app.py     # Unit tests
└── README.md

Setup

1. Install dependencies
pipenv install flask requests pytest

2. Run the Flask server
pipenv run python app.py
The server runs at http://127.0.0.1:5000 by default.

3. Use the CLI (in a separate terminal)
pipenv run python cli.py

Example Requests
  Add a new item
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"name": "Orange Juice", "price": 3.99, "stock": 25}'

  Update item price
curl -X PATCH http://127.0.0.1:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 4.99}'
Look up a product by barcode
curl http://127.0.0.1:5000/product/0048500005347