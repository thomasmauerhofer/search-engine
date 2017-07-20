#!/usr/bin/env python3
# encoding: utf-8

import numpy as np
from backend.datastore.structure.section import IMRaDType
from backend.preprocessing.chapter_classifier.classifier_base import ClassifierBase


class ClassifierSimple(ClassifierBase):

    def __init__(self):
        self.INTRO_TOKENS = ['introduct']
        self.BACKGROUND_TOKENS = ['relat work', 'previou work', 'propos method', "background", 'backgorund', 'backgroundand', 'research', \
            'gener model', 'literatur review', 'develop measur', 'methodolog', 'resourc', 'execut summari']
        #METHOD TOKENS not used by now
        self.METHOD_TOKENS = ['method', 'experi', 'algorithm', 'experiment', 'model', 'criteria', 'applic measur', 'architectur']
        self.RESULT_TOKENS = ['evalu', 'acknowledg', 'result', 'analysi', 'comparison']
        self.DISCUSSION_TOKENS = ['conclus', 'futur work', 'outlook', 'discuss']

    def predict_chapter(self, chapter_list):
        predictions = []

        for chapter in chapter_list:
            predictions.append([0, 0, 0, 0, 0])

            if any(token in chapter for token in self.INTRO_TOKENS):
                predictions[-1][IMRaDType.INDRODUCTION.value] = 1

            if any(token in chapter for token in self.RESULT_TOKENS):
                predictions[-1][IMRaDType.RESULTS.value] = 1

            if any(token in chapter for token in self.DISCUSSION_TOKENS):
                predictions[-1][IMRaDType.DISCUSSION.value] = 1

            if any(token in chapter for token in self.BACKGROUND_TOKENS):
                predictions[-1][IMRaDType.BACKGROUND.value] = 1

        # aditional rules:
        # if no Indroduction -> First Chapter is the Indroduction -> creates noise
        #if not any(prediction[0] == 1 for prediction in predictions):
        #    predictions[0][IMRaDType.INDRODUCTION.value] = 1

        # if no Background -> Background is in Indroduction
        if not any(prediction[1] == 1 for prediction in predictions):
            for prediction in predictions:
                if prediction[0] == 1:
                    prediction[IMRaDType.BACKGROUND.value] == 1


        # if no suitable token is found -> Have to be a method chapter
        for prediction in predictions:
            if not any(pred_class == 1 for pred_class in prediction):
                prediction[IMRaDType.METHODS.value] = 1

        return np.array(predictions)
