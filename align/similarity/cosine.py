#!/usr/bin/env python2.7
"""
http://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.pairwise_distances.html

example CLI usage:
# for self cosine similarity of columns:
cosine.py -X $HOME/path/to/some-matrix.tab -o ./cosine-somematrix.tab

# For similarity between two matricies
cosine.py -X $HOME/path/to/some-matrix.tab \
-Y $HOME/path/to/some-other-matrix.tab -o ./cosine-somematrix.tab
"""
import sklearn.metrics.pairwise as sklp
import pandas as pd


def calculate(df1, df2=None):

    rownames, colnames = _row_col_names(df1, df2)
    distances = sklp.pairwise_distances(X=df1, Y=df2, metric="cosine")

    distances = pd.DataFrame(
        distances, columns=colnames, index=rownames
    )

    similarities = 1 - distances

    return similarities


def enforce_equal_ncol(df1, df2):
    """Make sure that there are an equal number of columns so that
    the distance calc doesn't choke."""

    if df2 is None or df1.shape[1] == df2.shape[1]:
        return df1, df2


    raise UserWarning(
        """An equal number of features is being enforced by expanding
        each of the feature sets and setting absent features to 0."""
    )

    all_columns = set(df1.columns)
    all_columns.update(set(df2.columns))

    df1 = df1.reindex(columns=list(all_columns), fill_value=0)
    df2 = df2.reindex(columns=list(all_columns), fill_value=0)

    return df1, df2


def _row_col_names(df1, df2):
    """Gives you the new row and column names for your similarity
    matrix."""
    if df2 is None:
        return df1.index, df1.index

    return df1.index, df2.index



