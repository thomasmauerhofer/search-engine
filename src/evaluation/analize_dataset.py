import networkx as nx

from engine.api import API


def create_graph():
    print('create graph')
    api = API()
    papers = api.get_all_paper()
    g = nx.Graph()
    g.clear()

    for paper in papers:
        references = [x.get_paper_id() for x in paper.references if x.get_paper_id()]

        for ref_id in references:
            g.add_edge(str(paper.id), str(ref_id))


    print("# nodes: ", g.number_of_nodes())
    print("# edges: ", g.number_of_edges())
    print("# components: ", len(list(nx.connected_components(g))))
    print("max degree", max(len(g.edges(node)) for node in g.nodes))
    print("diameter: ", nx.diameter(g), " (maximum eccentricity - max path)")
    print("periphery: ", len(nx.periphery(g)), " (# nodes eccentricity equal to the diameter)")


def create_directed_graph():
    print('\ncreate directed graph')
    api = API()
    papers = api.get_all_paper()
    dg = nx.DiGraph()
    dg.clear()

    for paper in papers:
        references = [x.get_paper_id() for x in paper.references if x.get_paper_id()]

        for ref_id in references:
            dg.add_edge(str(paper.id), str(ref_id))

    count_in_edges = []
    count_out_edges = []
    for node in dg.nodes:
        count_in_edges.append(len(dg.in_edges(node)))
        count_out_edges.append(len(dg.out_edges(node)))
    print("Max in_edges: ", max(count_in_edges))
    print("Max out_edges: ", max(count_out_edges))


if __name__ == "__main__":
    create_graph()
    create_directed_graph()


