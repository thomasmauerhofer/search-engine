#!/usr/bin/env python3
# encoding: utf-8
import pprint
from enum import Enum

from engine.datastore.structure.paper_structure import PaperStructure
from engine.preprocessing.text_processor import TextProcessor


class Text(PaperStructure):
    def __init__(self, data):
        self.text_type = TextType[data.get('text_type')]
        self.text_raw = data.get('text_raw')
        self.text_proceed = data.get('text_proceed') if 'text_proceed' in data else TextProcessor.proceed_string(data.get('text_raw'))

    def __str__(self):
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pformat(self.to_dict())

    def to_dict(self):
        return {'text_type': self.text_type.name, 'text_raw': self.text_raw, 'text_proceed': self.text_proceed}



class TextType(Enum):
    MAIN = 10
    TABLE = 11
    SPARSE = 12
    CAPTION = 13
    PARAGRAPH = 14
    CITATION = 15
