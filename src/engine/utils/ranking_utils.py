#!/usr/bin/env python3
# encoding: utf-8
import copy

from engine.utils.paper_utils import sections_to_word_hist


def get_ignoring_keys(paper, queries, importance_sections):
    if not importance_sections:
        return paper.word_hist.query_to_keys(queries["whole-document"])

    ignored, sections = [], []
    for imrad, query in queries.items():
        if imrad == "whole-document":
            continue
        sections = paper.get_sections_with_imrad_type(imrad)
        ignored.extend(sections_to_word_hist(sections).query_to_keys(query))
    return ignored


def remove_ignored_words_from_query(paper, queries, importance_sections):
    info = {}
    ret = copy.deepcopy(queries)
    ignoring_keys = get_ignoring_keys(paper, queries, importance_sections)

    for imrad_type, query in ret.items():
        info[imrad_type] = {"ignored": []}
        if query == "":
            continue

        if (importance_sections and imrad_type == "whole-document") or (not importance_sections and imrad_type != "whole-document"):
            query = " " + query + " "
            for term in query.split():
                # ignoring_keys contain all keywords of the paper which can be
                # created for the whole doc/sections with the query
                keys_to_ignore = [key for key in ignoring_keys if term in key]

                # remove the term from the query
                if len(keys_to_ignore):
                    info[imrad_type]["ignored"].extend(keys_to_ignore)
                    query = query.replace(" " + term + " ", " ")
            ret[imrad_type] = query

    return ret, info


def combine_info(dict1, dict2):
    ret = copy.deepcopy(dict1)
    for imrad, value in dict2.items():
        for c_key, c_value in value.items():
            if imrad not in ret:
                ret[imrad] = {}
            ret[imrad][c_key] = c_value
    return ret




