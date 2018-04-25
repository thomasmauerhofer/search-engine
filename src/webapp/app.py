#!/usr/bin/env python3
# encoding: utf-8

import os
from flask import Flask
from flask_session import Session
from datetime import timedelta

from config import SESSION_KEY, ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from webapp.admin_view import admin
from webapp.backend import backend

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

app = Flask(__name__)
session = Session()
session.permanent = True

app.config['SECRET_KEY'] = SESSION_KEY
app.permanent_session_lifetime = timedelta(minutes=5)

app.register_blueprint(backend)
app.register_blueprint(admin)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run()
