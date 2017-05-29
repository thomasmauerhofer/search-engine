#!/usr/bin/env python3
# encoding: utf-8
from optparse import OptionParser
import os, shutil
from config import path_to_datastore
from backend.importer.importer_teambeam import ImporterTeambeam

def init_datastore(folder):
	init_database()
	add_files(folder)

def init_database():
	print ('implement method')

def add_files(folder):
	for filename in os.listdir(folder):

		if filename.endswith('.pdf'):
			print (filename)
			src = folder + "/" + filename
			dst = path_to_datastore + filename
			shutil.copy(src, dst)

			importer = ImporterTeambeam()
			importer.import_paper(dst)

def get_foldername():
	parser = OptionParser()
	parser.add_option("-f", "--folder", dest="folder",
                  help="import all data from folder to database", metavar="FOLDER")
	(options, args) = parser.parse_args()
	return options.folder


if __name__ == "__main__":
	folder = get_foldername()
	if(folder):
		init_datastore(folder)
	else:
		print("Usage: No Parameter! Use -f FOLDERPATH to upload all files of a folder, or -h for help")
