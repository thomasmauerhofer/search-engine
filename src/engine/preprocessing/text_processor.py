#!/usr/bin/env python3
# encoding: utf-8
from engine.utils.string_utils import remove_single_digits, remove_citations, remove_special_chars, \
    remove_single_chars, remove_stopwords, stem_words, remove_multiple_spaces


class TextProcessor(object):
    def proceed_paper(self, paper):
        paper.title_proceed = self.proceed_string(paper.title_raw)

        for section in paper.sections:
            self.proceed_section(section)

        paper.sections = [section for section in paper.sections if len(section.subsections) or len(section.text)]

        for reference in paper.references:
            reference.complete_ref_proceed = self.proceed_string(reference.complete_ref_raw)


    def proceed_section(self, section):
        section.heading_proceed = self.proceed_string(section.heading_raw)

        for text in section.text:
            text.text_proceed = self.proceed_string(text.text_raw)

        section.text = [text for text in section.text if len(text.text_proceed)]

        for subsection in section.subsections:
            self.proceed_section(subsection)


    def proceed_list(self, string_elements):
        return [self.proceed_string(element) for element in string_elements]


    @staticmethod
    def proceed_string(text):
        text = text.lower()
        text = remove_single_digits(text)
        text = remove_citations(text)  # possible feature -> number of citations
        text = remove_special_chars(text)
        text = remove_single_chars(text)
        text = remove_stopwords(text)
        text = stem_words(text)
        text = remove_multiple_spaces(text)
        return text.strip()
