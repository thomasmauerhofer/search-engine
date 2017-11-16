@echo off
SET port=27017
SET db_path=D:\MongoDB\data\db

echo -----------------------------------------------------------------------
echo Starting MongoDB on Port: %port%
echo Path to Datastore: %db_path%
echo -----------------------------------------------------------------------

mongod --port %port% --dbpath %db_path%

