from app import app


def test_health_check():
    # Use Flask’s built-in test client so we don’t need a real server running
    client = app.test_client()

    resp = client.get("/health")

    assert resp.status_code == 200

    assert resp.get_json() == {"status": "ok"}
