#!/usr/bin/env python3
# encoding: utf-8

from flask import Flask
from backend.backend import backend

app = Flask(__name__)
app.register_blueprint(backend)

if __name__ == "__main__":
    app.run()
