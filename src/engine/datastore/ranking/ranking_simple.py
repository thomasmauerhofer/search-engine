# encoding: utf-8
from engine.datastore.ranking.ranking_base import RankingBase
from engine.utils.paper_utils import sections_to_word_hist
from engine.utils.ranking_utils import get_query_keys


class RankingSimple(RankingBase):
    @staticmethod
    def get_ranking(paper, queries, settings):
        paper_rank = 0.0
        info = {}
        query_keys, ignored_keys = get_query_keys(paper, queries, settings["importance_sections"])


        for imrad_type, keys in query_keys.items():
            if imrad_type == "whole-document":
                hist = paper.word_hist
            else:
                sections = paper.get_sections_with_imrad_type(imrad_type)
                hist = sections_to_word_hist(sections)

            ranking, key_value = hist.get_rank_with_keys(keys)
            info[imrad_type] = {"rank": ranking, "sumwords": sum(hist.values()), "keyvalues": key_value,
                                "ignored": ignored_keys[imrad_type]}
            paper_rank += ranking


        return paper_rank, info
