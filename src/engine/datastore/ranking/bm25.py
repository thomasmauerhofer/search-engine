# encoding: utf-8
import math
import copy

from engine.datastore.models.section import IMRaDType
from engine.datastore.ranking.ranking_base import RankingBase
from engine.utils.math import mean
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
    def __get_avg_doc_length(papers):
        intro, background, methods, result, discussion, overall = [], [], [], [], [], []
        for paper in papers:
            overall.append(paper.word_hist.number_of_words())
            intro.append(sections_to_word_hist(paper.get_introduction()).number_of_words())
            background.append(sections_to_word_hist(paper.get_background()).number_of_words())
            methods.append(sections_to_word_hist(paper.get_methods()).number_of_words())
            result.append(sections_to_word_hist(paper.get_results()).number_of_words())
            discussion.append(sections_to_word_hist(paper.get_discussion()).number_of_words())

        return {
            "whole-document": mean(overall, True),
            IMRaDType.INTRODUCTION.name: mean(intro, True),
            IMRaDType.BACKGROUND.name: mean(background, True),
            IMRaDType.METHODS.name: mean(methods, True),
            IMRaDType.RESULTS.name: mean(result, True),
            IMRaDType.DISCUSSION.name: mean(discussion, True)
        }


    @staticmethod
    def add_papers_params(papers, queries, settings):
        settings["df"] = BM25.get_df(queries, papers)
        settings["N"] = len(papers)
        settings["avg_doc_length"] = BM25.__get_avg_doc_length(papers)


    @staticmethod
    def get_ranking(paper, queries, settings):
        k1 = copy.deepcopy(settings.get("k1"))
        b = copy.deepcopy(settings.get("b"))


        bm25 = {}
        df = settings["df"]
        N = settings["N"]
        avg_doc_length = settings["avg_doc_length"]

        for imrad, query in queries.items():
            if imrad == "whole-document":
                hist = paper.word_hist
            else:
                sections = paper.get_sections_with_imrad_type(imrad)
                hist = sections_to_word_hist(sections)

            doc_length = hist.number_of_words()
            avg_doc_length = avg_doc_length[imrad]

            key_values = {}
            queries = query.split()
            for querie_word in queries:
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
