# encoding: utf-8
from enum import Enum

import numpy as np

from config import WEIGHT_TITLE, WEIGHT_SECTION_TEXT, WEIGHT_SUBSECTION_TITLE, WEIGHT_SUBSECTION_TEXT, \
    WEIGHT_SUBSUBSECTION_TITLE, WEIGHT_SUBSUBSECTION_TEXT, WEIGHT_SECTION_TITLE
from engine.datastore.ranking.ranking_base import RankingBase
from engine.utils.exceptions.ranking_exceptions import RankingParameterError


def mean(values):
    return np.mean(values) if len(values) else 0


class RankedBooleanRetrieval(RankingBase):
    @staticmethod
    def get_name():
        return "Ranked Boolean Retrieval"


    @staticmethod
    def get_configuration():
        settings = {"algorithm": RankedBooleanRetrieval.get_name(),
                    "ranking-algo-params": {RetrievalType.TITLE.name: WEIGHT_TITLE,
                                            RetrievalType.SECTION_TITLE.name: WEIGHT_SECTION_TITLE,
                                            RetrievalType.SECTION_TEXT.name: WEIGHT_SECTION_TEXT,
                                            RetrievalType.SUBSECTION_TITLE.name: WEIGHT_SUBSECTION_TITLE,
                                            RetrievalType.SUBSECTION_TEXT.name: WEIGHT_SUBSECTION_TEXT,
                                            RetrievalType.SUBSUBSECTION_TITLE.name: WEIGHT_SUBSUBSECTION_TITLE,
                                            RetrievalType.SUBSUBSECTION_TEXT.name: WEIGHT_SUBSUBSECTION_TEXT}}
        return settings


    @staticmethod
    def __get_params(settings):
        if "ranking-algo-params" not in settings:
            raise RankingParameterError("No config found!")

        weights = settings.get("ranking-algo-params")

        if RetrievalType.TITLE.name not in weights:
            raise RankingParameterError("weight-title not in config!")

        if RetrievalType.SECTION_TITLE.name not in weights:
            raise RankingParameterError("weight-section-title not in config!")

        if RetrievalType.SECTION_TEXT.name not in weights:
            raise RankingParameterError("weight-section-text not in config!")

        if RetrievalType.SUBSECTION_TITLE.name not in weights:
            raise RankingParameterError("weight-subsection-title not in config!")

        if RetrievalType.SUBSECTION_TEXT.name not in weights:
            raise RankingParameterError("weight-subsection-text not in config!")

        if RetrievalType.SUBSUBSECTION_TITLE.name not in weights:
            raise RankingParameterError("weight-subsubsection-title not in config!")

        if RetrievalType.SUBSUBSECTION_TEXT.name not in weights:
            raise RankingParameterError("weight-subsubsection-text not in config!")

        if not np.isclose(sum(weights.values()), 1.0):
            raise RankingParameterError("Sum of all weights have to be 1 but is {}!".format(sum(weights.values())))

        return weights


    @staticmethod
    def __get_zone_lists_for_sections(query, sections):
        keys, s1, s2, s3, s4, s5, s6 = [], [], [], [], [], [], []

        for query_word in query.split():
            for section in sections:
                title_keys = [title_word for title_word in section.heading_proceed.split() if query_word in title_word]
                s1.append(1 if title_keys else 0)
                if title_keys:
                    keys.extend([[key, RetrievalType.SECTION_TITLE.name] for key in title_keys])

                for text in section.text:
                    text_keys = [text_word for text_word in text.text_proceed.split() if query_word in text_word]
                    s2.append(1 if text_keys else 0)
                    if text_keys:
                        keys.extend([[key, RetrievalType.SECTION_TEXT.name] for key in text_keys])

                for subsection in section.subsections:
                    title_keys = [title_word for title_word in subsection.heading_proceed.split() if query_word in title_word]
                    s1.append(1 if title_keys else 0)
                    if title_keys:
                        keys.extend([[key, RetrievalType.SUBSECTION_TITLE.name] for key in title_keys])

                    for text in subsection.text:
                        text_keys = [text_word for text_word in text.text_proceed.split() if query_word in text_word]
                        s2.append(1 if text_keys else 0)
                        if text_keys:
                            keys.extend([[key, RetrievalType.SUBSECTION_TEXT.name] for key in text_keys])

                    for subsubsection in subsection.subsections:
                        title_keys = [title_word for title_word in subsubsection.heading_proceed.split() if query_word in title_word]
                        s1.append(1 if title_keys else 0)
                        if title_keys:
                            keys.extend([[key, RetrievalType.SUBSUBSECTION_TITLE.name] for key in title_keys])

                        for text in subsubsection.text:
                            text_keys = [text_word for text_word in text.text_proceed.split() if query_word in text_word]
                            s2.append(1 if text_keys else 0)
                            if text_keys:
                                keys.extend([[key, RetrievalType.SUBSUBSECTION_TEXT.name] for key in text_keys])

        return s1, s2, s3, s4, s5, s6, keys


    @staticmethod
    def get_ranking(paper, queries, settings):
        info, s0, s1, s2, s3, s4, s5, s6 = {}, 0.0, [], [], [], [], [], []
        weights = RankedBooleanRetrieval.__get_params(settings)

        for imrad_type, query in queries.items():
            sections = paper.get_sections_with_imrad_type(imrad_type)
            ts1, ts2, ts3, ts4, ts5, ts6, keys = RankedBooleanRetrieval.__get_zone_lists_for_sections(query, sections)

            r1 = mean(ts1) * weights[RetrievalType.SECTION_TITLE.name]
            r2 = mean(ts2) * weights[RetrievalType.SECTION_TEXT.name]
            r3 = mean(ts3) * weights[RetrievalType.SUBSECTION_TITLE.name]
            r4 = mean(ts4) * weights[RetrievalType.SUBSECTION_TEXT.name]
            r5 = mean(ts5) * weights[RetrievalType.SUBSUBSECTION_TITLE.name]
            r6 = mean(ts6) * weights[RetrievalType.SUBSUBSECTION_TEXT.name]

            info[imrad_type] = {"rating": r1 + r2 + r3 + r4 + r5 + r6, "keys": keys,
                                RetrievalType.SECTION_TITLE.name: {"sum_of1": (np.array(ts1) == 1).sum(), "all": len(ts1), "mean": mean(ts1), "rank": r1},
                                RetrievalType.SECTION_TEXT.name: {"sum_of1": (np.array(ts2) == 1).sum(), "all": len(ts2), "mean": mean(ts2), "rank": r2},
                                RetrievalType.SUBSECTION_TITLE.name: {"sum_of1": (np.array(ts3) == 1).sum(), "all": len(ts3), "mean": mean(ts3), "rank": r3},
                                RetrievalType.SUBSECTION_TEXT.name: {"sum_of1": (np.array(ts4) == 1).sum(), "all": len(ts4), "mean": mean(ts4), "rank": r4},
                                RetrievalType.SUBSUBSECTION_TITLE.name: {"sum_of1": (np.array(ts5) == 1).sum(), "all": len(ts5), "mean": mean(ts5), "rank": r5},
                                RetrievalType.SUBSUBSECTION_TEXT.name: {"sum_of1": (np.array(ts6) == 1).sum(), "all": len(ts6), "mean": mean(ts6), "rank": r6}}

            if imrad_type == "whole-document":
                title_keys = [title_word for title_word in paper.title_proceed.split() if any(word in title_word for word in query.split())]
                s0 = 1.0 if title_keys else 0.0
                info[imrad_type][RetrievalType.TITLE] = {"sum_of1": s0, "all": 1, "mean": s0, "rank": s0 * weights[RetrievalType.TITLE.name]}

            s1.extend(ts1)
            s2.extend(ts2)
            s3.extend(ts3)
            s4.extend(ts4)
            s5.extend(ts5)
            s6.extend(ts6)

        paper_rank = s0 * weights[RetrievalType.TITLE.name]
        paper_rank += mean(s1) * weights[RetrievalType.SECTION_TITLE.name]
        paper_rank += mean(s2) * weights[RetrievalType.SECTION_TEXT.name]
        paper_rank += mean(s3) * weights[RetrievalType.SUBSECTION_TITLE.name]
        paper_rank += mean(s4) * weights[RetrievalType.SUBSECTION_TEXT.name]
        paper_rank += mean(s5) * weights[RetrievalType.SUBSUBSECTION_TITLE.name]
        paper_rank += mean(s6) * weights[RetrievalType.SUBSUBSECTION_TEXT.name]

        return paper_rank, info


class RetrievalType(Enum):
    TITLE = 0
    SECTION_TITLE = 1
    SECTION_TEXT = 2
    SUBSECTION_TITLE = 3
    SUBSECTION_TEXT = 4
    SUBSUBSECTION_TITLE = 5
    SUBSUBSECTION_TEXT = 6
