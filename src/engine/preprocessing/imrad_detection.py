#!/usr/bin/env python3
# encoding: utf-8

import numpy as np

from config import THRESHOLD
from engine.datastore.structure.section import IMRaDType
from engine.preprocessing.chapter_classifier.classifier_nn import ClassifierNN
from engine.preprocessing.chapter_classifier.classifier_simple import ClassifierSimple
from engine.utils.exceptions.import_exceptions import ClassificationError


class IMRaDDetection(object):
    def __init__(self):
        self.classifierNN = ClassifierNN()
        self.classifierSimple = ClassifierSimple()


    @staticmethod
    def __print_chapters_and_values(chapter_names, y):
        for i in range(len(chapter_names)):
            tmp = np.round(y[i], 3)
            print("{:30}: {}".format(chapter_names[i], tmp))


    @staticmethod
    def __set_section_in_paper(paper, positions, imrad_type):
        for pos in positions:
            paper.sections[pos].add_to_imrad(imrad_type)


    def proceed(self, paper):
        chapter_names = [name.heading for name in paper.sections]
        if not len(chapter_names):
            raise ClassificationError("Chapters can't be extracted from pdf-file.")

        imrad, all_pos = self.proceed_chapters(chapter_names)

        # INTRO have to be in the set:
        if not len(imrad[IMRaDType.INDRODUCTION]):
            raise ClassificationError("Introduction can't be extracted from pdf-file.")

        if not len(imrad[IMRaDType.DISCUSSION]) and not len(imrad[IMRaDType.RESULTS]):
            raise ClassificationError("Discussion and Results can't be extracted from pdf-file.")

        for imrad_type, chapters in imrad.items():
            self.__set_section_in_paper(paper, chapters, imrad_type)


    def proceed_chapters(self, chapters):
        imrad = {IMRaDType.METHODS: []}
        all_pos = []

        y = self.classifierNN.predict_chapter(chapters)
        y_simple = self.classifierSimple.predict_chapter(chapters)

        intro = np.array([x[IMRaDType.INDRODUCTION.value] for x in y])
        intro_pos = np.where(intro >= THRESHOLD)[0]

        if not len(intro_pos):
            intro = np.array([x[IMRaDType.INDRODUCTION.value] for x in y_simple])
            intro_pos = np.where(intro >= THRESHOLD)[0]

        imrad[IMRaDType.INDRODUCTION] = intro_pos
        all_pos.extend(intro_pos)


        # if no Background -> Background is in Indroduction
        background = np.array([x[IMRaDType.BACKGROUND.value] for x in y])
        background_pos = np.where(background >= THRESHOLD)[0]
        if not len(background_pos):
            background_pos = intro_pos

        imrad[IMRaDType.BACKGROUND] = background_pos
        all_pos.extend(background_pos)


        abstract = np.array([x[IMRaDType.ABSTRACT.value] for x in y])
        abstract_pos = np.where(abstract >= THRESHOLD)[0]
        imrad[IMRaDType.ABSTRACT] = abstract_pos
        all_pos.extend(abstract_pos)


        acknowledge = np.array([x[IMRaDType.ACKNOWLEDGE.value] for x in y])
        acknowledge_pos = np.where(acknowledge >= THRESHOLD)[0]
        imrad[IMRaDType.ACKNOWLEDGE] = acknowledge_pos
        all_pos.extend(acknowledge_pos)


        discussion = np.array([x[IMRaDType.DISCUSSION.value] for x in y])
        discussion_pos = np.where(discussion >= THRESHOLD)[0]

        result = np.array([x[IMRaDType.RESULTS.value] for x in y])
        result_pos = np.where(result >= THRESHOLD)[0]


        if not len(list(discussion_pos) + list(result_pos)):
            discussion_pos = np.where(intro >= THRESHOLD)[0]
            result_pos = np.where(intro >= THRESHOLD)[0]

        imrad[IMRaDType.DISCUSSION] = discussion_pos
        all_pos.extend(discussion_pos)

        imrad[IMRaDType.RESULTS] = result_pos
        all_pos.extend(result_pos)

        if not len(discussion_pos) or not len(result_pos) or not len(intro_pos):
            return imrad, all_pos

        disc_res_max = max(list(discussion_pos) + list(result_pos))
        intro_min = min(list(intro_pos))

        # Unset chapters between INTRO and DISCUSSION/RESULT are methods
        for pos in np.arange(intro_min + 1, disc_res_max):
            if pos not in all_pos:
                imrad[IMRaDType.METHODS].append(pos)

        return imrad, all_pos
