#!/usr/bin/env python3
# encoding: utf-8


class WordHist(dict):

    def append(self, d1):
        for key, value in d1.items():
            self[key] = self[key] + value if key in self else value
