from unittest import TestCase

import engine.datastore.datastore_utils.crypto as crypto
from engine.api import API
from engine.datastore.db_client import DBClient
from engine.datastore.ranking.ranking_simple import RankingSimple
from engine.datastore.structure.paper import Paper
from engine.datastore.structure.section import IMRaDType


class TestDB(TestCase):
    def test_encryption(self):
        password = "testpassword"

        encrypt = crypto.encrypt(password)
        self.assertTrue(crypto.verify(encrypt, password))
        self.assertFalse(crypto.verify(encrypt, "wrong_password"))


    def test_simple_ranking(self):
        queries = {IMRaDType.INTRODUCTION.name: "aaa",
                   IMRaDType.BACKGROUND: "",
                   IMRaDType.METHODS.name: "aaa bbb ccc ddd eee fff",
                   IMRaDType.RESULTS.name: "",
                   IMRaDType.DISCUSSION.name: "",
                   "whole-document": "ggg aaa ccc"}

        settings = {"importance_sections": True}

        api = API()
        ret = api.get_papers(queries, settings, RankingSimple)

        self.assertGreater(len(ret), 0)


    def test_update_paper(self):
        db = DBClient()
        paper = Paper({"filename": "testfile.pdf", "title": "test_title"})
        paper_id = db.add_paper(paper)
        self.assertIsNotNone(paper_id)

        paper.title_raw = "new_title"
        paper.filename = "new_filename.pdf"
        db.update_paper(paper)

        updated_paper = db.get_paper(paper_id)
        self.assertEquals(updated_paper.filename, "new_filename.pdf")
        self.assertEquals(updated_paper.title, "new_title")
        db.delete_paper(paper_id)
