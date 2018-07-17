#!/usr/bin/env python2.7
"""
Author: Duncan McColl duncmc831@gmail.com

Convert graph format. Specifically a weighted edge list file format
into a .gexf file format.

Check wel-to-gexf.py -h for args.
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
        help="",
        required=True
    )

    parser.add_argument(
        '-o', "--outfile", type=str,
        help="",
        default=None
    )

    parsed = parser.parse_args()

    return (
        parsed.infile, parsed.outfile
    )


def main():

    filename, fout = _parse_args()

    import align.readwrite.graph_format as inout
    G = inout.read_type(filename, "edgelist")
    inout.write_type(G, fout, "gexf")

if __name__ == "__main__":
    sys.exit(main())

