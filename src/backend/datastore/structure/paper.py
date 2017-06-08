#!/usr/bin/env python3
# encoding: utf-8

from backend.datastore.structure.reference import Reference
from backend.datastore.structure.section import Section, SectionType
from backend.datastore.structure.author import Authors

class Paper(object):
	def __init__(self):
		self.authors = Authors()
		self.sections = []
		self.references = []

	def __str__(self):
		str_paper = "--------------------------------------------------------------------------------\n"

		str_paper += "Authors:\n"
		str_paper += str(self.authors)
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

	def add_author(self, prename, surname):
		self.authors.add_author(prename, surname)
