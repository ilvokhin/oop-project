#! /usr/bin/env python
# -*- coding: utf-8 -*

# TODO: remove after testing
from PyQt4 import QtGui
import sys

from PyQt4 import QtCore
import vkontakte
import time

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
			new_data = self.function(*self.args, **self.kwargs)
			if new_data != self.data:
				self.data = new_data
				self.emit(self.signal, self.data)
			time.sleep(self.sleep_time)

class VkClientThread(QtCore.QThread):
	def __init__(self, access_token):
		QtCore.QThread.__init__(self)
		self.token = access_token
		self.vk = vkontakte.API(token = self.token)
		self.contacts = []
		self.online = []
		self.messages = []
		
		self.online_checker = VkOnTimeWorker(5 * 60, "updateOnline", self.vk.friends.getOnline)
		self.connect(self.online_checker, self.online_checker.signal, self.updateOnline)
		self.online_checker.start()
		
		self.message_checker = VkOnTimeWorker(100, "recieveMessages", self.vk.messages.get, filters = 1)
		self.connect(self.message_checker, self.message_checker.signal, self.recieveMessages)
		self.message_checker.start()

	#TODO: add signal to mainwindow
	
	def updateOnline(self, online):
		self.online = online
		print self.online
	
	def recieveMessages(self, msgs):
		self.messages = msgs
		print self.messages

        def getServerTime(self):
                """Test function to check connection to vk.com server."""
                return self.vk.GetServerTime()

        def getUserInfo(self, user_id):
                """Return dict with user info. 
                Example: {u'first_name': u'Pavel', u'last_name': u'Durov', u'uid': 1}"""
                return self.vk.users.get(uid = user_id)[0]

        def getUsersInfo(self, users_id):
                """Return list of dicts with users info.
                Example: [{u'first_name': u'Pavel', u'last_name': u'Durov', u'uid': 1}]"""
                uids_str = ', '.join(str(elem) for elem in users_id)
                return self.vk.users.get(uids=uids_str)

        def sendMessage(self, uid, message):
                return vk.messages.send(uid = uid, message = message)

def main():
	vk = VkClientThread('b617d396e883d3a4e3ca3e1569dbab6a9fb386e1b1ccc305e1954e9142c23f83e66e5314a226d78cccb94')
	app = QtGui.QApplication(sys.argv)
	
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
