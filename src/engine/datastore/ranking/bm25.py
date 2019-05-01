# encoding: utf-8
import math
import copy

from engine.datastore.ranking.ranking_base import RankingBase
from engine.utils.paper_utils import sections_to_word_hist


class BM25(RankingBase):
    @staticmethod
    def get_name():
        return "BM25"


    @staticmethod
    def get_default_config():
        return {"algorithm": BM25.get_name(),
                "k1": 1.2,
                "b": 0.75}


    @staticmethod
    def add_papers_params(papers, queries, settings):
        settings["df"] = BM25.get_df(queries, papers)
        settings["N"] = len(papers)


    @staticmethod
    def get_ranking(paper, queries, settings, api):
        k1 = copy.deepcopy(settings.get("k1"))
        b = copy.deepcopy(settings.get("b"))


        bm25 = {}
        df = settings["df"]
        N = settings["N"]
        avg_doc_length_dict = api.client.get_avg_doc_length()

        for imrad, query in queries.items():
            if imrad == "whole-document":
                hist = paper.word_hist
            else:
                sections = paper.get_sections_with_imrad_type(imrad)
                hist = sections_to_word_hist(sections)

            doc_length = hist.number_of_words() + 1
            avg_doc_length = avg_doc_length_dict[imrad]

            key_values = {}
            for querie_word in query.split():
                df_val = df[imrad][querie_word]

                # query word is in no other paper -> protect against dividing by 0
                if not df_val:
                    continue

                tf_val = hist.get_tf(querie_word)
                idf_val = math.log10((N - df_val + 0.5) / (df_val + 0.5))
                b25_val = idf_val * ((tf_val * (k1 + 1)) / (tf_val + k1 * (1 - b + b * (doc_length / avg_doc_length))))

                key_values[querie_word] = {"bm25": b25_val, "tf": tf_val, "idf": idf_val}

            bm25[imrad] = {"sumwords": sum(hist.values()), "keys": key_values,
                           "score": sum([val["bm25"] for val in key_values.values()])}

        return sum([rating["score"] for rating in bm25.values()]), bm25
