# encoding: utf-8

import os
from xml.dom import minidom
from config import path_to_teambeam_executable, path_to_datastore
from backend.importer.importer_base import ImporterBase
from backend.datastore.structure.paper import Paper
from backend.datastore.structure.section import SectionType, TextType
from backend.datastore.structure.reference import ReferenceType
from backend.utils.exceptions.import_exceptions import WrongReferenceError

EXTENTION_TEXT = ".txt"
EXTENTION_STRUCTURE = ".xml"
OUTPUT_FILENAME = "output.txt"
OUTPUT = open(OUTPUT_FILENAME, "w")

IGNORE_CASES = ["heading", "<table border=\"1\" summary=\"\""]

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
			text = data[start:end].rstrip('\n')

			if value == 'section':
				paper.add_section(text)
			elif value == 'subsection':
				paper.add_subsection(text)
			elif value == 'subsubsection':
				paper.add_subsubsection(text)
			elif value == 'main':
				paper.add_text_to_current_section(TextType.MAIN, text)
			elif value == 'table':
				paper.add_text_to_current_section(TextType.TABLE, text)
			elif value == 'sparse':
				paper.add_text_to_current_section(TextType.SPARSE, text)
			elif value == 'caption':
				paper.add_text_to_current_section(TextType.CAPTION, text)
			elif value == 'paragraph':
				paper.add_text_to_current_section(TextType.PARAGRAPH, text)
			elif value == 'citation':
				paper.add_text_to_current_section(TextType.CITATION, text)
			elif value == 'reference':
				paper.add_reference(text)
			elif 'ref-' in value:
				reference_values.append([value, text])
			elif value == 'authors' or \
				value == 'given-name' or \
				value == 'surname' or \
				value == 'email' or \
				value == 'affiliations':
				author_values.append([value, text])
			else:
				if (len(value.split()) == 1) and (not any(s in value for s in IGNORE_CASES)):
					OUTPUT.write("VALUE NOT IN LIST!\n")
					OUTPUT.write(value)
					OUTPUT.write("\n")

		self.__add_values_to_references__(paper, reference_values)
		self.__add_values_to_authors__(paper, author_values)
		return paper


#-------------------------------------------------------------------------------
	def __add_values_to_references__(self, paper, reference_values):
		full_round = False
		i = j = 0

		while j < len(reference_values):
			value, data = reference_values[j]

			try:
				if value == 'ref-authorGivenName':
					last_value, last_data = reference_values[j - 1]
					surname = last_data if last_value == 'ref-authorSurname' else ''

					paper.references[i].add_author(ReferenceType.AUTHOR, data, last_data)
				elif value == 'ref-authorOther':
					name = data.split(',')
					if(len(name) < 2):
						name.append('')

					paper.references[i].add_author(ReferenceType.AUTHOR_OTHER, name[1], name[0])
				elif value == 'ref-title':
					paper.references[i].add_title(data)
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
				elif value != 'ref-authorSurname':
					OUTPUT.write("REFERENCE NOT IN LIST!\n")
					OUTPUT.write(value)
					OUTPUT.write("\n")

				full_round = False
				j += 1
			except WrongReferenceError:
				i += 1

				if full_round:
					OUTPUT.write("CAN'T FIND CORRECT REFERENCE FOR:\n")
					OUTPUT.write(WrongReferenceError.value + ":\n")
					OUTPUT.write(WrongReferenceError.data + "\n\n")
					j += 1
					full_round = False
				elif i == len(paper.references):
					full_round = True
					i = 0

#-------------------------------------------------------------------------------
	def __add_values_to_authors__(self, paper, author_values):
		i = 0

		while i < len(author_values):
			value, data = author_values[i]

			if value == 'authors':
				paper.add_authors_text(data)
			elif value == 'surname':
				last_value, last_data = author_values[i-1]

				if last_value == 'given-name':
					paper.authors[-1].add_author(last_data, data)
			elif value == 'email':
				paper.authors[-1].add_email(data)
			elif value == 'affiliations':
				paper.authors[-1].add_affiliation(data)

			i += 1
#-------------------------------------------------------------------------------
ImporterBase.register(ImporterTeambeam)
