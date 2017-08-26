# encoding: utf-8

from flask import Blueprint, render_template, request, redirect, current_app, send_file
import os
from backend.datastore.api import API

backend = Blueprint('backend', __name__)
api = API()

@backend.route('/', methods=["GET", 'POST'])
def index():
    if request.method == "POST":
        query = request.form['search_text']
        print("Current query: ", query)

        result = "hier kommt result hin"
        return render_template('result.html', input_text=query, result=result)
    else:
        return render_template('index.html')


@backend.route('/upload', methods=["GET", 'POST'])
def upload():
	if request.method == 'POST':
		file = request.files['file']

		if file.filename == '':
			return redirect(request.url)
		elif api.allowed__upload_file(file.filename):
			file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
			api.add_paper(file.filename)

	return render_template('upload.html')


@backend.route('/view_pdf/<paper_id>', methods=['GET', 'POST'])
def view_pdf(paper_id):
	api = API()
	filepath = api.save_paper_as_pdf(paper_id)
	resp = send_file(filepath)
	api.delete_pdf(filepath)
	return resp
