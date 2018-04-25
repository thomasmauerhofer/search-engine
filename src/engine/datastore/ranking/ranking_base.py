# encoding: utf-8

from abc import ABCMeta, abstractmethod


class RankingBase(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_ranking(paper, queries, settings):
        """Returns ranking of an Paper"""
        return