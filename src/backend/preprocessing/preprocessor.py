#!/usr/bin/env python3
# encoding: utf-8

from backend.preprocessing.imrad_detection import IMRaDDetection
import backend.preprocessing.text_processing as text_processing


class Preprocessor(object):
    def __init__(self):
        self.imrad_detector = IMRaDDetection()

    def proceed_paper(self, paper):
        text_processing.proceed(paper)
        success = self.imrad_detector.proceed(paper)
        return success
