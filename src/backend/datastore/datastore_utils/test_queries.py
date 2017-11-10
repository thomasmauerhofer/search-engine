#!/usr/bin/env python3
# encoding: utf-8
from backend.datastore.api import API


def get_papers_with_query(indro_query, background_query, methods_query, results_query, discussion_query):
    api = API()
    api.get_ranked_papers_explicit(indro_query, background_query, methods_query, results_query, discussion_query)


if __name__ == "__main__":
    intro = "paper"
    background = ""
    methods = "inhom scenario allow user control home devic voic andor click architectur mimu first describ pérez et al 2006c work updat descript includ life demo mimu follow inform state updat approach dialogu manag develop eufund talk project talk project architectur consist setofoaaagentschey martin link central facilit shown figur"
    result = ""
    discussion = ""
    get_papers_with_query(intro, background, methods, result, discussion)
