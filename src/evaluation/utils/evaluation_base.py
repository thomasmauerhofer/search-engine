from abc import ABCMeta

from matplotlib import pyplot as plt

from engine.api import API


class EvaluationBase(metaclass=ABCMeta):

    def __init__(self):
        self.api = API()


    @staticmethod
    def average_precision(ranked_papers, relevant_papers):
        indexes = []
        ap = 0
        for relevant in relevant_papers:
            try:
                indexes.append([x["paper"].file for x in ranked_papers].index(relevant.file) + 1)
            except ValueError:
                pass

            # if no relevant document can be found add 0 to MAP
            if not indexes:
                return 0.0

            indexes = sorted(indexes)
            for i in range(len(indexes)):
                ap += (i + 1) / indexes[i]

        return ap / len(indexes)


    @staticmethod
    def histogram(data, title, filename):
        _, ax = plt.subplots()
        ax.hist(data, color='#539caf')
        ax.set_ylabel("frequency")
        ax.set_xlabel("rank")
        ax.set_title(title)
        # ax.set_ylim([0, 70])
        plt.savefig(filename + ".png")
        plt.close()
