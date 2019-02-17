# encoding: utf-8
from enum import Enum

import copy
import numpy as np

from config import WEIGHT_TITLE, WEIGHT_SECTION_TEXT, WEIGHT_SUBSECTION_TITLE, WEIGHT_SUBSECTION_TEXT, \
    WEIGHT_SUBSUBSECTION_TITLE, WEIGHT_SUBSUBSECTION_TEXT, WEIGHT_SECTION_TITLE, DEFAULT_EXTENDED
from engine.datastore.ranking.ranking_base import RankingBase
from engine.utils.exceptions.ranking_exceptions import RankingParameterError
from engine.utils.math import mean


class RankedBoolean(RankingBase):
    @staticmethod
    def get_name():
        return "Ranked Boolean Retrieval"


    @staticmethod
    def get_default_config():
        settings = {"algorithm": RankedBoolean.get_name(),
                    "extended": DEFAULT_EXTENDED,
                    "ranking-algo-params": {RetrievalType.TITLE.name: WEIGHT_TITLE,
                                            RetrievalType.SECTION_TITLE.name: WEIGHT_SECTION_TITLE,
                                            RetrievalType.SECTION_TEXT.name: WEIGHT_SECTION_TEXT,
                                            RetrievalType.SUBSECTION_TITLE.name: WEIGHT_SUBSECTION_TITLE,
                                            RetrievalType.SUBSECTION_TEXT.name: WEIGHT_SUBSECTION_TEXT,
                                            RetrievalType.SUBSUBSECTION_TITLE.name: WEIGHT_SUBSUBSECTION_TITLE,
                                            RetrievalType.SUBSUBSECTION_TEXT.name: WEIGHT_SUBSUBSECTION_TEXT}}
        return settings

    @staticmethod
    def add_papers_params(papers, queries, settings):
        pass

    @staticmethod
    def __add_keys(new_keys, keys=None):
        if not keys:
            keys = {}

        for key in new_keys:
            if not key[0] in keys:
                keys[key[0]] = {}

            keys[key[0]][key[1]] = keys[key[0]][key[1]] + 1 if key[1] in keys[key[0]] else 1
        return keys


    @staticmethod
    def __get_params(settings, paper):
        if "ranking-algo-params" not in settings:
            raise RankingParameterError("No config found!")

        weights = copy.deepcopy(settings.get("ranking-algo-params"))

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



        if not bool(settings.get("extended")):
            return weights

        present = [paper.title_exist(), paper.section_title_exist(), paper.section_text_exist(), paper.subsection_title_exist(),
                   paper.subsection_text_exist(), paper.subsubsection_title_exist(), paper.subsubsection_text_exist()]

        missing_zones = [i for i, x in enumerate(present) if not x]
        missing_weights = [weights[RetrievalType(i).name] for i in missing_zones]

        if not missing_weights:
            return weights

        present_zones = [i for i, x in enumerate(present) if x]
        for i in present_zones:
            weights[RetrievalType(i).name] += sum(missing_weights) / len(missing_weights)

        return weights


    @staticmethod
    def __get_info(s0, s1, s2, s3, s4, s5, s6, weights, keys):
        r0 = mean(s0) * weights[RetrievalType.TITLE.name]
        r1 = mean(s1) * weights[RetrievalType.SECTION_TITLE.name]
        r2 = mean(s2) * weights[RetrievalType.SECTION_TEXT.name]
        r3 = mean(s3) * weights[RetrievalType.SUBSECTION_TITLE.name]
        r4 = mean(s4) * weights[RetrievalType.SUBSECTION_TEXT.name]
        r5 = mean(s5) * weights[RetrievalType.SUBSUBSECTION_TITLE.name]
        r6 = mean(s6) * weights[RetrievalType.SUBSUBSECTION_TEXT.name]

        ret = {"rank": r0 + r1 + r2 + r3 + r4 + r5 + r6, "keys": RankedBoolean.__add_keys(keys),
               "info": {
                   RetrievalType.TITLE.name: {"sum_of1": (np.array(s0) == 1).sum(), "all": len(s0), "mean": mean(s0), "rank": r0},
                   RetrievalType.SECTION_TITLE.name: {"sum_of1": (np.array(s1) == 1).sum(), "all": len(s1), "mean": mean(s1), "rank": r1},
                   RetrievalType.SECTION_TEXT.name: {"sum_of1": (np.array(s2) == 1).sum(), "all": len(s2), "mean": mean(s2), "rank": r2},
                   RetrievalType.SUBSECTION_TITLE.name: {"sum_of1": (np.array(s3) == 1).sum(), "all": len(s3), "mean": mean(s3), "rank": r3},
                   RetrievalType.SUBSECTION_TEXT.name: {"sum_of1": (np.array(s4) == 1).sum(), "all": len(s4), "mean": mean(s4), "rank": r4},
                   RetrievalType.SUBSUBSECTION_TITLE.name: {"sum_of1": (np.array(s5) == 1).sum(), "all": len(s5), "mean": mean(s5), "rank": r5},
                   RetrievalType.SUBSUBSECTION_TEXT.name: {"sum_of1": (np.array(s6) == 1).sum(), "all": len(s6), "mean": mean(s6), "rank": r6}}}

        return ret


    @staticmethod
    def __get_zone_lists(imrad, query, paper):
        keys, s0, s1, s2, s3, s4, s5, s6 = [], [], [], [], [], [], [], []

        if imrad == "whole-document":
            title_keys = [title_word for title_word in paper.title_proceed.split() if any(word in title_word for word in query.split())]
            s0.append(1.0 if title_keys else 0.0)
            keys.extend([[key, RetrievalType.TITLE.name] for key in title_keys])


        for term in query.split():
            for section in paper.get_sections_with_imrad_type(imrad):
                title_keys = [title_word for title_word in section.heading_proceed.split() if term in title_word]
                s1.append(1 if title_keys else 0)
                keys.extend([[key, RetrievalType.SECTION_TITLE.name] for key in title_keys])

                for text in section.text:
                    text_keys = [text_word for text_word in text.text_proceed.split() if term in text_word]
                    s2.append(1 if text_keys else 0)
                    keys.extend([[key, RetrievalType.SECTION_TEXT.name] for key in text_keys])

                for subsection in section.subsections:
                    title_keys = [title_word for title_word in subsection.heading_proceed.split() if term in title_word]
                    s1.append(1 if title_keys else 0)
                    keys.extend([[key, RetrievalType.SUBSECTION_TITLE.name] for key in title_keys])

                    for text in subsection.text:
                        text_keys = [text_word for text_word in text.text_proceed.split() if term in text_word]
                        s2.append(1 if text_keys else 0)
                        keys.extend([[key, RetrievalType.SUBSECTION_TEXT.name] for key in text_keys])

                    for subsubsection in subsection.subsections:
                        title_keys = [title_word for title_word in subsubsection.heading_proceed.split() if term in title_word]
                        s1.append(1 if title_keys else 0)
                        keys.extend([[key, RetrievalType.SUBSUBSECTION_TITLE.name] for key in title_keys])

                        for text in subsubsection.text:
                            text_keys = [text_word for text_word in text.text_proceed.split() if term in text_word]
                            s2.append(1 if text_keys else 0)
                            keys.extend([[key, RetrievalType.SUBSUBSECTION_TEXT.name] for key in text_keys])

        return s0, s1, s2, s3, s4, s5, s6, keys


    @staticmethod
    def get_ranking(paper, queries, settings):
        info, keys, s0, s1, s2, s3, s4, s5, s6 = {}, [], [], [], [], [], [], [], []
        weights = RankedBoolean.__get_params(settings, paper)

        for imrad_type, query in queries.items():
            if not query:
                continue

            ts0, ts1, ts2, ts3, ts4, ts5, ts6, tkeys = RankedBoolean.__get_zone_lists(imrad_type, query, paper)
            info[imrad_type] = RankedBoolean.__get_info(ts0, ts1, ts2, ts3, ts4, ts5, ts6, weights, tkeys)

            s0.extend(ts0)
            s1.extend(ts1)
            s2.extend(ts2)
            s3.extend(ts3)
            s4.extend(ts4)
            s5.extend(ts5)
            s6.extend(ts6)
            keys.extend(tkeys)

        info["overall"] = RankedBoolean.__get_info(s0, s1, s2, s3, s4, s5, s6, weights, keys)
        return info["overall"]["rank"], info


class RetrievalType(Enum):
    TITLE = 0
    SECTION_TITLE = 1
    SECTION_TEXT = 2
    SUBSECTION_TITLE = 3
    SUBSECTION_TEXT = 4
    SUBSUBSECTION_TITLE = 5
    SUBSUBSECTION_TEXT = 6
