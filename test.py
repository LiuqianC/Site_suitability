# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 16:47:21 2023

@author: Andy Turner
"""
import unittest
import modules.geometry as gm

class TestDocs(unittest.TestCase):

    def test_mul(self):
        self.assertEqual(gm.multiply([[1,1],[1,1]], 1, [[2,2],[2,2]], 2, [[3,3],[3,3]], 3), [[14,14],[14,14]])
        self.assertEqual(gm.multiply([[1,1],[1,1]], 0.3, [[2,2],[2,2]], 0.3, [[3,3],[3,3]], 0.4), [[2,2],[2,2]])

if __name__ == '__main__':
    unittest.main()