
import pickle


def read_align_MCL(file, queryG):
    """
    Reads the output of align mcl into a lists of list
     [(query_graph_node, reference_graph_node)..]
    :param file:
    :param queryG:
    :param referenceG:
    :return:
    """
    with open(file, 'rb') as fh:
        # Arrays for each line representing a many to many mapping.
        output = []
        # Each line looks like:
        # query_graph_node/reference_graph_node\t...
        # which is turned into [(query_graph_node, reference_graph_node)..]
        for line in fh:
            output.append(
                map(
                    lambda x: tuple(x.split("/")),
                    line.strip().split("\t")
                )
            )


    def switch(tuple):
        if tuple[1] in queryG.nodes():
            return (tuple[1], tuple[0])
        return (tuple[0], tuple[1])

    for i, alignment in enumerate(output):
        output[i] = map(switch, alignment)

    return output


def read_pickle(file):
    with open(file, "rb") as fh:
        alignment_output = pickle.load(fh)
    return alignment_output


def write_pickle(file, alignment_output):
    with open(file, "wb") as fh:
        pickle.dump(alignment_output, fh)
