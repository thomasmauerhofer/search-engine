#!/usr/bin/env python3
# encoding: utf-8

from typing import Dict
from config import path_to_datastore
from backend.datastore.structure.paper_structure import PaperStructure
from backend.datastore.structure.reference import Reference
from backend.datastore.structure.section import Section, SectionType, TextType, IMRaDType
from backend.datastore.structure.author import Authors

class Paper(PaperStructure):
	def __init__(self, data):
		if isinstance(data, str):
			self.__create_object__(data)
		elif isinstance(data, Dict):
			self.__create_object_with_dict__(data)


	def __create_object__(self, filename):
		self.filename = filename
		self.title = ''
		self.id = ''
		self.authors = []
		self.sections = []
		self.references = []
		self.file = open(path_to_datastore + filename, "rb").read()



	def __create_object_with_dict__(self, data):
		self.filename = data.get('filename')
		self.title = data.get('title')
		self.id = data.get('_id')
		self.file = data.get('file')
		self.authors = []
		self.sections = []
		self.references = []

		for author in data.get('authors'):
			self.authors.append(Authors(author))

		for section in data.get('sections'):
			self.sections.append(Section(section))

		for reference in data.get('references'):
			self.references.append(Reference(reference))


	def __str__(self):
		str_paper = "--------------------------------------------------------------------------------\n"

		str_paper += "Authors:\n"
		for author in self.authors:
			str_paper += str(author) + "\n"
		str_paper += "\n"

		str_paper += "Sections:\n"
		for section in self.sections:
			str_paper += str(section) + "\n"
		str_paper += "\n"

		str_paper += "References:\n"
		for reference in self.references:
			str_paper += str(reference) + "\n"

		str_paper +="--------------------------------------------------------------------------------\n\n"
		return str_paper


	def to_dict(self):
		data = {}
		data['filename'] = self.filename
		data['title'] = self.title
		data['file'] = self.file
		data['authors'] = []
		data['sections'] = []
		data['references'] = []

		for author in self.authors:
			data['authors'].append(author.to_dict())
		for section in self.sections:
			data['sections'].append(section.to_dict())
		for reference in self.references:
			data['references'].append(reference.to_dict())

		return data


	def set_title(self, title):
		if title == '':
			self.title = title


	def add_abstract(self, text):
		self.sections.append(Section(SectionType.ABSTRACT, 'abstract'))
		self.sections[-1].imrad_type = IMRaDType.ABSTRACT
		self.add_text_to_current_section(TextType.MAIN, text)


	def add_section(self, section_name):
		self.sections.append(Section(SectionType.SECTION, section_name))


	def add_subsection(self, section_name):
		if not len(self.sections):
			self.add_section('')

		self.sections[-1].add_subsection(SectionType.SUBSECTION, section_name)


	def add_subsubsection(self, section_name):
		if not len(self.sections):
			self.add_section('')

		if not len(self.sections[-1].subsections):
			self.add_subsection('')

		self.sections[-1].subsections[-1].add_subsection(SectionType.SUBSUBSECTION, section_name)


	def add_text_to_current_section(self, text_type, text):
		if not len(self.sections):
			self.add_section('')

		self.sections[-1].add_text_object(text_type, text)


	def add_reference(self, full_reference):
		self.references.append(Reference(full_reference))


	def add_authors_text(self, full_authors):
		self.authors.append(Authors(full_authors))


	def get_capter_with_imrad_type(self, imrad_type):
		return next((indro for indro in self.sections if imrad_type in indro.imrad_type), None)


	def get_indroduction(self):
		return self.get_capter_with_imrad_type(IMRaDType.INDRODUCTION)


	def get_methods(self):
		return self.get_capter_with_imrad_type(IMRaDType.METHODS)


	def get_results(self):
		return self.get_capter_with_imrad_type(IMRaDType.RESULTS)


	def get_discussion(self):
		return self.get_capter_with_imrad_type(IMRaDType.DISCUSSION)

	def save_file_to_path(self, path):
		open(path + self.filename, 'wb').write(self.file)
		return path + self.filename
