#!/usr/bin/env python3
# encoding: utf-8

import backend.preprocessing.imrad_detection as imrad_detection
import backend.preprocessing.keyword_detection as keyword_detection

def proceed_paper(paper):
    imrad_detection.proceed(paper)
    keyword_detection.proceed(paper)
