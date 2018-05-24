#!/usr/bin/env python3
# encoding: utf-8

import os
import pprint
import re

from config import REQ_DATA_PATH
from engine.api import API
from engine.datastore.structure.section import IMRaDType
from engine.datastore.structure.text import TextType


def __check_citations_to_references(citations, references):
    last_cited = 0
    for citation in citations:
        regex = re.compile(r'(.*?)\[([0-9]+[–,\-]?[0-9]*)\]')
        values = re.match(regex, citation["full_citation"])
        index = values.group(2)

        if re.match(r'[0-9]+[–,\-][0-9]+', index):
            start, end = re.split("[–,\\-]", index)
        else:
            end = index

        last_cited = int(end) if int(end) > last_cited else last_cited

    # Highest reference should be cited -> No missing references
    return len(references) == last_cited


def __get_citations(filename, sections):
    citations = []

    for section in sections:
        for text in section.text:
            if text.text_type == TextType.MAIN:
                sentences = text.text_raw.split("\n")
                for sentence in sentences:
                    # There are two possible formats of citations:
                    # text [1] text
                    # text [1] text [2]
                    if sentence.count("[") > 1:
                        regex = re.compile(r'.*?\[[0-9]+[–,\-]?[0-9]*\]')
                    else:
                        regex = re.compile(r'.*?\[[0-9]+[–,\-]?[0-9]*\].*')

                    citation_texts = re.findall(regex, sentence)

                    if citation_texts:
                        values = [{"filename": filename, "full_citation": value, "references": [],
                                   "section": {"name": section.heading_raw.strip(),
                                               "imrad": [imrad.name for imrad in section.imrad_types]}}
                                  for value in citation_texts]
                        citations.extend(values)

        citations.extend(__get_citations(filename, section.subsections))
    return citations


def create_file():
    api = API()
    all_citations = []

    for paper in api.get_all_paper():
        if not any([ref.paper_id for ref in paper.references]):
            continue

        citations = []
        citations.extend(__get_citations(paper.filename, paper.get_sections_with_imrad_type(IMRaDType.ABSTRACT)))
        citations.extend(__get_citations(paper.filename, paper.get_sections_with_imrad_type(IMRaDType.INTRODUCTION)))
        citations.extend(__get_citations(paper.filename, paper.get_sections_with_imrad_type(IMRaDType.BACKGROUND)))
        citations.extend(__get_citations(paper.filename, paper.get_sections_with_imrad_type(IMRaDType.METHODS)))
        citations.extend(__get_citations(paper.filename, paper.get_sections_with_imrad_type(IMRaDType.RESULTS)))
        citations.extend(__get_citations(paper.filename, paper.get_sections_with_imrad_type(IMRaDType.DISCUSSION)))
        citations.extend(__get_citations(paper.filename, paper.get_sections_with_imrad_type(IMRaDType.ACKNOWLEDGE)))

        if not len(citations) or not len(paper.references): #or not __check_citations_to_references(citations, paper.references):
            continue

        for citation in citations:
            regex = re.compile(r'(.*?)\[([0-9]+[–,\-]?[0-9]*)\](.*)')
            values = re.match(regex, citation["full_citation"])
            citation["search_query"] = values.group(1)

            if values.group(3) and values.group(3) != ".":
                citation["search_query"] += " " + values.group(3)

            index = values.group(2)

            indices = []
            if re.match(r'[0-9]+[–,\-][0-9]+', index):
                start, end = re.split("[–,\\-]", index)
                indices.extend(range(int(start) - 1, int(end)))
            else:
                indices.append(int(index) - 1)

            for i in indices:
                if i < len(paper.references) and paper.references[i].paper_id != '':
                    citation["references"].append({"complete": paper.references[i].complete_ref_raw,
                                                   "paper_id": str(paper.references[i].paper_id)})

        for citation in citations:
            if len(citation["search_query"]) > 2 and citation["references"]:
                all_citations.append(citation)



    file1 = open(os.path.join(REQ_DATA_PATH, "citations.txt"), "w")
    file2 = open(os.path.join(REQ_DATA_PATH, "citations_pprint.txt"), "w")

    file1.write(str(all_citations))
    file1.close()
    file2.write(pprint.pformat(all_citations))
    file2.close()
    print("{} citations saved!".format(len(all_citations)))


if __name__ == "__main__":
    create_file()
