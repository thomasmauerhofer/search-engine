from unittest import TestCase

import engine.datastore.datastore_utils.crypto as crypto
from engine.api import API
from engine.datastore.db_client import DBClient
from engine.datastore.ranking.ranking_simple import RankingSimple
from engine.datastore.structure.paper import Paper
from engine.datastore.structure.section import IMRaDType
from engine.datastore.structure.text import TextType


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

        settings = {**{"importance_sections": False}, **RankingSimple.get_default_config()}

        api = API()
        ret = api.get_papers(queries, settings)

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


    def test_paper(self):
        paper = Paper({"filename": "testfile.pdf"})
        self.assertFalse(paper.title_exist())
        self.assertFalse(paper.section_title_exist())
        self.assertFalse(paper.section_text_exist())
        self.assertFalse(paper.subsection_title_exist())
        self.assertFalse(paper.subsection_text_exist())
        self.assertFalse(paper.subsubsection_title_exist())
        self.assertFalse(paper.subsubsection_text_exist())

        paper.set_title("test")
        self.assertTrue(paper.title_exist())
        self.assertFalse(paper.section_title_exist())
        self.assertFalse(paper.section_text_exist())
        self.assertFalse(paper.subsection_title_exist())
        self.assertFalse(paper.subsection_text_exist())
        self.assertFalse(paper.subsubsection_title_exist())
        self.assertFalse(paper.subsubsection_text_exist())

        paper.add_section("test")
        self.assertTrue(paper.title_exist())
        self.assertTrue(paper.section_title_exist())
        self.assertFalse(paper.section_text_exist())
        self.assertFalse(paper.subsection_title_exist())
        self.assertFalse(paper.subsection_text_exist())
        self.assertFalse(paper.subsubsection_title_exist())
        self.assertFalse(paper.subsubsection_text_exist())

        paper.add_text_to_current_section(TextType.MAIN, "test test")
        self.assertTrue(paper.title_exist())
        self.assertTrue(paper.section_title_exist())
        self.assertTrue(paper.section_text_exist())
        self.assertFalse(paper.subsection_title_exist())
        self.assertFalse(paper.subsection_text_exist())
        self.assertFalse(paper.subsubsection_title_exist())
        self.assertFalse(paper.subsubsection_text_exist())

        paper.add_subsection("test")
        self.assertTrue(paper.title_exist())
        self.assertTrue(paper.section_title_exist())
        self.assertTrue(paper.section_text_exist())
        self.assertTrue(paper.subsection_title_exist())
        self.assertFalse(paper.subsection_text_exist())
        self.assertFalse(paper.subsubsection_title_exist())
        self.assertFalse(paper.subsubsection_text_exist())

        paper.add_text_to_current_section(TextType.MAIN, "test")
        self.assertTrue(paper.title_exist())
        self.assertTrue(paper.section_title_exist())
        self.assertTrue(paper.section_text_exist())
        self.assertTrue(paper.subsection_title_exist())
        self.assertTrue(paper.subsection_text_exist())
        self.assertFalse(paper.subsubsection_title_exist())
        self.assertFalse(paper.subsubsection_text_exist())

        paper.add_subsubsection("test")
        self.assertTrue(paper.title_exist())
        self.assertTrue(paper.section_title_exist())
        self.assertTrue(paper.section_text_exist())
        self.assertTrue(paper.subsection_title_exist())
        self.assertTrue(paper.subsection_text_exist())
        self.assertTrue(paper.subsubsection_title_exist())
        self.assertFalse(paper.subsubsection_text_exist())

        paper.add_text_to_current_section(TextType.MAIN, "test")
        self.assertTrue(paper.title_exist())
        self.assertTrue(paper.section_title_exist())
        self.assertTrue(paper.section_text_exist())
        self.assertTrue(paper.subsection_title_exist())
        self.assertTrue(paper.subsection_text_exist())
        self.assertTrue(paper.subsubsection_title_exist())
        self.assertTrue(paper.subsubsection_text_exist())
