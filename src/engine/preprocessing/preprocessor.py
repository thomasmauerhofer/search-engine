#!/usr/bin/env python3
# encoding: utf-8
from difflib import SequenceMatcher

from config import REFERENCE_SIMULARITY_THRESHOLD
from engine.datastore.db_client import DBClient
from engine.preprocessing.imrad_detection import IMRaDDetection
from engine.preprocessing.text_processor import TextProcessor


class Preprocessor(object):
    def __init__(self):
        self.imrad_detector = IMRaDDetection()
        self.text_processor = TextProcessor()
        self.client = DBClient()


    def __add_paper_to_reference(self, paper1, paper2):
        if not paper2.title:
            return

        for ref in paper1.references:
            similarity = SequenceMatcher(None, ref.complete_reference.lower(), paper2.title.lower()).ratio()
            if similarity > REFERENCE_SIMULARITY_THRESHOLD:
                ref.paper_id = paper2.id
                self.client.update_paper(paper1)


    def proceed_paper(self, paper):
        self.text_processor.proceed(paper)
        self.imrad_detector.proceed(paper)


    def proceed_queries(self, queries):
        queries_proceed = {}
        for imrad_type, query in queries.items():
            queries_proceed[imrad_type] = self.text_processor.proceed_string(query)
        return queries_proceed


    def link_references(self, new_paper):
        for paper in self.client.get_all_paper():
            self.__add_paper_to_reference(paper, new_paper)
            self.__add_paper_to_reference(new_paper, paper)
