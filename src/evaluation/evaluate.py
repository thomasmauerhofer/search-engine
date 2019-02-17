#!/usr/bin/env python3
# encoding: utf-8
import ast
import copy
import os

from matplotlib import pyplot as plt
from config import REQ_DATA_PATH
from engine.api import API
from engine.datastore.ranking.mode import Mode
from engine.datastore.ranking.ranked_boolean_retrieval import RankedBoolean, RetrievalType
from engine.datastore.ranking.tf import TF
from engine.datastore.ranking.tfidf import TFIDF
from engine.datastore.models.section import IMRaDType


def average_precision(papers, relevant_papers):
    indexes = []
    ap = 0
    for relevant in relevant_papers:
        try:
            indexes.append([x["paper"].file for x in papers].index(relevant.file) + 1)
        except ValueError:
            pass

        if not indexes:
            return None

        indexes = sorted(indexes)
        for i in range(len(indexes)):
            ap += (i + 1) / indexes[i]

    return ap / len(indexes)


def histogram(data, title, filename):
    _, ax = plt.subplots()
    ax.hist(data, color='#539caf')
    ax.set_ylabel("frequency")
    ax.set_xlabel("rank")
    ax.set_title(title)
    # ax.set_ylim([0, 70])
    plt.savefig(filename + ".png")
    plt.close()


# ---------------------------------------------------------
#                Explict search
# ---------------------------------------------------------
def extract_query_ngramm(query, n):
    queries = []
    words = query.split()
    rounds = len(words) if n == 1 else len(words) - 1
    for i in range(0, rounds):
        query_list = words[i:i + n]
        if len(query_list) == n:
            query_words = " ".join(query_list)
            queries.append(query_words)
    return queries


def create_queries(n=None):
    queries = {}
    with open(os.path.join(REQ_DATA_PATH, "citations.txt"), encoding='utf-8') as data_file:
        data = ast.literal_eval(data_file.read())

    for citation in data:
        for imrad_type in citation["section"]["imrad"]:
            if imrad_type not in queries:
                queries[imrad_type] = []

            if n:
                ngramm = extract_query_ngramm(citation["search_query"], n)
                for query in ngramm:
                    entry = {"search_query": query, "references": citation["references"], "imrad": imrad_type}
                    queries[imrad_type].append(entry)
            else:
                entry = {"search_query": citation["search_query"], "references": citation["references"], "imrad": imrad_type}
                queries[imrad_type].append(entry)
    return queries


def calculate_ranking_sections(raw_queries, settings, plot=True):
    api = API()
    mean_ap_intro, mean_ap_background, mean_ap_methods, mean_ap_result, mean_ap_discussion = [], [], [], [], []

    queries = raw_queries[IMRaDType.INTRODUCTION.name] + raw_queries[IMRaDType.BACKGROUND.name] + \
              raw_queries[IMRaDType.METHODS.name] + raw_queries[IMRaDType.RESULTS.name] + \
              raw_queries[IMRaDType.DISCUSSION.name]

    for query in queries:
        relevant_paper = [api.get_paper(reference["paper_id"]) for reference in query["references"]]

        ranked_papers_intro = api.get_papers({IMRaDType.INTRODUCTION.name: query["search_query"]}, settings)
        ranked_papers_background = api.get_papers({IMRaDType.BACKGROUND.name: query["search_query"]}, settings)
        ranked_papers_methods = api.get_papers({IMRaDType.METHODS.name: query["search_query"]}, settings)
        ranked_papers_result = api.get_papers({IMRaDType.RESULTS.name: query["search_query"]}, settings)
        ranked_papers_discussion = api.get_papers({IMRaDType.DISCUSSION.name: query["search_query"]}, settings)

        ap_intro = average_precision(ranked_papers_intro, relevant_paper)
        ap_background = average_precision(ranked_papers_background, relevant_paper)
        ap_methods = average_precision(ranked_papers_methods, relevant_paper)
        ap_result = average_precision(ranked_papers_result, relevant_paper)
        ap_discussion = average_precision(ranked_papers_discussion, relevant_paper)

        if ap_intro and ap_background and ap_methods and ap_result and ap_discussion:
            mean_ap_intro.append(ap_intro)
            mean_ap_background.append(ap_background)
            mean_ap_methods.append(ap_methods)
            mean_ap_result.append(ap_result)
            mean_ap_discussion.append(ap_discussion)

    print("{} & {} & {} \\\\ \hline".format(Mode.only_introduction.name.replace("_", " "),
                                            len(mean_ap_intro), sum(mean_ap_intro) / len(mean_ap_intro)))
    print("{} & {} & {} \\\\ \hline".format(Mode.only_background.name.replace("_", " "),
                                            len(mean_ap_background), sum(mean_ap_background) / len(mean_ap_background)))
    print("{} & {} & {} \\\\ \hline".format(Mode.only_methods.name.replace("_", " "),
                                            len(mean_ap_methods), sum(mean_ap_methods) / len(mean_ap_methods)))
    print("{} & {} & {} \\\\ \hline".format(Mode.only_results.name.replace("_", " "),
                                            len(mean_ap_result), sum(mean_ap_result) / len(mean_ap_result)))
    print("{} & {} & {} \\\\ \hline".format(Mode.only_discussion.name.replace("_", " "),
                                            len(mean_ap_discussion), sum(mean_ap_discussion) / len(mean_ap_discussion)))
    if plot:
        histogram(mean_ap_intro, Mode.only_introduction.name.replace("_", " "), Mode.only_introduction.name.replace("_", " "))
        histogram(mean_ap_background, Mode.only_background.name.replace("_", " "), Mode.only_background.name.replace("_", " "))
        histogram(mean_ap_methods, Mode.only_methods.name.replace("_", " "), Mode.only_methods.name.replace("_", " "))
        histogram(mean_ap_result, Mode.only_results.name.replace("_", " "), Mode.only_results.name.replace("_", " "))
        histogram(mean_ap_discussion, Mode.only_discussion.name.replace("_", " "), Mode.only_discussion.name.replace("_", " "))


