#! /usr/bin/env python
# -*- coding: utf-8 -*

import os
import pickle

class Config(object):
	def __init__(self):
		self.config_file_path = "./data/config.conf"
		self.config = {}
		self.config['isLoggedIn'] = False
		if os.path.exists(self.config_file_path):
			with open(self.config_file_path) as f:
				self.config = pickle.load(f)
				if 'token' in self.config:
					self.config['isLoggedIn'] = True
		else:
			self.update ('enableSound', False)
			self.update ('showOffline', True)
			self.update ('loadHistory', True)
			self.update ('contactsTimeout', 30)
			self.update ('messagesTimeout', 2)
			self.update ('historyCount', 3)
			self.update ('myColor', '000000')
			self.update ('friendsColor', '000000')
			self.save()
			pass

	def isLoggedIn(self):
		return self.config['isLoggedIn']
	
	def save(self):
		with open(self.config_file_path, 'w+') as f:
			pickle.dump(self.config, f)
	
	def update(self, key, value):
		self.config[key] = value;
		if key == 'token':
			self.config['isLoggedIn'] = True
		self.save()
		

