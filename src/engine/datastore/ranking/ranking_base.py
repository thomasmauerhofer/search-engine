# encoding: utf-8

from abc import ABCMeta, abstractmethod

from engine.datastore.models.section import IMRaDType
from engine.utils.math import mean
from engine.utils.paper_utils import sections_to_word_hist


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
    def get_ranking(paper, queries, settings, api):
        """Returns ranking of an Paper"""
        return


    @staticmethod
    @abstractmethod
    def add_papers_params(papers, queries, settings):
        """Some params have to be calculated over all papers.
        Method is called before ranking to add those params to the config"""
        return


    @staticmethod
    def __create_hists(queries, papers):
        hists = {}
        for imrad, query in queries.items():
            hists[imrad] = {}
            for paper in papers:
                if imrad == "whole-document":
                    hist = paper.word_hist
                else:
                    sections = paper.get_sections_with_imrad_type(imrad)
                    hist = sections_to_word_hist(sections)

                hists[imrad][paper.id] = hist
        return hists


    @staticmethod
    def get_df(queries, papers):
        df = {}
        hists = RankingBase.__create_hists(queries, papers)
        for imrad, query in queries.items():
            df[imrad] = {}
            for querie_word in query.split():
                if querie_word not in df[imrad]:
                    # df = #papers where querie_word is part of it -> paper-histogram keys contains querie_word
                    # structure of hists: { imrad: { paperid: wordhist } }
                    df[imrad][querie_word] = len([hist for hist in hists[imrad].values() if querie_word in hist.keys()])
        return df
