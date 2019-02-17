#!/usr/bin/env python3
# encoding: utf-8
from engine.api import API
from engine.datastore.ranking.mode import Mode
from engine.datastore.ranking.ranked_boolean_retrieval import RankedBoolean, RetrievalType
from engine.datastore.ranking.tf import TF
from engine.datastore.ranking.tfidf import TFIDF


def evaluate_tf(n=None):
    print("Term Frequency")
    evaluate_algorithm(TF.get_default_config(), n)


def evaluate_tfidf(n=None):
    print("Term Frequency-Inverse Document Frequency")
    evaluate_algorithm(TFIDF.get_default_config(), n)


def evaluate_ranked_boolean(n=None):
    print("Ranked Boolean Retrieval")
    settings = {"algorithm": RankedBoolean.get_name(),
                "extended": False,
                "ranking-algo-params": {RetrievalType.TITLE.name: 0.2,
                                        RetrievalType.SECTION_TITLE.name: 0.3,
                                        RetrievalType.SECTION_TEXT.name: 0.2,
                                        RetrievalType.SUBSECTION_TITLE.name: 0.18,
                                        RetrievalType.SUBSECTION_TEXT.name: 0.05,
                                        RetrievalType.SUBSUBSECTION_TITLE.name: 0.05,
                                        RetrievalType.SUBSUBSECTION_TEXT.name: 0.02}}
    evaluate_algorithm(settings, n)


def evaluate_explicit_search():
    for N in range(2, 5):
        print("N = ", N)
        evaluate_tf(N)
        evaluate_tfidf(N)
        evaluate_ranked_boolean(N)

    print("Full queries")
    evaluate_tf()
    evaluate_tfidf()
    evaluate_ranked_boolean()


# ---------------------------------------------------------
#                More like this
# ---------------------------------------------------------
def evaluate_algorithm_mlt(settings):
    print(" & # queries & MAP")
    api = API()
    papers = api.get_all_paper()

    settings["mode"] = Mode.without_importance_to_sections
    calculate_ranking_mlt(settings, papers)

    settings["mode"] = Mode.importance_to_sections
    print("Next line don't use unclassified chapters")
    settings["use-unclassified-chapters"] = False
    calculate_ranking_mlt(settings, papers)
    print("Next line use unclassified chapters")
    settings["use-unclassified-chapters"] = True
    calculate_ranking_mlt(settings, papers)

    # settings["mode"] = Mode.only_introduction
    # calculate_ranking_mlt(settings, papers)
    # settings["mode"] = Mode.only_background
    # calculate_ranking_mlt(settings, papers)
    # settings["mode"] = Mode.only_methods
    # calculate_ranking_mlt(settings, papers)
    # settings["mode"] = Mode.only_results
    # calculate_ranking_mlt(settings, papers)
    # settings["mode"] = Mode.only_discussion
    # calculate_ranking_mlt(settings, papers)


def evaluate_tf_mlt():
    print("Term Frequency")
    evaluate_algorithm_mlt(TF.get_default_config())


def evaluate_tfidf_mlt():
    print("Term Frequency-Inverse Document Frequency")
    evaluate_algorithm_mlt(TFIDF.get_default_config())


def evaluate_ranked_boolean_mlt():
    print("Ranked Boolean Retrieval")
    settings = {"algorithm": RankedBoolean.get_name(),
                "extended": False,
                "ranking-algo-params": {RetrievalType.TITLE.name: 0.2,
                                        RetrievalType.SECTION_TITLE.name: 0.3,
                                        RetrievalType.SECTION_TEXT.name: 0.2,
                                        RetrievalType.SUBSECTION_TITLE.name: 0.18,
                                        RetrievalType.SUBSECTION_TEXT.name: 0.05,
                                        RetrievalType.SUBSUBSECTION_TITLE.name: 0.05,
                                        RetrievalType.SUBSUBSECTION_TEXT.name: 0.02}}
    evaluate_algorithm_mlt(settings)


def evaluate_ranked_boolean_extended_mlt():
    print("Ranked Boolean Retrieval-Extended Version")
    settings = {"algorithm": RankedBoolean.get_name(),
                "extended": True,
                "ranking-algo-params": {RetrievalType.TITLE.name: 0.05,
                                        RetrievalType.SECTION_TITLE.name: 0.05,
                                        RetrievalType.SECTION_TEXT.name: 0.8,
                                        RetrievalType.SUBSECTION_TITLE.name: 0.05,
                                        RetrievalType.SUBSECTION_TEXT.name: 0.03,
                                        RetrievalType.SUBSUBSECTION_TITLE.name: 0.01,
                                        RetrievalType.SUBSUBSECTION_TEXT.name: 0.01}}
    evaluate_algorithm_mlt(settings)


def evaluate_more_like_this():
    print("More Like This")
    evaluate_tf_mlt()
    evaluate_tfidf_mlt()
    evaluate_ranked_boolean_mlt()
    # evaluate_ranked_boolean_extended_mlt()


if __name__ == "__main__":
    # evaluate_explicit_search()
    evaluate_more_like_this()
