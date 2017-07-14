#!/usr/bin/env python3
# encoding: utf-8

from backend.utils.string_utils import remove_stopwords, remove_single_digits, remove_single_chars, remove_special_chars, remove_citations, remove_multiple_spaces, stem_words

def proceed(paper):
    for section in paper.sections:
        remove_stopwords_from_section(section)

    paper.sections = [section for section in paper.sections if len(section.subsections) or len(section.text)]

def remove_stopwords_from_section(section):
    section.heading = proceed_string(section.heading.lower())

    for section_text in section.text:
        section_text[1] = proceed_string(section_text[1].lower())

    for subsection in section.subsections:
        remove_stopwords_from_section(subsection)

    section = [text for text in section.text if len(text[1])]

def proceed_string(text):
    text = remove_single_digits(text)
    text = remove_citations(text)
    text = remove_special_chars(text)
    text = remove_single_chars(text)
    text = remove_stopwords(text)
    text = stem_words(text)
    text = remove_multiple_spaces(text)
    return text.strip()
