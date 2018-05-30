# encoding: utf-8
from engine.datastore.ranking.ranking_base import RankingBase
from engine.utils.paper_utils import sections_to_word_hist


class TF(RankingBase):
    @staticmethod
    def get_name():
        return "TF"


    @staticmethod
    def get_default_config():
        return {"algorithm": TF.get_name()}


    @staticmethod
    def get_ranking(paper, queries, settings):
        info = {}

        for imrad_type, query in queries.items():
            if imrad_type == "whole-document":
                hist = paper.word_hist
            else:
                sections = paper.get_sections_with_imrad_type(imrad_type)
                hist = sections_to_word_hist(sections)

            keys = hist.query_to_keys(query)
            ranking, key_value = hist.get_tf_of_keys(keys)
            info[imrad_type] = {"rank": ranking, "sumwords": sum(hist.values()), "keyvalues": key_value}

        return sum([ranking["rank"] for ranking in info.values()]), info
