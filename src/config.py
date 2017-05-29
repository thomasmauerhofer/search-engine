#!/usr/bin/env python3
# encoding: utf-8
import os

#Fileupload params
UPLOAD_FOLDER = '/static/data/'
ALLOWED_EXTENSIONS = set(['pdf'])

#paths
app_path = os.path.abspath(os.path.dirname(__file__))
path_to_datastore = app_path + UPLOAD_FOLDER

path_to_teambeam_executable = '/home/thomas11/program/teambeam/bin/'
