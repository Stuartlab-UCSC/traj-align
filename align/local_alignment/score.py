
import networkx as nx
import numpy as np


def induced_scores(manytomanys, queryG, referenceG):
    """
    Provides a scores for a list of many-to-many mapping of query nodes
    to reference nodes.
    :param manytomany: list of lists of 2-tuples, many to many mapping
    of the query graph nodes (first item in the tuple) to the reference
    graph nodes (second item in the tuple).
    :param queryG: networkx graph,
    :param referenceG: networkx graph,
    :return:
    """
    scores = [induced_score(manytomany, queryG, referenceG)
              for manytomany in manytomanys]
    return scores


def induced_score(manytomany, queryG, referenceG):
    """
    Provides a score for a many-to-many mapping of query nodes to
    reference nodes.
    :param manytomany: list of 2-tuples, many to many mapping
    of the query graph nodes (first item in the tuple) to the reference
    graph nodes (second item in the tuple).
    :param queryG: networkx graph,
    :param referenceG: networkx graph,
    :return:
    """
    qnodes, refnodes = _unpack(manytomany)
    score = _score_def(
        n_graphs=_n_subgraphs_induced(referenceG, refnodes),
        q_coverage=_node_coverage(queryG, qnodes),
        redundancy=_redundancy(qnodes),
        nodes_mapped=len(set(qnodes))
    )
    return score


def _score_def(n_graphs, q_coverage, redundancy, nodes_mapped):
    """

    :param n_graphs: The number of subgraphs the query nodes mapping
    induced in the reference.
    :param q_coverage: The percent or query nodes that are present
    in a mapping.
    :param redundancy: The percentage of duplicate query nodes
    in the mapping.
    :param nodes_mapped: The number of unique query nodes mapped to the
    reference.
    :return: float
    """
    graph_hit = 1.0 / n_graphs
    return graph_hit * q_coverage * redundancy * nodes_mapped


def _redundancy(nodes):
    """
    Number of unique nodes over number of nodes.
    :param nodes: A list of strings.
    :return: float 0-1
    """
    return len(set(nodes)) / float(len(nodes))


def _node_coverage(G, node_subset):
    """
    Number of unique nodes over number of nodes in G.
    :param G: networkx graph
    :param node_subset: list of nodes present in G.
    :return: float
    """
    return len(set(node_subset)) / float(len(G))


def _n_subgraphs_induced(G, node_subset):
    """
    :param G: networkx graph
    :param node_subset: list of nodes present in G.
    :return: int of the number of subgraphs created when reducing G to
    only contain nodes in the subset.
    """
    return len(G.subgraph(np.unique(node_subset)))


def _unpack(manytomany):
    """Separate the manytomany mapping into two arrays."""
    return zip(*manytomany)
