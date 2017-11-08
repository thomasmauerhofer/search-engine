#!/usr/bin/env python3
# encoding: utf-8

from typing import Dict
from enum import Enum
from backend.datastore.structure.paper_structure import PaperStructure


class Section(PaperStructure):
    def __init__(self, data_or_section_type, heading=''):
        if isinstance(data_or_section_type, SectionType):
            self.__create_object__(data_or_section_type, heading)
        elif isinstance(data_or_section_type, Dict):
            self.__create_object_with_dict__(data_or_section_type)

    def __create_object__(self, section_type, heading):
        self.imrad_types = []
        self.section_type = section_type
        self.heading = heading
        self.text = []
        self.subsections = []

    def __create_object_with_dict__(self, data):
        self.section_type = SectionType[data.get('section_type')]
        self.heading = data.get('heading')
        self.imrad_types = []
        self.text = []
        self.subsections = []

        for imrad_type in data.get('imrad_types'):
            self.imrad_types.append(IMRaDType[imrad_type])

        for obj in data.get('text'):
            self.text.append([TextType[obj.get('text_type')], obj.get('text')])

        for subsection in data.get('subsections'):
            self.subsections.append(Section(subsection))

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
        self.subsections.append(Section(section_type, heading))

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
