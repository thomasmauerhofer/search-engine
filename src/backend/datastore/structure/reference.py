#!/usr/bin/env python3
# encoding: utf-8

from typing import Dict
from enum import Enum
from backend.datastore.structure.paper_structure import PaperStructure
from backend.datastore.structure.author import Author
from backend.utils.exceptions.import_exceptions import WrongReferenceError

class Reference(PaperStructure):
	def __init__(self, data):
		if isinstance(data, str):
			self.__create_object__(data)
		elif isinstance(data, Dict):
			self.__create_object_with_dict__(data)


	def __create_object__(self, complete_reference):
		self.complete_reference = complete_reference
		self.title = ''
		self.authors = []
		self.reference_info = []


	def __create_object_with_dict__(self, data):
		self.complete_reference = data.get('complete_reference')
		self.title = data.get('title')
		self.authors = []
		self.reference_info = []

		for author in data.get('authors'):
			self.authors.append([ReferenceType[author.get('author_type')], Author(author.get('author'))])

		for info in data.get('reference_info'):
			self.reference_info.append([ReferenceType[info.get('reference_type')], info.get('reference_text')])


	def __str__(self):
		ref_str = self.complete_reference + '\n\n'
		ref_str += self.title + '\n'

		for author in self.authors:
			ref_str += author[0].name + ": " + author[1].surname + " " + author[1].prename + '\n'

		for info in self.reference_info:
			ref_str += info[0].name + ": " + info[1] + '\n'

		ref_str += '\n'
		return ref_str


	def to_dict(self):
		data = {}
		data['complete_reference'] = self.complete_reference
		data['title'] = self.title
		data['reference_info'] = []
		data['authors'] = []

		for reference in self.reference_info:
			dic = {}
			dic['reference_type'] = reference[0].name
			dic['reference_text'] = reference[1]
			data['reference_info'].append(dic)

		for author in self.authors:
			dic = {}
			dic['author_type'] = author[0].name
			dic['author'] = author[1].to_dict()
			data['authors'].append(dic)

		return data


	def add_author(self, author_type, prename, surname):
		if surname not in self.complete_reference:
			raise WrongReferenceError('Error: Reference does not contain author', 'author', str(Author(prename, surname)))

		self.authors.append([author_type, Author(prename, surname)])


	def add_title(self, title):
		if title not in self.complete_reference:
			raise WrongReferenceError('Error: Reference does not contain title', 'title', title)

		self.title += title


	def add_reference_info(self, reference_type, text):
		if text not in self.complete_reference:
			raise WrongReferenceError('Error: Reference does not contain text', 'info', text)

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
	PAGES = 59
	CONFERENCE = 60
	AUTHOR = 100
	AUTHOR_OTHER = 101
