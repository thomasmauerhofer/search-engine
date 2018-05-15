#!/bin/sh

cd ../../src/
python3 -m setup.create_dataset_and_train_helper $1 $2
