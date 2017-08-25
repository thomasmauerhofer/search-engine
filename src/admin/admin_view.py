#!/usr/bin/env python3
# encoding: utf-8

import base64
from Crypto.Cipher import AES
from flask import Blueprint, flash, redirect, render_template, request, session
from config import SHA3_KEY, admin_user, admin_password

admin = Blueprint('admin', __name__)


@admin.route('/admin/', methods=["GET", 'POST'])
def admin_index():
	return render_template('admin/index.html')


@admin.route('/admin/login', methods=['POST'])
def admin_login():
	if request.form['username'] == admin_user and \
		encrypt(request.form['password']) == admin_password:
		session['logged_in'] = True
		return render_template('admin/papers.html')
	else:
		return redirect('admin/')


def encrypt(decoded):
	cipher = AES.new(SHA3_KEY, AES.MODE_ECB)
	return base64.b64encode(cipher.encrypt(decoded.rjust(128))).decode('ascii')


def decrypt(encoded):
	encoded = encoded.encode('ascii')
	cipher = AES.new(SHA3_KEY, AES.MODE_ECB)
	return cipher.decrypt(base64.b64decode(encoded)).decode('ascii').strip()
