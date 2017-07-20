#!/usr/bin/env python3
# encoding: utf-8

import os
import tensorflow as tf
import numpy as np
from backend.datastore.structure.section import IMRaDType
from backend.preprocessing.chapter_classifier.classifier_nn import ClassifierNN
from backend.preprocessing.chapter_classifier.classifier_simple import ClassifierSimple

def proceed(paper):
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    chapter_names = [name.heading for name in paper.sections if not(name.heading.isspace() or name.heading is '')]
    if not len(chapter_names):
        return

    #classifier = ClassifierNN()
    classifier = ClassifierSimple()
    prob = classifier.predict_chapter(chapter_names)

    #tmp = np.round(prob, 3)
    for i in range(len(prob)):
        print("{0} {1}".format(chapter_names[i], prob[i]))
    print("\n\n")


#-------------------------------------------------------------------------------
def __print_sections__(paper):
    for section in paper.sections:
        if not section.heading.isspace():
            print(section.heading + ":" )
    print('\n')
