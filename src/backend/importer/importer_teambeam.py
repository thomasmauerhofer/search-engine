# encoding: utf-8

import os
from xml.dom import minidom
from config import path_to_teambeam_executable, path_to_datastore
from backend.importer.importer_base import ImporterBase
from backend.datastore.structure.paper import Paper

EXTENTION_TEXT = ".txt"
EXTENTION_STRUCTURE = ".xml"

class ImporterTeambeam(ImporterBase):
	def import_paper(self, filename):
		paper = Paper()
		path_to_file = path_to_datastore + filename
		#os.system('cd ' + path_to_teambeam_executable + ' &&  sh pdf-to-xml -a ' + path_to_file)

		with open (path_to_file + EXTENTION_TEXT, "r") as textfile:
			data = textfile.read()

		tree = minidom.parse(path_to_file + EXTENTION_STRUCTURE)
		features = tree.getElementsByTagName("feature")

		reference_values = []
		for feature in features:
			value = feature.getAttribute("value")

			parent = feature.parentNode
			start = int(parent.getAttribute("start"))
			end = int(parent.getAttribute("end"))

			if value == 'reference':
				paper.add_reference(data[start:end])
			elif value == 'ref-authorSurname' or \
				value == 'ref-authorGivenName' or \
				value == 'ref-title' or \
				value == 'ref-other' or \
				value == 'ref-source' or \
				value == 'ref-date' or \
				value == 'ref-note':
				reference_values.append([value, data[start:end]])


			#print(value + ": " + data[start:end])
		self.__add_values_to_references__(paper, reference_values)
		print(paper)

	def __add_values_to_references__(self, paper, reference_values):
		next_reference = previous = False
		i = j = 0
		surname = ""

		while j < len(reference_values):
			value, data = reference_values[j]

			try:
				if value == 'ref-authorSurname':
					surname = data
					#new reference always starts with ref-authorSurname.
					#Needed additionally to exception handling, because authors can be repeatedly in different references
					if next_reference:
						i+=1
						next_reference = False
				elif value == 'ref-authorGivenName':
					paper.references[i].add_author(surname, data)
				elif value == 'ref-title':
					paper.references[i].add_title(data)
					next_reference = True
				elif value == 'ref-other':
					paper.references[i].add_other(data)
				elif value == 'ref-source':
					paper.references[i].add_source(data)
				elif value == 'ref-date':
					paper.references[i].add_date(data)
				elif value == 'ref-note':
					paper.references[i].add_note(data)

				previous = False
				j += 1
			except Exception:
				i = i-2 if previous else i+1
				previous = not previous


ImporterBase.register(ImporterTeambeam)
