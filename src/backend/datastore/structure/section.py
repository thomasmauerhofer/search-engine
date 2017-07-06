#!/usr/bin/env python3
# encoding: utf-8

from enum import Enum

class Section(object):
	def __init__(self, section_type, heading):
		self.imrad_type = []
		self.section_type = section_type
		self.heading = heading
		self.text = []
		self.subsections = []

	def __str__(self):
		str_section = self.section_type.name
		str_section += self.heading + "\n"

		for obj in self.text:
		    str_section += obj[0].name + "\n"
		    str_section += obj[1] + "\n\n"

		for subsection in self.subsections:
		    str_section += str(subsection)

		return str_section

	def add_text_object(self, text_type, text):
		if len(self.subsections):
		    self.subsections[-1].add_text_object(text_type, text)
		else:
		    self.text.append([text_type, text])

	def add_subsection(self, section_type, heading):
		self.subsections.append(Section(section_type, heading))

	def add_to_imrad(self, imrad_type):
		self.imrad_type.append(imrad_type)

class SectionType(Enum):
	ABSTRACT = 1
	SECTION = 2
	SUBSECTION = 3
	SUBSUBSECTION = 4

class TextType(Enum):
    MAIN = 10
    TABLE = 11
    SPARSE = 12
    CAPTION = 13
    PARAGRAPH = 14
    CITATION = 15


class IMRaDType(Enum):
	INDRODUCTION = 21
	METHODS = 22
	RESULTS = 23
	DISCUSSION = 24
