from unittest import TestCase

from engine.api import API
from engine.datastore.models.section import IMRaDType
from engine.datastore.ranking.mode import Mode, Area
from engine.utils.paper_utils import paper_to_queries


class TestUtils(TestCase):
    def test_importance_to_sections(self):
        api = API()
        papers = api.get_all_paper()
        settings = {"mode": Mode.importance_to_sections}

        queries = paper_to_queries(papers[0], settings)
        self.assertEqual(len(queries["whole-document"]), 0)
        self.assertGreater(len(queries[IMRaDType.INTRODUCTION.name]), 0)
        self.assertGreater(len(queries[IMRaDType.BACKGROUND.name]), 0)
        self.assertGreater(len(queries[IMRaDType.METHODS.name]), 0)
        self.assertGreater(len(queries[IMRaDType.RESULTS.name]), 0)
        self.assertGreater(len(queries[IMRaDType.DISCUSSION.name]), 0)


    def test_import_intro_search_intro(self):
        api = API()
        papers = api.get_all_paper()
        settings = {
            "mode": Mode.areas,
            "input-area": Area.Introduction,
            "search-area": Area.Introduction
        }

        queries = paper_to_queries(papers[0], settings)
        self.assertEqual(len(queries["whole-document"]), 0)
        self.assertGreater(len(queries[IMRaDType.INTRODUCTION.name]), 0)
        self.assertEqual(len(queries[IMRaDType.BACKGROUND.name]), 0)
        self.assertEqual(len(queries[IMRaDType.METHODS.name]), 0)
        self.assertEqual(len(queries[IMRaDType.RESULTS.name]), 0)
        self.assertEqual(len(queries[IMRaDType.DISCUSSION.name]), 0)

    def test_import_intro_search_back(self):
        api = API()
        papers = api.get_all_paper()
        settings = {
            "mode": Mode.areas,
            "input-area": Area.Introduction,
            "search-area": Area.Background
        }

        queries = paper_to_queries(papers[0], settings)
        self.assertEqual(len(queries["whole-document"]), 0)
        self.assertEqual(len(queries[IMRaDType.INTRODUCTION.name]), 0)
        self.assertGreater(len(queries[IMRaDType.BACKGROUND.name]), 0)
        self.assertEqual(len(queries[IMRaDType.METHODS.name]), 0)
        self.assertEqual(len(queries[IMRaDType.RESULTS.name]), 0)
        self.assertEqual(len(queries[IMRaDType.DISCUSSION.name]), 0)
