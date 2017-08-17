#!/usr/bin/env python3
# encoding: utf-8

import numpy as np
from backend.datastore.structure.section import IMRaDType
from backend.preprocessing.chapter_classifier.classifier_base import ClassifierBase
from backend.utils.exceptions.import_exceptions import ClassificationException


class ClassifierSimple(ClassifierBase):

    def __init__(self):
        self.ABSTRACT_TOKENS = ['abstract']
        self.INTRO_TOKENS = ['introduct']
        self.BACKGROUND_TOKENS = ['relat work', 'previou work', 'propos method', "background", 'backgorund', 'backgroundand', 'research', \
            'gener model', 'literatur review', 'develop measur', 'methodolog', 'resourc', 'execut summari']
        self.RESULT_TOKENS = ['evalu', 'result', 'analysi', 'comparison', 'experi', 'experiment']
        self.DISCUSSION_TOKENS = ['conclus', 'futur work', 'outlook', 'discuss']
        self.ACKNOWLEG_TOKENS = ['acknowledg']

    def __get_index_of_imrad_chapter__(self, predictions, imrad_type):
        prediction = np.array([x[imrad_type.value] for x in predictions])

        if imrad_type == IMRaDType.INDRODUCTION:
            return np.where(prediction == prediction.max())[0].min()
        else:
            return np.where(prediction == prediction.max())[0].max()

    def predict_chapter(self, chapter_list):
        predictions = []
        result_discussion = []

        for chapter in chapter_list:
            predictions.append(np.zeros(len(IMRaDType)))

            if any(token in chapter for token in self.ABSTRACT_TOKENS):
                predictions[-1][IMRaDType.ABSTRACT.value] = 1

            if any(token in chapter for token in self.INTRO_TOKENS):
                predictions[-1][IMRaDType.INDRODUCTION.value] = 1

            if any(token in chapter for token in self.RESULT_TOKENS):
                predictions[-1][IMRaDType.RESULTS.value] = 1

            if any(token in chapter for token in self.DISCUSSION_TOKENS):
                predictions[-1][IMRaDType.DISCUSSION.value] = 1

            if any(token in chapter for token in self.BACKGROUND_TOKENS):
                predictions[-1][IMRaDType.BACKGROUND.value] = 1

            if any(token in chapter for token in self.ACKNOWLEG_TOKENS):
                predictions[-1][IMRaDType.ACKNOWLEDGE.value] = 1

        # aditional rules:
        # INTRO have to be in the set
        if not any(prediction[IMRaDType.INDRODUCTION.value] == 1 for prediction in predictions):
            raise ClassificationException('Indroduction is not present')

        # if no Background -> Background is in Indroduction
        if not any(prediction[IMRaDType.BACKGROUND.value] == 1 for prediction in predictions):
            for prediction in predictions:
                if prediction[IMRaDType.INDRODUCTION.value] == 1:
                    prediction[IMRaDType.BACKGROUND.value] == 1

        if any(prediction[IMRaDType.DISCUSSION.value] == 1 for prediction in predictions):
            result_discussion.append(self.__get_index_of_imrad_chapter__(predictions, IMRaDType.DISCUSSION))

        if any(prediction[IMRaDType.RESULTS.value] == 1 for prediction in predictions):
            result_discussion.append(self.__get_index_of_imrad_chapter__(predictions, IMRaDType.RESULTS))

        # DISCUSSION or RESULT have to be in the set
        if not result_discussion:
            raise ClassificationException('Discussion or Results are not present')

        start = self.__get_index_of_imrad_chapter__(predictions, IMRaDType.INDRODUCTION)
        end = min(result_discussion)

        # Intro have to be before result/discussion...
        if end <= start:
            raise ClassificationException('Intro have to be before result/discussion')

        # Unset chapters between INTRO and DISCUSSION/RESULT are methods
        for i in range(start + 1, end):
            prediction = predictions[i]
            if not any(pred_class == 1 for pred_class in prediction):
                prediction[IMRaDType.METHODS.value] = 1

        return np.array(predictions)
