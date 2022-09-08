#%%
import numpy as np
import mrcfile
import matplotlib.pyplot as plt
from pathlib import Path
import random
# %%
average_dir = Path("average")
denoising_dir = Path("denoising")
# %%
average_imfiles = list(average_dir.rglob("*.mrc"))
denoising_imfiles = list(denoising_dir.rglob("*mrc"))
# %%
print(f"Average imfiles: {len(average_imfiles)}")
print(f"Denoising imfiles: {len(denoising_imfiles)}")

# %%
# Inspect Average files:

def inspect_random_image(im_file_list):

    
    im_file = random.sample(average_imfiles, 1)
    im_file = im_file[0]

    with mrcfile.open(im_file) as mrc:
        img = mrc.data

    plt.figure(figsize=(12,12))
    # plt.title()
    plt.imshow(img, cmap="gray")


inspect_random_image(average_imfiles)


# %%
# Inspect Denoising files:
inspect_random_image(denoising_imfiles)