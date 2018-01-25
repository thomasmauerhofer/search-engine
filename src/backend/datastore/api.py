#!/usr/bin/env python3
# encoding: utf-8
import contextlib

import os

from backend.datastore.datastore_utils.crypto import Crypto
from backend.datastore.db_client import DBClient
from backend.importer.importer_teambeam import ImporterTeambeam
from backend.preprocessing.preprocessor import Preprocessor
from backend.utils.list_utils import insert_dict_into_sorted_list
from config import ALLOWED_EXTENSIONS, path_to_datastore


class API(object):
    def __init__(self, run_importer_exe=True):
        self.importer = ImporterTeambeam(run_importer_exe)
        self.client = DBClient()
        self.preprocessor = Preprocessor()
        self.crypto = Crypto()


    @staticmethod
    def allowed_upload_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    def add_paper(self, filename):
        if not self.allowed_upload_file(filename):
            return None

        paper = self.importer.import_paper(filename)
        if not paper:
            return None
        valid_paper = self.preprocessor.proceed_paper(paper)
        if not valid_paper:
            return None

        paper.get_combined_word_hist()
        return self.client.add_paper(paper)


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
        return paper.save_file_to_path(path_to_datastore)


    @staticmethod
    def delete_pdf(file_path):
        with contextlib.suppress(FileNotFoundError, PermissionError):
            os.remove(file_path)


    def get_ranked_papers_explicit(self, queries, remove_double_terms_in_section_query=True):
        ret = []

        queries_proceed = self.preprocessor.proceed_queries(queries)

        if all(not query for query in queries_proceed.values()):
            return ret

        papers = self.client.get_paper_which_contains_queries(queries_proceed, remove_double_terms_in_section_query)
        for paper_and_rank in papers:
            paper = paper_and_rank[0]
            raking = paper_and_rank[1]

            element = {"paper": paper, "ranking": raking}
            insert_dict_into_sorted_list(ret, element, "ranking")
        return ret


    # -------------------------------------------------------------------------------
    #                           User DB
    # -------------------------------------------------------------------------------
    def check_user_login(self, username, password):
        user = self.client.get_user(username)
        if not user:
            return False

        return username == user.get('username') and self.crypto.encrypt(password) == user.get('password')


    def add_user(self, username, password):
        user = {'username': username, 'password': self.crypto.encrypt(password)}
        return self.client.add_user(user)


    def get_all_user(self):
        return self.client.get_all_user()
