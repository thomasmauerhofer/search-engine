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
    def __create_hists(queries, papers):
        hists = {}
        for imrad, query in queries.items():
            hists[imrad] = {}
            for paper in papers:
                if imrad == "whole-document":
                    hist = paper.word_hist
                else:
                    sections = paper.get_sections_with_imrad_type(imrad)
                    hist = sections_to_word_hist(sections)

                hists[imrad][paper.id] = hist
        return hists




    @staticmethod
    def get_df(queries, papers):
        df = {}
        hists = TFIDF.__create_hists(queries, papers)
        for imrad, query in queries.items():
            df[imrad] = {}
            for querie_word in query.split():
                if querie_word not in df[imrad]:
                    # df = #papers where querie_word is part of it -> paper-histogram keys contains querie_word
                    # structure of hists: { imrad: { paperid: wordhist } }
                    df[imrad][querie_word] = len([hist for hist in hists[imrad].values() if querie_word in hist.keys()])
        return df



    @staticmethod
    def get_ranking(paper, queries, settings):
        tfidf = {}
        df = settings["df"]
        num_paper = settings["number_paper"]

        for imrad, query in queries.items():
            if imrad == "whole-document":
                hist = paper.word_hist
            else:
                sections = paper.get_sections_with_imrad_type(imrad)
                hist = sections_to_word_hist(sections)

            key_values = {}
            queries = query.split()
            for querie_word in queries:
                df_val = df[imrad][querie_word]

                # query word is in no other paper -> protect against dividing by 0
                if not df_val:
                    continue

                tf_val = hist.get_tf(querie_word)
                idf_val = math.log10(num_paper / df_val)
                tfidf_val = tf_val * idf_val

                if tfidf_val < 0:
                    print("sadasda")

                key_values[querie_word] = {"tfidf": tfidf_val, "tf": tf_val, "idf": idf_val}

            tfidf[imrad] = {"sumwords": sum(hist.values()), "keys": key_values,
                            "score": sum([val["tfidf"] for val in key_values.values()])}

        return sum([rating["score"] for rating in tfidf.values()]), tfidf




