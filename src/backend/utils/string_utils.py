#!/usr/bin/env python3
# encoding: utf-8

import re
from difflib import SequenceMatcher
from email.utils import parseaddr

def is_valid_email(email):
    return len(parseaddr(email)[1])

def remove_special_chars(text):
    return re.sub('[^A-Za-z0-9]+', '', text)

def longest_subsequence(str1, str2):
    s = SequenceMatcher(None, str1, str2)
    return s.find_longest_match(0, len(str1), 0, len(str2))
