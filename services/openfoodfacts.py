import requests

OFF_BASE = "https://world.openfoodfacts.net/api/v2"
FIELDS = "product_name,brands,ingredients_text,image_url,quantity,categories_tags"

def _clean_product(product: dict) -> dict:
    # return a clean subset (this becomes your "details")
    return {
        "product_name": product.get("product_name"),
        "brands": product.get("brands"),
        "ingredients_text": product.get("ingredients_text"),
        "image_url": product.get("image_url"),
        "quantity": product.get("quantity"),
        "categories_tags": product.get("categories_tags"),
    }

def fetch_by_barcode(barcode: str) -> dict | None:
    url = f"{OFF_BASE}/product/{barcode}"

    try:
        resp = requests.get(url, params={"fields": FIELDS}, timeout=5)
    except requests.RequestException:
        return None

    if resp.status_code != 200:
        return None

    payload = resp.json()
    product = payload.get("product")
    if not product:
        return None

    return _clean_product(product)

def fetch_by_name(name: str) -> dict | None:
    # Use the classic search endpoint (more reliable than /api/v2/search for keyword relevance)
    url = "https://world.openfoodfacts.org/cgi/search.pl"

    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 25,
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

    # Prefer a product whose product_name contains the query
    best = None
    for p in products:
        pname = (p.get("product_name") or "").strip()
        if not pname:
            continue
        if q and q in pname.lower():
            best = p
            break
        if best is None:
            best = p

    if best is None:
        return None

    return _clean_product(best)


