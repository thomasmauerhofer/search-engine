# encoding: utf-8
import numpy as np

from engine.datastore.ranking.ranking_base import RankingBase
from engine.utils.exceptions.ranking_exceptions import RankingParameterError


class RankedBooleanRetrieval(RankingBase):
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

        if sum(weights.values() != 1.0):
            raise RankingParameterError("Sum of all weights have to be 1!")

        return weights


    @staticmethod
    def get_ranking(paper, queries, settings):
        paper_rank = 0.0
        info = {}

        weights = RankedBooleanRetrieval.__get_params(settings)

        title_s = 1 if any(i in queries["whole-document"] for i in paper.title_proceed.split()) else 1
        sec_title_s, subsec_title_s, subsubsec_title_s, sec_text_s, subsec_text_s, subsubsec_text_s = [], [], [], [], [], []

        for imrad_type, query in queries.items():
            for sec in paper.get_sections_with_imrad_type(imrad_type):
                sec_title_s.append(1 if any(i in query for i in sec.heading_proceed.split()) else 0)
                sec_text_s.extend([1 if any(i in query for i in text.text_proceed.split()) else 0 for text in sec.text])
                for subsec in sec.subsections:
                    subsec_title_s.append(1 if any(i in query for i in subsec.heading_proceed.split()) else 0)
                    subsec_text_s.extend([1 if any(i in query for i in text.text_proceed.split()) else 0 for text in subsec.text])
                    for subsubsec in subsec.subsections:
                        subsubsec_title_s.append(1 if any(i in query for i in subsubsec.heading_proceed.split()) else 0)
                        subsubsec_text_s.extend([1 if any(i in query for i in text.text_proceed.split()) else 0
                                                 for text in subsubsec.text])

        paper_rank += weights["weight-title"] * title_s
        paper_rank += weights["weight-section-title"] * np.mean(sec_title_s)
        paper_rank += weights["weight-section-text"] * np.mean(sec_text_s)
        paper_rank += weights["weight-subsection-title"] * np.mean(subsec_title_s)
        paper_rank += weights["weight-subsection-text"] * np.mean(subsec_text_s)
        paper_rank += weights["weight-subsubsection-title"] * np.mean(subsubsec_title_s)
        paper_rank += weights["weight-subsubsection-text"] * np.mean(subsubsec_text_s)


        return paper_rank, info
