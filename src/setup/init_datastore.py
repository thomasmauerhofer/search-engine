#!/usr/bin/env python3
# encoding: utf-8

import os
import shutil
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
                paper_id = api.add_paper(filename)
                print(paper_id)
            except IOError as e:
                print(e)
            except OSError as e:
                print(e)
            except ClassificationError as e:
                print(e)


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


if __name__ == "__main__":
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    parser = OptionParser()
    parser.add_option("-f", "--folder", dest="folder",
                      help="import all data from folder to database", metavar="FOLDER")
    parser.add_option("-c", "--check", action="store_true", dest="check", default=False,
                      help="Check if there are values in the database")
    parser.add_option("-u", "--user", action="store_true", dest="user", default=False,
                      help="Add a new Adminuser to the database")
    (options, args) = parser.parse_args()

    if options.folder:
        __add_files(options.folder)
    elif options.check:
        __check_database()
    elif options.user:
        __add_user()
    else:
        print("Usage: No Parameter! Use -f FOLDERPATH to upload all files of a folder, or -h for help")
