"""
Created on Wed Apr  7 12:30:02 2021

@author: simon
"""
#%%
import numpy as np
from matplotlib import pyplot as plt
import read_star  #Eigenes Modul
from pathlib import Path   #more compatibility between diffrent OS's
import sys
import pandas as pd

plt.close("all")
plt.ioff()

#Einlesen von pfad und _ctf.star Datei 
#(per Komandozeilen Argument zu umständlich. Lieber interactive python):
path_str = "C:/Users/simon/OneDrive/Dokumente/Studium/Master/Masterarbeit/Auswertungen/Trehalose_Quantifoil_Blottingprotokoll_B3_20210409/CtfFind/73k/micrographs_ctf.star"

try:
    path = Path(path_str)
except:
    print("Problem beim Einlesen des übergebenen Pfades")

w_dir = path.parent
file = path.parts[-1]
    
assert path.exists()
assert w_dir.is_dir()
path_str = str(path)
print(path_str)
assert path_str.endswith("_ctf.star")

#Einlesen der .star datei mittels "read_star" modul:
ctf_data = read_star.read_type_of_data(path_str, "data_micrographs")
#umwandeln in DataFrame:
ctf_df = pd.DataFrame(ctf_data)

ctf_df.to_excel(w_dir / Path("ctffind_data.xlsx"))


# %% Plot relationsships between data
import seaborn as sns

fig = sns.relplot(data =ctf_df, x="rlnDefocusU", y = "rlnCtfMaxResolution")

sns.relplot(data = ctf_df, x= "rlnCtfFigureOfMerit", y="rlnCtfMaxResolution")

# %% 

# %%

