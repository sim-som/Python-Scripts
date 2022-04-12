#%%
# imports
import mrcfile
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
# %%
file_p = Path("/home/simon/Documents/Master/TMV_denmap_lit_emd_10129.map")
assert file_p.exists() and file_p.is_file()

# %%
with mrcfile.open(file_p) as f:
    images = f.data
    print(images.shape)
#%%
# metadata:
with mrcfile.open(file_p) as f:
    print(f.header)
    print(f.extended_header)
# %%
# pixel size:
with mrcfile.open(file_p) as f:
    print("pixel size (Å):", f.voxel_size)

# %%
plt.imshow(images[300])
# %%
