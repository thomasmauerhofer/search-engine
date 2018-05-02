#!/usr/bin/env python3
# encoding: utf-8
from engine.utils.string_utils import remove_single_digits, remove_citations, remove_special_chars, \
    remove_single_chars, remove_stopwords, stem_words, remove_multiple_spaces


class TextProcessor(object):
    def proceed(self, paper):
        for section in paper.sections:
            self.remove_stopwords_from_section(section)

        paper.sections = [section for section in paper.sections if len(section.subsections) or len(section.text)]


    def remove_stopwords_from_section(self, section):
        section.heading = self.proceed_string(section.heading.lower())

        for section_text in section.text:
            section_text[1] = self.proceed_string(section_text[1].lower())

        section.text = [text for text in section.text if len(text[1])]

        for subsection in section.subsections:
            self.remove_stopwords_from_section(subsection)


    def proceed_list(self, texts):
        return [self.proceed_string(text) for text in texts]


    @staticmethod
    def proceed_string(text):
        text = remove_single_digits(text)
        text = remove_citations(text)  # possible feature -> number of citations
        text = remove_special_chars(text)
        text = remove_single_chars(text)
        text = remove_stopwords(text)
        text = stem_words(text)
        text = remove_multiple_spaces(text)
        return text.strip()
