#!/usr/bin/env python3
# encoding: utf-8
import os
from optparse import OptionParser
import os, shutil, base64
from config import path_to_datastore
from backend.datastore.api import API


def __add_files__(folder):
	api = API()
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

	paper = api.get_paper(papers[0].id)
	print(paper.filename)



if __name__ == "__main__":
	os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

	parser = OptionParser()
	parser.add_option("-f", "--folder", dest="folder",
		help="import all data from folder to database", metavar="FOLDER")
	parser.add_option("-c", "--check", action="store_true" ,dest="check", default=False,
		help="Check if there are values in the database")
	(options, args) = parser.parse_args()

	if(options.folder):
		__add_files__(options.folder)
	elif(options.check):
		__check_database__()
	else:
		print("Usage: No Parameter! Use -f FOLDERPATH to upload all files of a folder, or -h for help")
