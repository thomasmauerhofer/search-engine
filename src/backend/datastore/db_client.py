#!/usr/bin/env python3
# encoding: utf-8

import json
from pymongo import MongoClient


class DBClient(object):
    def __init__(self):
        self.client = MongoClient('localhost', 27017) #'mongodb://localhost:27017/'
        self.db = self.client['test-database']
        self.collection = self.db.posts #posts is a temporary collection

    def add_paper(self, paper):
        x = paper.to_dict()
        print(x)
        #x = pickle.loads("(dp1\nS'text'\np2\nS'string'\np3\nsS'none'\np4\nNsS'boolean'\np5\nI01\nsS'number'\np6\nF3.4399999999999999\nsS'int_list'\np7\n(lp8\nI1\naI2\naI3\nas.")
        #post = paper.to_json()
        #post_id = self.collection.insert_one(post).inserted_id
        #print(post_id)

    def get_paper(self):
        cursor = self.collection.find({'filename': 'ijdl-2013.pdf'})
        for document in cursor:
            print(document)

    def get_all_paper(self):
        cursor = self.collection.find({})
        for document in cursor:
            print(document)

    def delete_paper(self):
        self.collection.remove({'filename': 'ijdl-2013.pdf'})

        cursor = self.collection.find({})
        for document in cursor:
            print(document)
        print("AAAAAAA")
