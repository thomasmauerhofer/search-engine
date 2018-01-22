# encoding: utf-8

import os

from flask import Blueprint, render_template, request, redirect, current_app, send_file

from backend.datastore.api import API
from backend.datastore.structure.section import IMRaDType

backend = Blueprint('backend', __name__)
api = API()


@backend.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')

    queries = {IMRaDType.INDRODUCTION.name: request.form['intro_text'],
               IMRaDType.BACKGROUND.name: request.form['background_text'],
               IMRaDType.METHODS.name: request.form['methods_text'],
               IMRaDType.RESULTS.name: request.form['results_text'],
               IMRaDType.DISCUSSION.name: request.form['discussion_text']}

    if all(not query for query in queries.values()):
        return render_template('index.html')

    result = api.get_ranked_papers_explicit(queries)
    return render_template('result.html', queries=queries, result=result)


@backend.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)
        elif api.allowed_upload_file(file.filename):
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
            ret = api.add_paper(file.filename)

            if not ret:
                print("Error: Can't use this PDF")

    return render_template('upload.html')


@backend.route('/view_pdf/<paper_id>', methods=['GET'])
def view_pdf(paper_id):
    path = api.save_paper_as_pdf(paper_id)
    resp = send_file(path)
    api.delete_pdf(path)
    return resp
