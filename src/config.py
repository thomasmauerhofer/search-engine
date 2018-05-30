#!/usr/bin/env python3
# encoding: utf-8
import os

APP_PATH = os.path.abspath(os.path.dirname(__file__))
REQ_DATA_PATH = os.path.abspath(os.path.join(APP_PATH, os.pardir)) + "/data/"
CLASSIFIER_DATA = REQ_DATA_PATH + "classifier/"

# Fileupload params
UPLOAD_FOLDER = os.path.join(APP_PATH, "datastore/")
ALLOWED_EXTENSIONS = {'pdf'}

# importer
CREATE_OUTPUT = False
TEAMBEAM_EXE = '/home/thomas11/program/teambeam/bin/'
REFERENCE_SIMULARITY_THRESHOLD = 0.56

# classifier
HDF5 = CLASSIFIER_DATA
DATASET = CLASSIFIER_DATA + "dataset/"
THRESHOLD = 0.85

# ranking
USED_ALGORITHM = "tf-idf"

# keys
KEYS = REQ_DATA_PATH + "keys/"

# Ranked boolean retrial
WEIGHT_TITLE = 0.2
WEIGHT_SECTION_TITLE = 0.3
WEIGHT_SECTION_TEXT = 0.2
WEIGHT_SUBSECTION_TITLE = 0.18
WEIGHT_SUBSECTION_TEXT = 0.05
WEIGHT_SUBSUBSECTION_TITLE = 0.05
WEIGHT_SUBSUBSECTION_TEXT = 0.02
DEFAULT_EXTENDED = False

