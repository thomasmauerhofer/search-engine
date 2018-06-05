#!/usr/bin/env python3
# encoding: utf-8
import ast
import os

import numpy as np
from matplotlib import pyplot as plt
from config import REQ_DATA_PATH
from engine.api import API
from engine.datastore.ranking.ranked_boolean_retrieval import RankedBoolean, RetrievalType
from engine.datastore.ranking.tf import TF
from engine.datastore.ranking.tfidf import TFIDF


def histogram(data, title, filename):
    _, ax = plt.subplots()
    ax.hist(data, color='#539caf')
    ax.set_ylabel("frequency")
    ax.set_xlabel("rank")
    ax.set_title(title)
    #ax.set_ylim([0, 70])
    plt.savefig(filename + ".png")
    plt.close()


def calculate_ranking(name, mode, settings, plot=True):
    api = API()

    ranks = []
    ranks_norm = []

    with open(os.path.join(REQ_DATA_PATH, "citations.txt"), encoding='utf-8') as data_file:
        data = ast.literal_eval(data_file.read())

    for citation in data:
        if mode == 0:
            query = {"whole-document": citation["search_query"]}
        elif mode == 1:
            query = {"BACKGROUND": citation["search_query"]}
        else:
            query = {}
            for imrad_type in citation["section"]["imrad"]:
                query[imrad_type] = citation["search_query"]


        ranking = api.get_papers(query, settings)

        for reference in citation["references"]:
            referred_paper = api.get_paper(reference["paper_id"])
            try:
                index = [x["paper"].filename for x in ranking].index(referred_paper.filename)
                ranks.append(index)
                ranks_norm.append(index / len(ranking))
            except ValueError:
                print("Error: {} -> {}".format(citation["full_citation"], reference["complete"]))
                pass

    if plot:
        print(name + ":")
        print("# ratings: {}".format(len(ranks_norm)))
        print("Mean: {} | {}".format(np.mean(ranks), np.mean(ranks_norm)))
        print("Standard Deviation: {} | {}".format(np.std(ranks), np.std(ranks_norm)))
        histogram(ranks, name, name)
        histogram(ranks_norm, name, name + "_norm")

    return np.mean(ranks), np.std(ranks)


def evaluate_tf():
    settings = {**{"importance_sections": False}, **TF.get_default_config()}
    calculate_ranking("tf - without importance to sections", 0, settings)
    settings["importance_sections"] = True
    calculate_ranking("tf - only background", 1, settings)
    calculate_ranking("tf - importance to sections", 2, settings)


def evaluate_tfidf():
    settings = {**{"importance_sections": False}, **TFIDF.get_default_config()}
    calculate_ranking("tf-idf - without importance to sections", 0, settings)
    settings["importance_sections"] = True
    calculate_ranking("tf-idf - only background", 1, settings)
    calculate_ranking("tf-idf - importance to sections", 2, settings)


def evaluate_ranked_boolean():
    settings = {"importance_sections": False,
                "algorithm": RankedBoolean.get_name(),
                "extended": False,
                "ranking-algo-params": {RetrievalType.TITLE.name: 0.2,
                                        RetrievalType.SECTION_TITLE.name: 0.3,
                                        RetrievalType.SECTION_TEXT.name: 0.2,
                                        RetrievalType.SUBSECTION_TITLE.name: 0.18,
                                        RetrievalType.SUBSECTION_TEXT.name: 0.05,
                                        RetrievalType.SUBSUBSECTION_TITLE.name: 0.05,
                                        RetrievalType.SUBSUBSECTION_TEXT.name: 0.02}}
    calculate_ranking("Ranked Boolean - without importance to sections", 0, settings)
    settings["importance_sections"] = True
    calculate_ranking("Ranked Boolean - only background", 1, settings)
    calculate_ranking("Ranked Boolean - importance to sections", 2, settings)


def evaluate_ranked_boolean_extended():
    settings = {"importance_sections": False,
                "algorithm": RankedBoolean.get_name(),
                "extended": True,
                "ranking-algo-params": {RetrievalType.TITLE.name: 0.05,
                                        RetrievalType.SECTION_TITLE.name: 0.05,
                                        RetrievalType.SECTION_TEXT.name: 0.8,
                                        RetrievalType.SUBSECTION_TITLE.name: 0.05,
                                        RetrievalType.SUBSECTION_TEXT.name: 0.03,
                                        RetrievalType.SUBSUBSECTION_TITLE.name: 0.01,
                                        RetrievalType.SUBSUBSECTION_TEXT.name: 0.01}}
    calculate_ranking("Ranked Boolean extended - without importance to sections", 0, settings)
    settings["importance_sections"] = True
    calculate_ranking("Ranked Boolean extended - only background", 1, settings)
    calculate_ranking("Ranked Boolean extended - importance to sections", 2, settings)


if __name__ == "__main__":
    evaluate_tf()
    evaluate_tfidf()
    evaluate_ranked_boolean()
    evaluate_ranked_boolean_extended()

