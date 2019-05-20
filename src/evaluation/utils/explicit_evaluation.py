import ast
import copy
import os
from random import shuffle

from config import REQ_DATA_PATH
from engine.api import API
from engine.datastore.models.section import IMRaDType
from engine.datastore.ranking.mode import Mode
from engine.utils.printing_utils import progressBar
from evaluation.utils.evaluation_base import EvaluationBase


class ExplicitEvaluation(EvaluationBase):
    @staticmethod
    def init_dict():
        api = API()
        dict = {}
        for ranking_algo in api.ranking_algos.values():
            dict[ranking_algo.get_name()] = []
        return dict


    @staticmethod
    def raw_queries_to_queries(raw_queries):
        return raw_queries[IMRaDType.INTRODUCTION.name] + \
                  raw_queries[IMRaDType.BACKGROUND.name] + \
                  raw_queries[IMRaDType.METHODS.name] + \
                  raw_queries[IMRaDType.RESULTS.name] + \
                  raw_queries[IMRaDType.DISCUSSION.name]

    @staticmethod
    def __extract_query_ngramm(query, n):
        queries = []
        words = query.split()
        rounds = len(words) if n == 1 else len(words) - 1
        for i in range(0, rounds):
            query_list = words[i:i + n]
            if len(query_list) == n:
                query_words = " ".join(query_list)
                queries.append(query_words)
        return queries


    def create_queries(self, n=None):
        queries = {}
        with open(os.path.join(REQ_DATA_PATH, "citations.txt"), encoding='utf-8') as data_file:
            data = ast.literal_eval(data_file.read())

        for citation in data:
            for imrad_type in citation["section"]["imrad"]:
                if imrad_type not in queries:
                    queries[imrad_type] = []

                if n:
                    ngramm = self.__extract_query_ngramm(citation["search_query"], n)
                    for query in ngramm:
                        entry = {"search_query": query, "references": citation["references"], "imrad": imrad_type}
                        queries[imrad_type].append(entry)
                else:
                    entry = {"search_query": citation["search_query"], "references": citation["references"],
                             "imrad": imrad_type}
                    queries[imrad_type].append(entry)
        return queries


    # performance - TODO: move doubled parts into function
    def calculate_ranking_with_papers_from_db(self, N):
        mean_ap_whole = self.init_dict()
        mean_ap_imrad = self.init_dict()
        api = API()

        raw_queries = self.create_queries(N)
        queries = self.raw_queries_to_queries(raw_queries)

        print("# queries", len(queries))
        for i, query in enumerate(queries):
            progressBar(i, len(queries))
            relevant_paper = [api.get_paper(reference["paper_id"]) for reference in query["references"]]

            whole_search_query = api.preprocessor.proceed_queries({"whole-document": query["search_query"]})
            imrad_search_query = api.preprocessor.proceed_queries({query["imrad"]: query["search_query"]})

            # if all(not query for query in search_query.values()):
            #    return []
            whole_papers = api.client.get_paper_which_contains_queries(whole_search_query)
            imrad_papers = api.client.get_paper_which_contains_queries(imrad_search_query)

            for ranking_algo in api.ranking_algos.values():
                whole_settings = ranking_algo.get_default_config()
                imrad_settings = copy.deepcopy(whole_settings)
                whole_settings["mode"] = Mode.without_importance_to_sections
                imrad_settings["mode"] = Mode.importance_to_sections

                ranking_algo.add_papers_params(whole_papers, whole_search_query, whole_settings)
                ranking_algo.add_papers_params(whole_papers, imrad_search_query, imrad_settings)

                ranked_papers_whole = api.get_ratings(whole_papers, whole_search_query, whole_settings)
                ranked_papers_imrad = api.get_ratings(imrad_papers, imrad_search_query, imrad_settings)

                ap_whole = self.average_precision(ranked_papers_whole, relevant_paper)
                ap_imrad = self.average_precision(ranked_papers_imrad, relevant_paper)

                mean_ap_whole[ranking_algo.get_name()].append(ap_whole)
                mean_ap_imrad[ranking_algo.get_name()].append(ap_imrad)

        print(Mode.without_importance_to_sections.name.replace("_", " "))
        for algo_name, values in mean_ap_whole.items():
            result_whole = sum(values) / len(values)
            print(algo_name, " ", len(values), " ", round(result_whole, 4))

        print(Mode.importance_to_sections.name.replace("_", " "))
        for algo_name, values in mean_ap_imrad.items():
            result_imrad = sum(values) / len(values)
            print(algo_name, " ", len(values), " ", round(result_imrad, 4))


    def calculate_overall_ranking(self, raw_queries, settings):
        api = API()
        mean_ap_whole = []
        mean_ap_doc = []

        queries = self.raw_queries_to_queries(raw_queries)
        settings["mode"] = Mode.without_importance_to_sections
        settings_sec = copy.deepcopy(settings)
        settings_sec["mode"] = Mode.importance_to_sections

        for i, query in enumerate(queries):
            progressBar(i, len(queries))
            ranked_papers_whole = api.get_papers({"whole-document": query["search_query"]}, settings)
            ranked_papers_sec = api.get_papers({query["imrad"]: query["search_query"]}, settings_sec)

            relevant_paper = [api.get_paper(reference["paper_id"]) for reference in query["references"]]

            ap_whole = self.average_precision(ranked_papers_whole, relevant_paper)
            ap_doc = self.average_precision(ranked_papers_sec, relevant_paper)

            mean_ap_whole.append(ap_whole)
            mean_ap_doc.append(ap_doc)

        result_whole = sum(mean_ap_whole) / len(mean_ap_whole)
        result_doc = sum(mean_ap_doc) / len(mean_ap_doc)
        print()
        print("{} & {} & {}".format(Mode.without_importance_to_sections.name.replace("_", " "), len(mean_ap_whole),
                                    round(result_whole, 4)))
        print("{} & {} & {}".format(Mode.importance_to_sections.name.replace("_", " "), len(mean_ap_doc),
                                    round(result_doc, 4)))


    def calculate_ranking_sections(self, raw_queries, settings):
        api = API()
        mean_ap_intro, mean_ap_background, mean_ap_methods, mean_ap_result, mean_ap_discussion = [], [], [], [], []

        queries = self.raw_queries_to_queries(raw_queries)

        for i, query in enumerate(queries):
            progressBar(i, len(queries))
            relevant_paper = [api.get_paper(reference["paper_id"]) for reference in query["references"]]

            ranked_papers_intro = api.get_papers({IMRaDType.INTRODUCTION.name: query["search_query"]}, settings)
            ranked_papers_background = api.get_papers({IMRaDType.BACKGROUND.name: query["search_query"]}, settings)
            ranked_papers_methods = api.get_papers({IMRaDType.METHODS.name: query["search_query"]}, settings)
            ranked_papers_result = api.get_papers({IMRaDType.RESULTS.name: query["search_query"]}, settings)
            ranked_papers_discussion = api.get_papers({IMRaDType.DISCUSSION.name: query["search_query"]}, settings)

            ap_intro = self.average_precision(ranked_papers_intro, relevant_paper)
            ap_background = self.average_precision(ranked_papers_background, relevant_paper)
            ap_methods = self.average_precision(ranked_papers_methods, relevant_paper)
            ap_result = self.average_precision(ranked_papers_result, relevant_paper)
            ap_discussion = self.average_precision(ranked_papers_discussion, relevant_paper)

            mean_ap_intro.append(ap_intro)
            mean_ap_background.append(ap_background)
            mean_ap_methods.append(ap_methods)
            mean_ap_result.append(ap_result)
            mean_ap_discussion.append(ap_discussion)

        print()
        print("{} & {} & {}".format(Mode.only_introduction.name.replace("_", " "),
                                    len(mean_ap_intro), sum(mean_ap_intro) / len(mean_ap_intro)))
        print("{} & {} & {}".format(Mode.only_background.name.replace("_", " "),
                                    len(mean_ap_background), sum(mean_ap_background) / len(mean_ap_background)))
        print("{} & {} & {}".format(Mode.only_methods.name.replace("_", " "),
                                    len(mean_ap_methods), sum(mean_ap_methods) / len(mean_ap_methods)))
        print("{} & {} & {}".format(Mode.only_results.name.replace("_", " "),
                                    len(mean_ap_result), sum(mean_ap_result) / len(mean_ap_result)))
        print("{} & {} & {}".format(Mode.only_discussion.name.replace("_", " "),
                                    len(mean_ap_discussion), sum(mean_ap_discussion) / len(mean_ap_discussion)))


    def calculate_ranking(self, settings, n, num_of_queries=0):
        raw_queries = self.create_queries(n)

        # TODO: Don't work at the moment - Structure {IMRAD: List<querie words>}.
        # Have to be done for all imrad chapters
        if num_of_queries > 0:
            num_of_queries = len(raw_queries) if num_of_queries == 0 or num_of_queries > len(raw_queries) else num_of_queries
            shuffled_queries = raw_queries[:num_of_queries]
            shuffle(shuffled_queries)

        print(" & #queries & MAP")
        self.calculate_overall_ranking(raw_queries, settings)
        # settings["mode"] = Mode.importance_to_sections
        # calculate_ranking_sections(raw_queries, settings, plot)
