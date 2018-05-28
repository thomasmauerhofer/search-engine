#!/usr/bin/env python3
# encoding: utf-8
import pprint
from enum import Enum

from engine.datastore.structure.paper_structure import PaperStructure
from engine.datastore.structure.text import Text
from engine.preprocessing.text_processor import TextProcessor
from engine.utils.objects.word_hist import WordHist


class Section(PaperStructure):
    def __init__(self, data):
        self.heading_raw = data.get('heading_raw')
        self.heading_proceed = data.get('heading_proceed') if 'heading_proceed' in data else \
            TextProcessor.proceed_string(data.get('heading_raw'))

        self.section_type = SectionType[data.get('section_type')]

        self.imrad_types = [IMRaDType[imrad_type] for imrad_type in data.get('imrad_types')] if 'imrad_types' in data else []
        self.text = [Text(text) for text in data.get('text')] if 'text' in data else []
        self.subsections = [Section(subsection) for subsection in data.get('subsections')] if 'subsections' in data else []

        self.word_hist = WordHist(data.get('word_hist')) if "word_hist" in data else WordHist()


    def __str__(self):
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pformat(self.to_dict())


    def to_dict(self):
        data = {'section_type': self.section_type.name, 'heading_raw': self.heading_raw, 'heading_proceed': self.heading_proceed,
                'text': [], 'subsections': [], 'imrad_types': [], 'word_hist': self.word_hist}

        for text in self.text:
            data['text'].append(text.to_dict())

        for subsection in self.subsections:
            data['subsections'].append(subsection.to_dict())

        for imrad_type in self.imrad_types:
            data['imrad_types'].append(imrad_type.name)

        return data


    def get_combined_word_hist(self):
        if not self.word_hist:
            for word in self.heading_proceed.split():
                self.word_hist[word] = self.word_hist[word] + 1 if word in self.word_hist else 1

            for text in self.text:
                for word in text.text_proceed.split():
                    self.word_hist[word] = self.word_hist[word] + 1 if word in self.word_hist else 1

        ret = WordHist(self.word_hist.copy())
        for subsection in self.subsections:
            ret.append(subsection.get_combined_word_hist())
        return ret


    def add_text_object(self, text_type, text_raw):
        if len(self.subsections):
            self.subsections[-1].add_text_object(text_type, text_raw)
        else:
            self.text.append(Text({"text_type": text_type.name, "text_raw": text_raw}))


    def add_subsection(self, section_type, heading):
        self.subsections.append(Section({'section_type': section_type.name, 'heading_raw': heading}))


    def add_to_imrad(self, imrad_type):
        if not any(imrad_type is x for x in self.imrad_types) and \
                (not (self.heading_raw.isspace() or self.heading_raw is '')):
            self.imrad_types.append(imrad_type)


    def title_exist(self):
        return bool(self.heading_proceed)


    def text_exist(self):
        return any([text for text in self.text if text.text_proceed])




class SectionType(Enum):
    ABSTRACT = 1
    SECTION = 2
    SUBSECTION = 3
    SUBSUBSECTION = 4


class IMRaDType(Enum):
    ABSTRACT = 0
    INTRODUCTION = 1
    BACKGROUND = 2
    METHODS = 3
    RESULTS = 4
    DISCUSSION = 5
    ACKNOWLEDGE = 6
