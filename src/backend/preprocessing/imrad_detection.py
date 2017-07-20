#!/usr/bin/env python3
# encoding: utf-8

from backend.datastore.structure.section import IMRaDType
from backend.preprocessing.chapter_classifier.classifier_nn import ClassifierNN

def proceed(paper):
    classifier = ClassifierNN()
    # Todo with all chapters at same time!
    ret = classifier.predict_chapter('method implement')
    #__print_sections__(paper)

    #for section in paper.sections:
    #    print(section)



#-------------------------------------------------------------------------------
def __print_sections__(paper):
    for section in paper.sections:
        if not section.heading.isspace():
            print(section.heading + ":" )
    print('\n')
