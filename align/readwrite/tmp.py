"""
Convenience functions to work with temp directories, specificly intended
 for wrapper scripts in the local alignment directory.

 Note that right now when you import this module a temp directory will
 be created in the location of the "local_alignment" module of this
 package.

 The clean_up() function removes this directory.
"""
import os
import tempfile
import errno
from align.readwrite import graph_format
import align.local_alignment as local_alignment
import shutil

dir_path = os.path.dirname(os.path.realpath(local_alignment.__file__))
tmp_path = os.path.join(dir_path, "tmp")


def make_tmp_dir(function):
    def wrapper(*args, **kwargs):
        # Make a tmp directory if its not there
        try:
            os.makedirs(tmp_path)
        except OSError as e:
            unexpected_exception = e.errno != errno.EEXIST
            if unexpected_exception:
                raise

        return function(*args, **kwargs)

    return wrapper


@make_tmp_dir
def output():
    """Make a file in the """
    fh = tempfile.NamedTemporaryFile("wb", dir=tmp_path, delete=True)
    fh.close()
    return fh.name


@make_tmp_dir
def write_graph(G, type="edgelist"):
    fh = tempfile.NamedTemporaryFile(
        "wb", dir=tmp_path, delete=False, suffix=".nif")
    graph_format.write_type(G, fh, type)
    fh.close()
    return fh.name


@make_tmp_dir
def write_sim(sim_df):
    fh = tempfile.NamedTemporaryFile(
        "wb", dir=tmp_path, delete=False, suffix=".ort")

    need_convert = sim_df.shape[1] != 3
    if need_convert:
        df_to_edge_list(sim_df).to_csv(fh, index=False, header=None, sep="\t")
    else:
        sim_df.to_csv(fh, index=False, header=None, sep="\t")

    fh.close()
    return fh.name


def clean_up():
    shutil.rmtree(tmp_path)


def df_to_edge_list(df):
    return df.stack().reset_index()
