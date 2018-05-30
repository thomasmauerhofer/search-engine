#!/usr/bin/env python3
# encoding: utf-8


class WordHist(dict):
    def append(self, d1):
        for key, value in d1.items():
            key = key.lower()
            self[key] = self[key] + value if key in self else value


    def get_tf(self, key):
        ret = float(self[key]) if key in self else 0.0
        return ret / sum(self.values())


    def get_tf_of_keys(self, keys):
        ranking = 0.0
        key_value = []

        for key in keys:
            rank = self.get_tf(key)
            key_value.append([key, rank, self[key]])
            ranking += rank

        return ranking, key_value


    def query_to_keys(self, query):
        return set([key for key in self.keys() for word in query.split() if word in key])


    def keys_to_query(self):
        query = ""
        for key, value in self.items():
            query += key.lower() + " "
        return query
