#!/usr/bin/env python3
# encoding: utf-8


class WordHist(dict):
    def append(self, d1):
        for key, value in d1.items():
            key = key.lower()
            self[key] = self[key] + value if key in self else value


    def get_normalized_key_value(self, key):
        ret = float(self[key]) if key in self else 0.0
        return ret / sum(self.values())


    def get_normalized_query_value(self, query, ignored_keys=None):
        if ignored_keys is None:
            ignored_keys = []

        query = query.split() if isinstance(query, str) else query
        ranking = 0.0
        key_value = []
        ignored = []

        keys = self.query_to_keys(query)
        for key in keys:
            if key in ignored_keys:
                ignored.append(key)
            else:
                rank = self.get_normalized_key_value(key)
                key_value.append([key, rank, self[key]])
                ranking += rank

        return ranking, key_value, ignored


    def query_to_keys(self, query):
        query = query.split() if isinstance(query, str) else query
        ret = []

        for word in query:
            ret += [key for key, value in self.items() if (word in key.lower()) and (key.lower() not in ret)]
        return ret

    def keys_to_query(self):
        query = ""
        for key, value in self.items():
            query += key.lower() + " "
        return query
