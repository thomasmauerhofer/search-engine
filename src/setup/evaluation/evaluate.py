#!/usr/bin/env python3
# encoding: utf-8
import ast
import copy
import os
import random
from enum import Enum

from matplotlib import pyplot as plt
from config import REQ_DATA_PATH
from engine.api import API
from engine.datastore.ranking.ranked_boolean_retrieval import RankedBoolean, RetrievalType
from engine.datastore.ranking.tf import TF
from engine.datastore.ranking.tfidf import TFIDF
from engine.datastore.models.section import IMRaDType


class Mode(Enum):
    without_importance_to_sections = 0
    importance_to_sections = 1
    only_introduction = 2
    only_background = 3
    only_methods = 4
    only_results = 5
    only_discussion = 6



def histogram(data, title, filename):
    _, ax = plt.subplots()
    ax.hist(data, color='#539caf')
    ax.set_ylabel("frequency")
    ax.set_xlabel("rank")
    ax.set_title(title)
    # ax.set_ylim([0, 70])
    plt.savefig(filename + ".png")
    plt.close()


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


def calculate_ranking_sections(raw_queries, mode, settings, plot=True):
    api = API()
    mean_ap = []

    min_val = min([len(raw_queries[IMRaDType.INTRODUCTION.name]), len(raw_queries[IMRaDType.BACKGROUND.name]),
                   len(raw_queries[IMRaDType.METHODS.name]), len(raw_queries[IMRaDType.RESULTS.name]),
                   len(raw_queries[IMRaDType.DISCUSSION.name])])

    queries = random.sample(raw_queries[IMRaDType(mode.value - 1).name], min_val)

    for query in queries:
        ranked_papers = api.get_papers({query["imrad"]: query["search_query"]}, settings)
        relevant_paper = [api.get_paper(reference["paper_id"]) for reference in query["references"]]
        ap = average_precision(ranked_papers, relevant_paper)

        if ap:
            mean_ap.append(ap)

    print("{} & {} & {} \\\\ \hline".format(mode.name.replace("_", " "), len(mean_ap), sum(mean_ap) / len(mean_ap)))
    if plot:
        histogram(mean_ap, mode.name.replace("_", " "), mode.name.replace("_", " "))


def calculate_ranking(raw_queries, settings, plot=True):
    api = API()
    mean_ap_whole = []
    mean_ap_doc = []

    queries = raw_queries[IMRaDType.INTRODUCTION.name] + raw_queries[IMRaDType.BACKGROUND.name] + \
              raw_queries[IMRaDType.METHODS.name] + raw_queries[IMRaDType.RESULTS.name] + \
              raw_queries[IMRaDType.DISCUSSION.name]

    settings_sec = copy.deepcopy(settings)
    settings_sec["importance_sections"] = True

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
    settings["importance_sections"] = False

    raw_queries = create_queries(n)
    calculate_ranking(raw_queries, settings, plot)
    settings["importance_sections"] = True
    calculate_ranking_sections(raw_queries, Mode.only_introduction, settings, plot)
    calculate_ranking_sections(raw_queries, Mode.only_background, settings, plot)
    calculate_ranking_sections(raw_queries, Mode.only_methods, settings, plot)
    calculate_ranking_sections(raw_queries, Mode.only_results, settings, plot)
    calculate_ranking_sections(raw_queries, Mode.only_discussion, settings, plot)
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


def evaluate_ranked_boolean_extended(plot, n=None):
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
    evaluate_algorithm(settings, plot, n)


if __name__ == "__main__":
    save_plots = False

    for N in range(2, 5):
        print("\subsection{N =", N, "}")
        evaluate_tf(save_plots, N)
        evaluate_tfidf(save_plots, N)
        evaluate_ranked_boolean(save_plots, N)
        evaluate_ranked_boolean_extended(save_plots, N)

    print("\subsection{Full queries}")
    evaluate_tf(save_plots)
    evaluate_tfidf(save_plots)
    evaluate_ranked_boolean(save_plots)
    evaluate_ranked_boolean_extended(save_plots)
