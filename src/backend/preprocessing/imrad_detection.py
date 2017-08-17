#!/usr/bin/env python3
# encoding: utf-8

import os
import tensorflow as tf
import numpy as np
from backend.datastore.structure.section import IMRaDType
from backend.preprocessing.chapter_classifier.classifier_nn import ClassifierNN
from backend.preprocessing.chapter_classifier.classifier_simple import ClassifierSimple
from backend.utils.exceptions.import_exceptions import ClassificationException

def __get_classes_of_sections__(sections):
    ret = []
    pos = np.where(sections == 1)[0]
    for index in pos:
        ret.append("{:12}".format(IMRaDType(index).name))

    return ret

def proceed(paper):
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    chapter_names = [name.heading for name in paper.sections if not(name.heading.isspace() or name.heading is '')]
    if not len(chapter_names):
        return

    #classifierNN = ClassifierNN()
    classifierSimple = ClassifierSimple()

    #probNN = classifierNN.predict_chapter(chapter_names)
    try:
        probSimple = classifierSimple.predict_chapter(chapter_names)
    except ClassificationException as e:
        return

    #tmp = np.round(probNN, 3)
    #for i in range(len(probSimple)):
        #print("{:30}: ".format(chapter_names[i])

        #tmp = "{}: ".format(chapter_names[i].rstrip())
        #for bla in __get_classes_of_sections__(probSimple[i]):
            #tmp += bla.rstrip() + " "
        #print("{:30}: S: {} {} NN: {}".format(chapter_names[i], probSimple[i], __get_classes_of_sections__(probSimple[i]), tmp[i]))
        #print(tmp)
    #print("\n\n")


#-------------------------------------------------------------------------------
def __print_sections__(paper):
    for section in paper.sections:
        if not section.heading.isspace():
            print(section.heading + ":" )
    print('\n')
