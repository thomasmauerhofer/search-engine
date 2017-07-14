#!/usr/bin/env python3
# encoding: utf-8

import re
from difflib import SequenceMatcher
from email.utils import parseaddr
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from string import digits

# if there is an error as Resource 'corpora/stopwords' not found. Use:
# import nltk
# nltk.download('all-corpora')
pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')

stemmer = PorterStemmer()

def is_valid_email(email):
    return len(parseaddr(email)[1])

def longest_subsequence(str1, str2):
    s = SequenceMatcher(None, str1, str2)
    return s.find_longest_match(0, len(str1), 0, len(str2))

def stem_words(text):
    tmp = [stemmer.stem(i) for i in word_tokenize(text)]
    return " ".join(tmp)

def remove_stopwords(text):
    return pattern.sub('', text.lower())

def remove_single_digits(text):
    return re.sub(r'\b\d+\b', '', text)

def remove_single_chars(text):
    return re.sub(r'\b\w{1,1}\b', '', text)

def remove_special_chars(text):
    return re.sub(r'([^\s\w]|_)+', '', text)

def remove_citations(text):
    return re.sub(r'\[\d+[\,\d+]*]+', '', text)

def remove_multiple_spaces(text):
    return re.sub(r'\s\s+', ' ', text)
