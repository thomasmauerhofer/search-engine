from engine.datastore.ranking.bm25 import BM25
from engine.datastore.ranking.mode import Mode, Area
from engine.datastore.ranking.tfidf import TFIDF
from evaluation.utils.mlt_evaluation import MltEvaluation


def evaluate(settings):
    print("Evaluate section matrix of: ", settings["algorithm"])
    mlt_evaluation = MltEvaluation()

    settings["mode"] = Mode.areas
    for input_area in Area:
        for search_area in Area:
            print("Input:", input_area, ",Search:", search_area)
            settings["input-area"] = input_area
            settings["search-area"] = search_area
            mlt_evaluation.compute_ranking_with_settings(settings)


if __name__ == "__main__":
    # evaluate(TFIDF.get_default_config())
    evaluate(BM25.get_default_config())