def calculate_ranking(raw_queries, settings, plot=True):
    api = API()
    mean_ap_whole = []
    mean_ap_doc = []

    queries = raw_queries[IMRaDType.INTRODUCTION.name] + raw_queries[IMRaDType.BACKGROUND.name] + \
              raw_queries[IMRaDType.METHODS.name] + raw_queries[IMRaDType.RESULTS.name] + \
              raw_queries[IMRaDType.DISCUSSION.name]

    settings["mode"] = Mode.without_importance_to_sections
    settings_sec = copy.deepcopy(settings)
    settings_sec["mode"] = Mode.importance_to_sections

    for query in queries:
        ranked_papers_whole = api.get_papers({"whole-document": query["search_query"]}, settings)
        ranked_papers_sec = api.get_papers({query["imrad"]: query["search_query"]}, settings_sec)

        relevant_paper = [api.get_paper(reference["paper_id"]) for reference in query["references"]]

        ap_whole = average_precision(ranked_papers_whole, relevant_paper)
        ap_doc = average_precision(ranked_papers_sec, relevant_paper)

        if ap_whole and ap_doc:
            mean_ap_whole.append(ap_whole)
            mean_ap_doc.append(ap_doc)

    print("{} & {} & {} \\\\ \hline".format(Mode.without_importance_to_sections.name.replace("_", " "), len(mean_ap_whole),
                                            sum(mean_ap_whole) / len(mean_ap_whole)))
    print("{} & {} & {} \\\\ \hline".format(Mode.importance_to_sections.name.replace("_", " "), len(mean_ap_doc),
                                            sum(mean_ap_doc) / len(mean_ap_doc)))
    if plot:
        histogram(mean_ap_whole, Mode.without_importance_to_sections.name.replace("_", " "),
                  Mode.without_importance_to_sections.name.replace("_", " "))
        histogram(mean_ap_doc, Mode.importance_to_sections.name.replace("_", " "),
                  Mode.importance_to_sections.name.replace("_", " "))


def evaluate_algorithm(settings, plot, n):
    print("\\begin{center}")
    print("\\begin{tabular}{ | c | c | l | }")
    print("\hline")
    print("\multicolumn{1}{|c}{} & \multicolumn{1}{|c}{\\textbf{\# queries}} & \multicolumn{1}{|c|}{\\textbf{MAP}} \\\\ \hline")

    raw_queries = create_queries(n)
    calculate_ranking(raw_queries, settings, plot)
    # TODO: split into own call....
    # settings["mode"] = Mode.importance_to_sections
    # calculate_ranking_sections(raw_queries, settings, plot)

    print("\end{tabular}")
    print("\end{center}\n")


def evaluate_tf(plot, n=None):
    print("Term Frequency")
    evaluate_algorithm(TF.get_default_config(), plot, n)


def evaluate_tfidf(plot, n=None):
    print("Term Frequency-Inverse Document Frequency")
    evaluate_algorithm(TFIDF.get_default_config(), plot, n)


def evaluate_ranked_boolean(plot, n=None):
    print("Ranked Boolean Retrieval")
    settings = {"algorithm": RankedBoolean.get_name(),
                "extended": False,
                "ranking-algo-params": {RetrievalType.TITLE.name: 0.2,
                                        RetrievalType.SECTION_TITLE.name: 0.3,
                                        RetrievalType.SECTION_TEXT.name: 0.2,
                                        RetrievalType.SUBSECTION_TITLE.name: 0.18,
                                        RetrievalType.SUBSECTION_TEXT.name: 0.05,
                                        RetrievalType.SUBSUBSECTION_TITLE.name: 0.05,
                                        RetrievalType.SUBSUBSECTION_TEXT.name: 0.02}}
    evaluate_algorithm(settings, plot, n)


