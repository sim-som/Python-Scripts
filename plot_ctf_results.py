# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 13:42:36 2021

@author: simon
"""

import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("AGG")   # simple backend just for saving
import read_star  #Eigenes Modul
from pathlib import Path   #more compatibility between diffrent OS's
import sys

plt.close("all")
plt.ioff()
#Einlesen von pfad und _ctf.star Datei per Komandozeilen Argument:
path_str = sys.argv[1]
try:
    path = Path(path_str)
except:
    print("Problem beim Einlesen des übergebenen Pfades")

parent = path.parent
file = path.parts[-1]
    
assert path.exists()
assert parent.is_dir()
path_str = str(path)
assert path_str.endswith("_ctf.star")

#einlesen der .star datei mittels "read_star" modul:
ctf_data = read_star.read_type_of_data(path_str, "data_micrographs")

categories = ["rlnCtfAstigmatism", "rlnCtfFigureOfMerit", "rlnCtfMaxResolution", 
                    "rlnDefocusAngle", "rlnDefocusU", "rlnDefocusV"]
# Define units for the categories:
units = {
    "rlnCtfAstigmatism": "A°",      # ??? not sure (TODO)
    "rlnCtfFigureOfMerit": None,
    "rlnCtfMaxResolution": "$A°$",
    "rlnDefocusAngle": "°",
    "rlnDefocusU": "$µm$",
    "rlnDefocusV": "$µm$"
}


# Covert defocus values from Angström (10^-10) to micro meter (10^-6):
ctf_data["rlnDefocusU"] = np.array(ctf_data["rlnDefocusU"]) * 1e-4
ctf_data["rlnDefocusV"] = np.array(ctf_data["rlnDefocusV"]) * 1e-4




#Plot the data of interest for each micrograph:
print("Plotting Data vs. micrographs")
for cat in categories:
    im_name = f"all_micrographs_{cat[3:]}"
    
    x = np.arange(len(ctf_data[cat]))
    y = np.array(ctf_data[cat])

    print(cat, ":")
    print(y)

    plt.figure(im_name)
    plt.title(parent)
    plt.scatter(x, y)
    plt.xlabel("micrograph")
    y_label = cat
    if units[cat]:
        y_label += f" / {units[cat]}"
    plt.ylabel(y_label)

plt.tight_layout()
    

fig, axs = plt.subplots(3,2, sharex=False, figsize = (10,10), num = "ctfestimate_Overview")
axs = axs.flatten()

for i, cat in enumerate(categories):

    y = ctf_data[cat]
    x = np.arange(len(y))
    axs[i].scatter(x,y)
    axs[i].set_title(cat)
    axs[i].set_xlabel("image #")
    y_label = cat
    if units[cat]:
        y_label += f" / {units[cat]}"
    axs[i].set_ylabel(y_label)

plt.suptitle(str(path.parent))
plt.tight_layout()


# Histograms for each data of interest:
print("Plotting histograms")
for data in categories:
    im_name = f"histogram_{data[3:]}"
    
    plt.figure(im_name)
    plt.title(parent)
    plt.hist(ctf_data[data])
    x_label = data
    if units[data]:
        x_label += f" / {units[data]}"
    plt.xlabel(x_label)
    plt.ylabel("counts")

plt.tight_layout()
    
# Overview of all histograms:
fig, axs = plt.subplots(3,2, sharey=True, figsize = (10,10), num = "histogram_Overview")
axs = axs.flatten()

for i, data in enumerate(categories):

    axs[i].hist(ctf_data[data])
    axs[i].set_title(data)
    x_label = data
    if units[data]:
        x_label += f" / {units[data]}"
    axs[i].set_xlabel(x_label)
    axs[i].set_ylabel(f"counts")

plt.tight_layout()



# Save all figures:
# user_input = input("Save all figures?")    
# if user_input.lower() == "yes":
print(f"Saving figures in {parent}")
im_format = "png"
for fig in plt.get_figlabels():
    plt.figure(fig)
    
    dest_path = parent / Path(fig + "." + im_format)
    print(f"Figure saved as {dest_path}")
    plt.savefig(dest_path, format = im_format)
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
