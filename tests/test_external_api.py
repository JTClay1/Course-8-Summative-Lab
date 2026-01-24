from app import app

def test_search_by_barcode_mocked(monkeypatch):
    def fake_fetch(barcode):
        return {"product_name": "Nutella", "brands": "Ferrero"}

    monkeypatch.setattr("app.fetch_by_barcode", fake_fetch)

    client = app.test_client()
    resp = client.get("/products/search?barcode=3017624010701")
    assert resp.status_code == 200
    assert resp.get_json()["product_name"] == "Nutella"

def test_search_by_name_mocked(monkeypatch):
    def fake_fetch(name):
        return {"product_name": "Nutella", "brands": "Ferrero"}

    monkeypatch.setattr("app.fetch_by_name", fake_fetch)

    client = app.test_client()
    resp = client.get("/products/search?name=nutella")
    assert resp.status_code == 200
    assert resp.get_json()["product_name"] == "Nutella"

def test_enrich_product_success(monkeypatch):
    def fake_fetch(barcode):
        return {"product_name": "Nutella", "brands": "Ferrero"}

    monkeypatch.setattr("app.fetch_by_barcode", fake_fetch)

    client = app.test_client()
    resp = client.patch("/products/1/enrich")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["details"]["product_name"] == "Nutella"

def test_enrich_product_no_barcode():
    client = app.test_client()
    resp = client.patch("/products/2/enrich")  # bananas has no barcode
    assert resp.status_code == 400

def test_enrich_external_not_found(monkeypatch):
    def fake_fetch(barcode):
        return None

    monkeypatch.setattr("app.fetch_by_barcode", fake_fetch)

    client = app.test_client()
    resp = client.patch("/products/1/enrich")
    assert resp.status_code == 404

def test_enrich_external_failure(monkeypatch):
    def fake_fetch(barcode):
        raise Exception("boom")

    monkeypatch.setattr("app.fetch_by_barcode", fake_fetch)

    client = app.test_client()
    resp = client.patch("/products/1/enrich")
    assert resp.status_code == 502
