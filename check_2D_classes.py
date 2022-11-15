#%%
import numpy as np
import napari
import mrcfile
from pathlib import Path

# %%
im_path = Path("/u3/data/simon/cryoSPARC_projects/P23/J198/J198_040_class_averages.mrc")
assert im_path.exists() and im_path.is_file()
# %%
with mrcfile.open(im_path) as mrc:
    mic_classes = mrc.data
print(f"Loaded mrc image stack of dimensions f{mic_classes.shape} and data type {mic_classes.dtype}")
# %%
napari.view_image(mic_classes)