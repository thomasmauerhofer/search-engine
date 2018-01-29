# encoding: utf-8

from abc import ABCMeta, abstractmethod


class RankingBase(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_ranking(paper, queries, remove_double_terms_in_section_query=True):
        """Returns ranking of an Paper"""
        return
