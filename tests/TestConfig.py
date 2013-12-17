#! /usr/bin/env python
# -*- coding: utf-8 -*

import sys

sys.path.append('../src')

from Config import Config
import unittest
import os

class TestConfig(unittest.TestCase):
	def setUp(self):
		self.conf = Config()
	def test1(self):
		self.assertFalse(self.conf.isLoggedIn())
	
	def test2(self):
		param = ['enableSound', 'showOffline', 'loadHistory', 
                       'contactsTimeout', 'messagesTimeout', 'historyCount',
                       'myColor', 'friendsColor']
		for elem in param:
			self.assertIn(elem, self.conf.config)

	def test3(self):
		param = ["test1", "test2", "test3"]
		for elem in param:
			self.assertNotIn(elem, self.conf.config)
		for elem in param:
			self.conf.update(elem, elem)
		for elem in param:
			self.assertIn(elem, self.conf.config)
	
	def test4(self):
		with open('token') as f:
			token = f.read().replace('\n', '')
			self.conf.update('token', token)
		
		self.assertTrue(self.conf.isLoggedIn())
		
	def tearDown(self):
		os.remove("./data/config.conf")

if __name__=="__main__":
        unittest.main()
