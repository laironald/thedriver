#!/usr/bin/python
import sys
import unittest
sys.path.append('../..')
import thedriver
import thedriver.download as drived


class TestTheDriver(unittest.TestCase):
    def setUp(self):
        self.g = thedriver.go()
        self.f = self.g.files(title="Testing")

    def tearDown(self):
        self.g = None

    def test___download(self):
        print drived.download(self.g, self.f[0])

if __name__ == '__main__':
    unittest.main()
