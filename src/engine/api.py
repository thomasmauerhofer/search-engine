#!/usr/bin/env python3
# encoding: utf-8
import contextlib
import os
import engine.datastore.datastore_utils.crypto as crypto

from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from engine.datastore.db_client import DBClient
from engine.datastore.ranking.ranking_simple import RankingSimple
from engine.importer.importer_teambeam import ImporterTeambeam
from engine.preprocessing.preprocessor import Preprocessor
from engine.utils.list_utils import insert_dict_into_sorted_list
from engine.utils.paper_utils import paper_to_queries


class API(object):
    def __init__(self, run_importer_exe=True):
        self.importer = ImporterTeambeam(run_importer_exe)
        self.client = DBClient()
        self.preprocessor = Preprocessor()


    @staticmethod
    def allowed_upload_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    def add_paper(self, filename):
        paper = self.get_imported_paper(filename)
        self.client.add_paper(paper)
        self.preprocessor.link_references(paper)
        return paper.id


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


    def get_papers_simple_ranking(self, queries, settings):
        ret = []
        queries_proceed = self.preprocessor.proceed_queries(queries)

        if all(not query for query in queries_proceed.values()):
            return ret

        papers = self.client.get_paper_which_contains_queries(queries_proceed)
        for paper in papers:
            rank, info = RankingSimple.get_ranking(paper, queries_proceed, settings)
            element = {"paper": paper, "rank": rank, "info": info}
            insert_dict_into_sorted_list(ret, element, "rank")

        return ret


    def get_papers_simple_ranking_with_paper(self, filename, settings):
        ret = []
        settings["importance_sections"] = True if settings["mode"] == "sections-uncategorized-sec" else False


        paper = self.get_imported_paper(filename)
        queries_proceed = paper_to_queries(paper, settings["mode"])

        papers = self.client.get_paper_which_contains_queries(queries_proceed)
        for paper in papers:
            if paper.filename == filename:
                continue

            rank, info = RankingSimple.get_ranking(paper, queries_proceed, settings)
            element = {"paper": paper, "rank": rank, "info": info}
            insert_dict_into_sorted_list(ret, element, "rank")

        return ret, queries_proceed



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
