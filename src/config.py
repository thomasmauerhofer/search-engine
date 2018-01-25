#!/usr/bin/env python3
# encoding: utf-8
import os

# Fileupload params
STATIC_FOLDER = 'static/'
UPLOAD_FOLDER = STATIC_FOLDER + 'data/'

ALLOWED_EXTENSIONS = {'pdf'}

# paths
app_path = os.path.abspath(os.path.dirname(__file__))
path_to_datastore = os.path.join(app_path, UPLOAD_FOLDER)

# importer
create_output = False
path_to_teambeam_executable = '/home/thomas11/program/teambeam/bin/'
path_to_teambeam_executable_windows = 'D:/MongoDB/teambeam/bin/'


# classifier
path_to_hdf5 = app_path + "/" + UPLOAD_FOLDER + "classifier/"
path_to_dataset = app_path + "/" + UPLOAD_FOLDER + "classifier/dataset/"
threshold = 0.85

# keys - WARNING: They should be on a save place, if you want to use this application online!
SESSION_KEY = '04ccc6a312869b83ad9d010789675539690ac658ff6b5ab0ee8ecbc4668e16ee' \
              'b2fa65e4d2f80e8710160b23593ab71265afbd4efba766f4fbbd0d8b443b89f5'
SHA3_KEY = 'bfb3f1338918940a009f6c84171eb85a'
