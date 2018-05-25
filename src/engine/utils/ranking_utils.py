#!/usr/bin/env python3
# encoding: utf-8
import copy

from engine.utils.paper_utils import sections_to_word_hist
from engine.utils.string_utils import remove_multiple_spaces


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
            for word in query.split():
                keys_to_ignore = [key for key in ignoring_keys if word in key]
                if len(keys_to_ignore):
                    info[imrad_type]["ignored"].extend(keys_to_ignore)
                    ret[imrad_type] = remove_multiple_spaces(query.replace(word, ""))

    return ret, info


def combine_info(dict1, dict2):
    ret = copy.deepcopy(dict1)
    for imrad, value in dict2.items():
        for c_key, c_value in value.items():
            ret[imrad][c_key] = c_value
    return ret




