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

        f_iq = 0
        f_ij = 0
        p_kic = 0
        p_kidi = 0

        for imrad, query in queries.items():
            if imrad == "whole-document":
                hist = paper.word_hist
            else:
                sections = paper.get_sections_with_imrad_type(imrad)
                hist = sections_to_word_hist(sections)

            doc_length = hist.number_of_words()
            avg_doc_length = avg_doc_length_dict[imrad]


        w_ij = p_kic * p_kidi
        rank = f_iq * w_ij