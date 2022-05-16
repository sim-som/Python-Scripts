# %%
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
from skimage import io
# %%
file_p = Path(
    "/home/simon/gpu-rechner_u3_mount/2021-10-15_Trehalose_grids_Arctica/211015_MZ_Trehalose+TMV_Data/tifData/tifData/FoilHole_15371679_Data_15372558_15372560_20211016_151458_fractions.mrc.tif"
)
assert file_p.exists() and file_p.is_file()
# %%
img = io.imread(file_p)
# %%
