#!/usr/bin/env python3
# encoding: utf-8

from enum import Enum
from backend.exceptions.import_exceptions import WrongReferenceError

class Reference(object):
	def __init__(self, complete_reference):
		self.complete_reference = complete_reference
		self.authors = []
		self.title = ''
		self.reference_info = []

	def __str__(self):
		ref_str = self.complete_reference + '\n\n'
		ref_str += self.title

		for author in self.authors:
			ref_str += author[0].name + ": " + author[1] + " " + author[2] + '\n'

		for info in self.reference_info:
			ref_str += info[0].name + ": " + info[1] + '\n'

		ref_str += '\n'
		return ref_str

	def add_author(self, author_type, sur_name, given_name):
		if given_name not in self.complete_reference:
			raise WrongReferenceError('Error: Reference does not contain author')

		if sur_name not in self.complete_reference:
			sur_name = ''

		self.authors.append([author_type, sur_name, given_name])

	def add_title(self, title):
		if title not in self.complete_reference:
			raise WrongReferenceError('Error: Reference does not contain title')

		self.title += title

	def add_reference_info(self, reference_type, text):
		if text not in self.complete_reference:
			raise WrongReferenceError('Error: Reference does not contain text')

		self.reference_info.append([reference_type, text])

class ReferenceType(Enum):
	SOURCE = 50
	EDITOR = 51
	DATE = 52
	NOTE = 53
	LOCATION = 54
	PUBLISHER = 55
	VOLUME = 56
	ISSUE = 57
	OTHER = 58
	AUTHOR = 100
	AUTHOR_OTHER = 101
