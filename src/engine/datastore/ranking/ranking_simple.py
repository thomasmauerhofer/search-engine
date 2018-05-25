# encoding: utf-8
from engine.datastore.ranking.ranking_base import RankingBase
from engine.utils.paper_utils import sections_to_word_hist


class RankingSimple(RankingBase):
    @staticmethod
    def get_name():
        return "Ranking Simple"


    @staticmethod
    def get_configuration():
        return {"algorithm": RankingSimple.get_name()}


    @staticmethod
    def get_ranking(paper, queries, settings):
        paper_rank = 0.0
        info = {}

        for imrad_type, query in queries.items():
            if imrad_type == "whole-document":
                hist = paper.word_hist
            else:
                sections = paper.get_sections_with_imrad_type(imrad_type)
                hist = sections_to_word_hist(sections)

            keys = hist.query_to_keys(query)
            ranking, key_value = hist.get_rank_with_keys(keys)
            info[imrad_type] = {"rank": ranking, "sumwords": sum(hist.values()), "keyvalues": key_value}
            paper_rank += ranking

        return paper_rank, info
