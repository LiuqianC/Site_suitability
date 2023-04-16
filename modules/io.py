# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 18:43:56 2023

@author: ASUS
"""

import csv

def read_data(filename):
    '''
    

    Parameters
    ----------
    filename : string
        The path of the csv input file.

    Returns
    -------
    n_rows : int
        To indentify how many rows are there.
    n_cols : int
        To indentify how many colums are there.
    data : list
        The csv input file will store in the list 'data'.

    '''
    # Read input data
    f = open(filename, newline='')
    data = []
    for line in csv.reader(f, quoting=csv.QUOTE_NONNUMERIC):
        row = []
        for value in line:
            row.append(value)
            #print(value)
        data.append(row)
    f.close()
    #print(data)
    return data

def write_data(filename,data):
    '''
    

    Parameters
    ----------
    filename : string
        The path of the csv output file.
    data : list
        The output csv file

    Returns
    -------
    None.

    '''
    
    f = open(filename,'w', newline='')
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row) #list of values
    f.close()