#!/usr/bin/env python3
# encoding: utf-8


class WordHist(dict):
    def append(self, d1):
        for key, value in d1.items():
            key = key.lower()
            self[key] = self[key] + value if key in self else value


    def get_tf(self, querie_word):
        word_count = 0.0

        for key, value in self.items():
            if querie_word in key:
                word_count += value

        return word_count / self.number_of_words() if self.values() else 0


    def number_of_words(self):
        return sum(self.values())


    '''
    @return: All keys where a query term is part of: e.g: abc -> {abcd, abce}
    '''
    def query_to_keys(self, query):
        return set([key for key in self.keys() for word in query.split() if word in key])


    def keys_to_query(self):
        query = ""
        for key, value in self.items():
            query += key.lower() + " "
        return query
