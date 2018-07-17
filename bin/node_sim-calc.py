#!/usr/bin/env python2.7
"""
Author: Duncan McColl duncmc831@gmail.com

CLI to calculate all-by-all cosine similarity.

python node_sim-calc.py -h for details on parameters

example usage:

# For self similarity of columns:
node_sim-calc.py -X $HOME/path/to/some-matrix.tab -o ./cosine-somematrix.tab
"""
import sys
import pandas as pd
import argparse
from align.similarity import cosine
import align.similarity.model as sim


def _parse_args():

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-X', "--matrix1", type=str,
        help="tab delimited matrix file.", required=True
    )

    parser.add_argument(
        '-Y', "--matrix2", type=str, help="tab delimited matrix file.",
        default=None
    )
    """
    parser.add_argument(
        '-m', "--metric", type=str, help="", default="cosine"
    )
    """
    parser.add_argument(
        '-o', "--output", type=str, help="", default="ortho-format.tab"
    )
    """
    parser.add_argument(
        '-r',
        "--cols",
        type=bool,
        help="Flag to produce row similarity.  By default the columns "
             "are the objects to be compared.",
        default=True
    )
    """

    parsed = parser.parse_args()

    return (
        parsed.matrix1, parsed.matrix2, parsed.output,

    )


def read_df(filename, index=None):
    """"""
    if filename is None:
        return None

    return pd.read_table(filename, index_col=index)


def _transpose_both(df1, df2=None):
    if df2 is None:
        return df1.transpose(), None
    return df1.transpose(), df2.transpose()

import align.similarity as sim

funcs = {
    sim.cosine.calculate,
    sim.model.calculate
}

def main():

    matrix1, matrix2, fout = _parse_args()

    df1 = read_df(matrix1)
    df2 = read_df(matrix2)


    df1, df2 = _transpose_both(df1, df2)

    df1, df2 = cosine.enforce_equal_ncol(df1, df2)

    #similarities = cosine.calculate(df1, df2)
    noise = lambda x: 0
    similarities = sim.model.calculate(df1, df2, noise, sim.model.true_mapping(df1.index))
    similarities.to_csv(fout, sep="\t")


if __name__ == "__main__":
    sys.exit(main())
