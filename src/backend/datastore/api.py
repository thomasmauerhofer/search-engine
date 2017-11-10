#!/usr/bin/env python3
# encoding: utf-8

from backend.datastore.datastore_utils.crypto import Crypto
from backend.datastore.db_client import DBClient
from backend.importer.importer_teambeam import ImporterTeambeam
from backend.preprocessing.preprocessor import Preprocessor
from config import ALLOWED_EXTENSIONS, path_to_datastore


class API(object):
    def __init__(self):
        self.importer = ImporterTeambeam()
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
        valid_paper = self.preprocessor.proceed_paper(paper)

        if not valid_paper:
            return None

        existing_papers = self.client.get_all_paper()
        paper_str = str(paper)
        for existing_paper in existing_papers:
            if str(existing_paper) == paper_str:
                return None

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

    def get_ranked_papers_explicit(self, indro_query, background_query, methods_query, results_query, discussion_query):
        papers = self.client.get_paper_which_contains_queries(indro_query.split(), background_query.split(),
                                                              methods_query.split(), results_query.split(), discussion_query.split())

        for paper in papers:
            print(paper.filename)

    # -------------------------------------------------------------------------------
    #                           User DB
    # -------------------------------------------------------------------------------
    def check_user_login(self, username, password):
        user = self.client.get_user(username)
        if not user:
            return False

        return username == user.get('username') and \
               self.crypto.encrypt(password) == user.get('password')

    def add_user(self, username, password):
        user = {'username': username, 'password': self.crypto.encrypt(password)}
        return self.client.add_user(user)

    def get_all_user(self):
        return self.client.get_all_user()
