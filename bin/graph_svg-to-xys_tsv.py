#!/usr/bin/env python2.7
"""
Author: Duncan McColl duncmc831@gmail.com

Convert file.svg graph output to a file.xys.tab (n_node, [x,y])

python graph-svg-to-xys-tsv.py -h for details on parameters

example usage:
    graph_svg-to-xys_tsv.py -i path/to/file.svg -o path/to/outfile.xys.tab
"""

import argparse
from xml.dom import minidom
import pandas as pd
import sys

def _parse_args():

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-i', "--infile", type=str,
        help="svg formatted file, all circles are nodes in the graph",
        required=True
    )

    parser.add_argument(
        '-o', "--outfile", type=str,
        help="3 column file tab delimited file. First is node name, "
             "second is 'x' coord, third is 'y' coord." ,
        default=None
    )

    parsed = parser.parse_args()

    return (
        parsed.infile, parsed.outfile
    )


def parse_svg(doc):
    """Retrieve node x's, node y's, and node names from doc."""

    xs = [float(circle.getAttribute('cx')) for circle in doc.getElementsByTagName('circle')]
    ys = [float(circle.getAttribute('cy')) for circle in doc.getElementsByTagName('circle')]
    names = [circle.getAttribute('class')[3:] for circle in doc.getElementsByTagName('circle')]

    return xs, ys, names

def xy_df(names, xs, ys):
    """Make an pandas xy dataframe."""
    df = pd.DataFrame([names, xs, ys]).transpose().set_index(0)
    return df

def normalize_df(df, offset=75, scale=500):
    # Set lowest number to offset
    df[1] = df[1] - df[1].min() + offset
    df[2] = df[2] - df[2].min() + offset

    # set highest number to scale
    df[1] = (df[1]/df[1].max()) * scale
    df[2] = (df[2]/df[2].max()) * scale

    return df


def main():

    filename, fout = _parse_args()

    doc = minidom.parse(filename)
    xs, ys, names = parse_svg(doc)

    df = xy_df(names, xs, ys)

    df = normalize_df(df)

    df.to_csv(fout, header=None, sep="\t")

if __name__ == "__main__":
    sys.exit(main())

