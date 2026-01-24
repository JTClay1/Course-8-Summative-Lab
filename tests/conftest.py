import os
import sys
import pytest

# Pytest sometimes runs with a weird working directory, so this forces the project root
# onto sys.path so imports like `import data` work consistently.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import data  # noqa: E402


@pytest.fixture(autouse=True)
def reset_products():
    # Since this app uses an in-memory list instead of a real DB, tests would leak state
    # into each other without a reset. This runs before every test automatically.
    data.products.clear()
    data.products.extend([
        {"id": 1, "name": "Whole Milk", "barcode": "012000001658", "price": 3.49, "stock": 24, "details": {}},
        {"id": 2, "name": "Bananas", "barcode": None, "price": 0.59, "stock": 120, "details": {}},
        {"id": 3, "name": "Peanut Butter", "barcode": "051500255872", "price": 4.99, "stock": 15, "details": {}},
    ])
