from matplotlib import pyplot as plt
import numpy as np
import pandas
import seaborn as sns


def plot_ctf_data(df:pandas.DataFrame):


    # ignore the spatial freq. in Angstroms column for plotting 
    ignored = "spatial frequency / Å"
    x_label = "spatial frequency (1/Angstroms)"
    # convert to long (tidy) form
    # this form is necessary to plot df with seaborn (https://stackoverflow.com/questions/44941082/plot-multiple-columns-of-pandas-dataframe-using-seaborn)
    dfm = df.loc[:, df.columns != ignored].melt(x_label, var_name='cols', value_name='vals')

    
    ax = sns.lineplot(
        data = dfm,
        x = x_label,
        y = "vals",
        hue = "cols",
    )

    # custom xticks in Angstrom: TODO
    return ax

def parse_fit_params(file_content:str):
    """_summary_

    Args:
        file_content (str): _description_
    """


    rows = file_content.split("\n")
    raw_cat_data = rows[-2]
    raw_num_data = rows[-1]

    # Parse categories:
    categs = raw_cat_data.split("#")
    # remove first two entries
    categs = categs[2:]
    # remove numbers at start and ; at end of each category:
    for i, cat in enumerate(categs):
        categs[i] = cat[4:].strip("; ") 

    # parse numerical rows as float arrays:
    num_data = np.array(raw_num_data.split(), dtype=float)
    # write parsed categories and corresponding numerical data into dictionary:
    data = dict(zip(categs, num_data))

    return data