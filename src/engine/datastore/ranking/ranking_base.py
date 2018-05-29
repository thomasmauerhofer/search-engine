# encoding: utf-8

from abc import ABCMeta, abstractmethod


class RankingBase(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_default_config():
        """Gets the configuration for the used ranking algorithm"""
        return

    @staticmethod
    @abstractmethod
    def get_name():
        """Returns the name of the Algorithm"""
        return

    @staticmethod
    @abstractmethod
    def get_ranking(paper, queries, settings):
        """Returns ranking of an Paper"""
        return
