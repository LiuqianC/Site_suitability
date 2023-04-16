# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 19:03:27 2023

@author: ASUS
"""
def multiply(data1, factor1, data2, factor2, data3, factor3):
    result = data1 *factor1 + data2 * factor2 + data3 * factor3
    result = round(result)
    return result

def get_rows_cols(data):
    '''
    Retrieve the number of rows in a list

    Parameters
    ----------
    data : list
        DESCRIPTION.

    Returns
    -------
    n_rows : int
        DESCRIPTION.
    n_cols : int
        DESCRIPTION.

    '''
    n_rows = 0 
    n_cols = 0
    for line in data:
        n_rows += 1
        n_cols = 0
        for value in line:
            n_cols +=1
    return n_rows, n_cols

def get_max_min(data, n_rows, n_cols):
    maxdata = 0
    mindata = 255
    for i in range(n_rows):
        for j in range(n_cols):
            if (maxdata < data[i][j]):
                maxdata = data[i][j]
            if (mindata > data[i][j]):
                mindata = data[i][j]
    return maxdata, mindata

def rescale(data):
    n_rows, n_cols = get_rows_cols(data)
    maxdata, mindata = get_max_min(data, n_rows, n_cols)
    rescaled_data = []
    for i in range(n_rows):
        rescaled_row = []
        for j in range(n_cols):
            result = round(((data[i][j] - mindata) / (maxdata - mindata)) * 255)
            rescaled_row.append(result)
        rescaled_data.append(rescaled_row)
    return rescaled_data