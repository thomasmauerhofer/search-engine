#!/usr/bin/env python3
# encoding: utf-8

import os
import pickle
import shutil
from getpass import getpass
from optparse import OptionParser

from pymongo.errors import DocumentTooLarge

from config import UPLOAD_FOLDER, REQ_DATA_PATH
from engine.api import API
from engine.utils.exceptions.import_exceptions import ClassificationError, PaperInStorage
from setup.utils.datastore_utils import link_references_to_paper


def __add_files(folder):
    api = API()
    text_file = open("newpapers.txt", "a+")

    for filename in os.listdir(os.path.abspath(folder)):
        print('CURRENT FILE: ' + str(filename))

        if filename.endswith('.pdf'):
            src = folder + "/" + filename
            dst = UPLOAD_FOLDER + filename
            shutil.move(src, dst)
            try:
                paper = api.add_paper(filename)
                text_file.write(str(paper.id) + "\n")
            except (IOError, OSError, ClassificationError, DocumentTooLarge, PaperInStorage) as e:
                print(e)
    text_file.close()


def __import_json(filepath):
    # Dosen't work with v2.4, v2.6 (max size 18mb)
    # works with v4.0.1
    os.popen("mongoimport --db searchengine --collection papers --file ", filepath)


def __export_json(name):
    if not name:
        print("Error: Enter a valid name")
        exit(-1)

    if not name.endswith(".json"):
        name += ".json"
    os.popen("mongoexport --db searchengine --collection papers --out ", name)


def __add_user():
    print("Add new admin to the database")
    name = input("username: ")
    password = getpass()
    api = API()
    api.add_user(name, password)
    print("Welcome on board {}".format(name))


def __link_references_to_paper():
    api = API()
    all_papers = api.get_all_paper()

    finished_files = []
    if not os.path.isfile(REQ_DATA_PATH + "finished_papers.txt"):
        with open(REQ_DATA_PATH + "finished_papers.txt", 'wb') as fp:
            pickle.dump(finished_files, fp)

    with open(REQ_DATA_PATH + "finished_papers.txt", 'rb') as fp:
        finished_files = pickle.load(fp)

    if os.path.isfile("newpapers.txt"):
        papers = []
        with open("newpapers.txt", 'r') as fp:
            for paper_id in fp:
                papers.append(api.get_paper(paper_id.rstrip()))
    else:
        papers = api.get_all_paper()


    i = 0
    for paper in papers:
        i += 1
        print("(", i, "/", len(papers), ")")

        if paper.id in finished_files:
            continue

        other_papers = [p for p in all_papers if p.id != paper.id]
        for other_paper in other_papers:
            if os.path.isfile("newpapers.txt"):
                link_references_to_paper(other_paper, paper, api)

            link_references_to_paper(paper, other_paper, api)

        finished_files.append(paper.id)
        with open(REQ_DATA_PATH + "finished_papers.txt", 'wb') as fp:
            pickle.dump(finished_files, fp)



if __name__ == "__main__":
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    parser = OptionParser()
    parser.add_option("-f", "--folder", dest="folder",
                      help="import all data from folder to database", metavar="FOLDER")
    parser.add_option("-i", "--imp", dest="imp",
                      help="import data from json into database", metavar="FOLDER")
    parser.add_option("-e", "--exp", dest="exp",
                      help="export data from database in json format", metavar="FOLDER")
    parser.add_option("-u", "--user", action="store_true", dest="user", default=False,
                      help="Add a new Adminuser to the database")
    parser.add_option("-r", "--link_references", action="store_true", dest="link_ref", default=False,
                      help="Link references manually")
    (options, args) = parser.parse_args()

    if options.folder:
        __add_files(options.folder)
    elif options.imp:
        __import_json(options.folder)
    elif options.exp:
        __export_json(options.folder)
    elif options.user:
        __add_user()
    elif options.link_ref:
        __link_references_to_paper()
    else:
        print("Usage: No Parameter! Use -f FOLDERPATH to upload all files of a folder, or -h for help")
