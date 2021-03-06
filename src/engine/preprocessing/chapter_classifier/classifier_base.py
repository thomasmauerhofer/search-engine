# encoding: utf-8

from abc import ABCMeta, abstractmethod


class ClassifierBase(metaclass=ABCMeta):
    @abstractmethod
    def predict_chapter(self, chapter_list):
        """Predict the class of a chapter name"""
        return
