#!/usr/bin/env python3
# encoding: utf-8

import os
import shutil
from difflib import SequenceMatcher
from getpass import getpass
from optparse import OptionParser

from config import UPLOAD_FOLDER
from engine.api import API
from engine.utils.exceptions.import_exceptions import ClassificationError


def __add_files(folder):
    api = API(False)
    api.delete_all_paper()

    for filename in os.listdir(os.path.abspath(folder)):
        try:
            if filename.endswith('.pdf'):
                print('CURRENT FILE: ' + str(filename))
        except UnicodeError:
            print("ERROR: Can't decode filename - Remove Special Characters!")
            continue

        if filename.endswith('.pdf'):
            src = folder + "/" + filename
            dst = UPLOAD_FOLDER + filename
            shutil.copy(src, dst)
            try:
                paper_id = api.add_papers([filename])
                print(paper_id)
            except IOError as e:
                print(e)
            except OSError as e:
                print(e)
            except ClassificationError as e:
                print(e)


def __import_json(filepath):
    os.popen("mongoimport --db searchengine --collection papers --file ", filepath)


def __check_database():
    api = API()
    papers = api.get_all_paper()
    print(len(papers))


def __add_user():
    print("Add new admin to the database")
    name = input("username: ")
    password = getpass()
    api = API()
    api.add_user(name, password)
    print("Welcome on board {}".format(name))


def __link_references_to_paper():
    api = API()
    papers = api.get_all_paper()
    yes_choices, nope_choices = {}, {}
    for paper in papers:
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
                    continue

                if ref.complete_ref_raw.lower() in nope_choices and \
                        nope_choices[ref.complete_ref_raw.lower()] == other_paper.title_raw.lower():
                    continue

                # annotate
                similarity = SequenceMatcher(None, ref.complete_ref_raw.lower(), other_paper.title_raw.lower()).ratio()
                if similarity >= 0.49:
                    choice = ''
                    while choice.lower() != 'y' and choice.lower() != 'n':
                        choice = input("{}\n ---> {}\n(y/n)".format(other_paper.title_raw.lower(), ref.complete_ref_raw.lower()))

                    if choice.lower() == 'y':
                        ref.paper_id = [other_paper.id, "manual"]
                        api.client.update_paper(paper)
                        yes_choices[ref.complete_ref_raw.lower()] = [other_paper.title_raw.lower(), other_paper.id]
                    elif choice.lower() == 'n':
                        nope_choices[ref.complete_ref_raw.lower()] = other_paper.title_raw.lower()


if __name__ == "__main__":
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    parser = OptionParser()
    parser.add_option("-f", "--folder", dest="folder",
                      help="import all data from folder to database", metavar="FOLDER")
    parser.add_option("-j", "--json", dest="json",
                      help="import data from json into database", metavar="JSON")
    parser.add_option("-c", "--check", action="store_true", dest="check", default=False,
                      help="Check if there are values in the database")
    parser.add_option("-u", "--user", action="store_true", dest="user", default=False,
                      help="Add a new Adminuser to the database")
    parser.add_option("-r", "--link_references", action="store_true", dest="link_ref", default=False,
                      help="Link references manually")
    (options, args) = parser.parse_args()

    if options.folder:
        __add_files(options.folder)
    elif options.json:
        __import_json(options.json)
    elif options.check:
        __check_database()
    elif options.user:
        __add_user()
    elif options.link_ref:
        __link_references_to_paper()
    else:
        print("Usage: No Parameter! Use -f FOLDERPATH to upload all files of a folder, or -h for help")
