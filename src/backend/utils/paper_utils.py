#!/usr/bin/env python3
# encoding: utf-8
from backend.datastore.structure.section import IMRaDType
from backend.utils.objects.word_hist import WordHist


def sections_to_word_hist(sections):
    hist = WordHist()

    for section in sections:
        hist.append(section.get_combined_word_hist())
    return hist


def paper_to_queries(paper, mode):
    queries = {
        "whole-document": "",
        IMRaDType.INDRODUCTION.name: "",
        IMRaDType.BACKGROUND.name: "",
        IMRaDType.METHODS.name: "",
        IMRaDType.RESULTS.name: "",
        IMRaDType.DISCUSSION.name: ""
    }

    if mode == "doc-all":
        queries["whole-document"] = paper.get_combined_word_hist().keys_to_query()

    if mode == "doc-categorized":
        queries["whole-document"] = sections_to_word_hist(paper.get_sections_with_an_imrad_type()).keys_to_query()

    if mode == "background" or mode == "sections-categorized" or mode == "sections-uncategorized-sec" or mode == "sections-uncategorized-doc":
        queries[IMRaDType.BACKGROUND.name] = sections_to_word_hist(paper.get_background()).keys_to_query()

    if mode == "sections-categorized" or mode == "sections-uncategorized-sec" or mode == "sections-uncategorized-doc":
        queries[IMRaDType.INDRODUCTION.name] = sections_to_word_hist(paper.get_introduction()).keys_to_query()
        queries[IMRaDType.METHODS.name] = sections_to_word_hist(paper.get_methods()).keys_to_query()
        queries[IMRaDType.RESULTS.name] = sections_to_word_hist(paper.get_results()).keys_to_query()
        queries[IMRaDType.DISCUSSION.name] = sections_to_word_hist(paper.get_discussion()).keys_to_query()

    if mode == "sections-uncategorized-sec" or mode == "sections-uncategorized-doc":
        queries["whole-document"] = sections_to_word_hist(paper.get_sections_without_an_imrad_type()).keys_to_query()

    return queries
