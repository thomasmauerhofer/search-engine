#!/usr/bin/env python3
# encoding: utf-8
import numpy as np
from backend.preprocessing.classifier.chapter_classifier import Classifier

def __create_plots__(self, score):
    # summarize history for accuracy
    plt.plot(score['acc'])
    plt.plot(score['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(score['loss'])
    plt.plot(score['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

def search_params(single):
    best_classification = 0
    best_size_input_layer = 0
    best_size_middle_layer = 0
    best_batch_size = 0
    epoch = 0

    if single:
        #size_input_layer, size_middle_layer, batch_size, num_epochs, opt:val_split=0.2
        classifier = Classifier(60, 110, 10, 80, 0.2)
        score = classifier.train()
    else:
        for size_input_layer in range(10, 210, 50):
            for size_middle_layer in range(10, 210, 50):
                for batch_size in range(10, 210, 50):
                    classifier = Classifier(size_input_layer, size_middle_layer, batch_size, 70)
                    score = classifier.train()
                    mean = np.mean(score['val_acc'])
                    if mean > best_classification:
                        best_classification = mean
                        best_size_input_layer = size_input_layer
                        best_size_middle_layer = size_middle_layer
                        best_batch_size = batch_size
                        epoch = score['val_acc'].index(max(score['val_acc'])) + 1
                        print("New Maxima with {0}".format(best_classification))
                        print("size_input_layer: {0}".format(best_size_input_layer))
                        print("size_middle_layer: {0}".format(best_size_middle_layer))
                        print("batch_size: {0}".format(best_batch_size))
                        print("epoch: {0}".format(epoch))



        print("FINAL Maxima with (Mean) {0}".format(best_classification))
        print("size_input_layer: {0}".format(best_size_input_layer))
        print("size_middle_layer: {0}".format(best_size_middle_layer))
        print("batch_size: {0}".format(best_batch_size))
        print("epoch: {0}".format(epoch))

if __name__ == "__main__":
    search_params(True)
