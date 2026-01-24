from app import app

def test_get_products():
    client = app.test_client()
    resp = client.get("/products")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 3

def test_get_product_by_id_success():
    client = app.test_client()
    resp = client.get("/products/1")
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "Whole Milk"

def test_get_product_by_id_404():
    client = app.test_client()
    resp = client.get("/products/999")
    assert resp.status_code == 404
    assert "error" in resp.get_json()

def test_post_product_success():
    client = app.test_client()
    resp = client.post("/products", json={"name": "Test", "price": 1.25, "stock": 2})
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["id"] == 4
    assert body["name"] == "Test"

def test_post_product_missing_body():
    client = app.test_client()
    resp = client.post("/products")
    assert resp.status_code in (400, 415)  # Flask can return 415 if no JSON content-type

def test_post_product_missing_name():
    client = app.test_client()
    resp = client.post("/products", json={"price": 1.0})
    assert resp.status_code == 400
    assert "error" in resp.get_json()

def test_patch_product_success():
    client = app.test_client()
    resp = client.patch("/products/1", json={"stock": 99})
    assert resp.status_code == 200
    assert resp.get_json()["stock"] == 99

def test_patch_product_404():
    client = app.test_client()
    resp = client.patch("/products/999", json={"stock": 1})
    assert resp.status_code == 404

def test_patch_product_no_body():
    client = app.test_client()
    resp = client.patch("/products/1")
    assert resp.status_code in (400, 415)

def test_delete_product_success():
    client = app.test_client()
    resp = client.delete("/products/1")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Product deleted"

def test_delete_product_404():
    client = app.test_client()
    resp = client.delete("/products/999")
    assert resp.status_code == 404
