# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 13:57:29 2020

@author: simon

This module contains two functions for reading Information from .star files, which are produced by Relion 3.1.0 during several steps of image processing.
It is (almost) the same as read_model_star.py, because all .star files have the same principle. 
"""

#functions:

def read_general_data(model_star_file):
    """Reads somewhat of the header in the star file. To my knowledge headers only exist in _model.star files"""
    assert model_star_file.endswith("_model.star")
    model_rows = []
    read_row = False
    with open(model_star_file, "r") as f:
        for row in f:
            if read_row:
                model_rows.append(row)
            if row.strip() == "data_model_general":
                #start to read/copy the rows...
                read_row = True
            if row.startswith("# version") and read_row:
                # ...  untill this happens
                break
    
    #clean up the rows from "\n" and blank space:
    for i in range(len(model_rows)):
        model_rows[i] = model_rows[i].strip()
        
    
    general_model_data = {}
    for row in model_rows:
        if row.startswith("_rln"):
            r = row.split()
            assert len(r) == 2
            key = r[0]
            value = float(r[1])
            general_model_data[key] = value
            
            
    return general_model_data
    

def read_type_of_data(model_star_file, type_of_data):
    """
    Reads specified parts of data from a _model.star file.
    INPUT:
        model_star_file:    a ..._model.star file from RELION
        type of data:       the type or part of the data that interests you
                            (e.g "data_model_classes" or "data_model_class_1 in _model.star files from Class2D")
                            NO "data_model_general" !!!
    RETURN: Dictionary with data
    """
    
    assert model_star_file.endswith(".star")
    assert type_of_data != "data_model_general"
    
    model_rows = []
    read_row = False
    with open(model_star_file, "r") as f:
        for row in f:
            if read_row:
                model_rows.append(row)
            if row.strip() == type_of_data:
                #start to read/copy the rows...
                read_row = True
            if row.startswith("# version") and read_row:
                # ...  untill this happens
                break
    
    #clean up the rows from "\n" and blank space:
    for i in range(len(model_rows)):
        model_rows[i] = model_rows[i].strip()
        
        
    #Get the column names:
    column_names = []
    for row in model_rows:
        if row.startswith("_rln"):
            r = row.split()
            col_name = r[0][1:]
            column_names.append(col_name)
            
    #read the data into a dictionary with column names as the keys
    data_model_classes = dict.fromkeys(column_names)
    #initialize lists for each key:
    for key in data_model_classes.keys():
        data_model_classes[key] = []
        
    for row in model_rows:
        data = row.split()
        if len(data) == len(column_names):
            for i in range(len(column_names)):
                data_model_classes[column_names[i]].append(data[i])
    
    
    #convert numbers into float data-type:
    for key in data_model_classes.keys():
        col = data_model_classes[key]
        try:
            for i in range(len(col)):
                data_model_classes[key][i] = float(col[i])
        except ValueError:
            print(f"ValueError: Values in column {key} can't be converted to float (might be no problem).")
            continue
        
    return data_model_classes


##############################################################################

#Usage example:

# model_star_file = "run_ct25_it025_model.star"
# general_data = read_general_data(model_star_file)
# data_model_classes = read_type_of_data(model_star_file, "data_model_classes")
    