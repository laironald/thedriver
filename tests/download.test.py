#!/usr/bin/python
import sys
import unittest
sys.path.append('..')
import thedriver
import thedriver.download as drived


class TestTheDriver(unittest.TestCase):
    def setUp(self):
        self.g = thedriver.go()
        #self.f = self.g.files(title="Testing")

    def tearDown(self):
        self.g = None

    def test_download(self):
        f = self.g.files(title="Testing")
        print f[0]
        #content = drived.download(self.g, self.f[0])
        #self.assertTrue("<html>" in content)

    # --- FORMAT CLASS ---
    def test_format_init(self):
        self.assertTrue("<html>" in drived.format('document.html').html)
        self.assertEqual(drived.format("content").html, "content")


if __name__ == '__main__':
    unittest.main()
