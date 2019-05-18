import statistics

import matplotlib
import networkx as nx
import seaborn as sns
from matplotlib import pyplot as plt

from engine.api import API
from engine.utils.math import mean


def create_degree_distribution(data, title, color, subplot_x_min=None, subplot_x_max=None, subplot_y_max=None):
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

    # ax.set_title(title)
    ax.set_xlabel('degree')
    ax.set_ylabel('# nodes')

    ax.tick_params('both', length=8, width=2, which='major')
    ax.tick_params('both', length=8, width=2, which='minor')

    sns.despine(offset=4, trim=False)

    if subplot_x_min and subplot_x_max and subplot_y_max:
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
        a.set_xlabel('degree')
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
    create_degree_distribution(in_degrees, 'In-Degree Distribution', '#33691e', 20, 100, 10)
    create_degree_distribution(out_degrees, 'Out-Degree Distribution', '#e65100')


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


def __is_word_in_titles(titles, words):
    for title in titles:
        for word in words:
            if word in title:
                return word
    return None


def analize_chapters():
    api = API()
    papers = api.get_all_paper()
    introduction, background, methods, result, discussion = {}, {}, {}, {}, {}
    print("# papers: ", len(papers))
    for paper in papers:
        intro_titles = [sec.heading_proceed for sec in paper.get_introduction()]
        back_titles = [sec.heading_proceed for sec in paper.get_background()]
        methods_titles = [sec.heading_proceed for sec in paper.get_methods()]
        result_titles = [sec.heading_proceed for sec in paper.get_results()]
        discuss_titles = [sec.heading_proceed for sec in paper.get_discussion()]

        intro_word = __is_word_in_titles(intro_titles, ["introduct"])
        back_word = __is_word_in_titles(back_titles, ["relat work", "background"])
        methods_word = __is_word_in_titles(methods_titles, ["method", "approach", "model"])
        results_word = __is_word_in_titles(result_titles, ["result", "experi", "evalu"])
        discuss_word = __is_word_in_titles(discuss_titles, ["discuss", "conclus", "futur work"])

        if intro_word:
            introduction[intro_word] = introduction[intro_word] + 1 if intro_word in introduction else 1

        if back_word:
            background[back_word] = background[back_word] + 1 if back_word in background else 1

        if methods_word:
            methods[methods_word] = methods[methods_word] + 1 if methods_word in methods else 1

        if results_word:
            result[results_word] = result[results_word] + 1 if results_word in result else 1

        if discuss_word:
            discussion[discuss_word] = discussion[discuss_word] + 1 if discuss_word in discussion else 1

    print("introduction:")
    print_imrad(introduction, len(papers))
    print("related work:")
    print_imrad(background, len(papers))
    print("methods:")
    print_imrad(methods, len(papers))
    print("result:")
    print_imrad(result, len(papers))
    print("discussion:")
    print_imrad(discussion, len(papers))


def print_imrad(imrad, all_papers):
    sum_imrad = sum(imrad.values())
    print("All:", sum_imrad, "papers, ", round(sum_imrad / all_papers * 100, 2), "%")
    for key in imrad:
        print(key, ":", imrad[key], "papers", round(imrad[key] / all_papers * 100, 2), "%")


if __name__ == "__main__":
    # create_graph()
    create_directed_graph()
    # analize_chapters()
