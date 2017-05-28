#!/usr/bin/env python3
# encoding: utf-8

from flask import Flask
from backend.backend import backend

UPLOAD_FOLDER = 'static/data'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.register_blueprint(backend)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

if __name__ == "__main__":
	app.run()
