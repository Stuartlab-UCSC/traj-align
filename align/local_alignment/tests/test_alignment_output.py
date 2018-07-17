"""
todo: Need to get the hard coded paths (and reading ggraphs in general)
out of here, hard code some data that will run.
Author: Duncan McColl duncmc831@gmail.com

These tests make sure that the output of python wrappers for alignment
algorithms is a list of lists containing 2-tuples.

To add a new test, simply import your module and add the wrapper to
"alignment_functions" below. You need to follow the call signature of
align_MCL.run for this to work. If you got here without realizing this,
you can get a quick look at the call signature with:

>>> from align.local_alignment import align_MCL
>>> help(align_MCL.run)
"""
from local_alignment import align_MCL

alignment_functions = [
    align_MCL.run
]

msg = "Assertion failed in function: {0}"

# Some data that didn't work testing the outputs.
"""
    G1 = nx.path_graph(5)
    G2 = nx.path_graph(10)
    sim = pd.DataFrame(
        [
            [0, 4, .8],
            [0, 3, .4],
            [0, 2, .1],
            [1, 5, .9],
            [1, 6, .3],
            [1, 4, .6],
            [2, 8, .6],
            [2, 9, .9],
            [3, 1, .4],
            [3, 2, .5],
            [4, 9, .9],
            [4, 8, .6]
        ]
    )
    """


def test_alignment_outputs():
    from readwrite import graph_format
    rg = graph_format.read_type("../../../data/mock-ref.wel", "edgelist")
    n = "/home/duncan/trajectory/traj-restapi/data/toy-graphs/linear-6.ef"
    from similarity import node_names
    qg = graph_format.read_type(n, "edgelist")
    sim = node_names.similarity(qg.nodes(), rg.nodes())

    for func in alignment_functions:
        assert output_is_valid(func(qg, rg, sim))


def output_is_valid(output):
    """
    Checks that output is a list of lists containing 2-tuples
    :param output: the output from an alignment algorithm
    :return: boolean
    """

    is_correct = type(output) is list
    for member in output:
        is_correct *= type(member) is list
        for item in member:
            is_correct *= type(item) is tuple and len(item) == 2

    return bool(is_correct)