#!/usr/bin/env python3
# encoding: utf-8

from pymongo import MongoClient
from bson.objectid import ObjectId
from backend.datastore.structure.paper import Paper


class DBClient(object):
    def __init__(self):
        self.client = MongoClient('localhost', 27017) #'mongodb://localhost:27017/'
        self.db = self.client['test-database']
        self.papers = self.db.posts
        self.users = self.db.users


    def add_paper(self, paper):
        post = paper.to_dict()
        post_id = self.papers.insert_one(post).inserted_id
        return post_id


    def get_paper(self, paper_id):
        #cursor = self.collection.find({'filename': 'ijdl-2013.pdf'})
        cursor = self.papers.find({ "_id": ObjectId(paper_id) })
        for paper in cursor:
            return Paper(paper)


    def get_all_paper(self):
        papers = []
        cursor = self.papers.find({})
        for paper in cursor:
            papers.append(Paper(paper))
        return papers


    def delete_paper(self, paper_id):
        self.papers.remove({ "_id": ObjectId(paper_id) })


    def delete_all_paper(self):
        self.papers.remove({ })


    def add_user(self, user):
        user_id = self.users.insert_one(user).inserted_id
        return user_id


    def get_user(self, user_name):
        cursor = self.users.find({'username': user_name})
        for user in cursor:
            return user


    def get_all_user(self):
        ret = []
        cursor = self.users.find({})
        for user in cursor:
            ret.append(user)
        return ret


    def delete_all_users(self):
        self.users.remove({ })
