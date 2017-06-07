#!/usr/bin/env python3
# encoding: utf-8

class Reference(object):
	def __init__(self, complete_reference):
		self.complete_reference = complete_reference
		self.authors = []
		self.other = ""
		self.title = ""
		self.source = ""
		self.date = ""
		self.note = ""

	def __str__(self):
		return str(self.complete_reference) + "\n\n" + \
			str(self.title) + "\n" + \
			str(self.authors) + "\n" + \
			str(self.other) + "\n" + \
			str(self.source) + "\n" + \
			str(self.date) + "\n" + \
			str(self.note)

	def add_author(self, sur_name, given_name):
		if sur_name not in self.complete_reference or \
			given_name not in self.complete_reference:
			raise Exception("Error: Reference does not contain author")

		self.authors.append([sur_name, given_name])

	def add_title(self, title):
		if title not in self.complete_reference:
			raise Exception("Error: Reference does not contain title")

		self.title += title

	def add_other(self, other):
		if other not in self.complete_reference:
			raise Exception("Error: Reference does not contain other")

		self.other += other

	def add_source(self, source):
		if source not in self.complete_reference:
			raise Exception("Error: Reference does not contain source")

		self.source += source

	def add_date(self, date):
		if date not in self.complete_reference:
			raise Exception("Error: Reference does not contain date")

		self.date += date

	def add_note(self, note):
		if note not in self.complete_reference:
			raise Exception("Error: Reference does not contain note")

		self.note += note
