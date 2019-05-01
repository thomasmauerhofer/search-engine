import time

from engine.api import API
from engine.datastore.ranking.divergence_from_randomness import DivergenceFromRandomness
from engine.datastore.ranking.mode import Mode
from engine.datastore.ranking.ranked_boolean_retrieval import RankedBoolean
from engine.datastore.ranking.tfidf import TFIDF
from engine.utils.math import mean


def evaluate_ranking_time(paper, settings):
    print("Evaluate ", settings["algorithm"])
    api = API()
    settings["mode"] = Mode.importance_to_sections
    settings["use-unclassified-chapters"] = True
    start = time.time()
    ranked_papers, queries = api.get_papers_with_paper(paper.filename, settings)
    end = time.time()
    elapsed_time = end - start
    print("Elapsed time: ", elapsed_time)


def evaluate_query_time(num_papers):
    api = API()
    papers = api.get_all_paper()[:num_papers]
    settings = TFIDF.get_default_config()
    settings["mode"] = Mode.importance_to_sections
    settings["use-unclassified-chapters"] = True

    all_elapsed_times = []
    for paper in papers:
        start = time.time()
        api.get_papers_with_paper(paper.filename, settings)
        end = time.time()
        elapsed_time = start - end
        print("Elapsed time: ", elapsed_time)
        all_elapsed_times.append(elapsed_time)

    print("Overall time: ", sum(all_elapsed_times))
    print("Mean: ", mean(all_elapsed_times))


if __name__ == "__main__":
    # evaluate_query_time(10)
    api = API()
    papers = api.get_all_paper()
    evaluate_ranking_time(papers[0], RankedBoolean.get_default_config())
    evaluate_ranking_time(papers[0], DivergenceFromRandomness.get_default_config())
