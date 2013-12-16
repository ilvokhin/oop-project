#! /usr/bin/env python
# -*- coding: utf-8 -*

# TODO: remove after testing
from PyQt4 import QtGui
import sys

from PyQt4 import QtCore
import vkontakte
import time
import ssl
from Registry import Registry

from functools import wraps

def exeption_handling(func):
	@wraps(func)
	def wrapper(*args, **kwds):
		#print "Wrapped"
		while True:
			try:
				return func(*args, **kwds)
			except Exception as e:
				print "Wrapper catch error: ", e.message
			else:
				break
	return wrapper

class VkOnTimeWorker(QtCore.QThread):
	def __init__(self, sleep_time, signal_name, function, *args, **kwargs):
		QtCore.QThread.__init__(self)
		self.sleep_time = sleep_time
		self.signal = QtCore.SIGNAL(signal_name)
		self.function = function
		self.args = args
		self.kwargs = kwargs
		self.data = []
	
	def __del__(self):
		self.wait()
	
	def run(self):
		while True:
			new_data = None
			while not new_data:
				try:
					new_data = self.function(*self.args, **self.kwargs)
				except Exception as e:
					print e.message
			#if new_data != self.data:
			self.data = new_data
			self.emit(self.signal, self.data)
			time.sleep(self.sleep_time)


class VkClientThread(QtCore.QThread):
	@exeption_handling
	def __init__(self, access_token):
		QtCore.QThread.__init__(self)
		self.token = access_token
		self.vk = vkontakte.API(token = self.token)
		self.online = []
		self.messages = []
		
		self.updateOnlineForMainWindow = QtCore.SIGNAL("updateOnlineForMainWindow")
		self.recieveMessagesForMainWindow = QtCore.SIGNAL("recieveMessagesForMainWindow")
		
		self.initContacts()
	
	@exeption_handling
	def run(self):
		updMsg = Registry().objects['config'].config['messagesTimeout']
		updCnt = Registry().objects['config'].config['contactsTimeout']

		self.online_checker = VkOnTimeWorker(updCnt, "updateOnline", self.vk.friends.getOnline)
		self.connect(self.online_checker, self.online_checker.signal, self.updateOnline)
		self.online_checker.start()
		
		self.message_checker = VkOnTimeWorker(updMsg, "recieveMessages", self.vk.messages.get, filters = 1)
		self.connect(self.message_checker, self.message_checker.signal, self.recieveMessages)
		self.message_checker.start()
		
 	@exeption_handling
	def initContacts(self):
		self.contacts_id = self.getAllFriends()
		response = self.getUsersInfo(self.contacts_id)
		self.id_to_name =  {}
		self.name_to_id = {}
		
		for elem in response:
			name = elem['first_name'] + ' ' + elem['last_name']
			_id = elem['uid']
			self.id_to_name[_id] = name
			self.name_to_id[name] = _id

	@exeption_handling
	def updateOnline(self, online):
		self.online = online
		#print self.online
		self.emit(self.updateOnlineForMainWindow, self.online)
	
	@exeption_handling
	def recieveMessages(self, msgs):
		self.messages = msgs
		#print self.messages
		self.emit(self.recieveMessagesForMainWindow, self.messages)

	@exeption_handling
	def getServerTime(self):
		"""Test function to check connection to vk.com server."""
		return self.vk.GetServerTime()
	
	@exeption_handling
	def getAllFriends(self):
		"""Return list *only* with users ids."""
		return self.vk.friends.get()
	
	@exeption_handling
	def getUserInfo(self, user_id):
		"""Return dict with user info.
		Example: {u'first_name': u'Pavel', u'last_name': u'Durov', u'uid': 1}"""
		return self.vk.users.get(uid = user_id)[0]

	@exeption_handling
	def getUsersInfo(self, users_id):
		"""Return list of dicts with users info.
		Example: [{u'first_name': u'Pavel', u'last_name': u'Durov', u'uid': 1}]"""
		uids_str = ', '.join(str(elem) for elem in users_id)
		return self.vk.users.get(uids=uids_str)
	
	@exeption_handling
	def sendMessage(self, uid, message):
		return self.vk.messages.send(uid = uid, message = message)
	
	@exeption_handling
	def markAsRead(self, mids):
		mids_str = ', '.join(str(elem) for elem in mids)
		self.vk.messages.markAsRead(mids = mids_str)
	
	@exeption_handling
	def getHistory(self, uid, count = 3, rev = 0):
		"""Return list of dict with history"""
		history = self.vk.messages.getHistory(uid = uid, count = count, rev = rev)
		history.pop(0)
		return reversed(history)

def main():
	vk = VkClientThread('')
	app = QtGui.QApplication(sys.argv)
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
