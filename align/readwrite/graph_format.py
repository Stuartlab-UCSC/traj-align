"""
author: Duncan McColl duncmc831@gmail.com

An interface to change the text format representation of a graph.

Main usage as a command line script.

Tab delimeters are expected from any format with a delimeter.
Ex:
graphformat.py --from adjlist --to xdef -i input.adj -o input.xdef
"""

import networkx as nx
from writeleda import write_leda

delimiter = "\t"

_keys = [
    "adjlist",
    "edgelist",
    "gexf",
    "gml",
    "gpickle",
    "graphml",
    "leda"
]
# Hold a bunch of a pointers for functions so we can tie the I/O
# together.
_read_funcs = dict(zip(_keys, [
        nx.read_adjlist, # Path.
        lambda path: nx.read_weighted_edgelist(path, delimiter=delimiter),
        nx.read_gexf,
        nx.read_gml,
        nx.read_gpickle,
        nx.read_graphml,
        nx.read_leda # Might be parse.
        ]
    )
)


_write_funcs = dict(zip(_keys, [
        nx.write_adjlist, # G, Path.
        lambda G, path: nx.write_weighted_edgelist(G, path, delimiter=delimiter),
        nx.write_gexf,
        nx.write_gml,
        nx.write_gpickle,
        nx.write_graphml,
        write_leda
        ]
    )
)


def read_type(filename, type="edgelist"):
    return _read_funcs[type](filename)


def write_type(G, path, type="edgelist"):
    return _write_funcs[type](G, path)

