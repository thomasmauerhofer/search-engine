#!/usr/bin/env python3
# encoding: utf-8

from pymongo import MongoClient
from bson.objectid import ObjectId
from backend.datastore.structure.paper import Paper


class DBClient(object):
    def __init__(self):
        self.client = MongoClient('localhost', 27017) #'mongodb://localhost:27017/'
        self.db = self.client['test-database']
        self.collection = self.db.posts #posts is a temporary collection


    def add_paper(self, paper):
        post = paper.to_dict()
        post_id = self.collection.insert_one(post).inserted_id
        return post_id


    def get_paper(self, paper_id):
        #cursor = self.collection.find({'filename': 'ijdl-2013.pdf'})
        cursor = self.collection.find({ "_id": ObjectId(paper_id) })
        for paper in cursor:
            return Paper(paper)


    def get_all_paper(self):
        papers = []
        cursor = self.collection.find({})
        for paper in cursor:
            papers.append(Paper(paper))
        return papers


    def delete_paper(self, paper_id):
        self.collection.remove({ "_id": ObjectId(paper_id) })


    def delete_all_paper(self):
        self.collection.remove({ })
