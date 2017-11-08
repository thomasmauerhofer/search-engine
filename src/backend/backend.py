# encoding: utf-8

from flask import Blueprint, render_template, request, redirect, current_app, send_file
import os
from backend.datastore.api import API

backend = Blueprint('backend', __name__)
api = API()


@backend.route('/', methods=["GET", 'POST'])
def index():
    if request.method == "POST":
        indro_query = request.form['intro_text']
        background_query = request.form['background_text']
        methods_query = request.form['methods_text']
        results_query = request.form['results_text']
        discussion_query = request.form['discussion_text']

        indro_proceed = api.preprocessor.proceed_query(indro_query)
        background_proceed = api.preprocessor.proceed_query(background_query)
        methods_proceed = api.preprocessor.proceed_query(methods_query)
        results_proceed = api.preprocessor.proceed_query(results_query)
        discussion_proceed = api.preprocessor.proceed_query(discussion_query)

        print("Intro query: ", indro_proceed)
        print("Background query: ", background_proceed)
        print("Methods query: ", methods_proceed)
        print("Results query: ", results_proceed)
        print("Discussion query: ", discussion_proceed)

        result = "result coming soon..."
        return render_template('result.html', indro_query=indro_query, background_query=background_query,
                               methods_query=methods_query, results_query=results_query,
                               discussion_query=discussion_query, result=result,)
    else:
        return render_template('index.html')


@backend.route('/upload', methods=["GET", 'POST'])
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


@backend.route('/view_pdf/<paper_id>', methods=['GET', 'POST'])
def view_pdf(paper_id):
    filepath = api.save_paper_as_pdf(paper_id)
    resp = send_file(filepath)
    api.delete_pdf(filepath)
    return resp
