import argparse
import json
import os
import sys
from typing import Any

import requests


DEFAULT_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000")


# ---------- helpers ----------
def _print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def _request(method: str, url: str, *, json_body: dict | None = None, timeout: int = 8) -> Any:
    try:
        resp = requests.request(method, url, json=json_body, timeout=timeout)
    except requests.RequestException as e:
        print(f"ERROR: Could not reach API: {e}", file=sys.stderr)
        raise SystemExit(2)

    # Try to parse JSON, but don’t explode if server sends non-json errors
    payload = None
    if resp.content:
        try:
            payload = resp.json()
        except ValueError:
            payload = resp.text

    if 200 <= resp.status_code < 300:
        return payload

    # Non-2xx: print useful error message
    if isinstance(payload, dict) and "error" in payload:
        msg = payload["error"]
    else:
        msg = payload if payload else f"HTTP {resp.status_code}"

    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def _base_url(args) -> str:
    return args.base_url.rstrip("/")


# ---------- command handlers ----------
def cmd_list(args) -> None:
    data = _request("GET", f"{_base_url(args)}/products")
    _print_json(data)


def cmd_show(args) -> None:
    data = _request("GET", f"{_base_url(args)}/products/{args.id}")
    _print_json(data)


def cmd_add(args) -> None:
    name = args.name or input("Name: ").strip()
    if not name:
        print("ERROR: name is required", file=sys.stderr)
        raise SystemExit(1)

    barcode = args.barcode
    if barcode is None:
        raw = input("Barcode (optional): ").strip()
        barcode = raw or None

    price = args.price
    if price is None:
        raw = input("Price (default 0): ").strip()
        price = float(raw) if raw else 0.0

    stock = args.stock
    if stock is None:
        raw = input("Stock (default 0): ").strip()
        stock = int(raw) if raw else 0

    body = {
        "name": name,
        "barcode": barcode,
        "price": price,
        "stock": stock,
    }

    data = _request("POST", f"{_base_url(args)}/products", json_body=body)
    _print_json(data)


def cmd_update(args) -> None:
    body = {}
    if args.name is not None:
        body["name"] = args.name
    if args.barcode is not None:
        body["barcode"] = args.barcode
    if args.price is not None:
        body["price"] = args.price
    if args.stock is not None:
        body["stock"] = args.stock

    if not body:
        print("ERROR: provide at least one field to update (--name/--barcode/--price/--stock)", file=sys.stderr)
        raise SystemExit(1)

    data = _request("PATCH", f"{_base_url(args)}/products/{args.id}", json_body=body)
    _print_json(data)


def cmd_delete(args) -> None:
    data = _request("DELETE", f"{_base_url(args)}/products/{args.id}")
    _print_json(data)


def cmd_find(args) -> None:
    if bool(args.barcode) == bool(args.name):
        print("ERROR: use exactly one of --barcode or --name", file=sys.stderr)
        raise SystemExit(1)

    if args.barcode:
        url = f"{_base_url(args)}/products/search?barcode={args.barcode}"
    else:
        # requests will handle encoding spaces if we let it, but keeping it simple here
        url = f"{_base_url(args)}/products/search?name={requests.utils.quote(args.name)}"

    data = _request("GET", url)
    _print_json(data)


def cmd_enrich(args) -> None:
    data = _request("PATCH", f"{_base_url(args)}/products/{args.id}/enrich")
    _print_json(data)


# ---------- argparse ----------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="inventory-cli",
        description="CLI for Inventory Management Flask API",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"API base url (default: {DEFAULT_BASE_URL}) or set API_BASE_URL env var",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List all products")
    p_list.set_defaults(func=cmd_list)

    p_show = sub.add_parser("show", help="Show a product by id")
    p_show.add_argument("id", type=int)
    p_show.set_defaults(func=cmd_show)

    p_add = sub.add_parser("add", help="Add a new product")
    p_add.add_argument("--name", help="Product name")
    p_add.add_argument("--barcode", help="Barcode (optional)")
    p_add.add_argument("--price", type=float, help="Price (default 0)")
    p_add.add_argument("--stock", type=int, help="Stock (default 0)")
    p_add.set_defaults(func=cmd_add)

    p_update = sub.add_parser("update", help="Update an existing product")
    p_update.add_argument("id", type=int)
    p_update.add_argument("--name", help="New name")
    p_update.add_argument("--barcode", help="New barcode (or blank to clear if you want)")
    p_update.add_argument("--price", type=float, help="New price")
    p_update.add_argument("--stock", type=int, help="New stock")
    p_update.set_defaults(func=cmd_update)

    p_delete = sub.add_parser("delete", help="Delete a product by id")
    p_delete.add_argument("id", type=int)
    p_delete.set_defaults(func=cmd_delete)

    p_find = sub.add_parser("find", help="Find product details via OpenFoodFacts")
    p_find.add_argument("--barcode", help="Barcode to look up")
    p_find.add_argument("--name", help="Name to search for")
    p_find.set_defaults(func=cmd_find)

    p_enrich = sub.add_parser("enrich", help="Enrich an existing product by id using its barcode")
    p_enrich.add_argument("id", type=int)
    p_enrich.set_defaults(func=cmd_enrich)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
