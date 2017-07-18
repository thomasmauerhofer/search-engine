#!/bin/sh

cd ../src/
python3 -m backend.preprocessing.classifier.chapter_classifier $1 $2
