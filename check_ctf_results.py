# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 13:42:36 2021

@author: simon
"""

import numpy as np
from matplotlib import pyplot as plt
import read_star
from pathlib import Path   #more compatibility between diffrent OS's

plt.close("all")

star_file = "micrographs_ctf.star"
path = Path.cwd() / Path(star_file)
path_str = str(path)

ctf_data = read_star.read_type_of_data(path_str, "data_micrographs")

data_of_interest = ["rlnCtfAstigmatism", "rlnCtfFigureOfMerit", "rlnCtfMaxResolution", 
                    "rlnDefocusAngle", "rlnDefocusU", "rlnDefocusV"]
#Einheiten:
units = dict.fromkeys(data_of_interest)
units["rlnCtfMaxResolution"] = "$A^°$"
units["rlnDefocusU"] = "$A^°$"
units["rlnDefocusV"] = "$A^°$"






    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
