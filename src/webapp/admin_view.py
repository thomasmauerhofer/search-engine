#!/usr/bin/env python3
# encoding: utf-8
from flask import session, render_template, request, redirect, Blueprint

from engine.api import API

admin = Blueprint('admin', __name__)


@admin.route('/admin/', methods=['GET'])
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


@admin.route('/admin/logout', methods=['POST'])
def admin_logout():
    session['logged_in'] = False
    return redirect('admin/')


@admin.route('/admin/paper_info/<paper_id>', methods=['GET'])
def paper_info(paper_id):
    api = API()
    papers = api.get_all_paper()
    id_to_filename = {paper.id: paper.filename for paper in papers}
    paper = api.get_paper(paper_id)

    return render_template('admin/paper_info.html', paper=paper, id_to_filename=id_to_filename)


@admin.route('/admin/user_info', methods=['GET'])
def user_info():
    if not ('logged_in' in session.keys() and session['logged_in']):
        return redirect('admin/')

    api = API()
    users = api.get_all_user()
    return render_template('admin/users.html', users=users)


@admin.route('/admin/remove_link/<paper_id>', methods=['POST'])
def remove_link(paper_id):
    if not ('logged_in' in session.keys() and session['logged_in']):
        return redirect('admin/')

    api = API()
    api.remove__link_of_paper(paper_id, request.form['ref_paper_id'])

    papers = api.get_all_paper()
    id_to_filename = {paper.id: paper.filename for paper in papers}
    paper = api.get_paper(paper_id)
    return render_template('admin/paper_info.html', paper=paper, id_to_filename=id_to_filename)