def evaluate_explicit_search():
    save_plots = False

    for N in range(2, 5):
        print("\subsection{N =", N, "}")
        evaluate_tf(save_plots, N)
        evaluate_tfidf(save_plots, N)
        evaluate_ranked_boolean(save_plots, N)

    print("\subsection{Full queries}")
    evaluate_tf(save_plots)
    evaluate_tfidf(save_plots)
    evaluate_ranked_boolean(save_plots)


# ---------------------------------------------------------
#                More like this
# ---------------------------------------------------------
def calculate_ranking_mlt(settings):
    api = API()
    mean_ap = []

    papers = api.get_all_paper()
    for paper in papers:
        relevant_papers = [api.get_paper(ref.get_paper_id()) for ref in paper.references if ref.paper_id]
        if not relevant_papers:
            continue

        ranked_papers, queries = api.get_papers_with_paper(paper.filename, settings)
        ap = average_precision(ranked_papers, relevant_papers)
        if ap:
            mean_ap.append(ap)

    round_map = round(sum(mean_ap) / len(mean_ap), 4)
    print("{} & {} & {} \\\\ \hline".format(settings["mode"].name.replace("_", " "), len(mean_ap), round_map))


def evaluate_algorithm_mlt(settings):
    print("\\begin{center}")
    print("\\begin{tabular}{ | c | c | l | }")
    print("\hline")
    print("\multicolumn{1}{|c}{} & \multicolumn{1}{|c}{\\textbf{\# queries}} & \multicolumn{1}{|c|}{\\textbf{MAP}} \\\\ \hline")

    settings["mode"] = Mode.without_importance_to_sections
    calculate_ranking_mlt(settings)

    settings["mode"] = Mode.importance_to_sections
    print("Next line don't use unclassified chapters")
    settings["use-unclassified-chapters"] = False
    calculate_ranking_mlt(settings)
    print("Next line use unclassified chapters")
    settings["use-unclassified-chapters"] = True
    calculate_ranking_mlt(settings)

    # settings["mode"] = Mode.only_introduction
    # calculate_ranking_mlt(settings)
    # settings["mode"] = Mode.only_background
    # calculate_ranking_mlt(settings)
    # settings["mode"] = Mode.only_methods
    # calculate_ranking_mlt(settings)
    # settings["mode"] = Mode.only_results
    # calculate_ranking_mlt(settings)
    # settings["mode"] = Mode.only_discussion
    # calculate_ranking_mlt(settings)

    print("\end{tabular}")
    print("\end{center}\n")


def evaluate_tf_mlt():
    print("Term Frequency")
    evaluate_algorithm_mlt(TF.get_default_config())


def evaluate_tfidf_mlt():
    print("Term Frequency-Inverse Document Frequency")
    evaluate_algorithm_mlt(TFIDF.get_default_config())


def evaluate_ranked_boolean_mlt():
    print("Ranked Boolean Retrieval")
    settings = {"algorithm": RankedBoolean.get_name(),
                "extended": False,
                "ranking-algo-params": {RetrievalType.TITLE.name: 0.2,
                                        RetrievalType.SECTION_TITLE.name: 0.3,
                                        RetrievalType.SECTION_TEXT.name: 0.2,
                                        RetrievalType.SUBSECTION_TITLE.name: 0.18,
                                        RetrievalType.SUBSECTION_TEXT.name: 0.05,
                                        RetrievalType.SUBSUBSECTION_TITLE.name: 0.05,
                                        RetrievalType.SUBSUBSECTION_TEXT.name: 0.02}}
    evaluate_algorithm_mlt(settings)


def evaluate_ranked_boolean_extended_mlt():
    print("Ranked Boolean Retrieval-Extended Version")
    settings = {"algorithm": RankedBoolean.get_name(),
                "extended": True,
                "ranking-algo-params": {RetrievalType.TITLE.name: 0.05,
                                        RetrievalType.SECTION_TITLE.name: 0.05,
                                        RetrievalType.SECTION_TEXT.name: 0.8,
                                        RetrievalType.SUBSECTION_TITLE.name: 0.05,
                                        RetrievalType.SUBSECTION_TEXT.name: 0.03,
                                        RetrievalType.SUBSUBSECTION_TITLE.name: 0.01,
                                        RetrievalType.SUBSUBSECTION_TEXT.name: 0.01}}
    evaluate_algorithm_mlt(settings)


def evaluate_more_like_this():
    print("\section{More Like This}")
    evaluate_tf_mlt()
    evaluate_tfidf_mlt()
    evaluate_ranked_boolean_mlt()
    # evaluate_ranked_boolean_extended_mlt()


if __name__ == "__main__":
    # evaluate_explicit_search()
    evaluate_more_like_this()
