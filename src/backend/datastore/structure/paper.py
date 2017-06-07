#!/usr/bin/env python3
# encoding: utf-8

from backend.datastore.structure.reference import Reference
from backend.datastore.structure.section import Section, SectionType

class Paper(object):
	def __init__(self):
		self.sections = []
		self.references = []
		self.add_section(SectionType.SECTION, "")

	def __str__(self):
		str_paper = "--------------------------------------------------------------------------------\n"

		str_paper += "Sections:\n"
		for section in self.sections:
			str_paper += str(section) + "\n"
		str_paper += "\n"

		str_paper += "References:\n"
		for reference in self.references:
			str_paper += str(reference) + "\n"

		str_paper +="--------------------------------------------------------------------------------\n\n"
		return str_paper

	def add_section(self, section_type, section_name):
		if section_type == SectionType.SECTION:
			self.sections.append(Section(section_type, section_name))
		elif section_type == SectionType.SUBSECTION:
			self.sections[-1].add_subsection(section_type, section_name)

	def add_text_to_current_section(self, text_type, text):
		self.sections[-1].add_text_object(text_type, text)

	def add_reference(self, full_reference):
		self.references.append(Reference(full_reference))
