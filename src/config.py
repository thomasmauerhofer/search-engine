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


# classifier
HDF5 = CLASSIFIER_DATA
DATASET = CLASSIFIER_DATA + "dataset/"
THRESHOLD = 0.85


KEYS = REQ_DATA_PATH + "keys/"
