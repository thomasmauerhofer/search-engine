import time

import math
from engine.datastore.ranking.ranking_base import RankingBase
from engine.utils.paper_utils import sections_to_word_hist


class DivergenceFromRandomness(RankingBase):
    @staticmethod
    def get_default_config():
        return {"algorithm": DivergenceFromRandomness.get_name()}

    @staticmethod
    def get_name():
        return "Divergence from Randomness"

    @staticmethod
    def add_papers_params(papers, queries, settings):
        pass


    @staticmethod
    def get_ranking(paper, queries, settings, api):
        dfr = {}
        start = time.time()
        avg_doc_length_dict = api.client.get_avg_doc_length()
        all_papers_hist_dict = api.client.get_all_papers_hist()
        N = len(api.get_all_paper())

        for imrad, query in queries.items():
            start3 = time.time()
            if imrad == "whole-document":
                hist = paper.word_hist
            else:
                sections = paper.get_sections_with_imrad_type(imrad)
                hist = sections_to_word_hist(sections)


            # + 1... avoid dividing by zero
            doc_length = hist.number_of_words() + 1
            avg_doc_length = avg_doc_length_dict[imrad]
            all_papers_hist = all_papers_hist_dict[imrad]

            key_values = {}
            for querie_word in query.split():
                start2 = time.time()
                # f_ij == term frequency
                f_ij_norm = hist.get_tf(querie_word) * (avg_doc_length / doc_length)

                if f_ij_norm == 0 or querie_word not in all_papers_hist:
                    continue

                pi_i = all_papers_hist[querie_word] / N
                p_kic = f_ij_norm * math.log10(f_ij_norm / pi_i) + (pi_i + (1 / (12 * f_ij_norm + 1)) - f_ij_norm) * math.log10(math.e) + 0.5 * math.log(2 * math.pi * f_ij_norm)
                p_kidi = 1 / (f_ij_norm + 1)

                w_ij = p_kic * p_kidi
                f_iq = query.count(querie_word)
                rank = f_iq * w_ij

                key_values[querie_word] = {"rank": rank, "f_iq": f_iq, "f_ij_norm": f_ij_norm, "pi_i": pi_i, "p_kic": p_kic, "p_kidi": p_kidi}
                end2 = time.time()
                elapsed_time2 = start2 - end2
            dfr[imrad] = {"sumwords": sum(hist.values()), "keys": key_values,
                          "score": sum([val["rank"] for val in key_values.values()])}
            end3 = time.time()
            elapsed_time3 = start3 - end3
            print("Imrad Elapsed time: ", elapsed_time3)


        end = time.time()
        elapsed_time = start - end
        print("A Elapsed time: ", elapsed_time)

        return sum([rating["score"] for rating in dfr.values()]), dfr
