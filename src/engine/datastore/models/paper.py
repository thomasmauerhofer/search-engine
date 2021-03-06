#!/usr/bin/env python3
# encoding: utf-8
import pprint

from config import UPLOAD_FOLDER
from engine.datastore.models.author import Authors
from engine.datastore.models.paper_structure import PaperStructure
from engine.datastore.models.reference import Reference
from engine.datastore.models.section import Section, IMRaDType, SectionType
from engine.datastore.models.text import TextType
from engine.preprocessing.text_processor import TextProcessor
from engine.utils.objects.word_hist import WordHist


class Paper(PaperStructure):
    def __init__(self, data):
        self.id = data.get('_id') if '_id' in data else ''
        self.filename = data.get('filename')

        self.title_raw = data.get('title_raw') if 'title_raw' in data else ''
        self.title_proceed = data.get('title_proceed') if 'title_proceed' in data else TextProcessor.proceed_string(self.title_raw)

        self.authors = [Authors(author) for author in data.get('authors')] if 'authors' in data else []
        self.sections = [Section(section) for section in data.get('sections')] if 'sections' in data else []
        self.references = [Reference(reference) for reference in data.get('references')] if 'references' in data else []
        self.cited_by = data.get('cited_by') if 'cited_by' in data else []

        self.word_hist = WordHist(data.get('word_hist')) if "word_hist" in data else WordHist()

        try:
            self.file = data.get('file') if 'file' in data else open(UPLOAD_FOLDER + self.filename, "rb").read()
        except FileNotFoundError as e:
            print("Cant import file: {}. This should only happen in Tests".format(e))
            self.file = bytearray()


    def __str__(self):
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pformat(self.to_dict())

    def __eq__(self, other):
        return self.file == other.file


    def get_sections_with_imrad_type(self, imrad_type):
        if imrad_type == "whole-document":
            return self.sections
        imrad_type = IMRaDType[imrad_type] if isinstance(imrad_type, str) else imrad_type
        return [chapter for chapter in self.sections if imrad_type in chapter.imrad_types]


    def get_sections_with_an_imrad_type(self):
        return [chapter for chapter in self.sections if (IMRaDType.INTRODUCTION in chapter.imrad_types or
                                                         IMRaDType.BACKGROUND in chapter.imrad_types or IMRaDType.METHODS in chapter.imrad_types or
                                                         IMRaDType.RESULTS in chapter.imrad_types or IMRaDType.DISCUSSION in chapter.imrad_types)]


    def get_sections_without_an_imrad_type(self):
        return [chapter for chapter in self.sections if (not len(chapter.imrad_types) or
                IMRaDType.ABSTRACT in chapter.imrad_types or IMRaDType.ACKNOWLEDGE in chapter.imrad_types)]


    def to_dict(self):
        data = {'filename': self.filename, 'title_raw': self.title_raw, 'title_proceed': self.title_proceed,
                'file': self.file, 'authors': [], 'sections': [], 'references': [], 'cited_by': self.cited_by, 'word_hist': self.word_hist}

        for author in self.authors:
            data['authors'].append(author.to_dict())
        for section in self.sections:
            data['sections'].append(section.to_dict())
        for reference in self.references:
            data['references'].append(reference.to_dict())

        return data


    def get_combined_word_hist(self):
        if not self.word_hist:
            for word in self.title_proceed.split():
                self.word_hist[word] = self.word_hist[word] + 1 if word in self.word_hist else 1

            for section in self.sections:
                self.word_hist.append(section.get_combined_word_hist())

        return WordHist(self.word_hist.copy())


    def set_title(self, title_raw):
        if title_raw != '':
            self.title_raw = title_raw
            self.title_proceed = TextProcessor.proceed_string(title_raw)


    def add_abstract(self, text):
        self.sections.append(Section({'section_type': SectionType.ABSTRACT.name, 'heading_raw': 'abstract'}))
        self.sections[-1].imrad_types.append(IMRaDType.ABSTRACT)
        self.add_text_to_current_section(TextType.MAIN, text)


    def add_section(self, section_name):
        self.sections.append(Section({'section_type': SectionType.SECTION.name, 'heading_raw': section_name}))


    def add_subsection(self, section_name):
        if not len(self.sections):
            self.add_abstract('')
        self.sections[-1].add_subsection(SectionType.SUBSECTION, section_name)


    def add_subsubsection(self, section_name):
        if not len(self.sections):
            self.add_abstract('')

        if not len(self.sections[-1].subsections):
            self.add_subsection('')

        self.sections[-1].subsections[-1].add_subsection(SectionType.SUBSUBSECTION, section_name)


    def add_text_to_current_section(self, text_type, text):
        if not len(self.sections):
            self.add_section('')
        self.sections[-1].add_text_object(text_type, text)


    def add_reference(self, full_reference):
        self.references.append(Reference({'complete_ref_raw': full_reference}))


    def add_authors_text(self, full_authors):
        self.authors.append(Authors({'all_authors_text': full_authors}))


    def get_introduction(self):
        return self.get_sections_with_imrad_type(IMRaDType.INTRODUCTION)


    def get_background(self):
        return self.get_sections_with_imrad_type(IMRaDType.BACKGROUND)


    def get_methods(self):
        return self.get_sections_with_imrad_type(IMRaDType.METHODS)


    def get_results(self):
        return self.get_sections_with_imrad_type(IMRaDType.RESULTS)


    def get_discussion(self):
        return self.get_sections_with_imrad_type(IMRaDType.DISCUSSION)


    def save_file_to_path(self, path):
        open(path + self.filename, 'wb').write(self.file)
        return path + self.filename


    def title_exist(self):
        return bool(self.title_proceed)


    def section_title_exist(self):
        return any([section.title_exist() for section in self.sections])


    def section_text_exist(self):
        return any([section.text_exist() for section in self.sections])


    def subsection_title_exist(self):
        return any(subsection.title_exist() for section in self.sections for subsection in section.subsections)


    def subsection_text_exist(self):
        return any(subsection.text_exist() for section in self.sections for subsection in section.subsections)


    def subsubsection_title_exist(self):
        return any(subsubsection.title_exist() for section in self.sections for subsection in section.subsections
                   for subsubsection in subsection.subsections)


    def subsubsection_text_exist(self):
        return any(subsubsection.text_exist() for section in self.sections for subsection in section.subsections
                   for subsubsection in subsection.subsections)
