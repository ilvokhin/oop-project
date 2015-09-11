#! /usr/bin/env python
# -*- coding: utf-8 -*

import sys, time, ssl, vk
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from functools import wraps
from Registry import Registry

def exeption_handling(func):
	@wraps(func)
	def wrapper(*args, **kwds):
		#print("Wrapped")
		while True:
			try:
				return func(*args, **kwds)
			except Exception as e:
				print("Wrapper caught error: %s" % e)
			else:
				break
	return wrapper

class VkOnTimeWorker(QtCore.QThread):
	onlineChanged = pyqtSignal(list)
	messagesReceived = pyqtSignal(dict)

	def __init__(self, sleep_time, fd, *args, **kwargs):
		QtCore.QThread.__init__(self)
		self.sleep_time = sleep_time
		self.updateOnline = fd['updateOnline']
		self.receiveMessages = fd['receiveMessages']
		self.args = args
		self.kwargs = kwargs
		self.data = []
	
	def __del__(self):
		self.wait()
	
	def run(self):
		while True:
			online, messages = None, None
			while not online:
				try:
					online = self.updateOnline()
				except Exception as e:
					print(e)
			while not messages:
				try:
					messages = self.receiveMessages(filters=1)
				except Exception as e:
					print(e)

			#if new_data != self.data:
			self.messages = messages
			self.online = online
			self.onlineChanged.emit(self.online)
			self.messagesReceived.emit(self.messages)
			time.sleep(self.sleep_time)

class VkClientThread(QtCore.QThread):
	updateOnlineForMainWindow = pyqtSignal(list)
	receiveMessagesForMainWindow = pyqtSignal(list)

	@exeption_handling
	def __init__(self, access_token):
		QtCore.QThread.__init__(self)
		self.token = access_token
		self.vk = vk.API(access_token = self.token)
		self.online = []
		self.messages = []		
		self.initContacts()
	
	@exeption_handling
	def run(self):
		updMsg = Registry().objects['config'].config['messagesTimeout']
		updCnt = Registry().objects['config'].config['contactsTimeout']

		func_dict = {'updateOnline':self.vk.friends.getOnline, 'receiveMessages':self.vk.messages.get}
		self.checker = VkOnTimeWorker(updCnt, func_dict)
		self.checker.onlineChanged.connect(self.updateOnline)
		self.checker.messagesReceived.connect(self.receiveMessages)
		self.checker.start()
		
	@exeption_handling
	def initContacts(self):
		self.contacts_id = self.getAllFriends()
		response = self.getUsersInfo(self.contacts_id)
		self.id_to_name = {}
		self.name_to_id = {}
		for elem in response:
			name = elem['first_name'] + ' ' + elem['last_name']
			_id = elem['id']
			self.id_to_name[_id] = name
			self.name_to_id[name] = _id

	@exeption_handling
	def updateOnline(self, online):
		self.online = online
		self.updateOnlineForMainWindow.emit(self.online)
	
	@exeption_handling
	def receiveMessages(self, msgs):
		self.messages = msgs['items']
		self.receiveMessagesForMainWindow.emit(self.messages)

	@exeption_handling
	def getServerTime(self):
		"""Test function to check connection to vk.com server."""
		return self.vk.GetServerTime()
	
	@exeption_handling
	def getAllFriends(self):
		"""Return list with users ids only."""
		return self.vk.friends.get()
	
	@exeption_handling
	def getUserInfo(self, user_ids):
		"""Return dict with user info.
		Example: {u'first_name': u'Pavel', u'last_name': u'Durov', u'id': 1}"""
		return self.vk.users.get(user_ids=user_id)[0]

	@exeption_handling
	def getUsersInfo(self, user_ids):
		"""Return list of dicts with users info.
		Example: [{u'first_name': u'Pavel', u'last_name': u'Durov', u'id': 1}]"""
		uids_str = ', '.join(str(elem) for elem in user_ids['items'])
		return self.vk.users.get(user_ids=uids_str)
	
	@exeption_handling
	def sendMessage(self, user_id, message):
		return self.vk.messages.send(user_id=uid, message=message)
	
	@exeption_handling
	def markAsRead(self, message_ids):
		mids_str = ', '.join(str(elem) for elem in message_ids)
		self.vk.messages.markAsRead(message_ids = mids_str)
	
	@exeption_handling
	def getHistory(self, user_id, count = 3, rev = 0):
		"""Return list of dict with history"""
		history = self.vk.messages.getHistory(user_id = user_id, count = count, rev = rev)['items']
		if history:
			history.pop(0)
		return reversed(history)

def main():
	vk = VkClientThread('')
	app = QtGui.QApplication(sys.argv)
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
