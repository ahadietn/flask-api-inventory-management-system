from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "barcode": "0025293004955",
        "ingredients_text": "Filtered water, almonds, cane sugar, vitamin E acetate",
        "quantity": 50,
        "price": 4.99,
        "category": "Beverages",
        "allergens": "tree nuts",
        "image_url": "https://images.openfoodfacts.org/images/products/002/529/300/4955/front_en.jpg"
    },
    {
        "id": 2,
        "product_name": "Greek Yogurt Plain",
        "brands": "Chobani",
        "barcode": "0818290011106",
        "ingredients_text": "Cultured nonfat milk, live and active cultures",
        "quantity": 30,
        "price": 1.89,
        "category": "Dairy",
        "allergens": "milk",
        "image_url": "https://images.openfoodfacts.org/images/products/081/829/001/1106/front_en.jpg"
    },
    {
        "id": 3,
        "product_name": "Whole Grain Bread",
        "brands": "Dave's Killer Bread",
        "barcode": "013764005037",
        "ingredients_text": "Whole wheat flour, water, cane sugar, oats, sunflower seeds",
        "quantity": 20,
        "price": 5.49,
        "category": "Bakery",
        "allergens": "wheat, soy",
        "image_url": "https://images.openfoodfacts.org/images/products/013/764/005/037/front_en.jpg"
    },
    {
        "id": 4,
        "product_name": "Peanut Butter Creamy",
        "brands": "Jif",
        "barcode": "051500755853",
        "ingredients_text": "Roasted peanuts, sugar, hydrogenated vegetable oils, salt",
        "quantity": 45,
        "price": 3.29,
        "category": "Condiments",
        "allergens": "peanuts",
        "image_url": "https://images.openfoodfacts.org/images/products/005/150/075/5853/front_en.jpg"
    },
    {
        "id": 5,
        "product_name": "Orange Juice",
        "brands": "Tropicana",
        "barcode": "048500205655",
        "ingredients_text": "100% pure squeezed pasteurized orange juice",
        "quantity": 60,
        "price": 3.79,
        "category": "Beverages",
        "allergens": "none",
        "image_url": "https://images.openfoodfacts.org/images/products/004/850/020/5655/front_en.jpg"
    },
]
 
next_id = 6

