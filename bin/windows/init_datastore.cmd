@echo off
SET mode=%1
SET data_path=%2

cd ../../src/
python -m backend.datastore.datastore_utils.init_datastore %mode% %data_path%
