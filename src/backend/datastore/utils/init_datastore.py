#!/usr/bin/env python3
# encoding: utf-8
from optparse import OptionParser
import tkinter, os, shutil
from tkinter import filedialog
from config import path_to_datastore
from backend.importer.importer_teambeam import add_paper

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

			add_paper(dst)

def get_foldername():
	parser = OptionParser()
	parser.add_option("-f", "--folder", dest="folder",
                  help="import all data from folder to database", metavar="FOLDER")
	(options, args) = parser.parse_args()

	if options.folder:
		return options.folder
	else:
		root = tkinter.Tk()
		root.withdraw()
		return filedialog.askdirectory()

if __name__ == "__main__":
	folder = get_foldername()
	if(folder):
		init_datastore(folder)
