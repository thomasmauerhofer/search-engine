# encoding: utf-8

import os
from config import path_to_teambeam_executable, path_to_datastore
from backend.importer.importer_base import ImporterBase

EXTENTION_TEXT = ".txt"
EXTENTION_STRUCTURE = ".xml"

class ImporterTeambeam(ImporterBase):
	def import_paper(self, filename):
		os.system('cd ' + path_to_teambeam_executable + ' &&  sh pdf-to-xml -a ' + path_to_datastore + filename)
		print(filename)

ImporterBase.register(ImporterTeambeam)
