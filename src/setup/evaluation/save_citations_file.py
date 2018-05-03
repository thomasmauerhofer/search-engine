#!/usr/bin/env python3
# encoding: utf-8

import os
import pprint
from xml.dom import minidom

import re

from config import TEAMBEAM_EXE, REQ_DATA_PATH
from engine.preprocessing.imrad_detection import IMRaDDetection
from engine.preprocessing.text_processor import TextProcessor

EXTENSION_TEXT = ".txt"
EXTENSION_STRUCTURE = ".xml"


def create_file(folder):
    chapter_detection = IMRaDDetection()
    text_processor = TextProcessor()
    all_citations = []

    #  files = ["Stonebraker, Çetintemel, Zdonik - 2005 - The 8 requirements of real-time stream processing.pdf"]
    for filename in os.listdir(os.path.abspath(folder)):
        if not filename.endswith('.pdf'):
            continue

        file_path = folder + filename
        print(filename)
        if not (os.path.exists(file_path + EXTENSION_TEXT) and os.path.exists(file_path + EXTENSION_STRUCTURE)):
            os.system('cd ' + TEAMBEAM_EXE + ' &&  sh pdf-to-xml -a \"' + file_path + '\"')

        with open(file_path + EXTENSION_TEXT, "r", encoding="utf8") as textfile:
            data = textfile.read()

        tree = minidom.parse(file_path + EXTENSION_STRUCTURE)
        features = tree.getElementsByTagName("feature")

        references = []
        citations = []
        sections = ["NO SECTION"]
        for feature in features:
            value = feature.getAttribute("value").strip()

            parent = feature.parentNode
            start = int(parent.getAttribute("start"))
            end = int(parent.getAttribute("end"))
            text = data[start:end].strip()

            if value == "main":
                sentences = text.split("\n")
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
                        citations.extend([{"filename": filename, "full_citation": value, "references": [],
                                           "section": sections[-1]} for value in citation_texts])

            elif value == "reference":
                references.append(text)

            elif value == "section":
                sections.append(text)

        if not len(citations) or not len(references):
            continue

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
        if len(references) != last_cited:
            print("NOPE: {}, {}".format(len(references), last_cited))
            continue


        imrad, all_chapters = chapter_detection.proceed_chapters(text_processor.proceed_list(sections))

        sections = [{"name": name, "imrad": []} for name in sections]
        for imrad_type, chapters in imrad.items():
            for pos in chapters:
                sections[pos]["imrad"].append(imrad_type.name)


        for citation in citations:
            citation["section"] = [section for section in sections if citation["section"] == section["name"]]

            regex = re.compile(r'(.*?)\[([0-9]+[–,\-]?[0-9]*)\](.*)')
            values = re.match(regex, citation["full_citation"])
            citation["search_query"] = values.group(1)

            if values.group(3) and values.group(3) != ".":
                citation["search_query"] += " " + values.group(3)

            index = values.group(2)

            if re.match(r'[0-9]+[–,\-][0-9]+', index):
                start, end = re.split("[–,\\-]", index)
                for i in range(int(start) - 1, int(end)):
                    citation["references"].append(references[i])
            else:
                citation["references"].append(references[int(index) - 1])

        for citation in citations:
            if len(citation["search_query"]) > 2:
                all_citations.append(citation)


    file1 = open(os.path.join(REQ_DATA_PATH, "citations.txt"), "w")
    file2 = open(os.path.join(REQ_DATA_PATH, "citations_pprint.txt"), "w")

    file1.write(str(all_citations))
    file1.close()
    file2.write(pprint.pformat(all_citations))
    file2.close()


if __name__ == "__main__":
    create_file("/media/thomas11/ad34827c-b739-48f3-87bc-98e376545686/thesis/all_data/data/")
