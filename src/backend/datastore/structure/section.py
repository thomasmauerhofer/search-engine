#!/usr/bin/env python3
# encoding: utf-8

from enum import Enum
from backend.datastore.structure.paper_structure import PaperStructure


class Section(PaperStructure):
    def __init__(self, data):
        self.heading = data.get('heading')
        self.section_type = SectionType[data.get('section_type')]

        self.imrad_types = [IMRaDType[imrad_type] for imrad_type in data.get('imrad_types')] if 'imrad_types' in data else []
        self.text = [[TextType[obj.get('text_type')], obj.get('text')] for obj in data.get('text')] if 'text' in data else []
        self.subsections = [Section(subsection) for subsection in data.get('subsections')] if 'subsections' in data else []

    def __str__(self):
        str_section = self.section_type.name + "\n"
        str_section += self.heading + "\n"

        for imrad_type in self.imrad_types:
            str_section += imrad_type.name + " "
        str_section += "\n"

        for obj in self.text:
            str_section += obj[0].name + "\n"
            str_section += obj[1] + "\n\n"

        for subsection in self.subsections:
            str_section += str(subsection)

        return str_section

    def to_dict(self):
        data = {'section_type': self.section_type.name, 'heading': self.heading, 'text': [], 'subsections': [],
                'imrad_types': []}

        for text in self.text:
            dic = {'text_type': text[0].name, 'text': text[1]}
            data['text'].append(dic)

        for subsection in self.subsections:
            data['subsections'].append(subsection.to_dict())

        for imrad_type in self.imrad_types:
            data['imrad_types'].append(imrad_type.name)

        return data

    def add_text_object(self, text_type, text):
        if len(self.subsections):
            self.subsections[-1].add_text_object(text_type, text)
        else:
            self.text.append([text_type, text])

    def add_subsection(self, section_type, heading):
        self.subsections.append(Section({'section_type': section_type, 'heading': heading}))

    def add_to_imrad(self, imrad_type):
        if not any(imrad_type is x for x in self.imrad_types) and \
                (not (self.heading.isspace() or self.heading is '')):
            self.imrad_types.append(imrad_type)


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
    ABSTRACT = 0
    INDRODUCTION = 1
    BACKGROUND = 2
    METHODS = 3
    RESULTS = 4
    DISCUSSION = 5
    ACKNOWLEDGE = 6
