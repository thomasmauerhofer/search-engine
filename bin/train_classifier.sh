#!/bin/sh

cd ../src/
python3 -m backend.preprocessing.chapter_classifier.search_params $1 $2
