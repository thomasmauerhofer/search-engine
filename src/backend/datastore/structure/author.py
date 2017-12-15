#!/usr/bin/env python3
# encoding: utf-8

from backend.datastore.structure.paper_structure import PaperStructure
from backend.utils.string_utils import is_valid_email, remove_special_chars, longest_subsequence


class Authors(PaperStructure):
    def __init__(self, data):
        self.all_authors_text = data.get('all_authors_text')
        self.emails_text = data.get('emails_text') if 'emails_text' in data else ''
        self.authors = [Author(author) for author in data.get('authors')] if 'authors' in data else []

    def __str__(self):
        str_authors = self.all_authors_text + "\n\n"

        for author in self.authors:
            str_authors += str(author)

        return str_authors

    def to_dict(self):
        data = {'all_authors_text': self.all_authors_text, 'emails_text': self.emails_text, 'authors': []}
        for author in self.authors:
            data['authors'].append(author.to_dict())

        return data

    def add_author(self, prename, surname, middle_name=None):
        # if surname not in self.all_authors_text:
        #    raise WrongAuthorError('Error: Authors does not contain surname')

        if not (prename, surname) in [(obj.prename, obj.surname) for obj in self.authors]:
            self.authors.append(Author({'prename': prename, 'surname': surname, 'middle_name': middle_name}))

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

        highest = max(longest_sequence_list, key=lambda item: item[0])
        if highest[0] >= len(highest[1].surname):
            highest[1].email = email

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

        higest = max(longest_sequence_list, key=lambda item: item[0])
        if higest[0] >= len(higest[1].surname):
            higest[1].affiliation = affiliation


class Author(PaperStructure):
    def __init__(self, data):
        self.surname = data.get('surname')
        self.prename = data.get('prename')

        self.middle_name = data.get('middle_name') if 'middle_name' in data else ''
        self.email = data.get('email') if 'email' in data else ''
        self.affiliation = data.get('affiliation') if 'affiliation' in data else ''

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

    def to_dict(self):
        data = {'surname': self.surname, 'prename': self.prename, 'middle_name': self.middle_name, 'email': self.email,
                'affiliation': self.affiliation}
        return data
