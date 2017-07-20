#!/usr/bin/env python3
# encoding: utf-8

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.preprocessing import sequence
from keras.callbacks import ModelCheckpoint
import numpy as np
import h5py as h5py
from config import path_to_dataset, path_to_hdf5
from backend.utils.string_utils import string_to_list_of_integers
from backend.datastore.structure.section import IMRaDType
from backend.preprocessing.chapter_classifier.classifier_base import ClassifierBase

# truncate and pad input sequences
max_chapter_length = 200

class ClassifierNN(ClassifierBase):
    def __init__(self, load_weigths=True, size_input_layer=60, size_middle_layer=110, batch_size=10, num_epochs=80, val_split=0.2):
        self.size_input_layer = size_input_layer
        self.size_middle_layer = size_middle_layer
        self.batch_size = batch_size
        self.num_epochs = num_epochs
        self.val_split = val_split
        self.__init_model__(load_weigths)


    def __init_model__(self, load_weigths):
        self.model = Sequential()
        # Input Layer:
        self.model.add(Dense(self.size_input_layer, input_dim=max_chapter_length, activation='relu'))
        # Hidden Layer
        self.model.add(Dense(self.size_middle_layer, activation='relu'))
        # Output-Layer holds all members of the IMRaDTypes; softmax = give the actual output class label probabilities
        self.model.add(Dense(len(IMRaDType) - 1, activation='softmax'))

        if load_weigths:
            self.model.load_weights(path_to_hdf5 + "weights-improvement-30-1.00.hdf5")
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


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

        #percent_to_split = 90
        #splitt = int((len(dataset) / 100) * percent_to_split)
        #X_train = X[:splitt]
        #Y_train = Y[:splitt]
        #X_test = X[splitt:]
        #Y_test = Y[splitt:]

        filepath="weights-improvement-{epoch:02d}-{val_acc:.2f}.hdf5"
        checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
        callbacks_list = [checkpoint]

        hist = self.model.fit(np.array(X), np.array(Y), batch_size=self.batch_size, nb_epoch=self.num_epochs, validation_split=self.val_split, verbose=1, callbacks=callbacks_list)
        return hist.history

    def test(self):
        (X_test, Y_test) = self.__load_testset__()
        scores = self.model.evaluate(np.array(X_test), np.array(Y_test), verbose=0)
        print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

    def predict_chapter(self, chapter_list):
        names_nummerical = np.array([string_to_list_of_integers(name) for name in chapter_list])
        X = sequence.pad_sequences(names_nummerical, maxlen=max_chapter_length)
        Y = self.model.predict(X, batch_size=self.batch_size, verbose=1)
        return Y
