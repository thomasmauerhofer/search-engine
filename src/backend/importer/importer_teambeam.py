# encoding: utf-8

import os
from xml.dom import minidom
from config import path_to_teambeam_executable, path_to_datastore
from backend.importer.importer_base import ImporterBase
from backend.datastore.structure.paper import Paper
from backend.datastore.structure.section import SectionType, TextType
from backend.datastore.structure.reference import ReferenceType
from backend.exceptions.import_exceptions import WrongReferenceError

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
		author_values = []
		for feature in features:
			value = feature.getAttribute("value").rstrip()

			parent = feature.parentNode
			start = int(parent.getAttribute("start"))
			end = int(parent.getAttribute("end"))

			if value == 'section':
				paper.add_section(data[start:end])
			elif value == 'subsection':
				paper.add_subsection(data[start:end])
			elif value == 'subsubsection':
				paper.add_subsubsection(data[start:end])
			elif value == 'main':
				paper.add_text_to_current_section(TextType.MAIN, data[start:end])
			elif value == 'table':
				paper.add_text_to_current_section(TextType.TABLE, data[start:end])
			elif value == 'sparse':
				paper.add_text_to_current_section(TextType.SPARSE, data[start:end])
			elif value == 'caption':
				paper.add_text_to_current_section(TextType.CAPTION, data[start:end])
			elif value == 'paragraph':
				paper.add_text_to_current_section(TextType.PARAGRAPH, data[start:end])
			elif value == 'reference':
				paper.add_reference(data[start:end])
			elif 'ref-' in value:
				reference_values.append([value, data[start:end]])
			elif value == 'authors' or \
				value == 'given-name' or \
				value == 'surname' or \
				value == 'email' or \
				value == 'affiliations':
				author_values.append([value, data[start:end]])
			#else:
			#	if (value != '') and (value != 'heading') and len(value) < 50:
			#		print("VALUE NOT IN LIST!")
			#		print(value + ": " + data[start:end])

		self.__add_values_to_references__(paper, reference_values)
		self.__add_values_to_authors__(paper, author_values)
		print(paper)


#-------------------------------------------------------------------------------
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
					paper.references[i].add_author(ReferenceType.AUTHOR, surname, data)
				elif value == 'ref-authorOther':
					name = data.split(',')
					if(len(name) < 2):
						name.append('')

					paper.references[i].add_author(ReferenceType.AUTHOR_OTHER, name[0], name[1])
				elif value == 'ref-title':
					paper.references[i].add_title(data)
					next_reference = True
				elif value == 'ref-other':
					paper.references[i].add_reference_info(ReferenceType.OTHER, data)
				elif value == 'ref-source':
					paper.references[i].add_reference_info(ReferenceType.SOURCE, data)
				elif value == 'ref-date':
					paper.references[i].add_reference_info(ReferenceType.DATE, data)
				elif value == 'ref-note':
					paper.references[i].add_reference_info(ReferenceType.NOTE, data)
				elif value == 'ref-location':
					paper.references[i].add_reference_info(ReferenceType.LOCATION, data)
				elif value == 'ref-publisher':
					paper.references[i].add_reference_info(ReferenceType.PUBLISHER, data)
				elif value == 'ref-volume':
					paper.references[i].add_reference_info(ReferenceType.VOLUME, data)
				elif value == 'ref-editor':
					paper.references[i].add_reference_info(ReferenceType.EDITOR, data)
				elif value == 'ref-issue':
					paper.references[i].add_reference_info(ReferenceType.ISSUE, data)
				else:
					print(value + ": " + data)

				previous = False
				j += 1
			except WrongReferenceError:
				i = i-2 if previous else i+1
				previous = not previous

#-------------------------------------------------------------------------------
	def __add_values_to_authors__(self, paper, author_values):
		i = 0

		while i < len(author_values):
			value, data = author_values[i]

			if value == 'authors':
				paper.authors.add_authors_text(data)
			elif value == 'surname':
				last_value, last_data = author_values[i-1]

				if last_value == 'given-name':
					paper.add_author(last_data, data)
			elif value == 'email':
				surname_value, surname_data = author_values[i-1]
				givenname_value, givenname_data = author_values[i-2]

				if (givenname_value == 'given-name') and (surname_value == 'surname'):
					paper.authors.add_email(givenname_data, surname_data, data)

			elif value == 'affiliations':
				surname_value, surname_data = author_values[i-1]
				givenname_value, givenname_data = author_values[i-2]

				if (givenname_value == 'given-name') and (surname_value == 'surname'):
					paper.authors.add_affiliation(givenname_data, surname_data, data)

			i += 1


ImporterBase.register(ImporterTeambeam)
