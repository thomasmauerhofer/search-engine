#!/usr/bin/env python3
# encoding: utf-8


class WordHist(dict):

    def append(self, d1):
        for key, value in d1.items():
            self[key] = self[key] + value if key in self else value


    def get_normalized_key_value(self, key):
        ret = float(self[key]) if key in self else 0.0
        return ret / sum(self.values())


    def get_normalized_query_value(self, query):
        query = [query] if isinstance(query, str) else query
        ret = 0.0
        for word in query:
            ret += self.get_normalized_key_value(word)
        return ret
