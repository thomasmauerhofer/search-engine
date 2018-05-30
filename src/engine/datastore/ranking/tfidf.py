# encoding: utf-8
import math

from engine.datastore.ranking.ranking_base import RankingBase
from engine.utils.paper_utils import sections_to_word_hist


class TFIDF(RankingBase):
    @staticmethod
    def get_name():
        return "tf-idf"


    @staticmethod
    def get_default_config():
        return {"algorithm": TFIDF.get_name()}


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
    def get_idf(queries, papers):
        idf = {}
        hists = TFIDF.__create_hists(queries, papers)
        for imrad, query in queries.items():
            idf[imrad] = {}
            for paper in papers:
                keys = hists[imrad][paper.id].query_to_keys(query)

                for key in keys:
                    if key not in idf[imrad]:
                        df = len([hist for hist in hists[imrad].values() if key in hist.keys()])
                        idf[imrad][key] = [math.log10(len(papers) / df), df]

        return idf


    @staticmethod
    def get_ranking(paper, queries, settings):
        tfidf = {}
        idf = settings["idf"]

        for imrad, query in queries.items():
            if imrad == "whole-document":
                hist = paper.word_hist
            else:
                sections = paper.get_sections_with_imrad_type(imrad)
                hist = sections_to_word_hist(sections)

            keys = hist.query_to_keys(query)
            key_values = {}
            for key in keys:
                key_values[key] = {"tfidf": hist.get_tf(key) * idf[imrad][key][0], "tf": hist.get_tf(key),
                                   "idf": idf[imrad][key][0], "count": hist[key], "count_docs": idf[imrad][key][1]}

            tfidf[imrad] = {"sumwords": sum(hist.values()), "keys": key_values,
                            "score": sum([val["tfidf"] for val in key_values.values()])}

        return sum([rating["score"] for rating in tfidf.values()]), tfidf




