# encoding: utf-8
import math

from engine.datastore.ranking.ranking_base import RankingBase
from engine.utils.paper_utils import sections_to_word_hist


class TFIDF(RankingBase):
    @staticmethod
    def get_name():
        return "tf-idf"


    @staticmethod
    def get_default_config():
        return {"algorithm": TFIDF.get_name()}

    @staticmethod
    def add_papers_params(papers, queries, settings):
        settings["df"] = TFIDF.get_df(queries, papers)
        settings["N"] = len(papers)

    @staticmethod
    def get_ranking(paper, queries, settings, api):
        tfidf = {}
        df = settings["df"]
        N = settings["N"]

        for imrad, query in queries.items():
            if imrad == "whole-document":
                hist = paper.word_hist
            else:
                sections = paper.get_sections_with_imrad_type(imrad)
                hist = sections_to_word_hist(sections)

            key_values = {}
            for querie_word in query.split():
                df_val = df[imrad][querie_word]

                # query word is in no other paper -> protect against dividing by 0
                if not df_val:
                    continue

                tf_val = hist.get_tf(querie_word)
                idf_val = math.log10(N / df_val)
                tfidf_val = tf_val * idf_val

                key_values[querie_word] = {"tfidf": tfidf_val, "tf": tf_val, "idf": idf_val}

            tfidf[imrad] = {"sumwords": sum(hist.values()), "keys": key_values,
                            "score": sum([val["tfidf"] for val in key_values.values()])}

        return sum([rating["score"] for rating in tfidf.values()]), tfidf
