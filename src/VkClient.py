#! /usr/bin/env python
# -*- coding: utf-8 -*

import vkontakte

class VkClient(object):
	def __init__(self, access_token):
		self.token = access_token
		self.vk = vkontakte.API(token = self.token)
	
	def getServerTime(self):
		"""Test function to check connection to vk.com server."""
		return self.vk.GetServerTime()
	
	def getAllFriends(self):
		"""Return list *only* with users ids."""
		return self.vk.friends.get()
	
	def getOnlineFriends(self):
		return self.vk.friends.getOnline()
	
	def getUserInfo(self, user_id):
		"""Return dict with user info. 
		Example: {u'first_name': u'Pavel', u'last_name': u'Durov', u'uid': 1}"""
		return self.vk.users.get(uid = user_id)[0]
	
	def getUsersInfo(self, users_id):
		"""Return list of dicts with users info.
		Example: [{u'first_name': u'Pavel', u'last_name': u'Durov', u'uid': 1}]"""
		uids_str = ', '.join(str(elem) for elem in users_id)
		return self.vk.users.get(uids=uids_str)
	
	def getUnreadMessages(self):
		"""Return list of dicts, first element of list is number of unread messages"""
		return self.vk.messages.get(filters = 1)
	
	def sendMessage(self, uid, message):
		return vk.messages.send(uid = uid, message = message)

