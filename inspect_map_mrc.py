#%%
# imports
import mrcfile
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
from natsort import natsorted
# %%
# example file:
file_p = Path(
    "/home/simon/jureca_project_mount/Trehalose_gunnar_2/Refine3D/job098/run_it007_half1_class001.mrc"
    )
assert file_p.exists() and file_p.is_file()
# directory:
dir_p = file_p.parent

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
plt.imshow(images[50])
# %%
iterations = list(dir_p.glob("*run_it*.mrc"))
iterations = natsorted(iterations)

for it_p in iterations:
    print(it_p)
    with mrcfile.open(it_p) as f:
        map = f.data
    print(map.shape)
    plt.figure()
    plt.imshow(map[50])
    plt.show()


# %%
# Save slice of last map as tiff image
from skimage import io
slice = map[50]

plt.imshow(slice)

# %%
# write 2D slice to .mrc
with mrcfile.new("map_slice.mrc", overwrite=True) as mrc:
    mrc.set_data(slice)
# %%
# check written file:
with mrcfile.open("map_slice.mrc") as f:
    plt.imshow(f.data)
# %%
