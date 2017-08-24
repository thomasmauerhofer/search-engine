# encoding: utf-8

from abc import ABCMeta, abstractmethod


class PaperStructure(metaclass=ABCMeta):
    @abstractmethod
    def __str__(self):
        """Print the Data of the Object"""
        return

    @abstractmethod
    def to_dict(self):
        """Creates an Dictionary with the objects Data"""
        return
