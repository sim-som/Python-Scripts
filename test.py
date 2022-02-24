# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 17:27:51 2021

@author: simon
"""

from pathlib import Path


path = "C:/Users/simon/Documents/Python Scripts/test.txt"
path = Path(path)

assert path.exists()
print("path:", path)
print("parent:", path.parent)
print(path.parent.is_dir())
print("suffix:", path.suffix)
print("parts:", path.parts)
print("file:", path.parts[-1])