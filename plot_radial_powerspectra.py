
# imports
import numpy as np
import pandas as pd
import seaborn as sns
# sns.set_theme(context= "paper")
from matplotlib import pyplot as plt
import argparse
from pathlib import Path
import json

from ctf_functions import *


############################################################################################################

parser = argparse.ArgumentParser(
    
    description="""
        Plotting script to plot the powerspectrum and fitted ctf from the *avrot.txt
        files produced by CTFFIND4 (https://grigoriefflab.umassmed.edu/ctffind4)
    """
    )
parser.add_argument("results_dir", help="The directory where the results from ctffind4 reside")
args = parser.parse_args()

results_dir = Path(args.results_dir)

# # for testing:
# results_dir = Path.cwd()

assert results_dir.exists() and results_dir.is_dir()

micrograph_nr = 0
for file_p in results_dir.glob("*avrot.txt"): 
    print(f"Plotting {file_p}")

    # Read file content into one string
    with open(file_p) as f:
        file_contents = f.read()
    file_contents = file_contents.strip()

    Nr_cat = 6      # number of categories
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
    # parse numerical rows as float arrays:
    num_data = [np.array(item.split(), dtype=float) for item in raw_num_data]
    # write parsed categories and corresponding numerical data into dictionary:
    data = dict(zip(categs, num_data))

    # convert to pandas dataframe:
    df = pd.DataFrame(data)
    # spatial frequency in Angstrom (Å)
    df["spatial frequency / Å"] = df["spatial frequency (1/Angstroms)"]

    # Corresponding image file:
    # img_dir_p = TODO
    img_file_name = f"{file_p.stem[:-6]}.png"

    # Parsing Ctffind4s fit parameters for the current file from {img_file.stem}.txt textfiles:
    fit_params_file_p = file_p.parent / Path(f"{file_p.stem[:-6]}.txt")
    assert fit_params_file_p.exists() and fit_params_file_p.is_file
    with open(fit_params_file_p) as f:
        file_content = f.read()
    file_content = file_content.strip()
    fit_params:dict = parse_fit_params(file_content)

    # modify the keys to save space for plotting:
    fit_params["#"] = fit_params['micrograph number']   # as far as I know this is always = 1.0 in the text files
    del fit_params['micrograph number']
    fit_params["#"] = micrograph_nr
    print(micrograph_nr)
    micrograph_nr += 1
    fit_params['defocus1 / A'] = fit_params['defocus 1 [Angstroms]']
    del fit_params['defocus 1 [Angstroms]']
    fit_params['defocus2'] = fit_params['defocus 2']
    del fit_params['defocus 2']
    # fit_params['defocus angle'] = fit_params['azimuth of astigmatism']
    del fit_params['azimuth of astigmatism']
    # fit_params['phase shift [rad]'] = fit_params['additional phase shift [radians]']
    del fit_params['additional phase shift [radians]']
    # fit_params['cross corr'] = fit_params['cross correlation']
    del fit_params['cross correlation']
    fit_params["CtfMaxRes / A"] = fit_params["spacing (in Angstroms) up to which CTF rings were fit successfully"]
    del fit_params["spacing (in Angstroms) up to which CTF rings were fit successfully"]


    # Turn dict content into a string for plotting:
    fit_params_content = json.dumps(fit_params)


    # plotting with seaborn:
    plt.figure(str(file_p))

    ax = plot_ctf_data(df)


    plt.title(f"CTF fit of {file_p.name}\n{fit_params_content}")
    plt.legend(title="")
    plt.ylabel("a.u.")

    # ignore weird high frequency peaks:
    plt.ylim((-4,4))
    

    # filesaving:
    img_format = "png"
    output_p = file_p.parent / Path(f"{file_p.stem}.{img_format}")
    print(f"Saving plot to {output_p}")
    plt.savefig(output_p, bbox_inches="tight")

    # plt.show()

    plt.close()