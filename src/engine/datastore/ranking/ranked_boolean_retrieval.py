# encoding: utf-8
import numpy as np

from engine.datastore.ranking.ranking_base import RankingBase
from engine.utils.exceptions.ranking_exceptions import RankingParameterError


def mean(values):
    return np.mean(values) if len(values) else 0


class RankedBooleanRetrieval(RankingBase):
    @staticmethod
    def get_name():
        return "Ranked Boolean Retrieval"


    @staticmethod
    def __get_params(settings):

        if "ranking-algo-params" not in settings:
            raise RankingParameterError("No config found!")

        weights = settings.get("ranking-algo-params")

        if "weight-title" not in weights:
            raise RankingParameterError("weight-title not in config!")

        if "weight-section-title" not in weights:
            raise RankingParameterError("weight-section-title not in config!")

        if "weight-section-text" not in weights:
            raise RankingParameterError("weight-section-text not in config!")

        if "weight-subsection-title" not in weights:
            raise RankingParameterError("weight-subsection-title not in config!")

        if "weight-subsection-text" not in weights:
            raise RankingParameterError("weight-subsection-text not in config!")

        if "weight-subsubsection-title" not in weights:
            raise RankingParameterError("weight-subsubsection-title not in config!")

        if "weight-subsubsection-text" not in weights:
            raise RankingParameterError("weight-subsubsection-text not in config!")

        if not np.isclose(sum(weights.values()), 1.0):
            raise RankingParameterError("Sum of all weights have to be 1 but is {}!".format(sum(weights.values())))

        return weights





    @staticmethod
    def get_ranking(paper, queries, settings):
        sec_title_s, subsec_title_s, subsubsec_title_s, sec_text_s, subsec_text_s, subsubsec_text_s = [], [], [], [], [], []
        info = {}
        weights = RankedBooleanRetrieval.__get_params(settings)

        title_s = 1 if any(i in queries["whole-document"] for i in paper.title_proceed.split()) else 1

        for imrad_type, query in queries.items():
            for query_word in query.split():

                for sec in paper.get_sections_with_imrad_type(imrad_type):
                    sec_title_s.append(1 if any(query_word in title_word for title_word in sec.heading_proceed.split()) else 0)
                    sec_text_s.extend([1 if any(query_word in text_word for text_word in text.text_proceed.split()) else 0
                                       for text in sec.text])
                    for subsec in sec.subsections:
                        subsec_title_s.append(1 if any(query_word in title_word for title_word in subsec.heading_proceed.split()) else 0)
                        subsec_text_s.extend([1 if any(query_word in text_word for text_word in text.text_proceed.split()) else 0
                                              for text in subsec.text])
                        for subsubsec in subsec.subsections:
                            subsubsec_title_s.append(1 if any(query_word in title_word for title_word in subsubsec.heading_proceed.split()) else 0)
                            subsubsec_text_s.extend([1 if any(query_word in text_word for text_word in text.text_proceed.split()) else 0
                                                     for text in subsubsec.text])

            key_value = [["Weight Title", title_s, 1]] if imrad_type == "whole-document" else []
            key_value.append(["Weight Section Title", mean(sec_title_s), len(sec_title_s)])
            key_value.append(["Weight Section Text", mean(sec_text_s), len(sec_title_s)])
            key_value.append(["Weight SubSection Title", mean(subsec_title_s), len(sec_title_s)])
            key_value.append(["Weight SubSection Text", mean(subsec_text_s), len(sec_title_s)])
            key_value.append(["Weight SubSection Title", mean(subsubsec_title_s), len(sec_title_s)])
            key_value.append(["Weight SubSection Text", mean(subsubsec_text_s), len(sec_title_s)])

            info[imrad_type] = {"rank": 0, "sumwords": "Can't be displayed with Ranked Boolean Retrieval", "keyvalues": key_value}

        mean_sec_title = mean(sec_title_s)
        mean_sec_text = mean(sec_text_s)
        mean_subsec_title = mean(subsec_title_s)
        mean_subsec_text = mean(subsec_text_s)
        mean_subsubsec_title = mean(subsubsec_title_s)
        mean_subsubsec_text = mean(subsubsec_text_s)

        paper_rank = weights["weight-title"] * title_s
        paper_rank += weights["weight-section-title"] * mean_sec_title
        paper_rank += weights["weight-section-text"] * mean_sec_text
        paper_rank += weights["weight-subsection-title"] * mean_subsec_title
        paper_rank += weights["weight-subsection-text"] * mean_subsec_text
        paper_rank += weights["weight-subsubsection-title"] * mean_subsubsec_title
        paper_rank += weights["weight-subsubsection-text"] * mean_subsubsec_text

        return paper_rank, info
