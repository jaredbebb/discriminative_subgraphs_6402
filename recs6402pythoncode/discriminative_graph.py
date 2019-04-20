import networkx as nx
import sys
import os
import json
from collections import deque
import heapq
import math
from os import listdir
from os.path import isfile, join


def graph_stats(graphs):
    nodes = {}
    edges = {}

    for g in graphs:
        for n in g.nodes():
            nodes[n] = nodes.get(n, 0) + 1
        for e in g.edges():
            edges[e] = edges.get(e, 0) + 1
    return nodes, edges


def build_dgraph(verts, edges, count):
    disc_graph = nx.DiGraph()
    for v in verts:
        if verts[v] == count:
            disc_graph.add_node(v)
    for e in edges:
        if edges[e] == count:
            disc_graph.add_edge(*e)
    return disc_graph


def contains_subgraph(G, edges):
    return all(map(lambda x: G.has_edge(*x), edges))


def augment_subgraph(g, freq_edges):
    return [g + [e] for e in freq_edges if e[0] == g[-1][1]]


def create_discriminative_graph(S1, S2):
    print('Comparing a set of', len(S1), 'graphs to a set of', len(S2), 'graphs')

    vinc, einc = graph_stats(S1)  # do we even need vinc?  is there a more efficient way of generating this info?
    freq_edges = {e for e in einc if einc[e] == len(S1)}
    # print('freq_edges is ', freq_edges)
    freq_sg = deque([[e] for e in freq_edges])
    result = nx.DiGraph()

    # print(len(freq_sg))
    print(len(freq_sg))
    while not len(freq_sg) == 0:
        sg = freq_sg.popleft()
        if not any(map(lambda g: contains_subgraph(g, sg), S2)):
            result.add_edges_from(sg)
            # freq_sg.clear()  # Don't stop, find longest sg!
        else:
            freq_sg.extend(augment_subgraph(sg, freq_edges))
    return result


def relaxed_create_discriminative_graph(S1, S2, threshold):
    vinc, einc = graph_stats(S1)  # do we even need vinc?  is there a more efficient way of generating this info?
    freq_edges = {e for e in einc if einc[e] == len(S1)}
    freq_sg = deque([[e] for e in freq_edges])
    result = nx.DiGraph()
    while not len(freq_sg) == 0:
        sg = freq_sg.popleft()
        if sum(map(lambda g: contains_subgraph(g, sg), S2)) < threshold:
            result.add_edges_from(sg)
            # freq_sg.clear()  # Don't stop, find longest sg!
        else:
            freq_sg.extend(augment_subgraph(sg, freq_edges))
    return nx.DiGraph()


def make_discriminative_graph(good_dir, bad_dir):
    good_files = [f for f in listdir(good_dir) if isfile(join(good_dir, f))]
    bad_files = [f for f in listdir(bad_dir) if isfile(join(bad_dir, f))]

    good_graphs = [nx.read_edgelist(join(good_dir, f), create_using=nx.DiGraph()) for f in good_files]
    bad_graphs = [nx.read_edgelist(join(bad_dir, f), create_using=nx.DiGraph()) for f in bad_files]

    # Find edges that ALL graphs (good and bad)
    # have in common
    non_disc_edges = set(good_graphs[0].edges())
    for g in good_graphs + bad_graphs:
        non_disc_edges &= set(g.edges())
    print('Edges that ALL graphs have in common: ', non_disc_edges, '\n')

    # Remove edges that ALL graphs have in common
    # and remove nodes that have 0 indegree and 0 outdegree
    for g in good_graphs:
        g.remove_edges_from(non_disc_edges)
        g.remove_nodes_from(list(nx.isolates(g)))

    for g in bad_graphs:
        g.remove_edges_from(non_disc_edges)
        g.remove_nodes_from(list(nx.isolates(g)))

    print('Looking for discriminative graph in bad graphs...')
    dgraph = create_discriminative_graph(bad_graphs, good_graphs)
    if len(dgraph.nodes()) == 0:
        print('\nHaving to relax constraints to try to find')
        print('discriminative graph in bad graphs...')
        thresholdGoods = (len(good_graphs) + 1) // 4
        print('Threshold = ', thresholdGoods)
        dgraph = relaxed_create_discriminative_graph(bad_graphs, good_graphs, thresholdGoods)

    if len(dgraph.nodes()) == 0:
        print('\nNow having to look for discriminative graph')
        print('in good graphs...')
        dgraph = create_discriminative_graph(good_graphs, bad_graphs)

    if len(dgraph.nodes()) == 0:
        print('\nHaving to relax constraints to try to find')
        print('discriminative graph in good graphs...')
        thresholdBads = (len(bad_graphs) + 1) // 4
        print('Threshold = ', thresholdBads)
        dgraph = relaxed_create_discriminative_graph(good_graphs, bad_graphs, thresholdBads)

    print('\nHere is resulting discriminative graph:')
    return dgraph


if __name__ == "__main__":
    #print(make_discriminative_graph('c:/DiscMining/good', 'c:/DiscMining/bad').edges())
    print(make_discriminative_graph('D:/Documents/Pycharm_Projects/discriminative_subgraphs_6402/data/formula_one/good', 'D:/Documents/Pycharm_Projects/discriminative_subgraphs_6402/data/formula_one/bad').edges())
    #print(make_discriminative_graph('D:/Downloads/graphs/good', 'D:/Downloads/graphs/bad').edges())
    #print(make_discriminative_graph(sys.argv[1], sys.argv[2]).edges())
