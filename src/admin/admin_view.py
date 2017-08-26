#!/usr/bin/env python3
# encoding: utf-8

import base64
from Crypto.Cipher import AES
from flask import Blueprint, flash, redirect, render_template, request, session
from config import SHA3_KEY, admin_user, admin_password
from backend.datastore.api import API

admin = Blueprint('admin', __name__)


@admin.route('/admin/', methods=['GET', 'POST'])
def admin_index():
	if 'logged_in' in session.keys() and session['logged_in']:
		api = API()
		papers = api.get_all_paper()
		return render_template('admin/papers.html', papers=papers)
	else:
		return render_template('admin/index.html')


@admin.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
	if request.method == 'GET':
		return redirect('admin/')

	if request.form['username'] == admin_user and \
		encrypt(request.form['password']) == admin_password:
		session['logged_in'] = True

		api = API()
		papers = api.get_all_paper()

		return render_template('admin/papers.html', papers=papers)
	else:
		return redirect('admin/')

@admin.route('/admin/paper_info/<paper_id>', methods=['GET', 'POST'])
def paper_info(paper_id):
	api = API()
	paper = api.get_paper(paper_id)
	return render_template('admin/paper_info.html', paper=paper)


def encrypt(decoded):
	cipher = AES.new(SHA3_KEY, AES.MODE_ECB)
	return base64.b64encode(cipher.encrypt(decoded.rjust(128))).decode('ascii')


def decrypt(encoded):
	encoded = encoded.encode('ascii')
	cipher = AES.new(SHA3_KEY, AES.MODE_ECB)
	return cipher.decrypt(base64.b64decode(encoded)).decode('ascii').strip()
