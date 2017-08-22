#!/usr/bin/env python3
# encoding: utf-8
import os

#Fileupload params
STATIC_FOLDER = 'static/'
UPLOAD_FOLDER = STATIC_FOLDER + 'data/'

ALLOWED_EXTENSIONS = set(['pdf'])

#paths
app_path = os.path.abspath(os.path.dirname(__file__))
path_to_datastore = app_path + "/" + UPLOAD_FOLDER

#importer
create_output = False
path_to_teambeam_executable = '/home/thomas11/program/teambeam/bin/'

#classifier
path_to_hdf5 = app_path + "/" + STATIC_FOLDER + "classifier/"
path_to_dataset = app_path + "/" + STATIC_FOLDER + "classifier/dataset/"
threshold = 0.85
