#!/usr/bin/env python3
# encoding: utf-8

import base64
from Crypto.Cipher import AES
from config import SHA3_KEY


class Crypto(object):
    def __init__(self):
        self.cipher = AES.new(SHA3_KEY, AES.MODE_ECB)

    def encrypt(self, decoded):
        return base64.b64encode(self.cipher.encrypt(decoded.rjust(128))).decode('ascii')

    def decrypt(self, encoded):
        encoded = encoded.encode('ascii')
        return self.cipher.decrypt(base64.b64decode(encoded)).decode('ascii').strip()
