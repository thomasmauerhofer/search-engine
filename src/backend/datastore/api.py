#!/usr/bin/env python3
# encoding: utf-8

from backend.importer.importer_teambeam import ImporterTeambeam
from backend.preprocessing.preprocessor import proceed_paper
from config import ALLOWED_EXTENSIONS

def allowed_upload_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_paper(filename):
    if not allowed_upload_file(filename):
        return False

    importer = ImporterTeambeam()
    paper = importer.import_paper(filename)
    valid_paper = proceed_paper(paper)

    if not valid_paper:
        return False

    for section in paper.sections:
        out = section.heading + " "
        for imrad in section.imrad_types:
            out += imrad.name + " "
        print(out)
    #ToDo: Import paper into database
