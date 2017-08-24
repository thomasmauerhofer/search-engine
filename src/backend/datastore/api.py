#!/usr/bin/env python3
# encoding: utf-8

from backend.importer.importer_teambeam import ImporterTeambeam
from backend.preprocessing.preprocessor import proceed_paper
from backend.datastore.db_client import DBClient
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


    #for section in paper.sections:
    #    out = section.heading + " "
    #    for imrad in section.imrad_types:
    #        out += imrad.name + " "
    #    print(out)
    #ToDo: Import paper into database
    client = DBClient()
    client.add_paper(paper)
    #599d72126919df1f68e8b6b0
