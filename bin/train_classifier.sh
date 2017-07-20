#!/bin/sh

cd ../src/
python3 -m backend.preprocessing.classifier.search_params $1 $2
