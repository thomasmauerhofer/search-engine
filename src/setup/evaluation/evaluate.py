#!/usr/bin/env python3
# encoding: utf-8
import ast
import os

from config import REQ_DATA_PATH
from engine.api import API


def evaluate():
    api = API()
    with open(os.path.join(REQ_DATA_PATH, "citations.txt"), encoding='utf-8') as data_file:
        data = ast.literal_eval(data_file.read())

    ''' Keys:
    search_query: str
    filename: str
    full_citation: str
    references: []
    section:[{ name: str
                imrad': []
            }]

    '''


    ''',
               IMRaDType.INDRODUCTION.name: "paper",
               IMRaDType.BACKGROUND: "",
               IMRaDType.METHODS.name: "inhom scenario allow user control home",
               IMRaDType.RESULTS.name: "",
               IMRaDType.DISCUSSION.name: ""}'''

    settings = {"importance_sections": False}
    for citation in data:
        raking = api.get_papers_simple_ranking({"whole-document": citation["search_query"]}, settings)
        print(raking)
        #exit()


if __name__ == "__main__":
    evaluate()
