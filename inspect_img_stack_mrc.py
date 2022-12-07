#%%
# imports
import mrcfile
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
# from natsort import natsorted
# %%
file_p = Path(
    "/u3/data/simon/image_data/cryoem_data/arctica/20221129_SiSo_Ins_Fib_Fractions/Extract/job006/average/FoilHole_29969857_Data_29966174_29966176_20221129_221246_fractions.mrcs"
)
assert file_p.exists() and file_p.is_file()

# %%
with mrcfile.open(file_p) as f:
    stack = f.data
    print(stack.shape)
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

def plot_all(images):
    N = images.shape[0]
    rc = np.sqrt(N)
    rc = int(np.ceil(rc))
    print(rc)
    fig, axs = plt.subplots(rc, rc, figsize=(12,12))
    axs = axs.flatten()
    # remove ticks:
    for i in range(len(axs)):
        axs[i].set_xticks([])
        axs[i].set_yticks([])
    # plot images:
    for i in range(N):
        axs[i].imshow(images[i, :, :], cmap="gray")
        axs[i].set_xlabel(f"Class {i}")

plot_all(stack)
# %%
# All iterations:

dir_p = file_p.parent
iterations = list(dir_p.glob("*it???*.mrcs"))
iterations = natsorted(iterations)

for path in iterations:
    print(path)
    # read image stack as np array:
    with mrcfile.open(path) as f:
        stack = f.data
    print("Shape:", stack.shape)
    plot_all(stack)
    plt.suptitle(str(path))
    plt.tight_layout()
    plt.show()
# %%
# plot most recent iteration:
dir_p = file_p.parent
iterations = list(dir_p.glob("*it???*.mrcs"))
iterations = natsorted(iterations)

with mrcfile.open(iterations[-1]) as f:
        stack = f.data

print(iterations[-1])
plot_all(stack)

# %%
