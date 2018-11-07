#!/usr/bin/env python3
# encoding: utf-8
from engine.datastore.models.section import IMRaDType
from engine.datastore.ranking.mode import Mode
from engine.utils.objects.word_hist import WordHist


def sections_to_word_hist(sections):
    hist = WordHist()
    for section in sections:
        hist.append(section.get_combined_word_hist())
    return hist


def paper_to_queries(paper, settings):
    queries = {
        "whole-document": "",
        IMRaDType.INTRODUCTION.name: "",
        IMRaDType.BACKGROUND.name: "",
        IMRaDType.METHODS.name: "",
        IMRaDType.RESULTS.name: "",
        IMRaDType.DISCUSSION.name: ""
    }

    if settings["mode"] == Mode.without_importance_to_sections:
        queries["whole-document"] = paper.get_combined_word_hist().keys_to_query()

    if settings["mode"] == Mode.importance_to_sections:
        queries["whole-document"] = paper.title_proceed
        if settings["use-unclassified-chapters"]:
            queries["whole-document"] += sections_to_word_hist(paper.get_sections_without_an_imrad_type()).keys_to_query()

    if settings["mode"] == Mode.only_introduction or settings["mode"] == Mode.importance_to_sections:
        queries[IMRaDType.INTRODUCTION.name] = sections_to_word_hist(paper.get_introduction()).keys_to_query()

    if settings["mode"] == Mode.only_background or settings["mode"] == Mode.importance_to_sections:
        queries[IMRaDType.BACKGROUND.name] = sections_to_word_hist(paper.get_background()).keys_to_query()

    if settings["mode"] == Mode.only_methods or settings["mode"] == Mode.importance_to_sections:
        queries[IMRaDType.METHODS.name] = sections_to_word_hist(paper.get_methods()).keys_to_query()

    if settings["mode"] == Mode.only_results or settings["mode"] == Mode.importance_to_sections:
        queries[IMRaDType.RESULTS.name] = sections_to_word_hist(paper.get_results()).keys_to_query()

    if settings["mode"] == Mode.only_discussion or settings["mode"] == Mode.importance_to_sections:
        queries[IMRaDType.DISCUSSION.name] = sections_to_word_hist(paper.get_discussion()).keys_to_query()

    return queries
