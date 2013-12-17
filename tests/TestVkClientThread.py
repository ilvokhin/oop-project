#! /usr/bin/env python
# -*- coding: utf-8 -*

import sys

sys.path.append('../src')

from VkClientThread import VkClientThread
import unittest
import random
import string

def get_random_string(n):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(n))

class TestVkClientThread(unittest.TestCase):
	def setUp(self):
		with open('token') as f:
			self.token = f.read().replace('\n', '')
		self.vk = VkClientThread(self.token)
		self.user = self.vk.vk.users.get()[0]
	def test_connection(self):
		vk_time = self.vk.vk.getServerTime()
		assert vk_time is not None
	def test_message_sending_and_recieving(self):
		msg = get_random_string(100)
		uid = self.user['uid']
 		mid = self.vk.vk.messages.send(uid = uid, message = msg)
		recieve = self.vk.vk.messages.get(filters = 1)
		recieve.pop(0)
		for m in recieve:
			if mid == m['mid']:
				break
		else:
			assertTrue(False)

if __name__=="__main__":
	unittest.main()
