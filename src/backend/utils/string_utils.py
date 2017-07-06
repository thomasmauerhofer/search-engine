#!/usr/bin/env python3
# encoding: utf-8

import re
from difflib import SequenceMatcher
from email.utils import parseaddr
from nltk.corpus import stopwords
from string import digits

# if there is an error as Resource 'corpora/stopwords' not found. Use:
# import nltk
# nltk.download('all-corpora')
pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')

remove_digits = str.maketrans('', '', digits)

def is_valid_email(email):
    return len(parseaddr(email)[1])

def remove_special_chars(text):
    return re.sub('[^A-Za-z0-9]+', '', text)

def longest_subsequence(str1, str2):
    s = SequenceMatcher(None, str1, str2)
    return s.find_longest_match(0, len(str1), 0, len(str2))

def remove_stopwords(text):
    return pattern.sub('', text.lower())

def remove_digits(text):
    return re.sub('\d+', '', text)

def remove_single_chars(text):
    return re.sub(r'\b\w{1,1}\b', '', text)

def remove_special_chars(text):
    return re.sub(r'([^\s\w]|_)+', '', text)
