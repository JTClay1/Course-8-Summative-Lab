# Course-8 Summative Lab
Python REST API with Flask – Inventory Management System

Overview
This project implements the core back-office logic for a grocery store inventory system.
It exposes a Flask-based REST API that allows employees to manage products stored in a mock, in-memory database.

The system supports full CRUD operations, integrates with the OpenFoodFacts API for product data enrichment, and includes a command-line interface (CLI) for interacting with the API. Unit tests are used to validate functionality and error handling.


Core Functionality
Employees can:
- Add products to inventory
- View all products or a single product
- Update product fields (price, stock, etc.)
- Delete products from inventory

When only a barcode or product name is available, the system can query the OpenFoodFacts API to retrieve additional product details and attach that data to a product.

A CLI acts as a keyboard-based controller for sending these actions to the API.


Product Data Model
Each product contains:
- id: unique identifier
- name: product name
- barcode: optional barcode value
- price: product price
- stock: quantity in stock
- details: optional data enriched from OpenFoodFacts

Product data is stored in memory using a Python list to simulate a database.


API Routes
GET /products
Returns all products.

GET /products/<id>
Returns a single product or 404 if not found.

POST /products
Creates a new product.
Returns the created product with status 201.

PATCH /products/<id>
Updates one or more fields on an existing product.
Returns the updated product.

DELETE /products/<id>
Deletes a product.
Returns a success message with status 200.

GET /products/search?barcode=...
GET /products/search?name=...
Returns product details retrieved from the OpenFoodFacts API.

PATCH /products/<id>/enrich
Retrieves external product data using the product barcode and stores it in the product's details field.


CLI Commands
- list
- show <id>
- add
- update <id>
- delete <id>
- find --barcode <code>
- find --name <text>
- enrich <id>


Setup and Usage
Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt
pip install pytest

Run the API server:
python app.py

Use the CLI:
python cli.py list
python cli.py add --name "Nutella" --barcode 3017624010701 --price 6.99 --stock 5
python cli.py enrich 4


Testing
Unit tests are written using pytest and include:
- API endpoint tests
- CLI command tests
- Mocked external API interaction tests

Run tests:
pytest -q


Tech Stack
- Python
- Flask
- pytest
- OpenFoodFacts API
- Git & GitHub
