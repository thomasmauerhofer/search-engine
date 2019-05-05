import statistics

import matplotlib
import networkx as nx
import seaborn as sns
from matplotlib import pyplot as plt

from engine.api import API
from engine.utils.math import mean


def create_degree_distribution(data, title, color, subplot_x_min, subplot_x_max, subplot_y_max):
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    matplotlib.rcParams['font.size'] = 18
    matplotlib.rcParams['axes.linewidth'] = 2

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.distplot(
        data,
        kde=False, norm_hist=False,
        bins=max(data),
        hist_kws=dict(align='mid', alpha=1, color=color),
    )

    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    ax.set_title(title)
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
        hist_kws=dict(align='mid', alpha=1, color=color),
        ax=a
    )

    a.tick_params('both', length=8, width=2, which='major')
    a.tick_params('both', length=8, width=2, which='minor')
    a.set_ylim(0, subplot_y_max)
    a.set_xlim(subplot_x_min, subplot_x_max)
    a.set_xlabel('degree of node')
    a.set_ylabel('# nodes')

    plt.tight_layout()
    plt.savefig(title.replace(" ", "_").lower() + '.pdf', dpi=600)
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

    degrees = [len(g.edges(node)) for node in g.nodes]

    for degree in degrees:
        if degree == 0:
            print("nope!")

    print("# nodes: ", g.number_of_nodes())
    print("# edges: ", g.number_of_edges())
    print("# components: ", len(list(nx.connected_components(g))))
    print("max degree: ", max(degrees))
    print("mean degree: ", round(mean(degrees), 4))
    print("median degree: ", statistics.median(degrees))
    print("diameter: ", nx.diameter(g), " (maximum eccentricity - max path)")
    print("periphery: ", len(nx.periphery(g)), " (# nodes eccentricity equal to the diameter)")
    create_degree_distribution(degrees, 'Degree Distribution', '#00365A', 13, 100, 3.5)


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

    # Data cleaning - if not done 5 papers which cite each other in dataset
    # preprints cited each other
    dg.remove_edge('5c52a9b9bf51c50be97c5145', '5c529cbdbf51c5359dce35f3')
    dg.remove_edge('5b0565406919df52a704f32c', '5b05673b6919df52a704f375')
    dg.remove_edge('5b97b226bf51c561194d9f1f', '5b05682a6919df52a704f395')
    dg.remove_edge('5c52a4f9bf51c50be97c5111', '5c533345bf51c5335baca21a')
    dg.remove_edge('5b97b0aebf51c561194d9f09', '5b97b31ebf51c561194d9f2a')
    print("# nodes: ", dg.number_of_nodes())
    print("# edges: ", dg.number_of_edges())
    print("# cycles: ", len(list(nx.simple_cycles(dg))))
    print("# strongly connected components: ", len(list(nx.strongly_connected_components(dg))))
    print("Dag longest path: ", len(nx.dag_longest_path(dg)))

    in_degrees = []
    out_degrees = []
    root_nodes = []
    for node in dg.nodes:
        if len(dg.in_edges(node)) > 0:
            in_degrees.append(len(dg.in_edges(node)))

        if len(dg.out_edges(node)) > 0:
            out_degrees.append(len(dg.out_edges(node)))

        if len(dg.out_edges(node)) == 0:
            root_nodes.append(node)

    print("# root nodes: ", len(root_nodes))
    print("In Degree:")
    print("  max degree: ", max(in_degrees))
    print("  mean degree: ", round(mean(in_degrees), 4))
    print("  median degree: ", statistics.median(in_degrees))
    print("\nOut Degree:")
    print("  max degree: ", max(out_degrees))
    print("  mean degree: ", round(mean(out_degrees), 4))
    print("  median degree: ", statistics.median(out_degrees))
    create_degree_distribution(in_degrees, 'In-Degree Distribution', '#33691e', 6, 100, 10)
    create_degree_distribution(out_degrees, 'Out-Degree Distribution', '#e65100', 7, 13.5, 6.5)


def print_circles(circles):
    api = API()
    tmp = []
    for circle in circles:
        tmp_circle_array = []
        for node in circle:
            tmp_circle_array.append(api.get_paper(node).filename)
        tmp.append(tmp_circle_array)
    print(tmp)
    print(circles)


if __name__ == "__main__":
    # create_graph()
    create_directed_graph()
