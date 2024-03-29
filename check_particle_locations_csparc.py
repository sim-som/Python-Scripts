#%%
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("default")
from matplotlib.patches import Circle
import pandas as pd
from pandas import DataFrame
from pathlib import Path
import mrcfile
import random
from skimage.filters import gaussian
# %%
IMAGE_DIR = Path("/u3/data/simon/20220307_GPCR_nanodisk_Simon/20220307_GPCR_nanodisk_Simon/average/")
particle_location_cs_file = Path(r"/u3/data/simon/cryoSPARC_projects/P23/J73/P23_J73_passthrough_particles_selected.cs")
particle_data_raw = np.load(particle_location_cs_file)
# %%
particle_example = particle_data_raw[0]
# %%
particle_data = []
for particle in particle_data_raw:
    particle_data.append(list(particle))
# %%
# get column names:

void_dtype = particle.dtype
# print(void_dtype)

column_names = []
for item in void_dtype.descr:
    print(item[0])
    column_names.append(item[0])
# %%
particle_df = DataFrame(
    data=particle_data,
    columns=column_names
)
# %%
def is_location_info(column_name:str):
    return "location/" in column_name

location_columns = []
for col in particle_df.columns:
    if is_location_info(col):
        print(col)
        location_columns.append(col)

particle_locations = particle_df[location_columns]
# %%
# format micrograph path column:

def correct_image_path(img_path_np_bytes):

    img_path = str(img_path_np_bytes)[2:-1]
    img_path = Path(img_path)

    return img_path


exmpl_mic_path = particle_locations["location/micrograph_path"][0]
print(correct_image_path(exmpl_mic_path))


# %%
# apply to the whole column:
particle_locations["location/micrograph_path"] = particle_locations["location/micrograph_path"].apply(correct_image_path)
particle_locations
# %%
# Add micrograph file name column:
particle_locations["micrograph_file"] = [path.name for path in particle_locations["location/micrograph_path"]]
particle_locations
#%%
MICROGRAPH_SHAPE = particle_locations["location/micrograph_shape"][0]
#%%
particle_locations["center_x_pix"] = np.around(particle_locations["location/center_x_frac"] * MICROGRAPH_SHAPE[1], 0).astype(int)
particle_locations["center_y_pix"] = np.around(particle_locations["location/center_y_frac"] * MICROGRAPH_SHAPE[0], 0).astype(int)
particle_locations
# %%
# Check particle locations in images:

image_files =  list(IMAGE_DIR.glob("*.mrc"))

# %%
# read image data:
def read_image_data_from_mrc_file(file_p):

    with mrcfile.open(file_p) as mrc:
        img_data = mrc.data
        px_size = mrc.voxel_size.x
    
    return img_data, px_size

test_img_file = random.sample(image_files, 1)[0]
test_img, _ = read_image_data_from_mrc_file(test_img_file)

#%%
plt.imshow(gaussian(test_img, sigma=1), cmap="gray")
plt.title("Test image")


# %%
# Given image file, plot image with annotated particles:

def plot_image_with_particles(image_file_p, particle_locations_df:DataFrame):

    belongs_to_image = particle_locations_df["micrograph_file"] == image_file_p.name
    per_image_sub_df = particle_locations_df[belongs_to_image]

    img, PX_SIZE_ANG = read_image_data_from_mrc_file(image_file_p)
    
    print(image_file_p.name)

    fig, axes = plt.subplots()
    axes.imshow(gaussian(img), cmap="gray")


    for x, y, radius in zip(per_image_sub_df["center_x_pix"], per_image_sub_df["center_y_pix"], per_image_sub_df["location/min_dist_A"]):

        # print("(x,y) = ", x, y)

        particles_patch = Circle((x,y), radius/PX_SIZE_ANG, fill=False, color="g")
        axes.add_patch(particles_patch)

# %%
plot_image_with_particles(test_img_file, particle_locations)
# plt.savefig(f"particles_in_{test_img_file.stem}.png")

# %%
# Get images with most particle locations

# group location data by images:
grouped_dict = particle_locations.groupby("micrograph_file").groups
# Sort images by number of particles:
image_file_names = list(grouped_dict.keys())
image_file_names.sort(key=lambda item: - len(grouped_dict[item]))
for file_name in image_file_names:
    print(len(grouped_dict[file_name]))

# %%
# plot N images with most particles
N = 10
for i in range(N):
    plot_image_with_particles(IMAGE_DIR / Path(image_file_names[i]), particle_locations)
    plt.show()


# %%
plot_image_with_particles(IMAGE_DIR / Path(image_file_names[-1]), particle_locations)