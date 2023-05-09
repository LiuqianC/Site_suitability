# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 16:47:21 2023

@author: Andy Turner
"""
import unittest
import numpy as np
import modules.geometry as gm
import modules.io as io
import os

class TestIO(unittest.TestCase):
    def test_read_data(self):
        # Test if read_data function returns list
        geology = io.read_data('../InputData/geology.txt')
        self.assertIsInstance(geology, list) 
        
        population = io.read_data('../InputData/population.txt')
        self.assertIsInstance(population, list)
        
        transport = io.read_data('../InputData/transport.txt')
        self.assertIsInstance(transport, list)
        
    def test_write_data(self):
        # Test if write_data function output correctly
        # Define input data
        data = [[1, 2, 3], [4, 5, 6]]
        
        # Define output file path
        file_path = '../OutputData/test_output.txt'
        
        # Write data to file
        io.write_data(file_path, data)
        
        # Read data from file
        output_data = io.read_data(file_path)
           
        # Remove output file
        os.remove(file_path)
        
        # Assert that data is correctly written to file
        self.assertEqual(output_data, data)
        
class TestGeometry(unittest.TestCase):
    def test_mul(self):
        # Define input data and factors
        data1 = [[1, 2], [3, 4]]
        factor1 = 0.2
        data2 = [[5, 6], [7, 8]]
        factor2 = 0.3
        data3 = [[9, 10], [11, 12]]
        factor3 = 0.5
        
        # Define expected output
        expected_output = [[6.2, 7.2], [8.2, 9.2]]
        
        # Call function and get actual output
        actual_output = gm.multiply(data1, factor1, data2, factor2, data3, factor3)
        
        # Assert that actual output matches expected output
        self.assertEqual(actual_output, expected_output)
        
    def test_get_rows_cols(self):
        data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        n_rows, n_cols = gm.get_rows_cols(data)
        self.assertEqual(n_rows, 3)
        self.assertEqual(n_cols, 3)
        
    def test_get_max_min(self):
        # Define input data
        data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        # Get expected output
        expected_max = 9
        expected_min = 1
    
        # Get actual output
        actual_max, actual_min = gm.get_max_min(data)
    
        # Assert that actual output equals expected output
        self.assertEqual(actual_max, expected_max)
        self.assertEqual(actual_min, expected_min)
        
    def test_rescale(self):
        # Define input data
        data = [[10, 235], [127, 63]]
        
        # Define expected output data
        expected_output = [[0, 255], [133, 60]]
        
        # Get actual output data
        actual_output = gm.rescale(data)
        
        # Assert that actual output matches expected output
        self.assertEqual(actual_output, expected_output)
        


if __name__ == '__main__':
    unittest.main()
    
