# %%
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
# %%
from pyem import metadata
# %%
# parse particle locations:
man_pick_cs_file_p = Path(
    "/home/simon/gpu-rechner_u3_mount/cryoSPARC_projects/P23/exports/groups/P23_J43_particles/P23_J43_particles_exported.cs"
)

particle_data = metadata.parse_cryosparc_2_cs(man_pick_cs_file_p)
particle_data

# %%
# parse results of patch ctf estimation:
ctf_results_cs_file_p = Path(
    "/home/simon/gpu-rechner_u3_mount/cryoSPARC_projects/P23/exports/groups/P23_J15_exposures/P23_J15_exposures_exported.cs"
)

ctf_data = metadata.parse_cryosparc_2_cs(ctf_results_cs_file_p)
ctf_data
# %%
plt.figure()
plt.plot(ctf_data["rlnDefocusV"], label = "rlnDefocusV", alpha = 0.7)
plt.plot(ctf_data["rlnDefocusU"], label = "rlnDefocusU", alpha = 0.7)
plt.ylabel("Defocus / Ang")
plt.xlabel("image ID")
plt.legend()
plt.title("Defocus")
plt.show()


plt.figure()
plt.hist(ctf_data["rlnDefocusV"], bins= "auto", label = "rlnDefocusV", alpha = 0.7)
plt.hist(ctf_data["rlnDefocusU"], bins="auto", label = "rlnDefocusU", alpha = 0.7)
plt.xlabel("Defocus / Ang")
plt.legend()
plt.title("Defocus")
plt.show()

# %%
# plot every axis with seaborn
## ID row
# ctf_data["ID"] = np.arange(len(ctf_data))
# # "melt" the data frame:
# ctf_data_melt = pd.melt(ctf_data, id_vars=["ID"])

# # plot the melted data:
# sns.relplot(data=ctf_data_melt, x="ID", y="value", hue="variable")


# %%
plt.figure()
plt.plot(ctf_data["rlnCtfMaxResolution"], label = "rlnCtfMaxResolution")
plt.ylabel("Resolution / Ang")
plt.xlabel("image ID")
plt.title("Estimated max. Resolution")
plt.show()

plt.figure()
plt.hist(ctf_data["rlnCtfMaxResolution"], bins="auto", label = "rlnCtfMaxResolution", alpha = 0.7)
plt.xlabel("Resolution / Ang")
plt.title("Estimated max. Resolution")
plt.show()


# %%
(ctf_data["rlnCtfFigureOfMerit"] == 0).all()

# %%
# parse results of motion correction:
motion_corr_results_p = Path(
    "/home/simon/gpu-rechner_u3_mount/cryoSPARC_projects/P20/J82/micrographs_rigid_aligned.cs"
)
motion_corr_df = metadata.parse_cryosparc_2_cs(motion_corr_results_p)
motion_corr_df
# %%
