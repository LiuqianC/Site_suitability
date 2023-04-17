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
import tkinter as tk
import tkinter.ttk as ttk

#%% Functions
def labeling(x):
    '''
    Purpose: Changing the label which indicates the value of the scale. Changing the factors as the label showing.
    Hints: When the function first runs, 3 factors are all 0.

    Parameters
    ----------
    x : str
        the value of scale.

    Returns
    -------
    None.

    '''
    # Transfer the 3 global variable
    global geofac, popfac, trafac
    
    # Change the label content, rounded to two decimal places
    # E.g. Geology factor= 20.34%
    if (round(scale1.get(),2) != geofac): # when geoslider changes
        scale1_label.config(text='Geology factor = ' + str(round((float(x)*100))) + '%')
        scale2.config(to=(1-round(scale1.get(),2)), state="normal")
    if (round(scale2.get(),2) != popfac): # when popslider changes
        scale2_label.config(text='Population factor = ' + str(round((float(x)*100))) + '%')
        scale3.config(from_=(1-round(scale1.get(),2)-round(scale2.get(),2)), to=(1-round(scale1.get(),2)-round(scale2.get(),2)), state="normal")
        scale3_label.config(text='Transport factor = ' + str(round(((1-float(scale1.get())-float(scale2.get()))*100))) + '%')
    
    # Change the factors' value to the new ones, rounded to two decimal places
    geofac = round(scale1.get(),2)
    popfac = round(scale2.get(),2)
    trafac = (1-round(scale1.get(),2)-round(scale2.get(),2))
    
    
def exiting():
    """
    Exit the program.
    """
    root.quit() # quit root
    root.destroy() # destory root
    #sys.exit(0)
    
def update(geofac, popfac, trafac):
    """
    Purpose: Updating scale_label and canvas.
    Hints: Closing existing figure is to avoid overlaping the new image with the old one.
           The new figure don't have source data images, so they need to be added again.

    Parameters
    ----------
    x : str.
        Number.

    Returns
    -------
    None.

    """
    
    # Transfer the global variables
    global figure, sum_raster
    
    # Calculate the final raster
    sum_raster = [] # create a new list to store the summed value raster data
    for i in range(n_rows): # loop for every row
        sum_row = [] # create a list to store the result data and clear it 
        for j in range(n_cols): # loop for every column
            result = geo.multiply(geology[i][j], geofac, population[i][j], popfac, transport[i][j], trafac) # multiply the raster by its factor
            sum_row.append(result) # append the result to the list sum_row
        sum_raster.append(sum_row) # append the list sum_row to the list sum_raster
    sum_raster = geo.rescale(sum_raster) # rescale the multiplied raster to (0, 255)
    
    # Close existing figure
    plt.close(figure)
    
    # Create a new figure
    figure = plt.figure(figsize=(24, 10))
    
    # Change the canva1's figure to the new one
    canva1.figure = figure
    
    # Combine 4 plots into one plot
    # subplot 1: geology
    plt.subplot(1, 4, 1) # the overall plot has 1 row and 4 columns and this is the first one
    plt.imshow(geology) # show list geology as image
    plt.title('Geology') # the subplot's title
    
    # subplot 2: population
    plt.subplot(1, 4, 2) # this is the second one
    plt.imshow(population)
    plt.title('Population')
    
    # subplot 3: transport
    plt.subplot(1, 4, 3) # the third one
    plt.imshow(transport)
    plt.title('Transport')
    
    #subplot 4: multiplied raster
    plt.subplot(1, 4, 4) # the fourth one
    plt.imshow(sum_raster)
    plt.title('Multiplied Raster')
    
    # show the overall plot at canva1
    canva1.draw()
    write_button.config(state="normal")
    return sum_raster

def output():
    '''
    Output resulting raster data to a txt file
    '''
    try:
        io.write_data("OutputData/suitability.txt", sum_raster) # output 
        label = ttk.Label(frame, text="Data has written to local path successfully!") 

    except FileNotFoundError:
        label = tk.Label(frame, text="ERROR! Please check the output file path")
    
    label.grid(row=6, column=1) # show label at (6, 1)
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
    
    # Create a list to store final raster
    sum_raster = []
    
    # GUI
    # Initialise figure
    figure = plt.figure(figsize=(24, 10))
    
    # Create the tkinter window
    root = tk.Tk()
    root.wm_title("Site Suitability") # the window's title
    
    # Create a canvas to display the figure
    canva1 = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(figure, master=root) # initialisation
    canva1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1) # canva1's position
    
    # Show source data 
    # subplot 1: geology
    plt.subplot(1, 4, 1) # the overall plot has 1 row and 4 columns and Geology is the first subplot
    plt.imshow(geology)
    plt.title('Geology')
    
    # subplot 2: population
    plt.subplot(1, 4, 2) # the second is Population
    plt.imshow(population)
    plt.title('Population')
    
    # subplot 3: transport
    plt.subplot(1, 4, 3) # the third is Transport
    plt.imshow(transport)
    plt.title('Transport')
    
    # Show the plot at canva1
    canva1.draw()    
    
    #Create a container to place sliders and labels
    frame = ttk.Frame(root) # in the root
    frame.pack() # auto placed
    
    # Create geology slider
    # Create a label to describe the variable
    scale1_name = ttk.Label(frame, text="Geology:") # text
    scale1_name.grid(row=0, column=0) # position at (0, 0)
    # Create a scale
    scale1 = ttk.Scale(frame, from_=0, to=1, command=labeling, length=500) # the scale ranges from 0 to 1; when changing the scale, call function 'label'
    scale1.grid(row=0,column=1) # position at (0, 1)
    # Create a Label widget to display scale value 
    scale1_label = ttk.Label(frame, text='Move the scale slider to change the factor.') #text
    scale1_label.grid(row=0,column=2) # position at (0, 2)
    
    # Create population slider
    # Similar to geology slider
    scale2_name = ttk.Label(frame, text="Population:")
    scale2_name.grid(row=1,column=0)
    scale2 = ttk.Scale(frame, from_=0, to=1, command=labeling, length=500, state="disabled")
    scale2.grid(row=1,column=1)
    scale2_label = ttk.Label(frame, text='Move the scale slider to change the factor.')
    scale2_label.grid(row=1,column=2)
    
    # Create transport slider
    # Similar to geology slider
    scale3_name = ttk.Label(frame, text="Transport:")
    scale3_name.grid(row=2,column=0)
    scale3 = ttk.Scale(frame, from_=0, to=1, command=labeling, length=500, state="disabled")
    scale3.grid(row=2,column=1)
    scale3_label = ttk.Label(frame, text='Move the scale slider to change the factor.')
    scale3_label.grid(row=2,column=2)
     
    # Create a button to generate the multiplied raster (resulting raster)
    #'command=lambda: update' :lambda be used to transfer CURRENT variable's value, otherwise the initial values are transfered to function 'update'
    gen_button = ttk.Button(frame, text="Generate suitability raster", command=lambda: update(scale1.get(), scale2.get(), scale3.get())) 
    gen_button.grid(row=5, column=0) # position at (5, 1)
    
    write_button = ttk.Button(frame, text = "Write suitability data", command=lambda: output())
    write_button.config(state="disabled")
    write_button.grid(row=5, column=1)
    
    # Create a Button widget and link this with the exiting function
    exit_button = ttk.Button(frame, text="Exit", command=exiting)
    exit_button.grid(row=5,column=2)
    
    # Exit if the window is closed.
    root.protocol('WM_DELETE_WINDOW', exiting)

    # Start the GUI
    root.mainloop()

    
        