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
TEAMBEAM_EXE_WIN = 'D:/MongoDB/teambeam/bin/'


# classifier
HDF5 = CLASSIFIER_DATA
DATASET = CLASSIFIER_DATA + "dataset/"
THRESHOLD = 0.85

# keys - WARNING: They should be on a save place, if you want to use this application online!
SESSION_KEY = '04ccc6a312869b83ad9d010789675539690ac658ff6b5ab0ee8ecbc4668e16ee' \
              'b2fa65e4d2f80e8710160b23593ab71265afbd4efba766f4fbbd0d8b443b89f5'
SHA3_KEY = 'bfb3f1338918940a009f6c84171eb85a'
