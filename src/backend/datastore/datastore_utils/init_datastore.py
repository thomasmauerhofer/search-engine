#!/usr/bin/env python3
# encoding: utf-8
import os
import shutil
from getpass import getpass
from optparse import OptionParser

from backend.datastore.api import API
from config import path_to_datastore


def __add_files__(folder):
    api = API()
    api.delete_all_paper()
    for filename in os.listdir(os.path.abspath(folder)):
        print('CURRENT FILE: ' + filename)

        if filename.endswith('.pdf'):
            src = folder + "/" + filename
            dst = path_to_datastore + filename
            shutil.copy(src, dst)
            paper_id = api.add_paper(filename)
            print(paper_id)


def __check_database__():
    api = API()
    papers = api.get_all_paper()
    print(len(papers))


def __add_user__():
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

    if (options.folder):
        __add_files__(options.folder)
    elif (options.check):
        __check_database__()
    elif (options.user):
        __add_user__()
    else:
        print("Usage: No Parameter! Use -f FOLDERPATH to upload all files of a folder, or -h for help")
