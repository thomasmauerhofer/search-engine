#!/usr/bin/env python3
# encoding: utf-8

from backend.datastore.structure.section import IMRaDType

def proceed(paper):
    __print_sections__(paper)

    for section in paper.sections:
        print(section)



#-------------------------------------------------------------------------------
def __print_sections__(paper):
    print('Sections:\n')
    for section in paper.sections:
        print(section.heading)
    print('\n\n')
