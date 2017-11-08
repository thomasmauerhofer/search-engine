#!/usr/bin/env python3
# encoding: utf-8

import numpy as np
from config import threshold
from backend.datastore.structure.section import IMRaDType
from backend.preprocessing.chapter_classifier.classifier_nn import ClassifierNN
from backend.preprocessing.chapter_classifier.classifier_simple import ClassifierSimple


class IMRaDDetection(object):
    def __init__(self):
        self.classifierNN = ClassifierNN()
        self.classifierSimple = ClassifierSimple()

    def __print_chapters_and_values__(self, chapter_names, Y):
        for i in range(len(chapter_names)):
            tmp = np.round(Y[i], 3)
            print("{:30}: {}".format(chapter_names[i], tmp))

    def __set_section_in_paper__(self, paper, positions, imrad_type):
        for pos in positions:
            paper.sections[pos].add_to_imrad(imrad_type)

    def proceed(self, paper):
        chapter_names = [name.heading for name in paper.sections]
        if not len(chapter_names):
            return False

        Y = self.classifierNN.predict_chapter(chapter_names)
        Y_simple = self.classifierSimple.predict_chapter(chapter_names)

        # self.__print_chapters_and_values__(chapter_names, Y)

        # additional rules:
        # INTRO have to be in the set:
        intro = np.array([x[IMRaDType.INDRODUCTION.value] for x in Y])
        intro_pos = np.where(intro >= threshold)[0]

        if not len(intro_pos):
            intro = np.array([x[IMRaDType.INDRODUCTION.value] for x in Y_simple])
            intro_pos = np.where(intro >= threshold)[0]

        if not len(intro_pos):
            return False
        else:
            self.__set_section_in_paper__(paper, intro_pos, IMRaDType.INDRODUCTION)

        # if no Background -> Background is in Indroduction
        background = np.array([x[IMRaDType.BACKGROUND.value] for x in Y])
        background_pos = np.where(background >= threshold)[0]
        if not len(background_pos):
            background_pos = intro_pos

        self.__set_section_in_paper__(paper, background_pos, IMRaDType.BACKGROUND)

        # ABSTRACT
        abstract = np.array([x[IMRaDType.ABSTRACT.value] for x in Y])
        abstract_pos = np.where(abstract >= threshold)[0]
        self.__set_section_in_paper__(paper, abstract_pos, IMRaDType.ABSTRACT)

        # ACKNOWLEDGE
        acknowledge = np.array([x[IMRaDType.ACKNOWLEDGE.value] for x in Y])
        acknowledge_pos = np.where(acknowledge >= threshold)[0]
        self.__set_section_in_paper__(paper, acknowledge_pos, IMRaDType.ACKNOWLEDGE)

        # DISCUSSION or RESULT have to be in the set
        discussion = np.array([x[IMRaDType.DISCUSSION.value] for x in Y])
        discussion_pos = np.where(discussion >= threshold)[0]
        self.__set_section_in_paper__(paper, discussion_pos, IMRaDType.DISCUSSION)

        result = np.array([x[IMRaDType.RESULTS.value] for x in Y])
        result_pos = np.where(result >= threshold)[0]
        self.__set_section_in_paper__(paper, result_pos, IMRaDType.RESULTS)

        # DISCUSSION and RESULT not set - Try simple classification
        if not len(list(discussion_pos) + list(result_pos)):
            discussion_pos = np.where(intro >= threshold)[0]
            self.__set_section_in_paper__(paper, discussion_pos, IMRaDType.DISCUSSION)

            result_pos = np.where(intro >= threshold)[0]
            self.__set_section_in_paper__(paper, result_pos, IMRaDType.RESULTS)

        if not len(list(discussion_pos) + list(result_pos)):
            return False

        disc_res_max = max(list(discussion_pos) + list(result_pos))
        indro_min = min(list(intro_pos))

        # Intro have to be before result/discussion...
        if disc_res_max <= indro_min:
            return False

        # Unset chapters between INTRO and DISCUSSION/RESULT are methods
        for pos in np.arange(indro_min + 1, disc_res_max):
            if not len(paper.sections[pos].imrad_types):
                paper.sections[pos].add_to_imrad(IMRaDType.METHODS)

        return True
