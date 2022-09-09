#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
from pathlib import Path
# %%
particle_location_cs_file = Path(r"C:\Users\simon\Downloads\P23_J73_passthrough_particles_selected.cs")
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

#%%
MICROGRAPH_SHAPE = particle_locations["location/micrograph_shape"][0]
#%%
particle_locations["center_x_pix"] = np.around(particle_locations["location/center_x_frac"] * MICROGRAPH_SHAPE[1], 0).astype(int)
particle_locations["center_y_pix"] = np.around(particle_locations["location/center_y_frac"] * MICROGRAPH_SHAPE[0], 0).astype(int)

# %%
