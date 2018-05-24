#!/usr/bin/env python3
# encoding: utf-8
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


def get_query_keys(paper, queries, importance_sections):
    keys, ignored_keys = {}, {}
    ignoring_keys = get_ignoring_keys(paper, queries, importance_sections)

    for imrad_type, query in queries.items():
        if query == "":
            continue

        if imrad_type == "whole-document":
            hist = paper.word_hist
        else:
            sections = paper.get_sections_with_imrad_type(imrad_type)
            hist = sections_to_word_hist(sections)

        keys[imrad_type] = hist.query_to_keys(query)
        ignored_keys[imrad_type] = []
        if (importance_sections and imrad_type == "whole-document") or (not importance_sections and imrad_type != "whole-document"):
            for ignoring_key in ignoring_keys:
                if ignoring_key in keys[imrad_type]:
                    ignored_keys[imrad_type].append(ignoring_key)
                    keys[imrad_type].remove(ignoring_key)

    return keys, ignored_keys



