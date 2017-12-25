#!/usr/bin/env python3
# encoding: utf-8

from backend.utils.string_utils import remove_stopwords, remove_single_digits, remove_single_chars, \
    remove_special_chars, remove_citations, remove_multiple_spaces, stem_words


class TextProcessor(object):
    def proceed(self, paper):
        for section in paper.sections:
            self.remove_stopwords_from_section(section)

        paper.sections = [section for section in paper.sections if len(section.subsections) or len(section.text)]

    def remove_stopwords_from_section(self, section):
        section.heading = self.proceed_string(section.heading.lower())
        section.text = [text for text in section.text if len(text[1])]

        for section_text in section.text:
            proceed_text = self.proceed_string(section_text[1].lower())

            if proceed_text:
                section_text[1] = proceed_text
            else:
                section.text.remove(section_text)

        for subsection in section.subsections:
            self.remove_stopwords_from_section(subsection)

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
