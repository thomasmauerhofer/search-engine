from unittest import TestCase

import engine.datastore.datastore_utils.crypto as crypto


class TestCrypto(TestCase):
    def test_encryption(self):
        password = "testpassword"

        encrypt = crypto.encrypt(password)
        self.assertTrue(crypto.verify(encrypt, password))
        self.assertFalse(crypto.verify(encrypt, "wrong_password"))

