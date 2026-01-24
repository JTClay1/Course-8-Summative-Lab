import requests

# OpenFoodFacts base URL for exact barcode lookups (fast + consistent)
OFF_BASE = "https://world.openfoodfacts.net/api/v2"

# Only request the fields we actually care about (keeps responses small and clean)
FIELDS = "product_name,brands,ingredients_text,image_url,quantity,categories_tags"


def _clean_product(product: dict) -> dict:
    # Return a clean subset (this becomes our "details" blob)
    # This keeps our API stable even if OpenFoodFacts includes a million other keys.
    return {
        "product_name": product.get("product_name"),
        "brands": product.get("brands"),
        "ingredients_text": product.get("ingredients_text"),
        "image_url": product.get("image_url"),
        "quantity": product.get("quantity"),
        "categories_tags": product.get("categories_tags"),
    }


def fetch_by_barcode(barcode: str) -> dict | None:
    # Barcode lookups are super direct: /product/<barcode>
    url = f"{OFF_BASE}/product/{barcode}"

    try:
        resp = requests.get(url, params={"fields": FIELDS}, timeout=5)
    except requests.RequestException:
        # Network issues / timeout / DNS / etc. -> treat as "no result" for our app
        return None

    if resp.status_code != 200:
        return None

    payload = resp.json()
    product = payload.get("product")
    if not product:
        return None

    return _clean_product(product)


def fetch_by_name(name: str) -> dict | None:
    # Name search is surprisingly flaky on the v2 search endpoint, so we use the classic one.
    # This gives better relevance for simple keyword searches.
    url = "https://world.openfoodfacts.org/cgi/search.pl"

    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 25,  # pull a handful so we can pick a good match
    }

    try:
        resp = requests.get(url, params=params, timeout=5)
    except requests.RequestException:
        return None

    if resp.status_code != 200:
        return None

    payload = resp.json()
    products = payload.get("products") or []
    if not products:
        return None

    q = name.strip().lower()

    # Prefer a product whose product_name actually contains the query (closer match)
    best = None
    for p in products:
        pname = (p.get("product_name") or "").strip()
        if not pname:
            continue

        if q and q in pname.lower():
            best = p
            break

        # Fallback: first product that at least has a name
        if best is None:
            best = p

    if best is None:
        return None

    return _clean_product(best)
