#!/bin/sh

cd ../src/
python3 -m backend.preprocessing.chapter_classifier.create_dataset_and_train_helper $1 $2
