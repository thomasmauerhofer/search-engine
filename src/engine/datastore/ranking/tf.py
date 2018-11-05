# encoding: utf-8
from engine.datastore.ranking.ranking_base import RankingBase
from engine.utils.paper_utils import sections_to_word_hist


class TF(RankingBase):
    @staticmethod
    def get_name():
        return "tf"


    @staticmethod
    def get_default_config():
        return {"algorithm": TF.get_name()}


    @staticmethod
    def get_ranking(paper, queries, settings):
        info = {}
        word_value = []
        ranking = 0.0

        for imrad_type, query in queries.items():
            if imrad_type == "whole-document":
                hist = paper.word_hist
            else:
                sections = paper.get_sections_with_imrad_type(imrad_type)
                hist = sections_to_word_hist(sections)

            for word in query.split():
                rank = hist.get_tf(word)
                ranking += rank
                word_value.append([word, rank])

            info[imrad_type] = {"rank": ranking, "sumwords": sum(hist.values()), "keyvalues": word_value}

        return sum([ranking["rank"] for ranking in info.values()]), info
