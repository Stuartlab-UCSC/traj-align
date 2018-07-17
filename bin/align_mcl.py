#!/usr/bin/env python2.7
"""
Author: Duncan McColl duncmc831@gmail.com

CLI run align_MCL

python align_mcl.py -h for details on parameters

example usage:

"""
import sys
import argparse
from align.readwrite.graph_format import read_type
from align.readwrite.similarities import read_similarities
from align.readwrite.alignments import write_pickle
from align.local_alignment.align_MCL import run as run_align_mcl
from align.local_alignment.cheat import run as run_cheat
def _parse_args():

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-q', "--query", type=str,
        help="weighted edgelist format", required=True
    )

    parser.add_argument(
        '-r', "--reference", type=str, help="weighted edgelist format",
        default=None
    )

    parser.add_argument(
        '-s', "--similarity", type=str, help="",
    )

    parser.add_argument(
        '-o', "--output", type=str, help="",
    )
    parser.add_argument(
        '-t', "--type", type=str, default="cheat", help="",
    )
    parsed = parser.parse_args()

    return (
        parsed.query, parsed.reference, parsed.similarity, parsed.output,
        parsed.type
    )


align_funcs = {
    "cheat": run_cheat,
    "mcl" : run_align_mcl
}

def main():

    query, reference, similarity, fout, align_type = _parse_args()

    queryG, referenceG = read_type(query), read_type(reference)
    sim = read_similarities(similarity)

    run = align_funcs[align_type]
    alignments = run(queryG, referenceG, sim)
    write_pickle(fout, alignments)


if __name__ == "__main__":
    sys.exit(main())
