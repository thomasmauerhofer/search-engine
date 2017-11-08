#!/usr/bin/env python3
# encoding: utf-8
import os
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
import backend.preprocessing.text_processing as text_processing
from optparse import OptionParser
from config import path_to_datastore, path_to_dataset
from backend.datastore.structure.section import IMRaDType
from backend.importer.importer_teambeam import ImporterTeambeam
from backend.preprocessing.chapter_classifier.classifier_simple import ClassifierSimple
from backend.preprocessing.chapter_classifier.classifier_nn import ClassifierNN


def __create_plots__(score):
    plt.plot(score['acc'])
    plt.plot(score['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='lower right')
    plt.savefig('acc.png')
    plt.clf()

    plt.plot(score['loss'])
    plt.plot(score['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper right')
    plt.savefig('loss.png')


# -------------------------------------------------------------------------------
def search_params(single):
    best_classification = 0
    best_size_input_layer = 0
    best_size_middle_layer = 0
    best_batch_size = 0
    epoch = 0

    if single:
        # load_weigths=True, size_input_layer=60, size_middle_layer=110, batch_size=10, num_epochs=80, val_split=0.2
        classifier = ClassifierNN(False, 60, 110, 10, 80, 0.2)
        score = classifier.train()
        __create_plots__(score)
    else:
        for size_input_layer in range(10, 210, 50):
            for size_middle_layer in range(10, 210, 50):
                for batch_size in range(10, 210, 50):
                    classifier = ClassifierNN(False, size_input_layer, size_middle_layer, batch_size, 70, 0.2)
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


# -------------------------------------------------------------------------------
def test_params():
    classifier = ClassifierNN()
    (names, scores) = classifier.test()
    for i in range(len(names)):
        print("%s: %f" % (names[i], scores[i]))


# -------------------------------------------------------------------------------
def create_dataset():
    classifier = ClassifierSimple()
    for filename in os.listdir(path_to_datastore):
        if filename.endswith('.pdf'):
            importer = ImporterTeambeam()
            paper = importer.import_paper(filename)

            text_processing.proceed(paper)
            chapter_names = [name.heading for name in paper.sections if
                             not (name.heading.isspace() or name.heading is '')]

            if not len(chapter_names):
                continue

            prob = classifier.predict_chapter(chapter_names)

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


# -------------------------------------------------------------------------------
def plot_words():
    dic = {}
    with open(path_to_dataset + 'dataset.txt') as f:
        content = f.readlines()

    for line in content:
        words = line.split(":")[0]
        for token in words.split(" "):
            if token in dic:
                dic[token] += 1
            else:
                dic[token] = 1

    for pair in sorted(dic.items(), key=itemgetter(1), reverse=True):
        print("{0}: {1}".format(pair[0], pair[1]))


# -------------------------------------------------------------------------------
if __name__ == "__main__":
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    parser = OptionParser()
    parser.add_option("-d", "--dataset", action="store_true", dest="dataset", default=False,
                      help="Creates Dataset to train the network")
    parser.add_option("-b", "--bag", action="store_true", dest="bag", default=False,
                      help="Plot words for bag")
    parser.add_option("-s", "--search", action="store_true", dest="search", default=False,
                      help="Search Prarams in for current network")
    parser.add_option("-t", "--test", action="store_true", dest="test", default=False,
                      help="Test Prarams in for current network")
    (options, args) = parser.parse_args()

    if options.dataset:
        create_dataset()
    elif options.search:
        search_params(True)
    elif options.test:
        test_params()
    elif options.bag:
        plot_words()
