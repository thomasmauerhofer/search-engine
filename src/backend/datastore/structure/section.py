#!/usr/bin/env python3
# encoding: utf-8

from enum import Enum

class Section(object):
	def __init__(self, section_type, heading):
		self.section_type = section_type
		self.heading = heading
		self.text = []
		self.subsections = []

	def __str__(self):
		str_section = self.section_type.name + ":\n"
		str_section += self.heading + "\n\n"

		for obj in self.text:
		    str_section += obj[0].name
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

class SectionType(Enum):
	SECTION = 1
	SUBSECTION = 2

class TextType(Enum):
    MAIN = 10
    SPARSE = 11
    CAPTION = 12
