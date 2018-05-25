# encoding: utf-8

import os

from flask import Blueprint, render_template, request, current_app, send_file

from config import USED_ALGORITHM
from engine.api import API
from engine.datastore.ranking.ranked_boolean_retrieval import RankedBooleanRetrieval
from engine.datastore.ranking.ranking_simple import RankingSimple
from engine.datastore.structure.section import IMRaDType
from engine.utils.exceptions.import_exceptions import ClassificationError
from engine.utils.string_utils import load_json

backend = Blueprint('backend', __name__)
api = API()


def __get_settings():
    if USED_ALGORITHM == RankedBooleanRetrieval.get_name():
        return RankedBooleanRetrieval.get_configuration()
    else:
        return RankingSimple.get_configuration()



@backend.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html', settings=__get_settings(), error=None)

    queries = {
        "whole-document": request.form['whole_text'],
        IMRaDType.INTRODUCTION.name: request.form['intro_text'],
        IMRaDType.BACKGROUND.name: request.form['background_text'],
        IMRaDType.METHODS.name: request.form['methods_text'],
        IMRaDType.RESULTS.name: request.form['results_text'],
        IMRaDType.DISCUSSION.name: request.form['discussion_text']}

    if all(not query for query in queries.values()):
        return '', 204

    settings = {"importance_sections": bool(request.form['importance']),
                "algorithm": request.form["algorithm"]}

    if settings["algorithm"] == RankedBooleanRetrieval.get_name():
        settings["ranking-algo-params"] = load_json(request.form["ranking-algo-params"])

    result = api.get_papers(queries, settings)
    return render_template('result.html', queries=queries, settings=settings, result=result)


@backend.route('/search_with_pdf', methods=["GET", "POST"])
def search_with_pdf():
    file = request.files['file']

    if file.filename == '' or not api.allowed_upload_file(file.filename):
        return '', 204

    settings = {"importance_sections": bool(request.form['importance']),
                "algorithm": request.form["algorithm"]}

    if settings["algorithm"] == RankedBooleanRetrieval.get_name():
        settings["ranking-algo-params"] = load_json(request.form["ranking-algo-params"])

    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
    try:
        result, queries = api.get_papers_with_paper(file.filename, settings)
        return render_template('result.html', queries=queries, settings=settings, result=result)
    except EnvironmentError as e:
        return render_template('index.html', settings=settings, error=str(e))


@backend.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        file = request.files['file']

        if file.filename == '' or not api.allowed_upload_file(file.filename):
            return '', 204

        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
        try:
            api.add_paper(file.filename)
        except IOError as e:
            print(e)
        except OSError as e:
            print(e)
        except ClassificationError as e:
            print(e)

    return render_template('upload.html')


@backend.route('/get_ranking_info/<paper_id>', methods=["GET", "POST"])
def get_ranking_info(paper_id):
    settings = {"importance_sections": bool(request.form['importance']),
                "algorithm": request.form["algorithm"]}

    if settings["algorithm"] == RankedBooleanRetrieval.get_name():
        settings["ranking-algo-params"] = load_json(request.form["ranking-algo-params"])

    queries = {
        "whole-document": request.form["whole-document"],
        IMRaDType.INTRODUCTION.name: request.form[IMRaDType.INTRODUCTION.name],
        IMRaDType.BACKGROUND.name: request.form[IMRaDType.BACKGROUND.name],
        IMRaDType.METHODS.name: request.form[IMRaDType.METHODS.name],
        IMRaDType.RESULTS.name: request.form[IMRaDType.RESULTS.name],
        IMRaDType.DISCUSSION.name: request.form[IMRaDType.DISCUSSION.name]}

    paper = api.get_paper(paper_id)
    queries_proceed = api.preprocessor.proceed_queries(queries)
    ret = api.get_ranking_info(paper, queries_proceed, settings)

    if settings["algorithm"] == RankedBooleanRetrieval.get_name():
        overall = ret["info"].pop("overall")
        return render_template('result_info_ranked_boolean.html', queries=queries,
                               result={"paper": paper, "overall": overall, "info": ret["info"]})
    else:
        return render_template('result_info_simple.html', queries=queries,
                               result={"paper": paper, "rank": ret["rank"], "info": ret["info"]})


@backend.route('/view_pdf/<paper_id>', methods=["GET", "POST"])
def view_pdf(paper_id):
    path = api.save_paper_as_pdf(paper_id)
    resp = send_file(path)
    api.delete_pdf(path)
    return resp
