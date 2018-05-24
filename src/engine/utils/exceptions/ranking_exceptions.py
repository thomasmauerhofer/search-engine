#!/usr/bin/env python3
# encoding: utf-8


class RankingParameterError(BaseException):
    """Raised when Params of the ranking Algorithm are set wrong"""

    def __init__(self, message):
        self.message = message
