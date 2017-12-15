#!/usr/bin/env python3
# encoding: utf-8

from enum import Enum
from backend.datastore.structure.paper_structure import PaperStructure
from backend.datastore.structure.author import Author
from backend.utils.exceptions.import_exceptions import WrongReferenceError


class Reference(PaperStructure):
    def __init__(self, data):
        self.complete_reference = data.get('complete_reference')
        self.title = data.get('title') if 'title' in data else ''

        self.authors = [[ReferenceType[author.get('author_type')], Author(author.get('author'))]
                        for author in data.get('authors')] if 'authors' in data else []
        self.reference_info = [[ReferenceType[info.get('reference_type')], info.get('reference_text')]
                               for info in data.get('reference_info')] if 'reference_info' in data else []

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
        data = {'complete_reference': self.complete_reference, 'title': self.title, 'reference_info': [], 'authors': []}

        for reference in self.reference_info:
            dic = {'reference_type': reference[0].name, 'reference_text': reference[1]}
            data['reference_info'].append(dic)

        for author in self.authors:
            dic = {'author_type': author[0].name, 'author': author[1].to_dict()}
            data['authors'].append(dic)

        return data

    def add_author(self, author_type, prename, surname):
        if surname not in self.complete_reference:
            raise WrongReferenceError('Error: Reference does not contain author', 'author',
                                      str(Author({'prename': prename, 'surname': surname})))

        self.authors.append([author_type, Author({'prename': prename, 'surname': surname})])

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
