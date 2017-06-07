#!/usr/bin/env python3
# encoding: utf-8

from backend.datastore.structure.reference import Reference

class Paper(object):
	def __init__(self):
		self.references = []

	def __str__(self):
		str_paper = ""
		for reference in self.references:
			str_paper +="--------------------------------------------------------------------------------\n" + \
                str(reference) + "\n" + \
                "--------------------------------------------------------------------------------\n\n"
		return str_paper

	def add_reference(self, full_reference):
		self.references.append(Reference(full_reference))
