#!/usr/bin/env python3
# encoding: utf-8

from backend.exceptions.import_exceptions import WrongAuthorError

class Authors(object):
    def __init__(self):
        self.all_authors_text = []
        self.authors = []

    def __str__(self):
        str_authors = 'All:\n'
        for text in self.all_authors_text:
            str_authors += text + "\n"

        str_authors = 'Single:\n'
        for author in self.authors:
            str_authors += str(author) + "\n"

        str_authors += "\n"
        return str_authors

    def add_authors_text(self, text):
        self.all_authors_text.append(text)

    def add_author(self, prename, surname):
        if not any((prename == el.prename) and (surname == el.surname) for el in self.authors):
            self.authors.append(Author(surname, prename))

    def add_email(self, prename, surname, email):
        author = [el for el in self.authors if el.prename ==  prename and el.surname ==  surname]
        if author:
            author.email = email

    def add_affiliation(self, prename, surname, affiliation):
        author = [el for el in self.authors if el.prename ==  prename and el.surname ==  surname]
        if author:
            author.affiliation.append(affiliation)

class Author(object):
    def __init__(self, prename, surname):
        self.surname = surname
        self.prename = ''
        self.email = ''
        self.affiliations = []

    def __str__(self):
        str_author = 'Surname: ' + self.surname + '\n'
        str_author += 'Prename: ' + self.prename + '\n'
        str_author += 'email: ' + self.email + '\n'

        for affiliation in self.affiliations:
            str_author += 'affiliation:' + self.affiliation

        str_author += '\n'
        return str_author

    def add_email(self, prename, surname, email):
        if (self.surname != surname) and (self.prename != prename):
            raise WrongAuthorError('Error: Can not add email')

        self.email = email

    def add_affiliation(self, prename, surname, affiliation):
        if (self.surname != surname) and (self.prename != prename):
            raise WrongAuthorError('Error: Can not add email')

        self.affiliations.append(affiliation)
