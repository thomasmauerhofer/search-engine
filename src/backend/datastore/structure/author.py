#!/usr/bin/env python3
# encoding: utf-8

from backend.utils.exceptions.import_exceptions import WrongAuthorError
from backend.utils.string_utils import is_valid_email, remove_special_chars, longest_subsequence

class Authors(object):
    def __init__(self, all_authors_text):
        self.all_authors_text = all_authors_text
        self.emails_text = ''
        self.authors = []

    def __str__(self):
        str_authors = self.all_authors_text + "\n\n"

        for author in self.authors:
            str_authors += str(author)

        return str_authors

    def add_author(self, prename, surname, middle_name = None):
        #if surname not in self.all_authors_text:
        #    raise WrongAuthorError('Error: Authors does not contain surname')

        if not (prename, surname) in [(obj.prename, obj.surname) for obj in self.authors]:
            self.authors.append(Author(prename, surname, middle_name))

    def add_email(self, email):
        if not is_valid_email(email):
            return

        name = remove_special_chars(email.split('@')[0]).lower()
        longest_sequence_list = []

        for author in self.authors:
            author_str = remove_special_chars(author.prename + author.surname).lower()
            match = longest_subsequence(name, author_str)
            longest_sequence_list.append([match.size, author])

            author_str = remove_special_chars(author.surname + author.prename).lower()
            match = longest_subsequence(name, author_str)
            longest_sequence_list.append([match.size, author])

        if not len(longest_sequence_list):
            return

        higest = max(longest_sequence_list, key=lambda item:item[0])
        if higest[0] >= len(higest[1].surname):
            higest[1].email = email

    def add_affiliation(self, affiliation):
        tmp_affiliation = remove_special_chars(affiliation).lower()
        longest_sequence_list = []

        for author in self.authors:
            author_str = remove_special_chars(author.prename + author.surname).lower()
            match = longest_subsequence(tmp_affiliation, author_str)
            longest_sequence_list.append([match.size, author])

            author_str = remove_special_chars(author.surname + author.prename).lower()
            match = longest_subsequence(tmp_affiliation, author_str)
            longest_sequence_list.append([match.size, author])

        if not len(longest_sequence_list):
            return

        higest = max(longest_sequence_list, key=lambda item:item[0])
        if higest[0] >= len(higest[1].surname):
            higest[1].affiliation = affiliation

class Author(object):
    def __init__(self, prename, surname, middle_name = None):
        self.surname = surname
        self.prename = prename
        self.middle_name = middle_name
        self.email = ''
        self.affiliation = ''

    def __eq__(self, other):
        return (self.surname == other.surname) and (self.prename == other.prename)

    def __str__(self):
        str_author = self.surname + '\n'

        if self.middle_name is not None:
            str_author = self.middle_name + '\n'

        str_author += self.prename + '\n'
        str_author += self.email + '\n'
        str_author += self.affiliation + '\n'
        str_author += '\n'
        return str_author
