from random import shuffle

from evaluation.utils.evaluation_base import EvaluationBase


class MltEvaluation(EvaluationBase):

    def calculate_ranking(self, settings, num_of_papers=0):
        papers = self.api.get_all_paper()
        num_of_papers = len(papers) if num_of_papers == 0 or num_of_papers > len(papers) else num_of_papers

        shuffled_papers = papers[:num_of_papers]
        shuffle(shuffled_papers)

        mean_aps = []

        for paper in papers:
            relevant_papers = [self.api.get_paper(ref.get_paper_id()) for ref in paper.references if ref.paper_id]
            if not relevant_papers:
                continue

            ranked_papers, queries = self.api.get_papers_with_paper(paper.filename, settings)
            ap = self.average_precision(ranked_papers, relevant_papers)
            if ap:
                mean_aps.append(ap)

        mean_ap = sum(mean_aps) / len(mean_aps)
        print("{} & {} & {}".format(settings["mode"].name.replace("_", " "), len(mean_aps), round(mean_ap, 4)))
