#!/usr/bin/env python3
# encoding: utf-8

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.preprocessing import sequence
import numpy as np
from backend.datastore.structure.section import IMRaDType
from backend.utils.string_utils import string_to_list_of_integers

# truncate and pad input sequences
max_chapter_length = 200

# Training parameters
batch_size = 200
num_epochs = 30 # iterations
val_split = 0.1

def train():
    input_strings = [['blaq', IMRaDType.INDRODUCTION.name], ['blao', IMRaDType.BACKGROUND.name], ['blau', IMRaDType.METHODS.name], ['blae', IMRaDType.RESULTS.name], ['blai', IMRaDType.DISCUSSION.name], ['blae', IMRaDType.INDRODUCTION.name]]
    #(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=10)
    words = [string_to_list_of_integers(list(name[0])) for name in input_strings]

    X_train = sequence.pad_sequences(words, maxlen=max_chapter_length)
    y = [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1], [1, 0, 0, 0, 0]]

    model = Sequential()

    # Input-Layer has the length of the train-set
    model.add(Dense(len(input_strings), input_dim=max_chapter_length, activation='relu'))
    # Output-Layer holds all members of the IMRaDTypes; softmax = give the actual output class label probabilities
    model.add(Dense(len(IMRaDType), activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    history = model.fit(np.array(X_train), np.array(y), batch_size=batch_size, nb_epoch=num_epochs, validation_split=val_split, verbose=1)


if __name__ == "__main__":
    train()
