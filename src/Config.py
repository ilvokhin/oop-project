#! /usr/bin/env python
# -*- coding: utf-8 -*

import os
import pickle

class Config(object):
	def __init__(self):
		self.config_file_path = "./data/config.conf"
		self.config = {}
		self.config['is_login'] = False
		if os.path.exists(self.config_file_path):
			with open(self.config_file_path) as f:
				config = pickle.load(f)
			if 'token' in config:
				self.config['is_login'] = True
		else:
			# add default values to config file
			pass
	
	def isLogin(self):
		return self.config['is_login']
	
	def save(self):
		with open(self.config_file_path, 'w+') as f:
			pickle.dump(self.config, f)
	
	def update(self, key, value):
		self.config[key] = value;
		self.save()

