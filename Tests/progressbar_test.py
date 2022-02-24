# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 18:34:39 2021

@author: simon
"""

import time
from progress.bar import IncrementalBar

mylist = [1,2,3,4,5,6,7,8]
bar = IncrementalBar("Countdown", max = len(mylist))
for item in mylist:
    bar.next()
    time.sleep(0.1)
bar.finish()