#!/usr/bin/env python3
# encoding: utf-8
import contextlib
import os

from pymongo.errors import DocumentTooLarge

import engine.datastore.datastore_utils.crypto as crypto
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from engine.datastore.db_client import DBClient
from engine.datastore.ranking.mode import Mode
from engine.datastore.ranking.ranked_boolean_retrieval import RankedBoolean
from engine.datastore.ranking.tf import TF
from engine.datastore.ranking.tfidf import TFIDF
from engine.importer.importer_teambeam import ImporterTeambeam
from engine.preprocessing.preprocessor import Preprocessor
from engine.utils.exceptions.import_exceptions import ClassificationError, PaperInStorage
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
        ratings = []
        for paper in papers:
            element = self.get_ranking_info(paper, queries_proceed, settings)
            insert_dict_into_sorted_list(ratings, element, "rank")
        return ratings


    def get_ranking_algos(self):
        algos = list(self.ranking_algos)
        algos.sort(reverse=True)
        return algos


    def get_ranking_info(self, paper, queries, settings):
        ranking_algo = self.ranking_algos[settings["algorithm"]]

        importance_to_section = settings["mode"] == Mode.importance_to_sections or settings["mode"] == Mode.only_introduction or \
                                settings["mode"] == Mode.only_background or settings["mode"] == Mode.only_methods or \
                                settings["mode"] == Mode.only_results or settings["mode"] == Mode.only_discussion

        reduced_queries, ignored = remove_ignored_words_from_query(paper, queries, importance_to_section)
        rank, info = ranking_algo.get_ranking(paper, reduced_queries, settings)
        return {"paper": paper, "rank": rank, "info": combine_info(info, ignored)}


    def add_papers(self, filenames):
        paper_ids = []
        for filename in filenames:
            try:
                paper_ids.append(self.add_paper(filename).id)
            except (ClassificationError, DocumentTooLarge, PaperInStorage):
                pass
        return paper_ids


    def add_paper(self, filename):
        paper = self.get_imported_paper(filename)

        if [x for x in self.get_all_paper() if paper == x]:
            raise PaperInStorage('Paper already exists in storage')

        self.client.add_paper(paper)
        # self.preprocessor.link_references(paper)
        return paper


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
            settings["df"] = TFIDF.get_df(queries_proceed, papers)
            settings["number_paper"] = len(papers)

        return self.__get_ratings(papers, queries_proceed, settings)


    def get_papers_with_paper(self, filename, settings):
        papers = self.client.get_papers_with_filename(filename)
        paper = papers[0] if papers else self.get_imported_paper(filename)
        queries = paper_to_queries(paper, settings)
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
