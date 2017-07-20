#!/usr/bin/env python3
# encoding: utf-8

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.preprocessing import sequence
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
from backend.datastore.structure.section import IMRaDType
from backend.utils.string_utils import string_to_list_of_integers
from config import path_to_dataset

# truncate and pad input sequences
max_chapter_length = 200

class Classifier(object):
    def __init__(self, size_input_layer=180, size_middle_layer=180, batch_size=200, num_epochs=30, val_split=0.2):
        # Training parameters
        self.size_input_layer = size_input_layer
        self.size_middle_layer = size_middle_layer
        self.batch_size = batch_size
        self.num_epochs = num_epochs # iterations
        self.val_split = val_split


    def __load_dataset__(self, filename):
        dataset = []
        with open(path_to_dataset + filename) as f:
            content = f.readlines()

        content = [line for line in content if "ABSTRACT" not in line]
        for line in content:
            tokens = line.split(":")
            name_nummerical = np.array(string_to_list_of_integers(tokens[0].rstrip()))
            dataset.append([name_nummerical, [0, 0, 0, 0, 0]])
            imrad_types = tokens[1].split(" ")

            for imrad in imrad_types:
                imrad = imrad.rstrip()
                if imrad == 'INDRODUCTION':
                    dataset[-1][1][IMRaDType.INDRODUCTION.value] = 1
                elif imrad == 'BACKGROUND':
                    dataset[-1][1][IMRaDType.BACKGROUND.value] = 1
                elif imrad == 'METHOD':
                    dataset[-1][1][IMRaDType.METHODS.value] = 1
                elif imrad == 'RESULT':
                    dataset[-1][1][IMRaDType.RESULTS.value] = 1
                elif imrad == 'DISCUSSION':
                    dataset[-1][1][IMRaDType.DISCUSSION.value] = 1
                elif imrad:
                    print("ERROR: " + imrad + " not defined!")

        X = sequence.pad_sequences([item[0] for item in dataset], maxlen=max_chapter_length)
        Y = [item[1] for item in dataset]
        return (X, Y)

    def __load_trainset__(self):
        return self.__load_dataset__('dataset_tmp.txt')

    def __load_testset__(self):
        return self.__load_dataset__('dataset_small.txt')


    def train(self):
        (X, Y) = self.__load_trainset__()
        #(X_test, Y_test) = self.__load_testset__()

        #percent_to_split = 90
        #splitt = int((len(dataset) / 100) * percent_to_split)
        #X_train = X[:splitt]
        #Y_train = Y[:splitt]
        #X_test = X[splitt:]
        #Y_test = Y[splitt:]

        model = Sequential()
        # Input-Layer has the length of the train-set
        model.add(Dense(self.size_input_layer, input_dim=max_chapter_length, activation='relu'))
        model.add(Dense(self.size_middle_layer, activation='relu'))

        # Output-Layer holds all members of the IMRaDTypes; softmax = give the actual output class label probabilities
        model.add(Dense(len(IMRaDType) - 1, activation='softmax'))

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        hist = model.fit(np.array(X), np.array(Y), batch_size=self.batch_size, nb_epoch=self.num_epochs, validation_split=self.val_split, verbose=1)
        return hist.history
