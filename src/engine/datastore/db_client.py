#!/usr/bin/env python3
# encoding: utf-8

from pymongo import MongoClient
from bson.objectid import ObjectId

from engine.datastore.models.paper import Paper
from engine.datastore.models.section import IMRaDType
from engine.utils.math import mean
from engine.utils.paper_utils import sections_to_word_hist


class DBClient(object):
    def __init__(self):
        self.client = MongoClient('localhost', 27017)  # 'mongodb://localhost:27017/'
        self.db = self.client['searchengine']
        self.papers = self.db.papers
        self.users = self.db.users
        self.avg_doc_length = self.db.avg_doc_length


    @staticmethod
    def __add_query_for_imrad_type(imrad, words, query):
        for word in words:
            query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "heading_proceed": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "text.text_proceed": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "subsections.heading_proceed": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "subsections.text.text_proceed": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "subsections.subsections.heading_proceed": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "subsections.subsections.text.text_proceed": {'$regex': word}}}})


    @staticmethod
    def __add_query_for_imrad_type_hist(imrad, words, query):
        for word in words:
            query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "word_hist": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "subsections.word_hist": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"imrad_types": imrad, "subsections.subsections.word_hist": {'$regex': word}}}})


    @staticmethod
    def __add_query_for_whole_doc(words, query):
        for word in words:
            query["$or"].append({"title_proceed": {'$regex': word}})
            query["$or"].append({"sections": {"$elemMatch": {"heading_proceed": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"text.text_proceed": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"subsections.heading_proceed": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"subsections.text.text_proceed": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"subsections.subsections.heading_proceed": {'$regex': word}}}})
            query["$or"].append({"sections": {"$elemMatch": {"subsections.subsections.text.text_proceed": {'$regex': word}}}})

    @staticmethod
    def __add_query_for_whole_doc_hist(words, query):
        for word in words:
            query["$or"].append({"word_hist": {'$regex': word}})


    @staticmethod
    def __cursor_to_list(cursor):
        papers = []
        for paper in cursor:
            papers.append(Paper(paper))
        return papers


    def add_paper(self, paper):
        post = paper.to_dict()
        paper.id = self.papers.insert_one(post).inserted_id


    def update_paper(self, paper):
        self.papers.update({"_id": ObjectId(paper.id)}, paper.to_dict())


    def get_paper(self, paper_id):
        cursor = self.papers.find({"_id": ObjectId(paper_id)})
        return Paper(cursor[0])


    def contains_paper(self, paper_id):
        try:
            cursor = self.papers.find({"_id": ObjectId(paper_id)})
            return cursor[0] is not None
        except IndexError:
            return False


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
            if imrad_type == "whole-document":
                self.__add_query_for_whole_doc_hist(query.split(), search_query)
            else:
                self.__add_query_for_imrad_type_hist(imrad_type, query.split(), search_query)

        cursor = self.papers.find(search_query)
        return self.__cursor_to_list(cursor)


    def get_paper_which_contains_queries(self, queries):
        search_query = {"$or": []}
        for imrad_type, query in queries.items():
            if imrad_type == "whole-document":
                self.__add_query_for_whole_doc(query.split(), search_query)
            else:
                self.__add_query_for_imrad_type(imrad_type, query.split(), search_query)

        cursor = self.papers.find(search_query)
        return self.__cursor_to_list(cursor)


    def get_paper_which_contains_query_in_introduction(self, introduction_words):
        search_query = {"$or": []}
        self.__add_query_for_imrad_type(IMRaDType.INTRODUCTION.name, introduction_words, search_query)
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
        user = list(cursor)
        if not len(user):
            return None
        return user[0]


    def get_all_user(self):
        ret = []
        cursor = self.users.find({})
        for user in cursor:
            ret.append(user)
        return ret


    def delete_all_users(self):
        self.users.remove({})


    def get_avg_doc_length(self):
        cursor = self.avg_doc_length.find({})
        avg_doc_length = list(cursor)
        if len(avg_doc_length) > 0:
            return avg_doc_length[0]
        else:
            avg_doc_length = self.__calculate_avg_doc_length()
            self.avg_doc_length.insert_one(avg_doc_length)
            return avg_doc_length


    def __calculate_avg_doc_length(self):
        papers = self.get_all_paper()
        intro, background, methods, result, discussion, overall = [], [], [], [], [], []
        for paper in papers:
            overall.append(paper.word_hist.number_of_words())
            intro.append(sections_to_word_hist(paper.get_introduction()).number_of_words())
            background.append(sections_to_word_hist(paper.get_background()).number_of_words())
            methods.append(sections_to_word_hist(paper.get_methods()).number_of_words())
            result.append(sections_to_word_hist(paper.get_results()).number_of_words())
            discussion.append(sections_to_word_hist(paper.get_discussion()).number_of_words())

        return {
            "whole-document": mean(overall, True),
            IMRaDType.INTRODUCTION.name: mean(intro, True),
            IMRaDType.BACKGROUND.name: mean(background, True),
            IMRaDType.METHODS.name: mean(methods, True),
            IMRaDType.RESULTS.name: mean(result, True),
            IMRaDType.DISCUSSION.name: mean(discussion, True)
        }
