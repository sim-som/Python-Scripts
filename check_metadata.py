#%%
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import sys


from numpy import append

sys.path.insert(1, "C:/Users/simon/OneDrive/Dokumente/Studium/Master/Masterarbeit/Code/Metadata")
import metadata as meta
# %%
# read in metadata dict from .json file
metadata_file_p = Path("metadata of treh-tmv.json")
with open(metadata_file_p) as f:    
    whole_metadata:dict = json.load(f)
# %%
# as dataframe
df = {
    "Image": [],

    "Magnification": [],
    "ObjAperture": [],
    "Defocus_µm": [],
    "PixelSize_m": [],
    "AcqTime": [],
    "StagePosition": [],
    "TiltAngle_deg": []
}

for image, metadata in whole_metadata.items():

    df["Image"].append(image)
    df["Magnification"].append(meta.get_magnification(metadata))
    df["ObjAperture"].append(meta.get_obj_aperture(metadata))
    df["Defocus_µm"].append(meta.get_defocus(metadata) * 1e6)
    df["PixelSize_m"].append(meta.get_pixel_size_meter(metadata))
    df["AcqTime"].append(meta.get_acqusition_time(metadata))
    df["StagePosition"].append(meta.get_stage_position(metadata))
    df["TiltAngle_deg"].append(meta.get_tilt_angle_rad(metadata) * 180 / np.pi)

df = pd.DataFrame(df)
df = df.set_index("Image")

# %%

df["ObjAperture"].unique()


# %%
df["Magnification"].unique()
# %%

hole_view_df = df["Magnification"]
# %%
