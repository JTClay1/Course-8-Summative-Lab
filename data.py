# In-memory products "database"
# Keeping it simple: a list of dicts stands in for real DB rows.

products = [
    {
        "id": 1,
        "name": "Whole Milk",
        "barcode": "012000001658",
        "price": 3.49,
        "stock": 24,
        "details": {},  # populated later by /enrich
    },
    {
        "id": 2,
        "name": "Bananas",
        "barcode": None,  # not everything has/needs a barcode
        "price": 0.59,
        "stock": 120,
        "details": {},
    },
    {
        "id": 3,
        "name": "Peanut Butter",
        "barcode": "051500255872",
        "price": 4.99,
        "stock": 15,
        "details": {},
    },
]
