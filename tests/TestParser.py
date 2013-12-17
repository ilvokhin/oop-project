#! /usr/bin/env python
# -*- coding: utf-8 -*

import sys

sys.path.append('../src')

from ChatTab import markUrl
from PyQt4.QtCore import QString
import unittest
import os

class TestParser(unittest.TestCase):
	def test1(self):
		s = "http://test.ru"
		res = markUrl (s, "http://")
		self.assertEqual (res, "<a href=\"http://test.ru\">http://test.ru</a>")
	def testMultiple1 (self):
		s = "http://test.ru ftp://test.ru https://test.ru"
		res = markUrl (markUrl (markUrl (s, "https://"), "ftp://"), "http://")
		self.assertEqual (res, "<a href=\"http://test.ru\">http://test.ru</a> <a href=\"ftp://test.ru\">ftp://test.ru</a> <a href=\"https://test.ru\">https://test.ru</a>")
		# there's nothing else to test, really.
		
if __name__=="__main__":
        unittest.main()
