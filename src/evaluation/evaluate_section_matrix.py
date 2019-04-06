from engine.api import API
from engine.datastore.ranking.mode import Mode, Area


def get_max_number_of_papers():
    api = API()
    settings = { "mode": Mode.importance_to_sections }
    for input_area in Area:
        for search_area in Area:
            settings["input-area"] = input_area
            settings["search-area"] = search_area
            max_num_papers = 0

            # Try with each paper if there is enough information in the areas
            for paper in api.get_all_paper():
                num_found_papers = api.get_number_of_papers(paper, settings)
                if num_found_papers > 0:
                    max_num_papers += 1

            print("Input:", input_area, ",Search:", search_area, "#useable papers:", max_num_papers)



def evaluate():
    print("implement me :-(")



if __name__ == "__main__":
    get_max_number_of_papers()
