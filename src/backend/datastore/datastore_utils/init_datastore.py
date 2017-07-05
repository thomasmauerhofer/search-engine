#!/usr/bin/env python3
# encoding: utf-8
from optparse import OptionParser
import os, shutil, base64
from config import path_to_datastore
from backend.datastore.api import add_paper

def __init_datastore__(folder):
	__init_database__()
	__add_files__(folder)

def __init_database__():
	print ('implement method')

def __add_files__(folder):
	for filename in os.listdir(os.path.abspath(folder)):

		print('CURRENT FILE: ' + filename)
		if filename.endswith('.pdf'):
			src = folder + "/" + filename
			dst = path_to_datastore + filename
			shutil.copy(src, dst)
			add_paper(filename)

def __get_foldername__():
	parser = OptionParser()
	parser.add_option("-f", "--folder", dest="folder",
                  help="import all data from folder to database", metavar="FOLDER")
	(options, args) = parser.parse_args()
	return options.folder


if __name__ == "__main__":
	folder = __get_foldername__()
	if(folder):
		__init_datastore__(folder)
	else:
		print("Usage: No Parameter! Use -f FOLDERPATH to upload all files of a folder, or -h for help")
