#!/usr/bin/env python3
# encoding: utf-8

import numpy as np
from backend.datastore.structure.section import IMRaDType
from backend.preprocessing.chapter_classifier.classifier_base import ClassifierBase


class ClassifierSimple(ClassifierBase):
    def __init__(self):
        self.ABSTRACT_TOKENS = ['abstract']
        self.INTRO_TOKENS = ['introduct']
        self.BACKGROUND_TOKENS = ['relat work', 'previou work', 'propos method', "background", 'backgorund', 'backgroundand', 'research', \
            'gener model', 'literatur review', 'develop measur', 'methodolog', 'resourc', 'execut summari']
        self.RESULT_TOKENS = ['evalu', 'result', 'analysi', 'comparison', 'experi', 'experiment']
        self.DISCUSSION_TOKENS = ['conclus', 'futur work', 'outlook', 'discuss']
        self.ACKNOWLEG_TOKENS = ['acknowledg']

    def predict_chapter(self, chapter_list):
        Y = []

        for chapter in chapter_list:
            Y.append(np.zeros(len(IMRaDType)))

            if any(token in chapter for token in self.ABSTRACT_TOKENS):
                Y[-1][IMRaDType.ABSTRACT.value] = 1

            if any(token in chapter for token in self.INTRO_TOKENS):
                Y[-1][IMRaDType.INDRODUCTION.value] = 1

            if any(token in chapter for token in self.RESULT_TOKENS):
                Y[-1][IMRaDType.RESULTS.value] = 1

            if any(token in chapter for token in self.DISCUSSION_TOKENS):
                Y[-1][IMRaDType.DISCUSSION.value] = 1

            if any(token in chapter for token in self.BACKGROUND_TOKENS):
                Y[-1][IMRaDType.BACKGROUND.value] = 1

            if any(token in chapter for token in self.ACKNOWLEG_TOKENS):
                Y[-1][IMRaDType.ACKNOWLEDGE.value] = 1

        return Y
