"""
# Enable network x to write out a leda graph.
# For some reason that is missing in networkx (or was)
"""
import networkx as nx
import itertools
from networkx.utils import open_file


@open_file(1, "wb")
def write_leda(G, path, encoding='utf-8', edge_type="int", node_type="string", edge_key="label"):
    """
    Write graph as a list of edges.

    Parameters
    ----------
    G : graph
       A NetworkX graph

    path : file or string
       File or filename to write. If a file is provided, it must be
       opened in 'wb' mode. Filenames ending in .gz or .bz2 will be
       compressed.

    encoding: string, optional
       Specify which encoding to use when writing file.

    Examples
    --------
    >>> G=nx.path_graph(4)
    >>> nx.write_edgelist(G, "test.edgelist")
    >>> G=nx.path_graph(4)
    >>> fh=open("test.edgelist",'wb')
    """
    for line in generate_leda(G, edge_type, node_type, edge_key):
        line += "\n"
        path.write(line.encode(encoding))


def generate_leda(G, node_type="string", edge_type="int", edge_key="label"):
    return itertools.chain(
        _generate_leda_header(G, node_type, edge_type),
        _generate_leda_nodes(G),
        _generate_leda_edges(G, edge_key)
    )


def _generate_leda_header(G, node_type="string", edge_type="int"):
    if nx.is_directed(G):
        code = "-2"
    else:
        code = "-1"

    header = ["LEDA.GRAPH", node_type, edge_type, code]
    for head in header:
        yield head


def _generate_leda_nodes(G):
    # First line.
    yield str(G.number_of_nodes())

    for node in G.nodes():
        yield _addbraket(str(node))


def _generate_leda_edges(G, edge_key="label"):
    # First line.
    yield str(G.number_of_edges())

    # Look up from node name to leda id.
    node_ids = dict(
        [(node, str(i + 1)) for i, node in enumerate(G.nodes())]
    )

    # Gather any labels for the edge data.
    edge_labels = nx.get_edge_attributes(G, edge_key)
    has_edge_labels = len(edge_labels) > 0

    # Set the labeling function.
    if has_edge_labels:
        labeler = _get_edge_label
    else:
        labeler = _get_edge_id

    for i, (node1, node2) in enumerate(G.edges()):
        # |{label1}| or |{i+1}|
        edge_label = labeler(edge_labels, (node1, node2), i)

        # Elements on the line, e.g. 1 2 0 |{label1}|
        line = (node_ids[node1], node_ids[node2], str(0),
                _addbraket(edge_label)
                )

        yield " ".join(line)


def _get_edge_label(edge_labels, edge, i):
    # Use edge label if it is present.
    try:
        edge_label = str(edge_labels[edge])
    except KeyError:
        edge_label = _get_edge_id(edge_label, edge, i)

    return edge_label


def _get_edge_id(edge_labels, edge, i):
    return str(i+1)


def _addbraket(item_str):
    return "|{" + item_str + "}|"

