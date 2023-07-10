#%%
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.collections import PatchCollection
import matplotlib as mpl
from matplotlib import gridspec
from pathlib import Path
import random
import mrcfile
from skimage import exposure
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
# %%

cs_project_path = Path("/home/simon/simon_data/cryoSPARC_projects/CS-insulin-glargine")
cs_job_id = 61

# particle data:
particles_data_p = cs_project_path / Path(f"J{cs_job_id}/J{cs_job_id}_020_particles.cs")
particles_passthrough_p = cs_project_path / Path(f"J{cs_job_id}/J{cs_job_id}_passthrough_particles.cs")

# class averages data:
classes_data_p = cs_project_path / Path(f"J{cs_job_id}/J{cs_job_id}_020_class_averages.cs")
classes_stk_p = cs_project_path / Path(f"J{cs_job_id}/J{cs_job_id}_020_class_averages.mrc")

# %%
# parsing functions:
def get_col_names_and_dtypes(raw_cs_data:np.ndarray):

    dt = raw_cs_data.dtype
    fields = dt.fields
    fields = dict(fields)
    col_names = list(fields.keys())
    dtypes = list(fields.values())
    return col_names, dtypes

def read_raw_cs_data(raw_cs_data:np.ndarray):

    col_names, dtypes = get_col_names_and_dtypes(raw_cs_data)

    list_of_row_dicts = []

    for i in range(len(raw_cs_data)):
        
        row = list(raw_cs_data[i])

        row_dict = dict(zip(col_names, row))

        # print(row_dict)
        list_of_row_dicts.append(row_dict)
    
    data_df = pd.DataFrame(list_of_row_dicts)

    return data_df

# %%
classes_df = read_raw_cs_data(np.load(classes_data_p))
classes_df

# %%

with mrcfile.open(classes_stk_p) as f:
    classes_img_stk = f.data

# %%
# Read particle data:
particles_df = read_raw_cs_data(np.load(particles_data_p))
particles_df
# %%
# Read "passthrough" particles data:
particles_pt_df = read_raw_cs_data(np.load(particles_passthrough_p))
particles_pt_df

# %%
# combine particle data:
particles_df_joined = pd.merge(particles_df, particles_pt_df, how="outer")
particles_df_joined
# %%
# Get class with align. res. 6.2 A:
class_spec_res = classes_df[np.isclose(classes_df["blob/res_A"], 6.2, atol=0.05)]
class_spec_res
# %%
class_idx:int = class_spec_res["blob/idx"].iloc[0]
print(f"Class index: {class_idx}")

# %%
# Class average:
class_avg_img = classes_img_stk[class_idx,:,:]
classes_angpix = classes_df["blob/psize_A"][0]
boxsize_px = class_avg_img.shape[0]
plt.figure()
plt.imshow(class_avg_img, cmap="gray")
plt.title("Class average")
plt.xlabel(f"boxsize = {boxsize_px} px = {np.round(boxsize_px * classes_angpix, 0)} A")

plt.show()

# %%
# particles belonging to that specific class:
particles_of_class = particles_df_joined[particles_df_joined["alignments2D/class"] == class_idx]
particles_of_class

# %%
# all micrographs including particles that belong to the selected class:
mics = particles_of_class["location/micrograph_path"].unique()
mics.shape
# %%
# Select random subset of those micrographs for inspection:
n_sub = 10
mics_subset = random.sample(list(mics), n_sub)
print(mics_subset)
# %%
# get the micrograph paths for all micrographs:
def get_mic_path(cs_mic_string:str):
    mic = str(cs_mic_string).strip("'b")
    return cs_project_path / Path(mic)
    
mics_subset_abs_paths = [get_mic_path(mic) for mic in mics_subset]
# %%
# Get the particles, that belong to the specified class AND are on the micrographs from the subset
particles_subset = [particles_of_class[particles_of_class["location/micrograph_path"] == mic] for mic in mics_subset]
particles_subset = pd.concat(particles_subset)
print(f"{particles_subset.shape[0]} particles")
particles_subset

# %%
# Draw the particle boxes on the micrographs from the random subset

def get_coords(particles_df):

    coords_list = []
    for idx, part in particles_df.iterrows():
        
        mic_shape = part["location/micrograph_shape"]

        x_coord_center_frac = part["location/center_x_frac"]
        y_coord_center_frac = part["location/center_y_frac"]


        xy_coords = np.array([x_coord_center_frac, y_coord_center_frac]) * mic_shape[::-1]
        coords_list.append(xy_coords)

    return coords_list

# Colormap for class2d_posterior indication:
cmap = plt.get_cmap('viridis')

for mic, mic_abs_p in zip(mics_subset, mics_subset_abs_paths):

    print(mic_abs_p.name)
    
    img_arr = load_mrc_file(mic_abs_p) 

    # get corresponding particles:
    particles = particles_of_class[particles_of_class["location/micrograph_path"] == mic]

    box_size = 576 # Hardcoded ! #TODO

    coords = get_coords(particles)
    patches = [Rectangle(xy + np.array([box_size // 2]*2), box_size, box_size, fill=False, edgecolor="tab:green") for xy in coords]

    patch_collection = PatchCollection(patches, match_original=True)

    # class assingment confidence from "alignments2D/class_posterior":
    # Convert class posterior values to colors for particle drawing
    colors = cmap(particles["alignments2D/class_posterior"])
    
     

    fig = plt.figure(figsize=(12,12))

    gs = gridspec.GridSpec(2,1, height_ratios=[1, 3])

    ax1 = fig.add_subplot(gs[0])

    ax1.imshow(class_avg_img, cmap="gray")
    ax1.set_title(f"Class {class_idx} @ {classes_data_p}")
    res_ang = class_spec_res["blob/res_A"].values[0]
    ax1.set_xlabel(f"boxsize = {boxsize_px} px = {np.round(boxsize_px * classes_angpix, 0)} A, Res = {np.round(res_ang, 1)} ")


    ax2 = fig.add_subplot(gs[1])

    ax2.imshow(contrast_scaling(img_arr), cmap="gray")
    # Draw particle boxes on micrograph:
    ax2.add_collection(patch_collection)
    # color particle boxes according to their class posterior
    patch_collection.set_edgecolor(colors)

    fig.colorbar(patch_collection, label="class posterior")

    ax2.set_title(f"mic: {mic_abs_p.name}")

    plt.tight_layout()

    plt.show()

    break
# %%
