# -*- coding: utf-8 -*-
"""
LPP Ukraine — UTM генератор.
Уся логіка UTM в index.html і працює в браузері. Сервер віддає сторінку
і скорочує посилання: із браузера запити до is.gd/TinyURL ріжуть CORS,
ORB у Chrome та блокувальники реклами, а з сервера таких обмежень немає.
"""

import os
import urllib.error
import urllib.parse
import urllib.request

from flask import Flask, jsonify, request, send_from_directory

ROOT = os.path.dirname(os.path.abspath(__file__))
# Скорочуємо лише посилання на кар'єрний сайт LPP, щоб сервер
# не став відкритим скорочувачем для чужих адрес.
ALLOWED_PREFIX = "https://lpp-sa.peopleforce.io/"
TIMEOUT = 3.5  # с на кожен сервіс; браузер чекає не довше 8 с
SHORTENERS = [
    ("is.gd", "https://is.gd/create.php?format=simple&url={}", "https://is.gd/"),
    ("tinyurl", "https://tinyurl.com/api-create.php?url={}", "https://tinyurl.com/"),
]

app = Flask(__name__)


def shorten(long_url):
    """Повертає коротке посилання або None, якщо жоден сервіс не відповів."""
    quoted = urllib.parse.quote(long_url, safe="")
    for name, template, expected in SHORTENERS:
        req = urllib.request.Request(
            template.format(quoted), headers={"User-Agent": "lpp-utm-generator"}
        )
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                text = resp.read(500).decode("utf-8", "replace").strip()
        except (urllib.error.URLError, OSError) as e:
            app.logger.warning("%s failed: %s", name, e)
            continue
        if text.startswith(expected):
            return text
        app.logger.warning("%s unexpected answer: %s", name, text[:200])
    return None


@app.route("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.route("/api/shorten")
def api_shorten():
    long_url = request.args.get("url", "")
    if not long_url.startswith(ALLOWED_PREFIX) or len(long_url) > 2000:
        return jsonify(error="url not allowed"), 400
    short = shorten(long_url)
    if not short:
        return jsonify(error="shortener unavailable"), 502
    return jsonify(shorturl=short)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
