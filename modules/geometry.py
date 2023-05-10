# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 19:03:27 2023

@author: ASUS
"""
def multiply(data1, factor1, data2, factor2, data3, factor3):
    '''
    Multiply data and its corresponding factor and then add them togeter

    Parameters
    ----------
    datas : lsit
    factors : number

    Returns
    -------
    sum_raster : list

    '''
    # Create a list to store resulting raster
    sum_raster = []
    # Get the number of rows and columns
    n_rows, n_cols = get_rows_cols(data1)
    # Loop
    for i in range(n_rows):
        sum_row = [] # create a list to store the result data and clear it 
        for j in range(n_cols):
            # Multiply each raster by a factor and add the weighted rasters together
            result = data1[i][j] *factor1 + data2[i][j] * factor2 + data3[i][j] * factor3
            result = round(result,2) # round the result to the nearest decimal point
            sum_row.append(result) # append the result to the list sum_row
        sum_raster.append(sum_row) # append the list sum_row to the list sum_raster
        
    return sum_raster

def get_rows_cols(data):
    '''
    Retrieve the number of rows in a list

    Parameters
    ----------
    data : list
        Two-dimensional array

    Returns
    -------
    n_rows : int
        The number of rows.
    n_cols : int
        The number of columns.

    '''
    # Initialisation
    n_rows = 0 
    n_cols = 0
    
    # Cumulation
    for line in data:
        n_rows += 1
        n_cols = 0
        for value in line:
            n_cols +=1
            
    return n_rows, n_cols

def get_max_min(data):
    '''
    Get the max value and min value in a data list

    Parameters
    ----------
    data : list
        Data.

    Returns
    -------
    maxdata : number
    mindata : number

    '''
    # Initialisation
    maxdata = 0 # set it as min value in range
    mindata = 255 # set it as max value in range
    n_rows, n_cols = get_rows_cols(data) # get the number of rows and columns
    # Loop
    for i in range(n_rows):
        for j in range(n_cols):
            if (maxdata < data[i][j]): # when maxdata meet a larger value
                maxdata = data[i][j] # change itself into the larger one
            if (mindata > data[i][j]): # when mindata meet a smaller value
                mindata = data[i][j] # change itself into the smaller one
                
    return maxdata, mindata

def rescale(data):
    '''
    Rescale the data into a new range (0, 255)

    Parameters
    ----------
    data : list

    Returns
    -------
    rescaled_data : list

    '''
    # Get the number of rows and columns
    n_rows, n_cols = get_rows_cols(data)
    # Get the max value and min value
    maxdata, mindata = get_max_min(data)
    # Create a list to store the new scaled data
    rescaled_data = []
    
    # Only rescale the raster when it really has values
    if (maxdata != mindata):
        # Loop
        for i in range(n_rows):
            rescaled_row = [] # initialise a list to store datas in a row or clear it
            for j in range(n_cols):
                result = round(((data[i][j] - mindata) / (maxdata - mindata)) * 255) # rescale
                rescaled_row.append(result) # append result to the list of row
            rescaled_data.append(rescaled_row) # append the row to the final list
    else : # When all values are 0
        # Loop
        for i in range(n_rows):
            rescaled_row = [] # initialise a list to store datas in a row or clear it
            for j in range(n_cols):
                result = maxdata # rescale
                rescaled_row.append(result) # append result to the list of row
            rescaled_data.append(rescaled_row) # append the row to the final list
            
    return rescaled_data