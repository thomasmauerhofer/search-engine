#!/usr/bin/env python3
# encoding: utf-8

from flask import Flask
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

app = Flask(__name__)
app.register_blueprint(backend)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

if __name__ == "__main__":
	app.run()
