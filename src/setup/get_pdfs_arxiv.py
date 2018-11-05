#!/usr/bin/env python3
# encoding: utf-8

from engine.api import API

api = API()
print("Start")
papers = api.get_all_paper()

for paper in papers:
    for section in paper.sections:
        for subsection in section.subsections:
            for imrad in section.imrad_types:
                print("blaa")
