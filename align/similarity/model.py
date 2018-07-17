
from itertools import product as cartesian_product
import pandas as pd



def calculate(queryDF, referenceDF, noise_gen, true_mapping={}):

    query_nodes, ref_nodes = queryDF.index, referenceDF.index

    sims = []
    tups = []
    for qnode, rnode in cartesian_product(query_nodes, ref_nodes):
        tups.append((qnode, rnode))
        if qnode in true_mapping and rnode == true_mapping[qnode]:
            sims.append(1)
        else:
            sims.append(noise_gen(0))


    indecies = pd.MultiIndex.from_tuples(tups)

    df = pd.Series(sims, index=indecies).unstack(level=-1)
    return df


def true_mapping(qnodes):

    true_lables = [qnode[2:] for qnode in qnodes]
    true_map = dict(zip(qnodes, true_lables))
    return true_map