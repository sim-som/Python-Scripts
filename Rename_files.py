#%%
import shutil
from pathlib import Path

# %%
# Define list of files to be ranamed 
# from working directory with pathlibs glob function:

file_list = list(Path.cwd().glob("*.tif")) + list(Path.cwd().glob("metadata*.json"))
file_list

# %%
# Replace "TMV_1to100_in_100mM_Tris" by "TMV_1to100_in_H2O"
def replace_substring(filename:str):
    old = "TMV_1to100_in_100mM_Tris"
    new = "TMV_1to100_in_H2O"

    new_filename = filename.replace(old, new)

    return new_filename


# %%
# Rename files according to output of replace function:

def rename(old_filename, new_filename):
    shutil.move(old_filename, new_filename)

# %%
# loop over all specified files in working directory:
for file in file_list:
    new_filename = replace_substring(file.name)
    print(f"Renaming {file.name} to {new_filename} ...")
    rename(file.name, new_filename)


# %%
#%%
import json

# %%
meta_filename = "metadata of 4F-Treh_5%-TMV_1to100_in_H2O.json"
with open(meta_filename) as f:
    data = json.load(f)
# %%
data
# %%
data.keys()

# %%
new_data = {}
for key in data.keys():
    new_key = replace_substring(key)
    new_data[new_key] = data[key]

# %%
new_data
# %%
with open(meta_filename, mode="w") as f:
    json.dump(new_data, f, indent=0)
# %%
