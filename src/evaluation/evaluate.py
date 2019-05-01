#!/usr/bin/env python3
# encoding: utf-8
from optparse import OptionParser

from engine.datastore.ranking.bm25 import BM25
from engine.datastore.ranking.divergence_from_randomness import DivergenceFromRandomness
from engine.datastore.ranking.ranked_boolean_retrieval import RankedBoolean, RetrievalType
from engine.datastore.ranking.tf import TF
from engine.datastore.ranking.tfidf import TFIDF
from evaluation.utils.explicit_evaluation import ExplicitEvaluation
from evaluation.utils.mlt_evaluation import MltEvaluation


def evaluate_algorithm(settings):
    explicit_evaluation = ExplicitEvaluation()
    mlt_evaluation = MltEvaluation()

    for N in range(2, 5):
        print("N = ", N)
        explicit_evaluation.calculate_ranking(settings, N)

    # print("Full queries")
    # explicit_evaluation.calculate_ranking(settings, None)

    print("More Like This")
    mlt_evaluation.calculate_ranking(settings)


def evaluate_bm25():
    settings = BM25.get_default_config()

    settings["k1"] = 1.2
    print("BM25 - b: 0.75, k1: 1.2")
    evaluate_algorithm(settings)

    settings["k1"] = 2.0
    print("BM25 - b: 0.75, k1: 2.0")
    evaluate_algorithm(settings)


def evaluate_tf():
    print("Term Frequency")
    evaluate_algorithm(TF.get_default_config())


def evaluate_tfidf():
    print("Term Frequency-Inverse Document Frequency")
    evaluate_algorithm(TFIDF.get_default_config())


def evaluate_dfr():
    print("Divergence from Randomness")
    evaluate_algorithm(DivergenceFromRandomness.get_default_config())


def evaluate_ranked_boolean():
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
    evaluate_algorithm(settings)


def evaluate_ranked_boolean_extended():
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
    evaluate_algorithm(settings)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-a", "--all", action="store_true", dest="all", default=False, help="Evaluate all algorithms")
    parser.add_option("-b", "--bm25", action="store_true", dest="bm25", default=False, help="Evaluate BM25")
    parser.add_option("-t", "--tf", action="store_true", dest="tf", default=False, help="Evaluate TF")
    parser.add_option("-i", "--tfidf", action="store_true", dest="tfidf", default=False, help="Evaluate TFIDF")
    parser.add_option("-r", "--rbr", action="store_true", dest="rbr", default=False, help="Evaluate Ranked BooleanRetrieval")
    parser.add_option("-d", "--dfr", action="store_true", dest="dfr", default=False, help="Evaluate Divergence from Randomness")
    (options, args) = parser.parse_args()

    if options.all or options.bm25:
        evaluate_bm25()
    if options.all or options.tf:
        evaluate_tf()
    if options.all or options.tfidf:
        evaluate_tfidf()
    if options.all or options.rbr:
        evaluate_ranked_boolean()
        # evaluate_ranked_boolean_extended()
    if options.all or options.dfr:
        evaluate_dfr()
