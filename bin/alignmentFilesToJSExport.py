#!/usr/bin/env python2.7
"""
Author: Duncan McColl duncmc831@gmail.com

Convert all alignment files to a .js importable javascript object.

The code is a quick patch to avoid needing any sort of server or parser
for the prototype trajectory-viewer app.

example usage:

"""
import numpy as np
import pandas as pd
import argparse
import sys
from align.readwrite.graph_format import read_type
from align.readwrite.alignments import read_pickle


def _parse_args():

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-x', "--xys", type=str,
        help="Tab sep 3 column matrix where first is node name, second"
             " is  x coord, third is y coord. Right now this is for"
             "BOTH GRAPHS.",
        default="../data/now.x"
    )

    parser.add_argument(
        '-s', "--similarity", type=str,
        help="Similarity between nodes in query graph and reference "
             "graph. Can be in weighted edgelist format or a full "
             "adjacency list format.",
        default="../data/now.s"
    )

    parser.add_argument(
        '-q', "--query", type=str,
        help="Query graph. Weighted edge file format.",
        default="../data/now.q"
    )

    parser.add_argument(
        '-r', "--reference", type=str,
        help="Reference graph. Weighted edge file format.",
        default="../data/now.r"
    )

    parser.add_argument(
        '-a', "--alignment", type=str,
        help="Output from align_MCL script (output.txt)",
        default="../data/now.a"
    )

    parser.add_argument(
        '-o', "--output", type=str,
        help="The importable .js output file.",
        required=True
    )
    parsed = parser.parse_args()

    return (
        parsed.alignment, parsed.reference, parsed.query, parsed.xys,
        parsed.similarity, parsed.output
    )


def main():

    alignment, reference, query, xys, similarity, fout = _parse_args()
    """
    similarity = "/home/duncan/Downloads/mn_sc_full_ortho.txt"
    query = "/home/duncan/Downloads/mn_trajectory.txt"
    reference = "/home/duncan/Downloads/hi_RG_PC_Trajectory.txt"
    alignment = "/home/duncan/trajectory/alignment/AlignMCL-1.2/test/out-actual"
    fout = "trash_fout.js"
    xys = "./data/layout/xys.ref.tab"
    """

    xys_df = pd.read_table(xys, index_col=0, header=None)
    queryG = read_type(query, type="edgelist")
    referenceG = read_type(reference, type="edgelist")

    alignments = read_pickle(alignment)


    simDF = pd.read_table(similarity, index_col=0).transpose()

    # # This assumes you have an edgelist read in and changes it to full.
    #simDF = pd.DataFrame(index=set(graph_sim_df[0]), columns=set(graph_sim_df[1]))
    #for row in graph_sim_df.index:
    #    simDF.loc[graph_sim_df.loc[row,0], graph_sim_df.loc[row,1]] = graph_sim_df.loc[row,2]

    # Make dictionaries to keep track of the indecies, they end up
    # being keys in the .js so muy importante.
    graph1_node_to_index = dict(
        zip(
            simDF.columns,
            range(len(simDF.columns))
        )
    )
    graph2_node_to_index = dict(
        zip(
            simDF.index,
            range(len(simDF.index))
        )
    )
    # Begin writing out all of the things... best close your eyes from
    # this point on.
    fout = open(fout, "w")

    fout.write(
"""const NODECOLOR = "#2e5e2c"
const NODEBORDER = "#33a12d"
const NODESIZE_Q = 10
const NODESIZE_R = 4\n\n"""
    )
    fout.write("export default {\n")
    fout.write("\tgraphL: { nodes: [\n")
    for node in simDF.columns:

        nodex, nodey = str(xys_df.loc[node, 1]), str(xys_df.loc[node, 2])
        fout.write("\t\t{ name: '" + str(node) + "', x: '"+nodex+"', y:'"+nodey+"', size: NODESIZE_Q, color: NODECOLOR},\n")

    fout.write("\t],\n edges: [\n")

    for (node1, node2) in queryG.edges():

        node1 = graph1_node_to_index[node1]
        node2 = graph1_node_to_index[node2]
        fout.write("\t\t{ node1: " +str(node1)+ ", node2: " + str(node2) + "},\n")

    fout.write("\t],\n\t},\n")


    fout.write("\tgraphR: { nodes: [\n")

    for node in simDF.index:
        node=str(node)
        nodex, nodey = str(xys_df.loc[node, 1]), str(xys_df.loc[node, 2])
        fout.write("\t\t{ name: '" + str(node) + "', x: '"+nodex+"', y:'"+nodey+"', size: NODESIZE_R, color: NODECOLOR},\n")

    fout.write("\t],\n edges: [\n")

    for (node1, node2) in referenceG.edges():

        node1 = graph2_node_to_index[node1]
        node2 = graph2_node_to_index[node2]
        fout.write("\t\t{ node1: " +str(node1)+ ", node2: " + str(node2) + "},\n")

    fout.write("\t],\n\t},\nsim: { graphL : [\n")

    simDF = simDF.transpose()
    for row in simDF.index:
        normed = simDF.loc[row] / simDF.loc[row].sum()
        fout.write(str(normed.tolist()) + ",\n")

    fout.write("],\ngraphR : [\n")
    for col in simDF.columns:
        normed = simDF[col] / simDF[col].sum()
        if simDF[col].sum() == 0:
            normed = pd.Series(np.repeat(0, len(simDF[col])))
        fout.write(str(normed.tolist()) + ",\n")

    fout.write("]\n},")

    fout.write("\nalignments: [\n")

    from align.local_alignment.score import induced_score
    for manytomany in alignments:

        score = induced_score(manytomany, queryG, referenceG)
        fout.write("{ score: " + str(score)+ ",\nalignment: [\n")
        for alignment in manytomany:
            nodeIdQ, nodeIdR = alignment[0], alignment[1]
            fout.write("{ nodeIdR: " + str(graph2_node_to_index[nodeIdR]) + ", nodeIdL: " + str(graph1_node_to_index[nodeIdQ]) + "},\n")

        fout.write("]\n},")

    fout.write("]\n}")

    fout.close()


if __name__ == "__main__":
    sys.exit(main())

