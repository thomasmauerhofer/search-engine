#!/usr/bin/env python3
# encoding: utf-8


class WordHist(dict):

    def append(self, d1):
        for key, value in d1.items():
            if key in self:
                self[key] += value
            else:
                self[key] = value
