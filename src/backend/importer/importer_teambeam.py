# encoding: utf-8

import os
from config import path_to_teambeam_executable
from backend.importer.importer_base import ImporterBase

class ImporterTeambeam(ImporterBase):
	def import_paper(self, file):
		os.system('cd ' + path_to_teambeam_executable + ' &&  sh pdf-to-xml -a ' + file)

ImporterBase.register(ImporterTeambeam)
