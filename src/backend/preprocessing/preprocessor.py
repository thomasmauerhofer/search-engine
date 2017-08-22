#!/usr/bin/env python3
# encoding: utf-8

import backend.preprocessing.imrad_detection as imrad_detection
import backend.preprocessing.text_processing as text_processing

def proceed_paper(paper):
    text_processing.proceed(paper)
    return imrad_detection.proceed(paper)
