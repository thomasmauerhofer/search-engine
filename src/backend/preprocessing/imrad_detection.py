#!/usr/bin/env python3
# encoding: utf-8

from backend.datastore.structure.section import IMRaDType

INDRODUCTION = ['introduction', 'related work', 'background']
METHODS = ['method', 'methods']
RESULTS = ['result', 'results', 'evaluation']
DISCUSSION = ['discussion']

def proceed(paper):
    __set_indroduction_in_paper__(paper)
    __set_methods_in_paper__(paper)
    __set_results_in_paper__(paper)
    __set_discussion_in_paper__(paper)

    print('IMRaD found for ' + paper.filename + '\n')
    print('INDRODUCTION: ' + paper.get_indroduction().heading + '\n')
    print('METHODS: ' + paper.get_methods().heading + '\n')
    print('RESULTS: ' + paper.get_results().heading + '\n')
    print('DISCUSSION: ' + paper.get_discussion().heading + '\n')


#-------------------------------------------------------------------------------
def __set_indroduction_in_paper__(paper):
    pos = __find_imrad_for_list__(paper, INDRODUCTION)

    if pos == -1:
        print('Cant find INDRODUCTION for paper: ' + paper.filename + '\n')
        __print_sections__(paper)
        exit(-1)
    else:
        paper.sections[pos].add_to_imrad(IMRaDType.INDRODUCTION)

#-------------------------------------------------------------------------------
def __set_methods_in_paper__(paper):
    pos = __find_imrad_for_list__(paper, METHODS)

    if pos == -1:
        print('Cant find METHODS for paper: ' + paper.filename + '\n')
        __print_sections__(paper)
        exit(-1)
    else:
        paper.sections[pos].add_to_imrad(IMRaDType.METHODS)

#-------------------------------------------------------------------------------
def __set_results_in_paper__(paper):
    pos = __find_imrad_for_list__(paper, RESULTS)

    if pos == -1:
        print('Cant find RESULTS for paper: ' + paper.filename + '\n')
        __print_sections__(paper)
        exit(-1)
    else:
        paper.sections[pos].add_to_imrad(IMRaDType.RESULTS)

#-------------------------------------------------------------------------------
def __set_discussion_in_paper__(paper):
    pos = __find_imrad_for_list__(paper, DISCUSSION)

    if pos == -1:
        print('Cant find DISCUSSION for paper: ' + paper.filename + '\n')
        __print_sections__(paper)
        exit(-1)
    else:
        paper.sections[pos].add_to_imrad(IMRaDType.DISCUSSION)

#-------------------------------------------------------------------------------
def __find_imrad_for_list__(paper, imrad_list):
    section_pos = -1

    for i in range(len(paper.sections)):
        heading = paper.sections[i].heading

        for j in range(len(imrad_list)):
            if imrad_list[j] in heading.lower():
                if (section_pos == -1) or (len(heading) < len(paper.sections[section_pos].heading)):
                    section_pos = i
                    #imrad_pos = j

    return section_pos

#-------------------------------------------------------------------------------
def __print_sections__(paper):
    print('Sections:\n')
    for section in paper.sections:
        print(section.heading)
    print('\n\n')
