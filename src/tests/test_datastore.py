from unittest import TestCase

import engine.datastore.datastore_utils.crypto as crypto
from engine.api import API
from engine.datastore.structure.section import IMRaDType


class TestCrypto(TestCase):
    def test_encryption(self):
        password = "testpassword"

        encrypt = crypto.encrypt(password)
        self.assertTrue(crypto.verify(encrypt, password))
        self.assertFalse(crypto.verify(encrypt, "wrong_password"))

    def test_simple_ranking(self):
        queries = {IMRaDType.INDRODUCTION.name: "paper",
                   IMRaDType.BACKGROUND: "",
                   IMRaDType.METHODS.name: "inhom scenario allow user control home",
                   IMRaDType.RESULTS.name: "",
                   IMRaDType.DISCUSSION.name: ""}

        settings = {"importance_sections": True}

        api = API()
        ret = api.get_papers_simple_ranking(queries, settings)
        self.assertGreater(len(ret), 0)
