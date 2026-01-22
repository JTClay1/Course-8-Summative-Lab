# Course-8 Summative Lab  
**Python REST API with Flask – Inventory Management System**

## Overview
This project implements the core back-office logic for a grocery store inventory system.  
It exposes a Flask-based REST API that allows employees to manage inventory items stored in a mock, in-memory database.

The system supports full CRUD operations, integrates with an external product API for enrichment, and includes a CLI tool for interacting with the API. Unit tests validate functionality and error handling.

---

## Core Functionality
Employees can:
- Add inventory items
- View all items or a single item
- Update item fields (price, stock, etc.)
- Delete items

All actions are performed through the REST API.

When only a barcode or product name is available, the system can query the OpenFoodFacts API to retrieve additional product details (e.g., brand, ingredients) and attach that data to the inventory item.

A command-line interface (CLI) acts as a keyboard-based controller for sending requests to the API.

---

## Inventory Item Structure
Each inventory item contains the following fields:

- `id`
- `name`
- `barcode`
- `price`
- `stock`
- `details` (optional data enriched from OpenFoodFacts)

Inventory data is stored in memory using a Python list to simulate a database.

---

## API Routes

### Inventory Routes
- `GET /inventory`  
  Returns all inventory items.

- `GET /inventory/<id>`  
  Returns a single item or a 404 if not found.

- `POST /inventory`  
  Creates a new inventory item.  
  Returns the created item with status `201`.

- `PATCH /inventory/<id>`  
  Updates one or more fields on an existing item.  
  Returns the updated item.

- `DELETE /inventory/<id>`  
  Deletes an item.  
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