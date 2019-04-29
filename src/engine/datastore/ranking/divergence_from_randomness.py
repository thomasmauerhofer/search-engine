from engine.datastore.ranking.ranking_base import RankingBase
from engine.utils.paper_utils import sections_to_word_hist


class DivergenceFromRandomness(RankingBase):
    @staticmethod
    def get_default_config():
        pass

    @staticmethod
    def get_name():
        return "Divergence from Randomness"

    @staticmethod
    def add_papers_params(papers, queries, settings):
        pass


    @staticmethod
    def get_ranking(paper, queries, settings, api):
        avg_doc_length_dict = api.client.get_avg_doc_length()
        N = len(api.get_all_paper())

        for imrad, query in queries.items():
            if imrad == "whole-document":
                hist = paper.word_hist
            else:
                sections = paper.get_sections_with_imrad_type(imrad)
                hist = sections_to_word_hist(sections)

            doc_length = hist.number_of_words()
            avg_doc_length = avg_doc_length_dict[imrad]

            key_values = {}
            queries = query.split()
            for querie_word in queries:
                # f_ij == term frequency
                f_ij_norm = hist.get_tf(querie_word) * (avg_doc_length / doc_length)

                if f_ij_norm == 0:
                    continue

                pi_i = 0 / N
                p_kic = 0
                p_kidi = 0

                w_ij = p_kic * p_kidi

                f_iq = 0
                rank = f_iq * w_ij