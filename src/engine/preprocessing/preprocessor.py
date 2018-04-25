#!/usr/bin/env python3
# encoding: utf-8
from engine.preprocessing.imrad_detection import IMRaDDetection
from engine.preprocessing.text_processor import TextProcessor


class Preprocessor(object):
    def __init__(self):
        self.imrad_detector = IMRaDDetection()
        self.text_processor = TextProcessor()


    def proceed_paper(self, paper):
        self.text_processor.proceed(paper)
        self.imrad_detector.proceed(paper)


    def proceed_queries(self, queries):
        queries_proceed = {}
        for imrad_type, query in queries.items():
            queries_proceed[imrad_type] = self.text_processor.proceed_string(query)
        return queries_proceed
