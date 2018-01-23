#!/usr/bin/env python3
# encoding: utf-8

from pymongo import MongoClient
from bson.objectid import ObjectId
from backend.datastore.structure.paper import Paper
from backend.datastore.structure.section import IMRaDType


class DBClient(object):
    def __init__(self):
        self.client = MongoClient('localhost', 27017)  # 'mongodb://localhost:27017/'
        self.db = self.client['test-database']
        self.papers = self.db.posts
        self.users = self.db.users


    @staticmethod
    def __add_query_for_imrad_type(imrad, words, query):
        for word in words:
            query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "heading": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "text.text": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "subsections.heading": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "subsections.text.text": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "subsections.subsections.heading": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "subsections.subsections.text.text": {'$regex': word}}}})

    @staticmethod
    def __add_query_for_imrad_type_hist(imrad, words, query):
        for word in words:
            query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "word_hist": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "subsections.word_hist": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "subsections.subsections.word_hist": {'$regex': word}}}})


    @staticmethod
    def __cursor_to_list(cursor):
        papers = []
        for paper in cursor:
            papers.append(Paper(paper))
        return papers


    def add_paper(self, paper):
        post = paper.to_dict()
        post_id = self.papers.insert_one(post).inserted_id
        return post_id


    def get_paper(self, paper_id):
        cursor = self.papers.find({"_id": ObjectId(paper_id)})
        return Paper(cursor[0])


    def get_papers_with_filename(self, filename):
        cursor = self.papers.find({'filename': filename})
        return self.__cursor_to_list(cursor)


    def get_all_paper(self):
        cursor = self.papers.find({})
        return self.__cursor_to_list(cursor)


    def delete_paper(self, paper_id):
        self.papers.remove({"_id": ObjectId(paper_id)})


    def delete_all_paper(self):
        self.papers.remove({})


    def get_paper_which_contains_queries_in_hist(self, queries):
        search_query = {"$or": []}
        for imrad_type, query in queries.items():
            self.__add_query_for_imrad_type_hist(imrad_type, query.split(), search_query)

        cursor = self.papers.find(search_query)
        papers = []

        for paper in self.__cursor_to_list(cursor):
            rank = paper.get_ranking(queries)
            papers.append([paper, rank])
        return papers



    def get_paper_which_contains_queries(self, queries):
        search_query = {"$or": []}
        for imrad_type, query in queries.items():
            self.__add_query_for_imrad_type(imrad_type, query.split(), search_query)

        cursor = self.papers.find(search_query)
        papers = []

        for paper in self.__cursor_to_list(cursor):
            rank = paper.get_ranking(queries)
            papers.append([paper, rank])
        return papers


    def get_paper_which_contains_query_in_introduction(self, introduction_words):
        search_query = {"$or": []}
        self.__add_query_for_imrad_type(IMRaDType.INDRODUCTION.name, introduction_words, search_query)
        cursor = self.papers.find(search_query)
        return self.__cursor_to_list(cursor)


    def get_paper_which_contains_query_in_background(self, background_words):
        search_query = {"$or": []}
        self.__add_query_for_imrad_type(IMRaDType.BACKGROUND.name, background_words, search_query)
        cursor = self.papers.find(search_query)
        return self.__cursor_to_list(cursor)


    def get_paper_which_contains_query_in_methods(self, methods_words):
        search_query = {"$or": []}
        self.__add_query_for_imrad_type(IMRaDType.METHODS.name, methods_words, search_query)
        cursor = self.papers.find(search_query)
        return self.__cursor_to_list(cursor)


    def get_paper_which_contains_query_in_results(self, results_words):
        search_query = {"$or": []}
        self.__add_query_for_imrad_type(IMRaDType.RESULTS.name, results_words, search_query)
        cursor = self.papers.find(search_query)
        return self.__cursor_to_list(cursor)


    def get_paper_which_contains_query_in_discussion(self, discussion_words):
        search_query = {"$or": []}
        self.__add_query_for_imrad_type(IMRaDType.DISCUSSION.name, discussion_words, search_query)
        cursor = self.papers.find(search_query)
        return self.__cursor_to_list(cursor)


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
