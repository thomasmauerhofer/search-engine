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

admin_user = 'admin'
admin_password = '1Mxq4/idC6Y/WNCbyGychtTMauP4nQumP1jQm8hsnIbUzGrj+J0Lpj9Y0JvIb' \
                'JyG1Mxq4/idC6Y/WNCbyGychtTMauP4nQumP1jQm8hsnIbUzGrj+J0Lpj9Y0JvI' \
                'bJyG1Mxq4/idC6Y/WNCbyGychlIyRkccbaLIRp7z1bN2by4='

#keys - WARNING: They should be on a save place, if you want to use this application online!
SESSION_KEY = '04ccc6a312869b83ad9d010789675539690ac658ff6b5ab0ee8ecbc4668e16ee' \
                'b2fa65e4d2f80e8710160b23593ab71265afbd4efba766f4fbbd0d8b443b89f5'
SHA3_KEY = 'bfb3f1338918940a009f6c84171eb85a'
