import requests

OFF_BASE = "https://world.openfoodfacts.net/api/v2"
FIELDS = "product_name,brands,ingredients_text,image_url,quantity,categories_tags"

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

    # return a clean subset (this becomes your "details")
    return {
        "product_name": product.get("product_name"),
        "brands": product.get("brands"),
        "ingredients_text": product.get("ingredients_text"),
        "image_url": product.get("image_url"),
        "quantity": product.get("quantity"),
        "categories_tags": product.get("categories_tags"),
    }
