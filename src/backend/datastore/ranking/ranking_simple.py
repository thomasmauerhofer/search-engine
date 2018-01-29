# encoding: utf-8
from backend.datastore.ranking.ranking_base import RankingBase
from backend.utils.objects.word_hist import WordHist


class RankingSimple(RankingBase):
    @staticmethod
    def get_ranking(paper, queries, remove_double_terms_in_section_query=True):
        paper_rank = 0.0
        whole_rank, whole_values, ignored = paper.word_hist.get_normalized_query_value(queries["whole-document"])
        info = {}

        for imrad_type, query in queries.items():
            if query == "":
                continue

            if imrad_type == "whole-document":
                paper_rank += whole_rank
                info[imrad_type] = {"rank": whole_rank, "keyvalues": whole_values}
            else:
                # Only sections of the imrad_type influence the ranking
                raking_hist = WordHist()
                sections = paper.get_sections_with_imrad_type(imrad_type)
                for section in sections:
                    raking_hist.append(section.get_combined_word_hist())

                whole_keys = []
                if remove_double_terms_in_section_query:
                    whole_keys = [key[0] for key in whole_values]

                ranking, key_value, ignored = raking_hist.get_normalized_query_value(query, whole_keys)
                info[imrad_type] = {"rank": ranking, "sumwords": sum(raking_hist.values()), "keyvalues": key_value, "ignored": ignored}
                paper_rank += ranking

        return paper_rank, info
