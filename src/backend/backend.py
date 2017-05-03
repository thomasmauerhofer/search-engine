# encoding: utf-8

from flask import Blueprint, render_template, request, make_response, redirect, url_for

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

@backend.route('/add')
def add():
    print ("Implement Method to add pdf")
