# encoding: utf-8
import json
import os

from flask import Blueprint, render_template, request, current_app, send_file

from engine.api import API
from engine.datastore.ranking.ranked_boolean_retrieval import RankedBoolean
from engine.datastore.ranking.tfidf import TFIDF
from engine.datastore.models.section import IMRaDType

backend = Blueprint('backend', __name__)
api = API()


@backend.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html', error=None, algorithm=api.get_ranking_algos())

    queries = {
        "whole-document": request.form['whole_text'],
        IMRaDType.INTRODUCTION.name: request.form['intro_text'],
        IMRaDType.BACKGROUND.name: request.form['background_text'],
        IMRaDType.METHODS.name: request.form['methods_text'],
        IMRaDType.RESULTS.name: request.form['results_text'],
        IMRaDType.DISCUSSION.name: request.form['discussion_text']}

    if all(not query for query in queries.values()):
        return '', 204

    settings = {"mode": bool(request.form['importance']),
                "algorithm": request.form["algorithm"]}

    if settings["algorithm"] == RankedBoolean.get_name():
        settings.update(RankedBoolean.get_default_config())

    result = api.get_papers(queries, settings)
    return render_template('result.html', queries=queries, settings=settings, result=result, algorithm=api.get_ranking_algos())


@backend.route('/search_with_pdf', methods=["GET", "POST"])
def search_with_pdf():
    file = request.files['file']

    if file.filename == '' or not api.allowed_upload_file(file.filename):
        return '', 204

    settings = {"importance_sections": bool(request.form['importance']), "algorithm": request.form["algorithm"]}

    if settings["algorithm"] == RankedBoolean.get_name():
        settings.update(RankedBoolean.get_default_config())

    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
    try:
        result, queries = api.get_papers_with_paper(file.filename, settings)
        return render_template('result.html', queries=queries, settings=settings, result=result, algorithm=api.get_ranking_algos())
    except EnvironmentError as e:
        return render_template('index.html', settings=settings, error=str(e), algorithm=api.get_ranking_algos())


@backend.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files')

        if not files:
            return '', 204

        for file in files:
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
        api.add_papers(files)
    return render_template('upload.html')


@backend.route('/get_ranking_info/<paper_id>', methods=["GET", "POST"])
def get_ranking_info(paper_id):
    settings = {"mode": json.loads(request.form['importance'].lower()),
                "algorithm": request.form["algorithm"]}

    queries = {
        "whole-document": request.form["whole-document"],
        IMRaDType.INTRODUCTION.name: request.form[IMRaDType.INTRODUCTION.name],
        IMRaDType.BACKGROUND.name: request.form[IMRaDType.BACKGROUND.name],
        IMRaDType.METHODS.name: request.form[IMRaDType.METHODS.name],
        IMRaDType.RESULTS.name: request.form[IMRaDType.RESULTS.name],
        IMRaDType.DISCUSSION.name: request.form[IMRaDType.DISCUSSION.name]}

    paper, papers = api.get_paper(paper_id), []
    queries_proceed = api.preprocessor.proceed_queries(queries)

    if settings["algorithm"] == RankedBoolean.get_name():
        settings.update(RankedBoolean.get_default_config())

    if settings["algorithm"] == TFIDF.get_name():
        papers = api.client.get_paper_which_contains_queries(queries_proceed)
        settings["idf"] = TFIDF.get_idf(queries_proceed, papers)

    ret = api.get_ranking_info(paper, queries_proceed, settings)

    if settings["algorithm"] == RankedBoolean.get_name():
        overall = ret["info"].pop("overall")
        return render_template('ranking_info_pages/result_info_ranked_boolean.html', queries=queries,
                               result={"paper": paper, "overall": overall, "info": ret["info"]})
    elif settings["algorithm"] == TFIDF.get_name():
        return render_template('ranking_info_pages/result_info_tfidf.html', queries=queries,
                               result={"paper": paper, "rank": ret["rank"], "info": ret["info"], "N": len(papers)})
    else:
        return render_template('ranking_info_pages/result_info_tf.html', queries=queries,
                               result={"paper": paper, "rank": ret["rank"], "info": ret["info"]})


@backend.route('/view_pdf/<paper_id>', methods=["GET", "POST"])
def view_pdf(paper_id):
    path = api.save_paper_as_pdf(paper_id)
    resp = send_file(path)
    api.delete_pdf(path)
    return resp
