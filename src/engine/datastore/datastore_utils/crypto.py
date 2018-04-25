#!/usr/bin/env python3
# encoding: utf-8
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError


def encrypt(plain):
    ph = PasswordHasher()
    return ph.hash(plain)


def verify(user_hash, plain):
    ph = PasswordHasher()
    try:
        return ph.verify(user_hash, plain)
    except (VerifyMismatchError, VerificationError) as e:
        return False


