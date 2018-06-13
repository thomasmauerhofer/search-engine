#!/usr/bin/env python3
# encoding: utf-8
import ast
import os
from enum import Enum

from matplotlib import pyplot as plt
from config import REQ_DATA_PATH
from engine.api import API
from engine.datastore.ranking.ranked_boolean_retrieval import RankedBoolean, RetrievalType
from engine.datastore.ranking.tf import TF
from engine.datastore.ranking.tfidf import TFIDF
from engine.datastore.structure.section import IMRaDType


class Mode(Enum):
    without_importance_to_sections = 0
    importance_to_sections = 1
    only_introduction = 2
    only_background = 3
    only_methods = 4
    only_results = 5
    only_discussion = 6


def calculate_ranking(mode, settings, plot=True):
    api = API()
    mean_ap = []

    with open(os.path.join(REQ_DATA_PATH, "citations.txt"), encoding='utf-8') as data_file:
        data = ast.literal_eval(data_file.read())

    for citation in data:
        query = {}
        if mode == Mode.without_importance_to_sections:
            query = {"whole-document": citation["search_query"]}
        elif mode == Mode.only_introduction:
            query = {IMRaDType.INTRODUCTION.name: citation["search_query"]}
        elif mode == Mode.only_background:
            query = {IMRaDType.BACKGROUND.name: citation["search_query"]}
        elif mode == Mode.only_methods:
            query = {IMRaDType.METHODS.name: citation["search_query"]}
        elif mode == Mode.only_discussion:
            query = {IMRaDType.DISCUSSION.name: citation["search_query"]}
        elif mode == Mode.only_results:
            query = {IMRaDType.RESULTS.name: citation["search_query"]}
        elif mode == Mode.importance_to_sections:
            for imrad_type in citation["section"]["imrad"]:
                query[imrad_type] = citation["search_query"]

        ranked_papers = api.get_papers(query, settings)
        relevant_paper = [api.get_paper(reference["paper_id"]) for reference in citation["references"]]
        ap = average_precision(ranked_papers, relevant_paper)

        if ap:
            mean_ap.append(ap)

    print("{} & {} & {} \\\\ \hline".format(mode.name.replace("_", " "), len(mean_ap), sum(mean_ap) / len(mean_ap)))
    if plot:
        histogram(mean_ap, mode.name.replace("_", " "), mode.name.replace("_", " "))


def histogram(data, title, filename):
    _, ax = plt.subplots()
    ax.hist(data, color='#539caf')
    ax.set_ylabel("frequency")
    ax.set_xlabel("rank")
    ax.set_title(title)
    #ax.set_ylim([0, 70])
    plt.savefig(filename + ".png")
    plt.close()


def average_precision(papers, relevant_papers):
    indexes = []
    ap = 0
    for relevant in relevant_papers:
        try:
            indexes.append([x["paper"].filename for x in papers].index(relevant.filename) + 1)
        except ValueError:
            pass

        if not indexes:
            return None

        indexes = sorted(indexes)
        for i in range(len(indexes)):
            ap += (i + 1) / indexes[i]

    return ap / len(indexes)


def extract_query_ngramm(citation, mode, n):
    queries = []
    words = citation["search_query"].split()
    rounds = len(words) if n == 1 else len(words) - 1
    for i in range(0, rounds):
        query_list = words[i:i + n]
        if len(query_list) == n:
            query = {}

            query_words = " ".join(query_list)
            if mode == Mode.without_importance_to_sections:
                query = {"whole-document": query_words}
            elif mode == Mode.only_introduction:
                query = {IMRaDType.INTRODUCTION.name: query_words}
            elif mode == Mode.only_background:
                query = {IMRaDType.BACKGROUND.name: query_words}
            elif mode == Mode.only_methods:
                query = {IMRaDType.METHODS.name: query_words}
            elif mode == Mode.only_discussion:
                query = {IMRaDType.DISCUSSION.name: query_words}
            elif mode == Mode.only_results:
                query = {IMRaDType.RESULTS.name: query_words}
            elif mode == Mode.importance_to_sections:
                for imrad_type in citation["section"]["imrad"]:
                    query[imrad_type] = query_words

            queries.append(query)
    return queries


