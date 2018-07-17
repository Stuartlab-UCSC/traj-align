
import pandas as pd

def read_similarities(file):
    """ Auto dectects full adjancy or weighted edgelist.
    :param file:
    :return:
    """
    sim_df = pd.read_table(file, index_col=0)

    # Check for 3 columns in file
    edgelist_format = sim_df.shape[1] == 2
    if edgelist_format: # Ignore header.
        sim_df.iloc[sim_df.shape[0]] = sim_df.columns

    return sim_df