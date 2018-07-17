
import numpy.random as rand

from align.similarity.model import true_mapping
def run(queryG, refG, sim_df):
    alignments = []
    alignment=[]
    true_map = true_mapping(queryG.nodes())
    # Makes a true 1-1 alignment
    for node in true_map.keys():
        alignment.append((node, true_map[node]))

    alignments.append(alignment)
    # Makes a true 1-neighbors alignment
    alignment=[]
    for node in true_map.keys():
        matching_node = true_map[node]
        alignment.append((node, matching_node))
        for neighbor in refG.neighbors(matching_node):
            alignment.append((node, neighbor))

    alignments.append(alignment)

    # Random mix of a true 1-1  alignment
    alignment=[]
    true_nodes = true_map.values()
    for node in true_map.keys():
        matching_node = rand.choice(true_nodes, 1)[0]
        alignment.append((node, matching_node))

    alignments.append(alignment)

    # Random 1->3 mapping
    alignment=[]
    true_nodes = refG.nodes()
    for node in true_map.keys():
        matching_nodes = rand.choice(true_nodes, 3)
        for matching_node in matching_nodes:
            alignment.append((node, matching_node))

    alignments.append(alignment)

    return alignments