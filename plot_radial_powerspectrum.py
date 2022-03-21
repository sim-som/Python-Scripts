# %%
# imports

import numpy as np
import pandas as pd
import seaborn as sns
sns.set_theme(style="darkgrid")
from matplotlib import pyplot as plt
import argparse
from pathlib import Path

from ctf_functions import *
# %%
# parser = argparse.ArgumentParser(
    
#     description="""
#         Plotting script to plot the powerspectrum and fitted ctf from the *avrot.txt
#         files produced by CTFFIND4 (https://grigoriefflab.umassmed.edu/ctffind4)
#     """
#     )
# parser.add_argument("results_dir", help="The directory where the results from ctffind4 reside")
# args = parser.parse_args()

# results_dir = Path(args.results_dir)

# for testing:
results_dir = Path.cwd()

assert results_dir.exists() and results_dir.is_dir()

file_p = list(results_dir.glob("*avrot.txt"))[0]

# %% 
# Read file content into one string
with open(file_p) as f:
    file_contents = f.read()
file_contents = file_contents.strip()

Nr_cat = 6      # number of categories
# %%
# parse with string methods: 
rows = file_contents.split("\n")
# presort the rows into three groups:
raw_meta_data = rows[:4]
raw_categ_data = rows[4]
raw_num_data = rows[- Nr_cat:]
# Get categories:
categs = raw_categ_data.split("#")
# remove first two entries
categs = categs[2:]
# remove numbers at start and ; at end of each category:
for i, cat in enumerate(categs):
    categs[i] = cat[4:].strip("; ")
# %% 
# parse numerical rows as float arrays:
num_data = [np.array(item.split(), dtype=float) for item in raw_num_data]
# %%
# write parsed categories and corresponding numerical data into dictionary:
data = dict(zip(categs, num_data))

# %%
# convert to pandas dataframe:
df = pd.DataFrame(data)
# %%
# spatial frequency in Angstrom (Å)
df["spatial frequency / Å"] = df["spatial frequency (1/Angstroms)"]

# %%
# plotting with seaborn:

plot_ctf_data(df, file_p)