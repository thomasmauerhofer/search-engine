#!/usr/bin/env python3
# encoding: utf-8
from engine.datastore.models.section import IMRaDType
from engine.datastore.ranking.mode import Mode, Area
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
        return queries


    if settings["mode"] == Mode.importance_to_sections:
        use_unclassified_chapters = settings["use-unclassified-chapters"] if "use-unclassified-chapters" in settings else False
        if use_unclassified_chapters:
            queries["whole-document"] = paper.title_proceed
            queries["whole-document"] += sections_to_word_hist(paper.get_sections_without_an_imrad_type()).keys_to_query()

        queries[IMRaDType.INTRODUCTION.name] = sections_to_word_hist(paper.get_introduction()).keys_to_query()
        queries[IMRaDType.BACKGROUND.name] = sections_to_word_hist(paper.get_background()).keys_to_query()
        queries[IMRaDType.METHODS.name] = sections_to_word_hist(paper.get_methods()).keys_to_query()
        queries[IMRaDType.RESULTS.name] = sections_to_word_hist(paper.get_results()).keys_to_query()
        queries[IMRaDType.DISCUSSION.name] = sections_to_word_hist(paper.get_discussion()).keys_to_query()
        return queries

    if settings["mode"] == Mode.areas:
        input_area = settings["input-area"]
        search_area = settings["search-area"]
        input_imrad_area = __area_to_imrad(input_area)
        search_imrad_area = __area_to_imrad(search_area)

        queries[search_imrad_area.name] = sections_to_word_hist(paper.get_sections_with_imrad_type(input_imrad_area)).keys_to_query()
        return queries


def __area_to_imrad(area):
    if area == Area.Introduction:
        return IMRaDType.INTRODUCTION
    elif area == Area.Background:
        return IMRaDType.BACKGROUND
    elif area == Area.Method:
        return IMRaDType.METHODS
    elif area == Area.Result:
        return IMRaDType.RESULTS
    elif area == Area.Discussion:
        return IMRaDType.DISCUSSION
