# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 15:39:13 2023

@author: ASUS
"""

'''
Scenario:
A company that produces rock aggregate wants to explore three factors they consider important in locating a factory in the UK. They have asked you to produce some software that helps them do this. They have provided two dimensional raster data for each factor with values in the range [0, 255]. The higher the value of a factor, the more suitable the location is for the factory. Each factor is to be multiplied by a weight and the weighted factors are to be added up to give an overall suitability for each raster location.

The company wants the software to allow them to easily choose the factor weights and visualise the suitability.

Write some software which does the following.
1.Reads the raster data and displays them.
2.Multiplies each raster by a factor, adds the weighted rasters together and rescales the resulting raster to have values in the range [0, 255].
3.Displays the result raster and writes this to a file.
4.Provides a GUI that allows the user to choose the weights by means of ‘sliders’ and that displays the result.

Hints:
●Use lists (of lists) to store the raster data.
●Process the data row by row and column by column and create a combined weighted and summed value raster, then rescale this raster.
'''

#%% Packages
import modules.io as io
import modules.geometry as geo
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import matplotlib.animation as anim
import tkinter as tk
import tkinter.ttk as ttk
import csv

#%% Functions
def label(x):
    
    global geofac, popfac, trafac
    
    if (round(scale1.get(),2) != geofac):
        scale1_label.config(text='Geology factor= ' + str(round(float(x)*100,2)) + '%')
    if (round(scale2.get(),2) != popfac):
        scale2_label.config(text='Population factor= ' + str(round(float(x)*100,2)) + '%')
    if (round(scale3.get(),2) != trafac):
        scale3_label.config(text='Transport factor= ' + str(round(float(x)*100,2)) + '%')
    
    geofac = round(scale1.get(),2)
    popfac = round(scale2.get(),2)
    trafac = round(scale3.get(),2)
    
    
def exiting():
    try:
        root.quit()
        root.destroy()
    except Exception:
        # Prevents reporting of a harmless Tcl error message:
        # "TclError: can't invoke "destroy" command: application has been destroyed"
        pass

def update(geofac, popfac, trafac):
    """
    Updates scale_label and canvas.

    Parameters
    ----------
    x : str.
        Number.

    Returns
    -------
    None.

    """
    
    
    # Calculate the final raster
    sum_raster = [] # create a new list to store the summed value raster data
    for i in range(n_rows): # loop for every row
        sum_row = [] # create a list to store the result data and clear it 
        for j in range(n_cols): # loop for every column
            result = geo.multiply(geology[i][j], geofac, population[i][j], popfac, transport[i][j], trafac) # multiply the raster by its factor
            sum_row.append(result) # append the result to the list sum_row
        sum_raster.append(sum_row) # append the list sum_row to the list sum_raster
    sum_raster = geo.rescale(sum_raster) # rescale the multiplied raster to (0, 255)
    plt.imshow(sum_raster)
    plt.show()
    #canvas.draw()

#%% Main body
if __name__ == '__main__':
    
    # Input data, read raster data from local path
    geology=io.read_data('InputData/geology.txt') #read geology
    population=io.read_data('InputData/population.txt') #read population
    transport=io.read_data('InputData/transport.txt') #read transport
    
    # Retrieve the number of rows and columns in the raster 
    n_rows, n_cols = geo.get_rows_cols(geology) # all rasters have the same number of rows(530) and columns(335)
    
    # Define the facotr and set a default value
    geofac = 0
    popfac = 0
    trafac = 0
    
    #GUI
    # Initialise source data figure
    sd_figure = plt.figure(figsize=(18, 10))
    re_figure = plt.figure(figsize=(18, 10))
    #ax = figure.add_axes([0, 0, 1, 1])
    
    # Create the tkinter window
    root = tk.Tk()
    root.wm_title("Site Suitability")
    
    # Create a canvas to display the figure
    canva1 = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(sd_figure, master=root)
    canva1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    # Show source data 
    # subplot 1: geology
    plt.subplot(1, 3, 1)
    plt.imshow(geology)
    plt.title('Geology')
    
    # subplot 2: population
    plt.subplot(1, 3, 2)
    plt.imshow(population)
    plt.title('Population')
    
    # subplot 3: transport
    plt.subplot(1, 3, 3)
    plt.imshow(transport)
    plt.title('Transport')
    
    plt.tight_layout()  # adjust spacing between subplots
    
    plt.show()
    canva1.draw()    
    
    #Create a container to place sliders and labels
    frame = ttk.Frame(root)
    frame.pack()
    
    # Create geology slider
    # Create a label to describe the variable
    scale1_name = ttk.Label(frame, text="Geology:")
    scale1_name.grid(row=0,column=0)
    # Create a scale
    scale1 = ttk.Scale(frame, from_=0, to=1, command=label, length=500)
    scale1.grid(row=0,column=1)
    # Create a Label widget to display scale value 
    scale1_label = ttk.Label(frame, text='Move the scale slider to change the factor.')
    scale1_label.grid(row=0,column=2)
    
    # Create population slider
    scale2_name = ttk.Label(frame, text="Population:")
    scale2_name.grid(row=1,column=0)
    scale2 = ttk.Scale(frame, from_=0, to=1, command=label, length=500)
    scale2.grid(row=1,column=1)
    scale2_label = ttk.Label(frame, text='Move the scale slider to change the factor.')
    scale2_label.grid(row=1,column=2)
    
    # Create transport slider
    scale3_name = ttk.Label(frame, text="Transport:")
    scale3_name.grid(row=2,column=0)
    scale3 = ttk.Scale(frame, from_=0, to=1, command=label, length=500)
    scale3.grid(row=2,column=1)
    scale3_label = ttk.Label(frame, text='Move the scale slider to change the factor.')
    scale3_label.grid(row=2,column=2)
     
    
    button = ttk.Button(frame, text="Generate result raster", command=lambda: update(scale1.get(), scale2.get(), scale3.get()))
    button.grid(row=5,column=1) # add the button to the window
    
    
    
    # Create a Button widget and link this with the exiting function
    exit_button = ttk.Button(frame, text="Exit", command=exiting)
    exit_button.grid(row=5,column=2)
    
    # Exit if the window is closed.
    root.protocol('WM_DELETE_WINDOW', exiting)

    # Start the GUI
    root.mainloop()

    
        