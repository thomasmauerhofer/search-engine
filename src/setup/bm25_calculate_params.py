from random import shuffle

from engine.api import API

if __name__ == "__main__":
    api = API()
    random_papers = api.get_all_paper()[:10]
    shuffle(random_papers)
    print(random_papers[0].id)
    shuffle(random_papers)
    print(random_papers[0].id)
    shuffle(random_papers)
    print(random_papers[0].id)



