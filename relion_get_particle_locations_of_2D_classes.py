#%%
# imports
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
from natsort import natsorted
import pandas as pd
from matplotlib import patches
import argparse
import random
from skimage import filters

from starparser import fileparser
import mrcfile
# %%
# file/directory management:
data_star_file_p = Path(
    "/home/simon/jureca_scratch_mount/20221129_SiSo_Ins_Fib_Fractions/relion4_processing/Class2D/job043/run_it025_data.star"
)
assert data_star_file_p.exists() and data_star_file_p.is_file()
job_dir_p = data_star_file_p.parent
assert len(job_dir_p.name) == 6 and job_dir_p.name[:3] == "job"
project_dir_p = job_dir_p.parents[1]
assert project_dir_p.exists() and project_dir_p.is_dir()
img_stack_file_p = job_dir_p / Path(data_star_file_p.name[:-10] + "_classes.mrcs")
assert img_stack_file_p.exists() and img_stack_file_p.is_file()

#%%
# parse the _data.star file
particles, metadata = fileparser.getparticles(str(data_star_file_p))
# convert numerical columns to float or int:
particles = particles.apply(pd.to_numeric, errors="ignore")

particles.info()
# %%
def get_classes_angpix_from_particles_star_metadata(metadata_df:pd.DataFrame):

    return float(metadata[2]._rlnImagePixelSize)

def get_boxsize_from_particles_star_metadata(metadata_df:pd.DataFrame, angpix_classes:float):

    box_size_rescaled = float(metadata[2]._rlnImageSize)
    box_size_ang = box_size_rescaled * angpix_classes

    return box_size_ang

def get_micrograph_angpix(mrc__file_path:Path):

    with mrcfile.open(mrc__file_path) as f:
        angpix = float(f.voxel_size.x)
    
    return angpix

def calc_scaling_factor(angpix_mic:float, angpix_classes:float):

    return int(angpix_classes / angpix_mic)

def calc_boxsize_in_micrograph(box_size_ang, angpix_mic, angpix_classes):

    s = calc_scaling_factor(angpix_mic=angpix_mic, angpix_classes=angpix_classes)

    box_size_px_classes = box_size_ang * angpix_classes
    box_size_px_mic = box_size_px_classes * s

    return box_size_px_mic

angpix_classes = get_classes_angpix_from_particles_star_metadata(metadata)
print(f"Pixel size of 2D classes = {angpix_classes} A")
box_size_ang = get_boxsize_from_particles_star_metadata(metadata, angpix_classes)
print(f"Boxsize: {box_size_ang} A ")
angpix_mic = get_micrograph_angpix() # not given what the angpix on microgprahps is ! #TODO

# %% 
# load img stack containing 2D classes
with mrcfile.open(img_stack_file_p) as f:
    stack = f.data
    print(stack.shape)

# %%
# show all classes

def plot_all(images):
    N = images.shape[0]
    n_cols = 5
    n_rows = int(np.ceil(N / n_cols))
    fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(10,100))
    axs = axs.flatten()
    # remove ticks:
    for i in range(len(axs)):
        axs[i].set_xticks([])
        axs[i].set_yticks([])
    # plot images:
    for i in range(N):
        axs[i].imshow(images[i, :, :], cmap="gray")
        axs[i].set_xlabel(f"Class {i+1}")
    
plot_all(stack)
plt.show()
# %%
# ID of the class of interest (Get this from the relion gui or the plot above):
class_id = 243

class_particles = particles[particles["_rlnClassNumber"] == class_id]
N_part = len(class_particles)

# %%
# Show selected class:
plt.figure()
plt.imshow(stack[class_id - 1, :, :], cmap="gray")   # watch out class IDs start at 1!
plt.title(f"Class {class_id} of {job_dir_p}")
plt.xlabel(f"Nr. particles: {N_part}")

# %%
# plot micrographs together with particles of selected class:
def draw_particle(x, y, radius):
    
    circle = patches.Circle(
        (x, y),
        radius=radius,
        color="tab:green",
        fill = False
    )
    ax.add_patch(circle)


micrographs = list(pd.unique(class_particles["_rlnMicrographName"]))
print(f"Number of micrographs with particles from class {class_id}: {len(micrographs)}")

#%%
max_image_num = 3
mics_subset = random.sample(micrographs, max_image_num)
#%%
for mic in mics_subset:
    print(mic)
    # correct full path of micrograph:
    mic_p = project_dir_p / Path(mic)
    assert mic_p.exists() and mic_p.is_file()
    # data for just the micrograph:
    image_class_particles = class_particles[class_particles["_rlnMicrographName"] == mic]
    print("Nr. particles in image:" ,len(image_class_particles))
    # load the micrograph and plot:
    fig, ax = plt.subplots(figsize=(24,12))
    plt.gray()
    with mrcfile.open(mic_p) as f:
        img = f.data
    

    img = filters.median(img)
    plt.imshow(img)
    # draw coordinates on image:
    for x, y in zip(image_class_particles["_rlnCoordinateX"], image_class_particles["_rlnCoordinateY"]):
        draw_particle(x, y, box_size_ang/2.)
    ax.set_title(f"Coords. $\in$ Class {class_id} of {job_dir_p}")
    ax.set_xlabel(mic_p.name)
    plt.show()
    
    

 # %%
