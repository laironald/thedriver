#!/usr/bin/python
import sys
import unittest
sys.path.append('..')

import thedriver
class TestTheDriver(unittest.TestCase):
    def setUp(self):
        self.g = thedriver.go()
        pass

    def tearDown(self):
        pass

    def test___init__(self):
        self.assertEqual(1, 1)
        self.assertItemsEqual([1,2],[2,1])
        self.assertIn(1, [1,2])
        pass

    def test_files(self):
        tot_files = len(self.g.files())
        self.assertTrue(self.g.files(title="liwen") < tot_files)

if __name__ == '__main__':
    unittest.main()

