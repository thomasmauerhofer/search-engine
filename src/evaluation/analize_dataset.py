import matplotlib
import networkx as nx
import seaborn as sns
from matplotlib import pyplot as plt

from engine.api import API


def create_degree_distribution(data):
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    matplotlib.rcParams['font.size'] = 18
    matplotlib.rcParams['axes.linewidth'] = 2

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.distplot(
        data,
        kde=False, norm_hist=False,
        bins=max(data),
        hist_kws=dict(align='mid', alpha=1, color='#00365A'),
    )

    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    ax.set_title('Degree Distribution')
    ax.set_xlabel('degree of node')
    ax.set_ylabel('# nodes')

    ax.tick_params('both', length=8, width=2, which='major')
    ax.tick_params('both', length=8, width=2, which='minor')

    sns.despine(offset=4, trim=False)

    a = plt.axes([0.45, 0.45, 0.45, 0.35])
    sns.distplot(
        data,
        kde=False, norm_hist=False,
        bins=max(data),
        hist_kws=dict(align='mid', alpha=1, color='#00365A'),
        ax=a
    )

    a.tick_params('both', length=8, width=2, which='major')
    a.tick_params('both', length=8, width=2, which='minor')
    a.set_ylim(0, 3)
    a.set_xlim(20, 100)
    a.set_xlabel('degree of node')
    a.set_ylabel('# nodes')

    plt.tight_layout()
    plt.savefig('degree_distribution.pdf', dpi=600)
    plt.show()


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
    create_degree_distribution([len(g.edges(node)) for node in g.nodes])


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
    # create_directed_graph()


