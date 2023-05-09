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
import unittest
import TestData.test as tt

#%% Functions
def labeling(x):
    '''
    Purpose: Changing the label which indicates the value of the scale. Changing the factors as the label showing.
    Hints: When the function first runs, 3 factors are all 0.
           Floating point numbers have a finite representation in a computer and are stored in binary, 
           so there are rounding errors when performing calculations.
           If using float number to calculate the result is lack of accuracy.0.47-0.46=0.009999999999999953

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
    # Get scale value
    geoget = int(scale1.get())
    popget = int(scale2.get())
    # Change the label content, rounded to two decimal places
    # E.g. Geology factor= 20%
    if (geoget != (geofac*100)): # when geoslider changes
        scale1_label.config(text='Geology factor = ' + str(geoget) + '%') # change the label1 text
        scale2.config(to=(100-geoget), length=(100-geoget)*5, state="normal") # change scale range
        write_button.config(state='disabled') # close write button

    if (popget != (popfac*100)): # when popslider changes
        scale2_label.config(text='Population factor = ' + str(popget) + '%') # change the label2 text
        scale3.config(from_=(100-geoget-popget), to=(100-geoget-popget), length=(100-geoget-popget)*5, state="normal") # change scale range
        scale3_label.config(text='Transport factor = ' + str(int(100-geoget-popget)) + '%') #autoly change label3 text
        scale1.config(state='disabled') # close scale1
    
    # Change the factors' value to the new ones, in two decimal places ranging (0, 1)
    geofac = geoget/100
    popfac = popget/100
    trafac = (100-geoget-popget)/100
    
def exiting():
    """
    Exit the program.
    """
    root.quit() # quit root
    root.destroy() # destory root
    
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
    global figure, sum_raster, write_label
    
    # Calculate the final raster
    sum_raster = geo.multiply(geology, geofac, population, popfac, transport, trafac)
    
    # Rescale the multiplied raster to (0, 255)
    sum_raster = geo.rescale(sum_raster) 
    
    # subplot 4: multiplied raster
    plt.subplot(1, 4, 4)# the fourth one
    plt.cla()
    plt.imshow(sum_raster)
    plt.title('Multiplied Raster')
    
    # Set the interval between individual subplots
    plt.subplots_adjust(wspace=0.3, hspace=0)
    
    # Show the overall plot at canva1
    canva1.draw()
    # plt.close()
    
    # Set widgets' state
    write_button.config(state="normal") # active write button
    scale1.config(state='disabled') # active scale1
    scale2.config(state='disabled') # close scale2
    scale3.config(state='disabled') # close scale3
    write_label.destroy() # delete write label
    return sum_raster

def output():
    '''
    Output resulting raster data to a txt file
    '''
    global write_label
    
    try:
        # Export txt
        filename = 'OutputData/suitability(geo' + str(geofac) + '_pop' + str(popfac) + '_tra' + str(trafac) +').txt'
        io.write_data(filename, sum_raster) # 
        # Export png
        imagename = 'OutputData/suitability(geo' + str(geofac) + '_pop' + str(popfac) + '_tra' + str(trafac) +').png'
        plt.close()
        plt.imshow(sum_raster) # plot the resulting raster
        plt.title("Site Suitability [geo" + str(geofac) + ", pop" + str(popfac) + ", tra" + str(trafac) + "]")
        plt.savefig(imagename) # export the output image
        plt.close()
        # Print success information
        write_label = ttk.Label(frame, text="Data has written to local path successfully!")
        
    except FileNotFoundError:
        # Print error information
        write_label = ttk.Label(frame, text="ERROR! Please check the output file path")
    
    write_label.grid(row=6, column=1) # show label at (6, 1)
    
def reset():
    # Transfer the 3 global variable
    global geofac, popfac, trafac
    
    # Change the factors' value to 0
    geofac = 0
    popfac = 0
    trafac = 0
    
    # Reset widgets' state and value
    scale1.config(state='normal')
    scale1.set(0)
    scale1_label.config(text='Transport factor = ' + str(0) + '%')
    
    scale2.config(state='normal')
    scale2.set(0)
    scale2.config(length=0)
    scale2_label.config(text='Transport factor = ' + str(0) + '%')
    
    scale3.config(state='normal')
    scale3.config(from_=0, to=0, length=0)
    scale3.set(0)
    scale3_label.config(text='Transport factor = ' + str(0) + '%')

    scale1.config(state='normal')
    scale2.config(state='disabled')
    scale3.config(state='disabled')
    

    
    
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
    figure = plt.figure(figsize=(12, 5), dpi=100)
    
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

    plt.subplots_adjust(wspace=0.3, hspace=0)
    
    # Create the tkinter window
    root = tk.Tk()
    root.wm_title("Site Suitability") # the window's title
    root.geometry("1500x1000")
    root.attributes("-topmost", True) # keep window at top
    
    # Create a canvas to display the figure
    canva1 = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(figure, master=root) # initialisation
    canva1._tkcanvas.pack(side=tk.TOP, fill=tk.NONE, expand=1) # canva1's position   
    canva1._tkcanvas.config(width=1200, height=500)
    
    # Show the plot at canva1
    canva1.draw()
    # Close the redundant window
    # plt.close() 
    
    #Create a container to place sliders and labels
    frame = ttk.Frame(root) # in the root
    frame.pack() # auto placed
    
    # Create geology slider
    # Create a label to describe the variable
    scale1_name = ttk.Label(frame, text="Geology:") # text
    scale1_name.grid(row=0, column=0,sticky='e') # position at (0, 0)
    # Create a scale
    scale1 = ttk.Scale(frame, from_=0, to=100, command=labeling, length=500) # the scale ranges from 0 to 100; when changing the scale, call function 'label'
    scale1.grid(row=0,column=1,sticky='w') # position at (0, 1)
    # Create a Label widget to display scale value 
    scale1_label = ttk.Label(frame, text='Move the scale slider to change the factor.') #text
    scale1_label.grid(row=0,column=2,sticky='w') # position at (0, 2)
    
    # Create population slider
    # Similar to geology slider
    scale2_name = ttk.Label(frame, text="Population:")
    scale2_name.grid(row=1,column=0,sticky='e')
    scale2 = ttk.Scale(frame, from_=0, to=100, command=labeling, length=500, state="disabled")
    scale2.grid(row=1,column=1,sticky='w')
    scale2_label = ttk.Label(frame)
    scale2_label.grid(row=1,column=2,sticky='w')
    
    # Create transport slider
    # Similar to geology slider
    scale3_name = ttk.Label(frame, text="Transport:")
    scale3_name.grid(row=2,column=0,sticky='e')
    scale3 = ttk.Scale(frame, from_=0, to=100, command=labeling, length=500, state="disabled")
    scale3.grid(row=2,column=1,sticky='w')
    scale3_label = ttk.Label(frame)
    scale3_label.grid(row=2,column=2,sticky='w')
     
    # Create a button to generate the multiplied raster (resulting raster)
    #'command=lambda: update' :lambda be used to transfer CURRENT variable's value, otherwise the initial values are transfered to function 'update'
    gen_button = ttk.Button(frame, text="Generate suitability raster", width=35, command=lambda: update(scale1.get(), scale2.get(), scale3.get())) 
    gen_button.grid(row=5, column=0) # position at (5, 1)
    
    write_button = ttk.Button(frame, text = "Write suitability data", width=35, command=lambda: output())
    write_button.config(state="disabled")
    write_button.grid(row=5, column=1)
    write_label = ttk.Label(frame) 
    
    # Create a Button widget and link this with the exiting function
    exit_button = ttk.Button(frame, text="Exit", width=35, command=exiting)
    exit_button.grid(row=5,column=2)
    
    # Create a button to reset 
    reset_button = ttk.Button(frame, text="Reset factors", padding=(0,15), command=lambda: reset())
    reset_button.grid(row=0, column=3, rowspan=3)
    
    # Exit if the window is closed.
    root.protocol('WM_DELETE_WINDOW', exiting)

    # Start the GUI
    root.mainloop()
    
    # generate test report
    suite = unittest.TestSuite()
    suite.addTest(tt.TestIO("test_read_data"))
    suite.addTest(tt.TestIO("test_write_data"))
    suite.addTest(tt.TestGeometry("test_mul"))
    suite.addTest(tt.TestGeometry("test_get_rows_cols"))
    suite.addTest(tt.TestGeometry("test_get_max_min"))
    suite.addTest(tt.TestGeometry("test_rescale"))
    with open("TestData/TestReport.txt","w")as f:
        runner = unittest.TextTestRunner(stream=f)
        result = runner.run(suite)   
        # write test report
        f.write(str(result))

    
        