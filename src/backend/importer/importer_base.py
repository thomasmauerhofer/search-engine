# encoding: utf-8

from abc import ABCMeta, abstractmethod


class ImporterBase(metaclass=ABCMeta):
    @abstractmethod
    def import_paper(self, file):
        """Import data from paper, and store it in an object."""
        return
