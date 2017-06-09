#!/bin/sh

cd ../src/
python3 -m backend.datastore.datastore_utils.init_datastore $1 $2
