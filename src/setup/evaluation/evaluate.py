#!/usr/bin/env python3
# encoding: utf-8
import ast
import os

import numpy as np
from matplotlib import pyplot as plt
from config import REQ_DATA_PATH
from engine.api import API



def histogram(data, title, filename):
    _, ax = plt.subplots()
    ax.hist(data, color='#539caf')
    ax.set_ylabel("frequency")
    ax.set_xlabel("rank")
    ax.set_title(title)
    plt.savefig(filename + ".png")


def calculate_ranking(name, mode):
    api = API()

    settings = {"importance_sections": True}
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
                # print("Error: {} -> {}".format(citation["full_citation"], reference["complete"]))
                pass


    print(name + ":")
    print("Mean: {} | {}".format(np.mean(ranks), np.mean(ranks_norm)))
    print("Standard Deviation: {} | {}".format(np.std(ranks), np.std(ranks_norm)))
    histogram(ranks, name, name)
    histogram(ranks_norm, name, name + "_norm")


def evaluate():
    calculate_ranking("Simple Approach - without importance to sections", 0)
    calculate_ranking("Simple Approach - only background", 1)
    calculate_ranking("Simple Approach - importance to sections", 2)


if __name__ == "__main__":
    evaluate()
