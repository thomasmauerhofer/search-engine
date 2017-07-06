#!/usr/bin/env python3
# encoding: utf-8

from nltk.corpus import stopwords
from backend.utils.string_utils import remove_stopwords, remove_digits, remove_single_chars, remove_special_chars

def proceed(paper):
    #for section in paper.sections:
    #    print(section)

    for section in paper.sections:
        remove_stopwords_from_section(section)

    #for section in paper.sections:
    #    print(section)
    #print(proceed_string("A B+B C+CC DDDD EEEEE FFFFFF "))


def remove_stopwords_from_section(section):
    section.heading = proceed_string(section.heading)

    for section_text in section.text:
        section_text[1] = proceed_string(section_text[1])

    for subsection in section.subsections:
        remove_stopwords_from_section(subsection)

def proceed_string(text):
    #text = remove_digits(text)
    text = remove_single_chars(text)
    text = remove_special_chars(text)
    text = remove_stopwords(text)
    return text.strip()
