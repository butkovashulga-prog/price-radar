# -*- coding: utf-8 -*-
"""
LPP Ukraine — UTM генератор.
Уся логіка в index.html і працює в браузері; сервер лише віддає цю сторінку.
"""

import os

from flask import Flask, send_from_directory

ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory(ROOT, "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
