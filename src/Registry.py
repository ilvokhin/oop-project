#! /usr/bin/env python
# -*- coding: utf-8 -*
class Registry(object):
	objects = {}
	def __new__(cls):
		if not hasattr(cls, 'instance'):
			cls.instance = super(Registry, cls).__new__(cls)
		return cls.instance
