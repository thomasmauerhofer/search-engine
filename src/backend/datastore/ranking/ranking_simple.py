# encoding: utf-8
from backend.datastore.ranking.ranking_base import RankingBase
from backend.utils.objects.word_hist import WordHist


class RankingSimple(RankingBase):
    @staticmethod
    def get_ranking(paper, queries, settings):
        paper_rank = 0.0
        info = {}
        section_ignored_keys = []
        doc_ignored_keys = []


        if not settings["importance_sections"]:
            section_ignored_keys = paper.word_hist.query_to_keys(queries["whole-document"])


        for imrad_type, query in queries.items():
            if query == "" or imrad_type == "whole-document":
                continue

            raking_hist = WordHist()
            sections = paper.get_sections_with_imrad_type(imrad_type)
            for section in sections:
                raking_hist.append(section.get_combined_word_hist())

            ranking, key_value, ignored = raking_hist.get_normalized_query_value(query, section_ignored_keys)
            info[imrad_type] = {"rank": ranking, "sumwords": sum(raking_hist.values()), "keyvalues": key_value, "ignored": ignored}
            paper_rank += ranking

            if settings["importance_sections"]:
                doc_ignored_keys += [item[0] for item in key_value]

        ranking, key_values, ignored = paper.word_hist.get_normalized_query_value(queries["whole-document"], doc_ignored_keys)
        paper_rank += ranking
        info["whole-document"] = {"rank": ranking, "keyvalues": key_values, "ignored": ignored}

        return paper_rank, info