def calculate_ranking_ngramm(mode, settings, plot=True, n=1):
    api = API()
    mean_ap = []

    with open(os.path.join(REQ_DATA_PATH, "citations.txt"), encoding='utf-8') as data_file:
        data = ast.literal_eval(data_file.read())

    for citation in data:
        queries = extract_query_ngramm(citation, mode, n)
        for query in queries:
            ranked_papers = api.get_papers(query, settings)
            relevant_paper = [api.get_paper(reference["paper_id"]) for reference in citation["references"]]
            ap = average_precision(ranked_papers, relevant_paper)

            if ap:
                mean_ap.append(ap)

    print("{} & {} & {} \\\\ \hline".format(mode.name.replace("_", " "), len(mean_ap), sum(mean_ap) / len(mean_ap)))


def evaluate_algorithm(settings, plot, n):
    print("\\begin{center}")
    print("\\begin{tabular}{ | c | c | l | }")
    print("\hline")
    print("\multicolumn{1}{|c}{} & \multicolumn{1}{|c}{\\textbf{\# queries}} & \multicolumn{1}{|c|}{\\textbf{MAP}} \\\\ \hline")
    settings["importance_sections"] = False

    if n:
        calculate_ranking_ngramm(Mode.without_importance_to_sections, settings, plot, n)
        settings["importance_sections"] = True
        calculate_ranking_ngramm(Mode.importance_to_sections, settings, plot, n)
        calculate_ranking_ngramm(Mode.only_introduction, settings, plot, n)
        calculate_ranking_ngramm(Mode.only_background, settings, plot, n)
        calculate_ranking_ngramm(Mode.only_methods, settings, plot, n)
        calculate_ranking_ngramm(Mode.only_results, settings, plot, n)
        calculate_ranking_ngramm(Mode.only_discussion, settings, plot, n)
    else:
        calculate_ranking(Mode.without_importance_to_sections, settings, plot)
        settings["importance_sections"] = True
        calculate_ranking(Mode.importance_to_sections, settings, plot)
        calculate_ranking(Mode.only_introduction, settings, plot)
        calculate_ranking(Mode.only_background, settings, plot)
        calculate_ranking(Mode.only_methods, settings, plot)
        calculate_ranking(Mode.only_results, settings, plot)
        calculate_ranking(Mode.only_discussion, settings, plot)
    print("\end{tabular}")
    print("\end{center}\n")


def evaluate_tf(plot, n):
    print("Term Frequency")
    evaluate_algorithm(TF.get_default_config(), plot, n)


def evaluate_tfidf(plot, n):
    print("Term Frequency-Inverse Document Frequency")
    evaluate_algorithm(TFIDF.get_default_config(), plot, n)


def evaluate_ranked_boolean(plot, n):
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


def evaluate_ranked_boolean_extended(plot, n):
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


def tmp(plot):
    print("Term Frequency")
    evaluate_algorithm(TF.get_default_config(), plot, None)

    print("Term Frequency-Inverse Document Frequency")
    evaluate_algorithm(TFIDF.get_default_config(), plot, None)

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
    evaluate_algorithm(settings, plot, None)

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
    evaluate_algorithm(settings, plot, None)




if __name__ == "__main__":
    save_plots = False
    tmp(save_plots)
    exit(0)

    for N in range(1, 4):
        print("\subsection{N =", N, "}")
        evaluate_tf(save_plots, N)
        evaluate_tfidf(save_plots, N)
        evaluate_ranked_boolean(save_plots, N)
        evaluate_ranked_boolean_extended(save_plots, N)
