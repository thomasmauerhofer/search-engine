#!/usr/bin/env python3
# encoding: utf-8
import os
import numpy as np
import matplotlib.pyplot as plt
import backend.preprocessing.text_processing as text_processing
from optparse import OptionParser
from config import path_to_datastore
from backend.datastore.structure.section import IMRaDType
from backend.importer.importer_teambeam import ImporterTeambeam
from backend.preprocessing.chapter_classifier.classifier_simple import ClassifierSimple
from backend.preprocessing.chapter_classifier.classifier_nn import ClassifierNN
from backend.utils.exceptions.import_exceptions import ClassificationException


def __create_plots__(score):
    plt.plot(score['acc'])
    plt.plot(score['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig('acc.png')
    plt.clf()

    plt.plot(score['f1'])
    plt.plot(score['val_f1'])
    plt.title('model f1')
    plt.ylabel('f1')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig('f1.png')
    plt.clf()

    plt.plot(score['recall'])
    plt.plot(score['val_recall'])
    plt.title('model recall')
    plt.ylabel('recall')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig('recall.png')
    plt.clf()

    plt.plot(score['precision'])
    plt.plot(score['val_precision'])
    plt.title('model precision')
    plt.ylabel('precision')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig('precision.png')
    plt.clf()

    plt.plot(score['loss'])
    plt.plot(score['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig('loss.png')

#-------------------------------------------------------------------------------
def search_params(single):
    best_classification = 0
    best_size_input_layer = 0
    best_size_middle_layer = 0
    best_batch_size = 0
    epoch = 0

    if single:
        #size_input_layer, size_middle_layer, batch_size, num_epochs, opt:val_split=0.2
        classifier = ClassifierNN(False ,60, 110, 10, 80, 0.2)
        score = classifier.train()
        __create_plots__(score)
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

        print("FINAL Maxima with (Mean) {0}".format(best_classification))
        print("size_input_layer: {0}".format(best_size_input_layer))
        print("size_middle_layer: {0}".format(best_size_middle_layer))
        print("batch_size: {0}".format(best_batch_size))
        print("epoch: {0}".format(epoch))


#-------------------------------------------------------------------------------
def test_params():
    classifier = ClassifierNN()
    classifier.test()


#-------------------------------------------------------------------------------
def create_dataset():
    classifier = ClassifierSimple()
    for filename in os.listdir(path_to_datastore):
        if filename.endswith('.pdf'):
            #print('CURRENT FILE: ' + filename)
            importer = ImporterTeambeam()
            paper = importer.import_paper(filename)

            text_processing.proceed(paper)
            chapter_names = [name.heading for name in paper.sections if not(name.heading.isspace() or name.heading is '')]

            if not len(chapter_names):
                continue

            try:
                prob = classifier.predict_chapter(chapter_names)
            except ClassificationException as e:
                continue

            for i in range(len(prob)):
                tmp = ""
                if prob[i][IMRaDType.ABSTRACT.value] == 1:
                    tmp += IMRaDType.ABSTRACT.name + " "
                if prob[i][IMRaDType.INDRODUCTION.value] == 1:
                    tmp += IMRaDType.INDRODUCTION.name + " "
                if prob[i][IMRaDType.BACKGROUND.value] == 1:
                    tmp += IMRaDType.BACKGROUND.name + " "
                if prob[i][IMRaDType.RESULTS.value] == 1:
                    tmp += IMRaDType.RESULTS.name + " "
                if prob[i][IMRaDType.DISCUSSION.value] == 1:
                    tmp += IMRaDType.DISCUSSION.name + " "
                if prob[i][IMRaDType.ACKNOWLEDGE.value] == 1:
                    tmp += IMRaDType.ACKNOWLEDGE.name + " "

                if tmp is not "":
                    print("{0}: {1}".format(chapter_names[i], tmp))
            #print("\n\n")

#-------------------------------------------------------------------------------
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-d", "--dataset", action="store_true" ,dest="dataset", default=False,
        help="Creates Dataset to train the network")
    parser.add_option("-s", "--search", action="store_true" ,dest="search", default=False,
        help="Search Prarams in for current network")
    parser.add_option("-t", "--test", action="store_true" ,dest="test", default=False,
        help="Test Prarams in for current network")
    (options, args) = parser.parse_args()

    if options.dataset:
        create_dataset()
    elif options.search:
        search_params(True)
    elif options.test:
        test_params()
