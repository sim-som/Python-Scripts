# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 13:42:36 2021

@author: simon
"""

import numpy as np
from matplotlib import pyplot as plt
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
print(path_str)
assert path_str.endswith("_ctf.star")

#einlesen der .star datei mittels "read_star" modul:
ctf_data = read_star.read_type_of_data(path_str, "data_micrographs")
N = len(ctf_data)

data_of_interest = ["rlnCtfAstigmatism", "rlnCtfFigureOfMerit", "rlnCtfMaxResolution", 
                    "rlnDefocusAngle", "rlnDefocusU", "rlnDefocusV"]
#Einheiten:
units = dict.fromkeys(data_of_interest)
units["rlnCtfMaxResolution"] = "$A^°$"
units["rlnDefocusU"] = "$A^°$"
units["rlnDefocusV"] = "$A^°$"


#Plot the data of interest for each micrograph:
print("Plotting Data vs. micrographs")
for data in data_of_interest:
    im_name = f"all_micrographs_{data[3:]}"
    
    print(data)
    x = np.arange(len(ctf_data[data]))
    y = np.array(ctf_data[data])
    plt.figure(im_name)
    plt.title(parent)
    plt.bar(x, y)
    plt.xlabel("micrograph")
    y_label = data
    if units[data]:
        y_label += f" / {units[data]}"
    plt.ylabel(y_label)
    

fig, axs = plt.subplots(3,2, sharex=True, figsize = (10,10), num = "ctfestimate_Overview")

print("Overview")

N = len(data_of_interest)
for i in range(N):
    #print("i =", i)
    
    data = data_of_interest[i]
    
    y = ctf_data[data]
    x = np.arange(len(y))
    
    if i == 0:
        row = 0
    else:
        row = i // 2
    #print("row =" ,row)
    col = i % 2
    #print("col =" ,col)
    axs[row, col].bar(x,y)
    axs[row, col].set_title(data)




    

# Histograms for each number of interest:
print("Plotting histograms")
for data in data_of_interest:
    im_name = f"histogram_{data[3:]}"
    
    plt.figure(im_name)
    plt.title(parent)
    plt.hist(ctf_data[data], bins = 200)
    x_label = data
    if units[data]:
        x_label += f" / {units[data]}"
    plt.xlabel(x_label)
    plt.ylabel("counts")
    


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
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
