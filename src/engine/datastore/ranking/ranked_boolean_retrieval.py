# encoding: utf-8
import numpy as np

from engine.datastore.ranking.ranking_base import RankingBase
from engine.utils.exceptions.ranking_exceptions import RankingParameterError
from engine.utils.ranking_utils import get_query_keys


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

        if not np.isclose(sum(weights.values()), 1.0):
            raise RankingParameterError("Sum of all weights have to be 1 but is {}!".format(sum(weights.values())))

        return weights





    @staticmethod
    def get_ranking(paper, queries, settings):
        sec_title_s, subsec_title_s, subsubsec_title_s, sec_text_s, subsec_text_s, subsubsec_text_s = [], [], [], [], [], []
        info, ignored = {}, []
        weights = RankedBooleanRetrieval.__get_params(settings)
        query_keys, ignored_keys = get_query_keys(paper, queries, settings["importance_sections"])

        title_s = 1 if any(i in queries["whole-document"] for i in paper.title_proceed.split()) else 1

        for imrad_type, query in queries.items():
            for query_word in query.split():
                if any([key for key in ignored_keys[imrad_type] if query_word in key]):
                    ignored.append(query_word)
                    continue

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
            key_value.append(["Weight Section Title", np.mean(sec_title_s), len(sec_title_s)])
            key_value.append(["Weight Section Text", np.mean(sec_text_s), len(sec_title_s)])
            key_value.append(["Weight SubSection Title", np.mean(subsec_title_s), len(sec_title_s)])
            key_value.append(["Weight SubSection Text", np.mean(subsec_text_s), len(sec_title_s)])
            key_value.append(["Weight SubSection Title", np.mean(subsubsec_title_s), len(sec_title_s)])
            key_value.append(["Weight SubSection Text", np.mean(subsubsec_text_s), len(sec_title_s)])

            info[imrad_type] = {"rank": "Can't be displayed with Ranked Boolean Retrieval", "sumwords": "-- nicht vorhanden --",
                                "keyvalues": key_value, "ignored": ignored}

        mean_sec_title = np.mean(sec_title_s) if len(sec_title_s) else 0
        mean_sec_text = np.mean(sec_text_s) if len(sec_text_s) else 0
        mean_subsec_title = np.mean(subsec_title_s) if len(subsec_title_s) else 0
        mean_subsec_text = np.mean(subsec_text_s) if len(subsec_text_s) else 0
        mean_subsubsec_title = np.mean(subsubsec_title_s) if len(subsubsec_title_s) else 0
        mean_subsubsec_text = np.mean(subsubsec_text_s) if len(subsubsec_text_s) else 0

        paper_rank = weights["weight-title"] * title_s
        paper_rank += weights["weight-section-title"] * mean_sec_title
        paper_rank += weights["weight-section-text"] * mean_sec_text
        paper_rank += weights["weight-subsection-title"] * mean_subsec_title
        paper_rank += weights["weight-subsection-text"] * mean_subsec_text
        paper_rank += weights["weight-subsubsection-title"] * mean_subsubsec_title
        paper_rank += weights["weight-subsubsection-text"] * mean_subsubsec_text

        return paper_rank, info
