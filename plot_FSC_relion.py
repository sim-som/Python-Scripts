# %%
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pathlib import Path
from starparser import fileparser
# %%
# parse the (modified) star file:
data, metadata = fileparser.getparticles(
    "/home/simon/jureca_project_mount/Trehalose_gunnar_2/Refine3D/job098/run_model_ausschnitt.star"
    )
# %%
# cast each column to float
data = data.astype(float)
#%%
data
#%%
# metadata:
metadata
# %%
metadata = metadata[2]
#%%
metadata = metadata.astype(str)
metadata
# %%
plt.figure()
plt.plot(data["_rlnResolution"], data["_rlnGoldStandardFsc"], label = "_rlnGoldStandardFsc")
# plt.plot(data["_rlnResolution"], data["_rlnSsnrMap"], label = "_rlnSsnrMap")
# plt.legend()
plt.xlabel("Resolution [A$^{-1}$]")
plt.title("FSC curve of: " + metadata["_rlnReferenceImage"][0])
plt.show()
# %%
