"""
Price Radar — моніторинг цін конкурентів.
Бекенд: приймає список URL, витягує назву, ціну, стару ціну, наявність.
"""

import json
import re
import concurrent.futures
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "uk-UA,uk;q=0.9,ru;q=0.8,en;q=0.7",
}

TIMEOUT = 20

AVAILABILITY_MAP = {
    "instock": "В наявності",
    "outofstock": "Немає в наявності",
    "preorder": "Передзамовлення",
    "backorder": "Очікується поставка",
    "limitedavailability": "Обмежена кількість",
    "discontinued": "Знято з виробництва",
}


def clean_price(value):
    """'5 199 грн.' / '2999₴' / '2,657.00' -> float або None."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value)
    text = re.sub(r"[^\d.,]", "", text)
    if not text:
        return None
    if "," in text and "." in text:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        parts = text.split(",")
        if len(parts[-1]) == 2:
            text = text.replace(",", ".")
        else:
            text = text.replace(",", "")
    try:
        price = float(text)
        return price if price > 0 else None
    except ValueError:
        return None


def normalize_availability(value):
    if not value:
        return None
    key = re.sub(r"[^a-z]", "", str(value).lower().split("/")[-1])
    return AVAILABILITY_MAP.get(key, str(value))


def walk_jsonld(node):
    if isinstance(node, list):
        for item in node:
            found = walk_jsonld(item)
            if found:
                return found
        return None
    if isinstance(node, dict):
        node_type = node.get("@type", "")
        types = node_type if isinstance(node_type, list) else [node_type]
        if any(str(t).lower() == "product" for t in types):
            return node
        for key in ("@graph", "mainEntity", "itemListElement", "item"):
            if key in node:
                found = walk_jsonld(node[key])
                if found:
                    return found
    return None


def parse_jsonld(soup):
    for script in soup.find_all("script", type="application/ld+json"):
        raw = script.string or script.get_text()
        if not raw:
            continue
        try:
            data = json.loads(raw.strip())
        except (json.JSONDecodeError, TypeError):
            continue
        product = walk_jsonld(data)
        if not product:
            continue

        result = {"name": product.get("name")}
        offers = product.get("offers")
        if isinstance(offers, list):
            offers = offers[0] if offers else {}
        if isinstance(offers, dict):
            result["price"] = clean_price(
                offers.get("price") or offers.get("lowPrice")
            )
            result["currency"] = offers.get("priceCurrency")
            result["availability"] = normalize_availability(
                offers.get("availability")
            )
        if result.get("price"):
            return result
    return None


def parse_meta(soup):
    result = {}
    price_meta = soup.find(
        "meta", property=re.compile(r"(product|og):price:amount")
    ) or soup.find("meta", attrs={"itemprop": "price"})
    if price_meta:
        result["price"] = clean_price(price_meta.get("content"))
    cur_meta = soup.find(
        "meta", property=re.compile(r"(product|og):price:currency")
    ) or soup.find("meta", attrs={"itemprop": "priceCurrency"})
    if cur_meta:
        result["currency"] = cur_meta.get("content")
    avail_meta = soup.find("link", attrs={"itemprop": "availability"}) or soup.find(
        "meta", attrs={"itemprop": "availability"}
    )
    if avail_meta:
        result["availability"] = normalize_availability(
            avail_meta.get("href") or avail_meta.get("content")
        )
    title_meta = soup.find("meta", property="og:title")
    if title_meta:
        result["name"] = title_meta.get("content")
    return result if result.get("price") else None


STORE_SELECTORS = {
    "default": {
        "price": [
            ".product-price .price-new", ".price-new",
            ".product-price", ".autocalc-product-price",
            '[data-price]', ".price",
        ],
        "old_price": [".price-old", ".product-price .price-old", "s.price", "del"],
        "name": ["h1"],
        "in_stock_text": ["в наявності", "є в наявності", "в наличии", "є в магазині"],
        "out_stock_text": [
            "немає в наявності", "нет в наличии",
            "очікується поставка", "під замовлення", "не виробляється",
        ],
    },
}


def parse_selectors(soup):
    cfg = STORE_SELECTORS["default"]
    result = {}

    for sel in cfg["price"]:
        el = soup.select_one(sel)
        if el:
            price = clean_price(el.get("data-price") or el.get_text())
            if price:
                result["price"] = price
                break

    for sel in cfg["old_price"]:
        el = soup.select_one(sel)
        if el:
            old = clean_price(el.get_text())
            if old:
                result["old_price"] = old
                break

    h1 = soup.select_one("h1")
    if h1:
        result["name"] = h1.get_text(strip=True)

    page_text = soup.get_text(" ", strip=True).lower()[:20000]
    if any(t in page_text for t in cfg["out_stock_text"]):
        result["availability"] = "Немає / очікується"
    elif any(t in page_text for t in cfg["in_stock_text"]):
        result["availability"] = "В наявності"

    return result if result.get("price") else None


def find_old_price(soup, current_price):
    candidates = []
    for sel in (".price-old", "s", "del", '[class*="old"]', '[class*="discount"]'):
        for el in soup.select(sel):
            text = el.get_text(strip=True)
            if len(text) > 30:
                continue
            price = clean_price(text)
            if price and current_price and price > current_price:
                candidates.append(price)
    return min(candidates) if candidates else None


def parse_url(url):
    store = urlparse(url).netloc.replace("www.", "")
    result = {
        "url": url, "store": store, "name": None, "price": None,
        "old_price": None, "currency": "UAH", "availability": None,
        "status": "ok", "error": None,
    }
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        if resp.encoding in (None, "ISO-8859-1"):
            resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text, "lxml")

        data = parse_jsonld(soup) or parse_meta(soup) or parse_selectors(soup)
        if not data:
            result["status"] = "no_data"
            result["error"] = "Не вдалося знайти ціну на сторінці"
            h1 = soup.select_one("h1")
            if h1:
                result["name"] = h1.get_text(strip=True)
            return result

        result.update({k: v for k, v in data.items() if v is not None})
        if not result.get("old_price"):
            result["old_price"] = find_old_price(soup, result.get("price"))
        if not result.get("name"):
            h1 = soup.select_one("h1")
            if h1:
                result["name"] = h1.get_text(strip=True)
    except requests.exceptions.Timeout:
        result.update(status="error", error="Сайт не відповів за 20 секунд")
    except requests.exceptions.HTTPError as exc:
        code = exc.response.status_code if exc.response is not None else "?"
        result.update(status="error", error=f"Сайт повернув помилку {code} (можливо, блокує ботів)")
    except requests.exceptions.RequestException:
        result.update(status="error", error="Не вдалося з'єднатися з сайтом")
    return result


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/parse", methods=["POST"])
def api_parse():
    payload = request.get_json(silent=True) or {}
    urls = payload.get("urls", [])
    urls = [u.strip() for u in urls if isinstance(u, str) and u.strip().startswith("http")]
    urls = list(dict.fromkeys(urls))[:30]
    if not urls:
        return jsonify({"error": "Додайте хоча б одне коректне посилання"}), 400

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(parse_url, urls))
    return jsonify({"results": results})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
