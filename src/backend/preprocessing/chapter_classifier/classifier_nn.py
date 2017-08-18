#!/usr/bin/env python3
# encoding: utf-8

import numpy as np
import h5py as h5py
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import ModelCheckpoint
from config import path_to_dataset, path_to_hdf5
from backend.datastore.structure.section import IMRaDType
from backend.preprocessing.chapter_classifier.classifier_base import ClassifierBase
from backend.preprocessing.chapter_classifier.bag_of_words import BagOfWords

class ClassifierNN(ClassifierBase):
    def __init__(self, load_weigths=True, size_input_layer=60, size_middle_layer=110, batch_size=10, num_epochs=80, val_split=0.2):
        self.size_input_layer = size_input_layer
        self.size_middle_layer = size_middle_layer
        self.batch_size = batch_size
        self.num_epochs = num_epochs
        self.val_split = val_split
        self.bag = BagOfWords()
        self.__init_model__(load_weigths)


    def __init_model__(self, load_weigths):
        self.model = Sequential()
        # Input Layer:
        self.model.add(Dense(self.size_input_layer, input_dim=len(self.bag.get_vocabulary()), activation='relu'))
        # Hidden Layer
        self.model.add(Dense(self.size_middle_layer, activation='relu'))
        # Output-Layer holds all members of the IMRaDTypes; softmax = give the actual output class label probabilities
        self.model.add(Dense(len(IMRaDType), activation='softmax'))

        if load_weigths:
            self.model.load_weights(path_to_hdf5 + "weights.hdf5")
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


    def __load_dataset__(self, filename):
        dataset = []
        with open(path_to_dataset + filename) as f:
            content = f.readlines()

        for line in content:
            tokens = line.split(":")
            dataset.append([tokens[0].rstrip(), np.zeros(len(IMRaDType))])
            imrad_types = tokens[1].split(" ")

            for imrad in imrad_types:
                imrad = imrad.rstrip()
                if imrad == IMRaDType.INDRODUCTION.name:
                    dataset[-1][1][IMRaDType.INDRODUCTION.value] = 1
                elif imrad == IMRaDType.BACKGROUND.name:
                    dataset[-1][1][IMRaDType.BACKGROUND.value] = 1
                elif imrad == IMRaDType.RESULTS.name:
                    dataset[-1][1][IMRaDType.RESULTS.value] = 1
                elif imrad == IMRaDType.DISCUSSION.name:
                    dataset[-1][1][IMRaDType.DISCUSSION.value] = 1
                elif imrad == IMRaDType.ABSTRACT.name:
                    dataset[-1][1][IMRaDType.ABSTRACT.value] = 1
                elif imrad == IMRaDType.ACKNOWLEDGE.name:
                    dataset[-1][1][IMRaDType.ACKNOWLEDGE.value] = 1
                elif imrad:
                    print("ERROR: " + imrad + " not defined!")

        X = [self.bag.text_to_vector(item[0]) for item in dataset]
        Y = [item[1] for item in dataset]
        return (X, Y)

    def __load_trainset__(self):
        return self.__load_dataset__('dataset.txt')

    def __load_testset__(self):
        return self.__load_dataset__('dataset.txt')


    def train(self):
        (X, Y) = self.__load_trainset__()

        filepath="weights-improvement-{epoch:02d}-{val_acc:.2f}.hdf5"
        checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
        callbacks_list = [checkpoint]

        hist = self.model.fit(np.array(X), np.array(Y), batch_size=self.batch_size, nb_epoch=self.num_epochs, validation_split=self.val_split, verbose=1, callbacks=callbacks_list)
        return hist.history

    def test(self):
        (X_test, Y_test) = self.__load_testset__()
        scores = self.model.evaluate(np.array(X_test), np.array(Y_test), verbose=0)
        print("%s: %.2f%%" % (self.model.metrics_names[1], scores[1]*100))

    def predict_chapter(self, chapter_list):
        X = np.array([self.bag.text_to_vector(name) for name in chapter_list])
        Y = self.model.predict(X, batch_size=self.batch_size, verbose=1)
        return Y
