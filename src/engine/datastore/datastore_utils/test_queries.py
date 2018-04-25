#!/usr/bin/env python3
# encoding: utf-8
from engine.api import API
from engine.datastore.structure.section import IMRaDType


def get_papers_with_query():
    api = API()
    ret = api.get_papers_simple_ranking(queries)
    print(ret)


if __name__ == "__main__":
    queries = {IMRaDType.INDRODUCTION.name: "paper",
               IMRaDType.BACKGROUND: "",
               IMRaDType.METHODS.name: "inhom scenario allow user control home",
               IMRaDType.RESULTS.name: "",
               IMRaDType.DISCUSSION.name: ""}

    get_papers_with_query()
