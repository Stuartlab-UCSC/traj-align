"""

todo: messy use of passing bin path to script to avoid needing to set
the path for the alignment script, see where bin_path() is called...
"""
import subprocess
import os
from align.readwrite import tmp


def run(queryG, refG, sim_df, clean_up=True):
    """

    :param queryG:
    :param refG:
    :param similarity:
    :param clean_up: boolean, get rid of script output (default False)
    :return:
    """
    tmp_path_query = tmp.write_graph(queryG)
    tmp_path_reference = tmp.write_graph(refG)
    tmp_path_sim = tmp.write_sim(sim_df)
    outfile = tmp.output()
    bin_path = align_bin()
    align_script = align_MCL_path(bin_path)
    subprocess.call([
        align_script, tmp_path_query, tmp_path_reference, tmp_path_sim,
        outfile, bin_path
    ])

    output = gather_output_align_MCL(outfile, queryG)

    if clean_up:
        tmp.clean_up()

    return output


def align_bin():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_path, "bin")
    return path


def align_MCL_path(bin_path):
    align_script = os.path.join(bin_path, "alignMCL.sh")
    return align_script


def gather_output_align_MCL(outpath, queryG):
    """
    Create many to many mappings from the output of alignMCL.
    :param outpath:
    :return: A list of lists with 2-tuples in the form of:
     [
        [(query_graph_node, reference_graph_node), ...],
     ...]
    """
    from align.readwrite.alignments import read_align_MCL
    outpath += ".txt"
    return read_align_MCL(outpath, queryG)


