# encoding: utf-8

from flask import Blueprint, render_template, request, redirect
from flask import current_app as app
import os

backend = Blueprint('profile', __name__)

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

		file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
		return redirect(request.url)

	return render_template('upload.html')
