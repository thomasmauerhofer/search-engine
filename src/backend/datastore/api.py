#!/usr/bin/env python3
# encoding: utf-8

from backend.importer.importer_teambeam import ImporterTeambeam
from backend.preprocessing.preprocessor import Preprocessor
from backend.datastore.db_client import DBClient
from config import ALLOWED_EXTENSIONS

class API(object):
    def __init__(self):
        self.importer = ImporterTeambeam()
        self.client = DBClient()
        self.preprocessor = Preprocessor()


    def allowed_upload_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    def add_paper(self, filename):
        if not self.allowed_upload_file(filename):
            return None

        paper = self.importer.import_paper(filename)
        valid_paper = self.preprocessor.proceed_paper(paper)

        if not valid_paper:
            return None

        return self.client.add_paper(paper)


    def get_paper(self, paper_id):
        return self.client.add_paper(paper_id)


    def get_all_paper(self):
        return self.client.get_all_paper()


    def delete_paper(self, paper_id):
        self.client.delete_paper(paper_id)
