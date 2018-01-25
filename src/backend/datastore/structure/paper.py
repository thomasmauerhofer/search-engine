#!/usr/bin/env python3
# encoding: utf-8
import pprint
from backend.utils.objects.word_hist import WordHist
from backend.datastore.structure.paper_structure import PaperStructure
from backend.datastore.structure.reference import Reference
from backend.datastore.structure.section import Section, SectionType, TextType, IMRaDType
from backend.datastore.structure.author import Authors
from config import path_to_datastore


class Paper(PaperStructure):
    def __init__(self, data):
        self.filename = data.get('filename')
        self.title = data.get('title') if 'title' in data else ''
        self.id = data.get('_id') if '_id' in data else ''
        self.file = data.get('file') if 'file' in data else open(path_to_datastore + self.filename, "rb").read()

        self.authors = [Authors(author) for author in data.get('authors')] if 'authors' in data else []
        self.sections = [Section(section) for section in data.get('sections')] if 'sections' in data else []
        self.references = [Reference(reference) for reference in data.get('references')] if 'references' in data else []

        self.word_hist = WordHist(data.get('word_hist')) if "word_hist" in data else WordHist()


    def __str__(self):
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pformat(self.to_dict())


    def to_dict(self):
        data = {'filename': self.filename, 'title': self.title, 'file': self.file, 'authors': [], 'sections': [],
                'references': [], 'word_hist': self.word_hist}

        for author in self.authors:
            data['authors'].append(author.to_dict())
        for section in self.sections:
            data['sections'].append(section.to_dict())
        for reference in self.references:
            data['references'].append(reference.to_dict())

        return data


    def get_combined_word_hist(self):
        if not self.word_hist:
            for word in self.title.split():
                word = word.replace('.', " ")
                self.word_hist[word] = self.word_hist[word] + 1 if word in self.word_hist else 1

            for section in self.sections:
                self.word_hist.append(section.get_combined_word_hist())

        return WordHist(self.word_hist.copy())


    def set_title(self, title):
        if title is not '':
            self.title = title


    def add_abstract(self, text):
        self.sections.append(Section({'section_type': SectionType.ABSTRACT.name, 'heading': 'abstract'}))
        self.sections[-1].imrad_types.append(IMRaDType.ABSTRACT)
        self.add_text_to_current_section(TextType.MAIN, text)


    def add_section(self, section_name):
        self.sections.append(Section({'section_type': SectionType.SECTION.name, 'heading': section_name}))


    def add_subsection(self, section_name):
        if not len(self.sections):
            self.add_section('')

        self.sections[-1].add_subsection(SectionType.SUBSECTION, section_name)


    def add_subsubsection(self, section_name):
        if not len(self.sections):
            self.add_section('')

        if not len(self.sections[-1].subsections):
            self.add_subsection('')

        self.sections[-1].subsections[-1].add_subsection(SectionType.SUBSUBSECTION, section_name)


    def add_text_to_current_section(self, text_type, text):
        if not len(self.sections):
            self.add_section('')

        self.sections[-1].add_text_object(text_type, text)


    def add_reference(self, full_reference):
        self.references.append(Reference({'complete_reference': full_reference}))


    def add_authors_text(self, full_authors):
        self.authors.append(Authors({'all_authors_text': full_authors}))


    def get_sections_with_imrad_type(self, imrad_type):
        imrad_type = IMRaDType[imrad_type] if isinstance(imrad_type, str) else imrad_type
        return [chapter for chapter in self.sections if imrad_type in chapter.imrad_types]


    def get_indroduction(self):
        return self.get_sections_with_imrad_type(IMRaDType.INDRODUCTION)


    def get_methods(self):
        return self.get_sections_with_imrad_type(IMRaDType.METHODS)


    def get_results(self):
        return self.get_sections_with_imrad_type(IMRaDType.RESULTS)


    def get_discussion(self):
        return self.get_sections_with_imrad_type(IMRaDType.DISCUSSION)


    def get_ranking(self, queries):
        paper_rank = 0.0
        for imrad_type, query in queries.items():
            if "whole-document":
                ranking, key_value = self.word_hist.get_normalized_query_value(query)
                paper_rank += ranking
            else:
                # Only sections of the imrad_type influence the ranking
                raking_hist = WordHist()
                sections = self.get_sections_with_imrad_type(imrad_type)
                for section in sections:
                    raking_hist.append(section.get_combined_word_hist())

                ranking, key_value = raking_hist.get_normalized_query_value(query)
                paper_rank += ranking

        return paper_rank


    def save_file_to_path(self, path):
        open(path + self.filename, 'wb').write(self.file)
        return path + self.filename

