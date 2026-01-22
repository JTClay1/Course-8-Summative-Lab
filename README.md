# Course-8-Summative-Lab #
--Python REST API w Flask : Inventory Management System--


# Summary Breakdown #
We’re building the bones of a grocery store’s back-office inventory system.
There’s a simple list of products living in memory (mock database). 
Employees need to be able to do the following: 
 --Add items
 --look items up
 --update prices
 --update stock
 --delete items
All the above will be executable through an API. 

When the store only has a barcode or product name, the system can ask an outside service (OpenFoodFacts) for extra details like brand or ingredients and attach that info to the item. 

A CLI tool is just a keyboard-based remote control that sends those same actions to the API. 

Tests exist to prove each action works and doesn’t break when things go wrong.


# Inventory Fields to be Used #
--id
--name
--barcode
--price
--stock
--details


# Flask Route Structure #
GET /inventory -> return list of items
GET /inventory/<id> -> returns one item or 404
POST /inventory -> creates item, returns created item + 201
PATCH /inventory/<id> -> update fields, returns updated item
DELETE /inventory/<id> -> deletes, returns success message or 204
External Helper:
   --GET /products/search?barcode=... or GET /products/search?name=...
   --returns "product details" pulled from OpenFoodFacts (or a clean subset)


# CLI Commands that map to Routes #
--list
--show <id>
--add
--update <id>
--delete <id>
--find --barcode <code>/find --name <text>