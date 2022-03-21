# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 12:48:45 2021

@author: simon
"""

# Short script for renaming mrc files that have blankspace in their names.
# Relion CTFfind4 and several other programs don't like filenames with blankspace

import os
import sys
from pathlib import Path   #more compatibility between diffrent OS's
import argparse

# %%
# function definitions:
def replace_blank_space(file_path:Path, replacement = " "):
        file_name:str = file_path.name
        new_file_name = file_name.replace("_", replacement)
        print("File with blankspace:", file_name)
        print("File without blankspace:", new_file_name)
        os.rename(file_path, file_path.parent / Path(new_file_name))

# %%

# Angabe von pfad des image Ordners per Komandozeilen Argument:

parser = argparse.ArgumentParser(
    description="""     Short script for renaming mrc files that have underscores in their names.
                        The underscore is replaced by a blankspace."""
    )
parser.add_argument("images_dir", help="The directory with the image files")
parser.add_argument("glob_pattern", help="A glob pattern specifying, which files in the directory should be renamed")
args = parser.parse_args()

try:
    img_dir_p = Path(args.images_dir)
except:
    print("Problem beim Einlesen des übergebenen Pfades")
    sys.exit()

assert img_dir_p.is_dir() and img_dir_p.exists()

for img_file_p in img_dir_p.glob(args.glob_pattern):
    print(f"Replacing uncerscore with blank space in: {img_file_p}" )
    replace_blank_space(img_file_p)

    