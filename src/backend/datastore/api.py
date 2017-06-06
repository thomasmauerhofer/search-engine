#!/usr/bin/env python3
# encoding: utf-8

from backend.importer.importer_teambeam import ImporterTeambeam
from config import ALLOWED_EXTENSIONS

def add_paper(filename):
	if allowed__upload_file(filename):
		importer = ImporterTeambeam()
		importer.import_paper(filename)

def allowed__upload_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
