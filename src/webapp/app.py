#!/usr/bin/env python3
# encoding: utf-8

import os
from flask import Flask
from flask_session import Session
from datetime import timedelta

from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, KEYS
from webapp.admin_view import admin
from webapp.backend import backend

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

app = Flask(__name__)
session = Session()
session.permanent = True

app.register_blueprint(backend)
app.register_blueprint(admin)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

key = os.path.join(KEYS, "secret_key")

try:
    app.config['SECRET_KEY'] = open(key, 'rb').read()
except IOError:
    os.makedirs(KEYS, exist_ok=True)
    os.system("head -c 24 /dev/urandom >" + key)
    app.config['SECRET_KEY'] = open(key, 'rb').read()

app.permanent_session_lifetime = timedelta(minutes=5)

if __name__ == "__main__":
    app.run()
