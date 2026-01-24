import cli


class FakeResp:
    # Tiny fake response object so we can test CLI logic without making real HTTP calls
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self._payload = payload
        self.content = b"1"  # non-empty so cli tries json()

    def json(self):
        return self._payload

    @property
    def text(self):
        # Fallback path if cli can't parse JSON
        return str(self._payload)


def test_cli_list_calls_products(monkeypatch, capsys):
    # Make sure "list" hits GET /products and prints JSON
    def fake_request(method, url, json=None, timeout=8):
        assert method == "GET"
        assert url.endswith("/products")
        return FakeResp(200, [{"id": 1}])

    monkeypatch.setattr(cli.requests, "request", fake_request)

    cli.main(["--base-url", "http://127.0.0.1:5000", "list"])
    out = capsys.readouterr().out
    assert '"id": 1' in out


def test_cli_find_name_builds_query(monkeypatch, capsys):
    # Find by name should call the /products/search?name=... endpoint
    def fake_request(method, url, json=None, timeout=8):
        assert method == "GET"
        assert "/products/search?name=" in url
        return FakeResp(200, {"product_name": "Nutella"})

    monkeypatch.setattr(cli.requests, "request", fake_request)

    cli.main(["--base-url", "http://x", "find", "--name", "nutella"])
    out = capsys.readouterr().out
    assert "Nutella" in out


def test_cli_error_non_2xx(monkeypatch, capsys):
    # When the API returns a non-2xx response, the CLI should exit with code 1 and print an error
    def fake_request(method, url, json=None, timeout=8):
        return FakeResp(404, {"error": "Not found"})

    monkeypatch.setattr(cli.requests, "request", fake_request)

    try:
        cli.main(["--base-url", "http://x", "show", "999"])
    except SystemExit as e:
        assert e.code == 1

    err = capsys.readouterr().err
    assert "ERROR" in err
