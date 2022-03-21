# %%
# imports
import numpy as np
import pandas as pd
from pathlib import Path

from ctf_functions import *

# %%
# file reading:
test_file_p = Path(r"C:\Users\simon\OneDrive\Dokumente\Studium\Master\Masterarbeit\Auswertungen\Gunnars_Treh_TMV_data_Talos\CtfFind\a4-5perc_45.3_kx_1516_20200916_0001_Ceta.txt")
assert test_file_p.exists() and test_file_p.is_file

with open(test_file_p) as f:
    file_content = f.read()
file_content = file_content.strip()

data = parse_fit_params(file_content)

print(f"Fit parameters from {test_file_p}:")
for key, val in data.items():
    print(f"\t{key}: {val}")

# %%
