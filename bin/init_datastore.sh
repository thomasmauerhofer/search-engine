#!/bin/sh

cd ../src/
python3 -m backend.datastore.utils.init_datastore $1 $2
