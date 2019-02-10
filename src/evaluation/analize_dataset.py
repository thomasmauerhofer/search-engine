import networkx as nx

from engine.api import API


def create_graph():
    print('create graph')
    api = API()
    papers = api.get_all_paper()
    g = nx.Graph()
    g.clear()

    g.add_nodes_from([str(paper.id) for paper in papers])
    for paper in papers:
        for ref in paper.references:
            if ref.get_paper_id():
                g.add_edge(str(ref.get_paper_id()), str(paper.id))


    # print(g.number_of_nodes())
    # print(g.number_of_edges())
    # print(len(list(nx.connected_components(g))))
    print('--------------------')
    for tmp in list(nx.connected_components(g)):
        print(len(tmp))





def create_directed_graph():
    print('create graph')
    api = API()
    papers = api.get_all_paper()
    dg = nx.DiGraph()
    dg.clear()

    dg.add_nodes_from([str(paper.id) for paper in papers])
    for paper in papers:
        for ref in paper.references:
            if ref.get_paper_id():
                dg.add_edge(str(ref.get_paper_id()), str(paper.id))


    print(dg.number_of_nodes())
    print(dg.number_of_edges())


if __name__ == "__main__":
    create_graph()
