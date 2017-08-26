#!/usr/bin/env python3
# encoding: utf-8

from flask import Blueprint, flash, redirect, render_template, request, session
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
	api = API()
	if api.check_user_login(request.form['username'], request.form['password']):
		session['logged_in'] = True
		papers = api.get_all_paper()
		return render_template('admin/papers.html', papers=papers)
	else:
		return redirect('admin/')

@admin.route('/admin/paper_info/<paper_id>', methods=['GET', 'POST'])
def paper_info(paper_id):
	api = API()
	paper = api.get_paper(paper_id)
	return render_template('admin/paper_info.html', paper=paper)
