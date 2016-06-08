#!/usr/bin/env python

from fractalsfun.fractalcluster import FractalCluster
import unittest
import numpy

class test_Sanity(unittest.TestCase):
    def test_nothing(self):
        pass

class test_Basic(unittest.TestCase):
    def test_size(self):
        fc = FractalCluster(1000, 1.6)
        self.assertTrue(fc.size >= 1000)

    def test_finalsize(self):
        fc = FractalCluster(1000, 1.6)
        self.assertEqual(len(fc.positions), 1000)

