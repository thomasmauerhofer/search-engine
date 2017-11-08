#!/usr/bin/env python3
# encoding: utf-8

from backend.utils.exceptions.exception import Error


class WrongReferenceError(Error):
    """Raised when reference don't contain text"""

    def __init__(self, message, value, data):
        self.message = message
        self.value = value
        self.data = data


class WrongAuthorError(Error):
    """Raised when attribute is added to wrong author"""

    def __init__(self, message):
        self.message = message


class ClassificationException(Error):
    """Raised when one of the additional classification rules are not observed"""

    def __init__(self, message):
        self.message = message
