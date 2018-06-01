#!/usr/bin/env python3
# encoding: utf-8
import contextlib
import os
import queue
import threading
from threading import Thread

from flask import current_app

import engine.datastore.datastore_utils.crypto as crypto
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, MAX_WORKERS
from engine.datastore.db_client import DBClient
from engine.datastore.ranking.ranked_boolean_retrieval import RankedBoolean
from engine.datastore.ranking.tf import TF
from engine.datastore.ranking.tfidf import TFIDF
from engine.importer.importer_teambeam import ImporterTeambeam
from engine.preprocessing.preprocessor import Preprocessor
from engine.utils.exceptions.import_exceptions import ClassificationError
from engine.utils.list_utils import insert_dict_into_sorted_list
from engine.utils.paper_utils import paper_to_queries
from engine.utils.ranking_utils import remove_ignored_words_from_query, combine_info


class API(object):
    def __init__(self, run_importer_exe=True):
        self.importer = ImporterTeambeam(run_importer_exe)
        self.client = DBClient()
        self.preprocessor = Preprocessor()

        self.ranking_algos = {
            RankedBoolean.get_name(): RankedBoolean,
            TF.get_name(): TF,
            TFIDF.get_name(): TFIDF
        }


    @staticmethod
    def allowed_upload_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    def __get_ratings(self, papers, queries_proceed, settings):
        ratings, ratings_lock, q = [], threading.Lock(), queue.Queue()
        q.queue = queue.deque(papers)

        for i in range(MAX_WORKERS):
            worker = Thread(target=self.__rate_parallel, args=(q, queries_proceed, settings, ratings, ratings_lock))
            worker.setDaemon(True)
            worker.start()

        q.join()
        return ratings


    def __rate_parallel(self, q, queries_proceed, settings, ratings, ratings_lock):
        while not q.empty():
            paper = q.get()

            element = self.get_ranking_info(paper, queries_proceed, settings)
            with ratings_lock:
                insert_dict_into_sorted_list(ratings, element, "rank")


    def __add_paper_parallel(self, q, db_lock, paper_ids, id_lock):
        while not q.empty():
            file = q.get()

            if not self.allowed_upload_file(file.filename):
                continue

            try:
                paper = self.get_imported_paper(file.filename)
                with db_lock:
                    self.client.add_paper(paper)
                self.preprocessor.link_references(paper, db_lock)
                with id_lock:
                    paper_ids.append(paper.id)
            except (IOError, OSError, ClassificationError) as e:
                print(e)


    def get_ranking_algos(self):
        algos = list(self.ranking_algos)
        algos.sort(reverse=True)
        return algos


    def get_ranking_info(self, paper, queries, settings):
        ranking_algo = self.ranking_algos[settings["algorithm"]]

        reduced_queries, ignored = remove_ignored_words_from_query(paper, queries, settings["importance_sections"])
        rank, info = ranking_algo.get_ranking(paper, reduced_queries, settings)
        return {"paper": paper, "rank": rank, "info": combine_info(info, ignored)}


    def add_papers(self, filenames):
        paper_ids, id_lock, db_lock, q = [], threading.Lock(), threading.Lock(), queue.Queue()
        q.queue = queue.deque(filenames)

        for i in range(MAX_WORKERS):
            worker = Thread(target=self.__add_paper_parallel, args=(q, db_lock, paper_ids, id_lock))
            worker.setDaemon(True)
            worker.start()

        q.join()
        return paper_ids


    def get_imported_paper(self, filename):
        if not self.allowed_upload_file(filename):
            raise IOError('Wrong extension. Only files in pdf-Format can be used.')

        paper = self.importer.import_paper(filename)
        self.preprocessor.proceed_paper(paper)
        paper.get_combined_word_hist()
        return paper


    def get_paper(self, paper_id):
        return self.client.get_paper(paper_id)


    def get_all_paper(self):
        return self.client.get_all_paper()


    def delete_paper(self, paper_id):
        self.client.delete_paper(paper_id)


    def delete_all_paper(self):
        self.client.delete_all_paper()


    def save_paper_as_pdf(self, paper_id):
        paper = self.client.get_paper(paper_id)
        return paper.save_file_to_path(UPLOAD_FOLDER)


    @staticmethod
    def delete_pdf(file_path):
        with contextlib.suppress(FileNotFoundError, PermissionError):
            os.remove(file_path)


    def get_papers(self, queries, settings):
        queries_proceed = self.preprocessor.proceed_queries(queries)

        if all(not query for query in queries_proceed.values()):
            return []

        papers = self.client.get_paper_which_contains_queries(queries_proceed)

        if settings["algorithm"] == TFIDF.get_name():
            settings["idf"] = TFIDF.get_idf(queries_proceed, papers)

        return self.__get_ratings(papers, queries_proceed, settings)


    def get_papers_with_paper(self, filename, settings):
        settings["importance_sections"] = True if settings["mode"] == "sections-uncategorized-sec" else False
        paper = self.get_imported_paper(filename)
        queries = paper_to_queries(paper, settings["mode"])
        return self.get_papers(queries, settings), queries



    # -------------------------------------------------------------------------------
    #                           User DB
    # -------------------------------------------------------------------------------
    def check_user_login(self, username, password):
        user = self.client.get_user(username)
        if not user:
            return False

        return username == user.get('username') and crypto.verify(user.get('password'), password)


    def add_user(self, username, password):
        user = {'username': username, 'password': crypto.encrypt(password)}
        return self.client.add_user(user)


    def get_all_user(self):
        return self.client.get_all_user()
