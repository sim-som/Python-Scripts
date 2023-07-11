#%%
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.collections import PatchCollection
from matplotlib import gridspec
from pathlib import Path
import random
import mrcfile
from skimage import exposure
# %%
# Own modules:
import sys
path_to_starparse_module = Path.home() / Path("OneDrive/Dokumente/Promotion/Code/starparse_module")
assert path_to_starparse_module.exists()
sys.path.append(str(path_to_starparse_module))
from starparse_module_general import parse_star_file

# %%
def contrast_scaling(img, p=0.5):

    percentiles = np.percentile(img, (p, 100-p))
    scaled_img = exposure.rescale_intensity(
            img,
            in_range=tuple(percentiles)
        )
    
    return scaled_img
# %%
def load_mrc_file(mrc_file_path):
    with mrcfile.open(mrc_file_path) as f:
        img_data = f.data
    return img_data

def get_angpix(mrc_file_path) -> float:
    with mrcfile.open(mrc_file_path) as f:
        angpix = float(f.voxel_size.x)
    return angpix
# %%
# File locations:

relion_project_path = Path("/home/simon/judac_scratch_mount/SiSo-Krios-Ins_Glarg_3-Acquistion-20230623/relion4_proc")
relion_job_id = "073"

# particle data:
particles_data_p = relion_project_path / Path(f"Class2D/job{relion_job_id}/run_it025_data.star")


# class averages data:
classes_data_p = relion_project_path / Path(f"Class2D/job{relion_job_id}/run_it025_model.star")
classes_stk_p = relion_project_path / Path(f"Class2D/job{relion_job_id}/run_it025_classes.mrcs")

# %%
# Load metadata describing Class averages:

classes_df = parse_star_file(classes_data_p, keyword="data_model_classes")
# Add class number (index + 1)
classes_df["ClassNumber"] = pd.Series(classes_df.index + 1)
classes_df

# %%
# load mrc_stk with class averages
classes_img_stk = load_mrc_file(classes_stk_p)
classes_angpix = get_angpix(classes_stk_p)
print(f"Classes pix = {classes_angpix} A")
classes_img_stk.shape

# %%
# all picked particles data: #TODO
# all_picked_particels_p = cs_project_path / Path("J32/J32_passthrough_particles.cs")
# all_picked_particels_df = read_raw_cs_data(np.load(all_picked_particels_p))
# all_picked_particels_df.columns


# %%
# Read particle data:
particles_df = parse_star_file(particles_data_p, keyword="data_particles")
particles_df
# %%
# Get class with align. res. 6.2 A:
def get_class_with_certain_res(res_ang):

    return classes_df[np.isclose(classes_df["EstimatedResolution"], res_ang, atol=0.05)]

def get_class(ClassNumber):
    return classes_df[classes_df["ClassNumber"] == ClassNumber]

selected_class = get_class(81)
selected_class
# %%
class_num = selected_class.ClassNumber.iloc[0]
print(f"Class number: {class_num}")
class_idx:int = pd.Series(selected_class.index).iloc[0]
print(f"Class index ( = class_num -1): {class_idx}")

# %%
# Class average:
class_avg_img = classes_img_stk[class_idx,:,:]
boxsize_px = class_avg_img.shape[0]
plt.figure()
plt.imshow(class_avg_img, cmap="gray")
plt.title("Class average")
plt.xlabel(f"boxsize = {boxsize_px} px = {np.round(boxsize_px * classes_angpix, 0)} A")

plt.show()

# %%
# particles belonging to that specific class:
particles_of_class = particles_df[particles_df["ClassNumber"] == class_num]
particles_of_class

# %%
# all micrographs including particles that belong to the selected class:
mics = particles_of_class["MicrographName"].unique()
mics = list(mics)
print(len(mics))

# %% 
# Count number of particles per micrograph
part_cnts_per_mic = {}
for mic in mics:
    cnts = len(particles_of_class[particles_of_class["MicrographName"] == mic])
    part_cnts_per_mic[mic] = cnts

plt.figure()
plt.hist(part_cnts_per_mic.values())
plt.xlabel("particles per microgrgraph")
plt.ylabel("Count")

# %%
# Sort mics by particle count:
mics.sort(key=lambda mic: - part_cnts_per_mic[mic])

# %%
# Select subset of those micrographs for inspection:
n_sub = 10

# Use random subset:
# mics_subset = random.sample(list(mics), n_sub)
# Or most populated mics:
mics_subset = mics[:n_sub]

print(mics_subset)
# %%
# get the micrograph paths for all micrographs:
def get_mic_path(relion_mic_string:str):
    return relion_project_path / Path(relion_mic_string)
    
mics_subset_abs_paths = [get_mic_path(mic) for mic in mics_subset]
# %%
# Get the particles, that belong to the specified class AND are on the micrographs from the subset
particles_subset = [particles_of_class[particles_of_class["MicrographName"] == mic] for mic in mics_subset]
particles_subset = pd.concat(particles_subset)
print(f"{particles_subset.shape[0]} particles")
particles_subset

# %%
# Draw the particle boxes on the micrographs from the random subset

def get_coords(particles_df):

    coords_list = []
    for idx, part in particles_df.iterrows():

        x_coord = part["CoordinateX"]
        y_coord = part["CoordinateY"]


        xy_coords = np.array([x_coord, y_coord])

        coords_list.append(xy_coords)

    return coords_list

# Colormap for class2d_posterior indication:
cmap = plt.get_cmap('viridis')

for mic, mic_abs_p in zip(mics_subset, mics_subset_abs_paths):

    print(mic_abs_p.name)
    
    img_arr = load_mrc_file(mic_abs_p) 

    # get corresponding particles:
    particles = particles_of_class[particles_of_class["MicrographName"] == mic]

    box_size = 576 # Hardcoded ! #TODO

    coords = get_coords(particles)
    patches = [Rectangle(xy + np.array([box_size // 2]*2), box_size, box_size, fill=False, edgecolor="tab:green") for xy in coords]

    patch_collection = PatchCollection(patches, match_original=True)

    # class assingment confidence from "MaxValueProbDistribution":
    # Convert class posterior values to colors for particle drawing
    colors = cmap(particles["MaxValueProbDistribution"])
    
     

    fig = plt.figure(figsize=(12,12))

    gs = gridspec.GridSpec(2,1, height_ratios=[1, 3])

    ax1 = fig.add_subplot(gs[0])

    ax1.imshow(class_avg_img, cmap="gray")
    ax1.set_title(f"Class {class_num} @ {classes_data_p}")
    res_ang = selected_class["EstimatedResolution"].values[0]
    ax1.set_xlabel(f"boxsize = {boxsize_px} px = {np.round(boxsize_px * classes_angpix, 0)} A, Res = {np.round(res_ang, 1)} ")


    ax2 = fig.add_subplot(gs[1])

    ax2.imshow(contrast_scaling(img_arr, p=5), cmap="gray")
    # Draw particle boxes on micrograph:
    ax2.add_collection(patch_collection)
    # color particle boxes according to their class posterior
    patch_collection.set_edgecolor(colors)

    fig.colorbar(patch_collection, label="class posterior")

    ax2.set_title(f"mic: {mic_abs_p.name}")

    plt.tight_layout()

    plt.show()

# %%
