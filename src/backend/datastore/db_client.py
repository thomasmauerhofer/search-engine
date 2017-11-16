#!/usr/bin/env python3
# encoding: utf-8

from pymongo import MongoClient
from bson.objectid import ObjectId
from backend.datastore.structure.paper import Paper
from backend.datastore.structure.section import IMRaDType


def __add_search_queries_for_imrad_type__(imrad, words, query):
    for word in words:
        query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "heading": {'$regex': word}}}})
        query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "text.text": {'$regex': word}}}})
        query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "subsections.heading": {'$regex': word}}}})
        query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "subsections.text.text": {'$regex': word}}}})
        query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "subsections.subsections.heading": {'$regex': word}}}})
        query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "subsections.subsections.text.text": {'$regex': word}}}})


def __cursor_to_papers__(cursor):
    if cursor.count() == 1:
        return Paper(cursor[0])
    else:
        papers = []
        for paper in cursor:
            papers.append(Paper(paper))
        return papers


class DBClient(object):
    def __init__(self):
        self.client = MongoClient('localhost', 27017)  # 'mongodb://localhost:27017/'
        self.db = self.client['test-database']
        self.papers = self.db.posts
        self.users = self.db.users

    def add_paper(self, paper):
        post = paper.to_dict()
        post_id = self.papers.insert_one(post).inserted_id
        return post_id

    def get_paper(self, paper_id):
        cursor = self.papers.find({"_id": ObjectId(paper_id)})
        return __cursor_to_papers__(cursor)

    def get_papers_with_filename(self, filename):
        cursor = self.papers.find({'filename': filename})
        return __cursor_to_papers__(cursor)

    def get_all_paper(self):
        cursor = self.papers.find({})
        return __cursor_to_papers__(cursor)

    def delete_paper(self, paper_id):
        self.papers.remove({"_id": ObjectId(paper_id)})

    def delete_all_paper(self):
        self.papers.remove({})

    def get_paper_which_contains_queries(self, queries):
        search_query = {"$or": []}
        for imrad_type, query in queries.items():
            __add_search_queries_for_imrad_type__(imrad_type, query.split(), search_query)

        cursor = self.papers.find(search_query)
        return __cursor_to_papers__(cursor)

    def get_paper_which_contains_query_in_introduction(self, introduction_words):
        search_query = {"$or": []}
        __add_search_queries_for_imrad_type__(IMRaDType.INDRODUCTION.name, introduction_words, search_query)
        cursor = self.papers.find(search_query)
        return __cursor_to_papers__(cursor)

    def get_paper_which_contains_query_in_background(self, background_words):
        search_query = {"$or": []}
        __add_search_queries_for_imrad_type__(IMRaDType.BACKGROUND.name, background_words, search_query)
        cursor = self.papers.find(search_query)
        return __cursor_to_papers__(cursor)

    def get_paper_which_contains_query_in_methods(self, methods_words):
        search_query = {"$or": []}
        __add_search_queries_for_imrad_type__(IMRaDType.METHODS.name, methods_words, search_query)
        cursor = self.papers.find(search_query)
        return __cursor_to_papers__(cursor)

    def get_paper_which_contains_query_in_results(self, results_words):
        search_query = {"$or": []}
        __add_search_queries_for_imrad_type__(IMRaDType.RESULTS.name, results_words, search_query)
        cursor = self.papers.find(search_query)
        return __cursor_to_papers__(cursor)

    def get_paper_which_contains_query_in_discussion(self, discussion_words):
        search_query = {"$or": []}
        __add_search_queries_for_imrad_type__(IMRaDType.DISCUSSION.name, discussion_words, search_query)
        cursor = self.papers.find(search_query)
        return __cursor_to_papers__(cursor)

    def add_user(self, user):
        user_id = self.users.insert_one(user).inserted_id
        return user_id

    def get_user(self, user_name):
        cursor = self.users.find({'username': user_name})
        return cursor[0]

    def get_all_user(self):
        ret = []
        cursor = self.users.find({})
        for user in cursor:
            ret.append(user)
        return ret

    def delete_all_users(self):
        self.users.remove({})
