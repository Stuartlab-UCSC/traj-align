"""

"""

from difflib import SequenceMatcher
from itertools import product as cartesian_product
import pandas as pd


def similarity(names1, names2):
    df = pd.DataFrame(columns=[0, 1, 2])
    row = 0
    for name1, name2 in cartesian_product(names1, names2):
        sim = SequenceMatcher(None, name1, name2).ratio()
        df.loc[row] = [name1, name2, sim]
        row += 1

    return df




