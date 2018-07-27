#!/usr/bin/env python3
# encoding: utf-8

import os
import pickle
import shutil
from difflib import SequenceMatcher
from getpass import getpass
from optparse import OptionParser

from config import UPLOAD_FOLDER, REQ_DATA_PATH
from engine.api import API
from engine.utils.exceptions.import_exceptions import ClassificationError


def __add_files(folder):
    api = API()

    for filename in os.listdir(os.path.abspath(folder)):
        print('CURRENT FILE: ' + str(filename))

        if filename.endswith('.pdf'):
            src = folder + "/" + filename
            dst = UPLOAD_FOLDER + filename
            shutil.move(src, dst)
            try:
                api.add_paper(filename)
            except (IOError, OSError, ClassificationError) as e:
                print(e)


def __import_json(filepath):
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

    finished_files = []
    if not os.path.isfile(REQ_DATA_PATH + "finished_papers.txt"):
        with open(REQ_DATA_PATH + "finished_papers.txt", 'wb') as fp:
            pickle.dump(finished_files, fp)

    with open(REQ_DATA_PATH + "finished_papers.txt", 'rb') as fp:
        finished_files = pickle.load(fp)

    papers = api.get_all_paper()
    yes_choices, nope_choices = {}, {}
    i = 0
    for paper in papers:
        i += 1
        print("(", i, "/", len(papers), ")")

        if paper.id in finished_files:
            continue

        other_papers = [p for p in papers if p.filename != paper.filename]
        for other_paper in other_papers:
            if not other_paper.title_raw:
                continue

            for ref in paper.references:
                # Don't reannotate references
                if ref.paper_id and isinstance(ref.paper_id, list) and ref.paper_id[1] == "manual":
                    paper = api.get_paper(ref.paper_id[0])
                    yes_choices[ref.complete_ref_raw.lower()] = [paper.title_raw.lower(), paper.id]
                    continue

                # if already annotated set the same paper again
                if ref.complete_ref_raw.lower() in yes_choices and \
                        yes_choices[ref.complete_ref_raw.lower()][0] == other_paper.title_raw.lower():
                    ref.paper_id = [other_paper.id, "manual"]
                    api.client.update_paper(paper)
                    other_paper.cited_by.append(paper.id)
                    api.client.update_paper(other_paper)
                    continue

                if ref.complete_ref_raw.lower() in nope_choices and \
                        nope_choices[ref.complete_ref_raw.lower()] == other_paper.title_raw.lower():
                    continue

                # annotate
                similarity = SequenceMatcher(None, ref.complete_ref_raw.lower(), other_paper.title_raw.lower()).ratio()
                if similarity >= 0.49:
                    choice = ''
                    while choice.lower() != 'y' and choice.lower() != 'n' and choice.lower() != "exit":
                        choice = input("{}\n ---> {}\n(y/n)".format(other_paper.title_raw.lower(), ref.complete_ref_raw.lower()))

                    if choice.lower() == 'y':
                        ref.paper_id = [other_paper.id, "manual"]
                        api.client.update_paper(paper)
                        other_paper.cited_by.append(paper.id)
                        api.client.update_paper(other_paper)
                        yes_choices[ref.complete_ref_raw.lower()] = [other_paper.title_raw.lower(), other_paper.id]
                    elif choice.lower() == 'n':
                        nope_choices[ref.complete_ref_raw.lower()] = other_paper.title_raw.lower()
                    elif choice.lower() == 'exit':
                        with open(REQ_DATA_PATH + "finished_papers.txt", 'wb') as fp:
                            pickle.dump(finished_files, fp)
                        print("bye!")
                        exit(0)

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
