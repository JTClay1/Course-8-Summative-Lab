# Course-8 Summative Lab  
**Python REST API with Flask – Inventory Management System**

## Overview
This project implements the core back-office logic for a grocery store inventory system.  
It exposes a Flask-based REST API that allows employees to manage products stored in a mock, in-memory database.

The system supports full CRUD operations, integrates with an external product API for data enrichment, and includes a command-line interface (CLI) for interacting with the API. Unit tests are used to validate functionality and error handling.

---

## Core Functionality
Employees can:
- Add products to inventory
- View all products or a single product
- Update product fields (price, stock, etc.)
- Delete products from inventory

All actions are performed through the REST API.

When only a barcode or product name is available, the system can query the OpenFoodFacts API to retrieve additional product details (such as brand or ingredients) and attach that data to a product.

A CLI acts as a keyboard-based controller for sending these actions to the API.

---

## Product Data Model
Each product contains the following fields:

- `id` – unique identifier
- `name` – product name
- `barcode` – optional barcode value
- `price` – product price
- `stock` – quantity in stock
- `details` – optional data enriched from OpenFoodFacts

Product data is stored in memory using a Python list to simulate a database.

---

## API Routes

### Product Routes
- `GET /products`  
  Returns all products.

- `GET /products/<id>`  
  Returns a single product or a `404` error if not found.

- `POST /products`  
  Creates a new product.  
  Returns the created product with status `201`.

- `PATCH /products/<id>`  
  Updates one or more fields on an existing product.  
  Returns the updated product.

- `DELETE /products/<id>`  
  Deletes a product.  
  Returns a success message or `204 No Content`.

### External Product Lookup
- `GET /products/search?barcode=...`
- `GET /products/search?name=...`

Returns product details retrieved from the OpenFoodFacts API (or a clean subset of the response).

---

## CLI Commands
The CLI maps directly to API functionality:

- `list`
- `show <id>`
- `add`
- `update <id>`
- `delete <id>`
- `find --barcode <code>`
- `find --name <text>`

---

## Testing
Unit tests are written using `pytest` and include:
- API endpoint tests (GET, POST, PATCH, DELETE)
- CLI command tests
- Mocked external API interaction tests

---

## Tech Stack
- Python
- Flask
- pytest
- OpenFoodFacts API
- Git & GitHub
