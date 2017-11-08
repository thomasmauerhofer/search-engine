#!/usr/bin/env python3
# encoding: utf-8

from sklearn.feature_extraction.text import CountVectorizer
from config import path_to_hdf5


class BagOfWords(object):
    def __init__(self):
        with open(path_to_hdf5 + 'bag_of_words.txt', 'r') as f:
            lines = [line.strip() for line in f.readlines()]

        self.vectorizer = CountVectorizer(vocabulary=lines)

    def text_to_vector(self, text):
        return self.vectorizer.fit_transform([text]).toarray()[0]

    def get_vocabulary(self):
        return self.vectorizer.vocabulary
