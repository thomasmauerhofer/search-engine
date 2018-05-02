#!/usr/bin/env python3
# encoding: utf-8
import ast
import os

from config import REQ_DATA_PATH


def evaluate():
    with open(os.path.join(REQ_DATA_PATH, "citations.txt"), encoding='utf-8') as data_file:
        data = ast.literal_eval(data_file.read())

    for tmp in data:
        print(tmp["full_citation"])


if __name__ == "__main__":
    evaluate()
