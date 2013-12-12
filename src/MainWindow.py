#! /usr/bin/env python
# -*- coding: utf-8 -*

import sys

from PyQt4 import QtGui
from PyQt4 import uic

from VkClientThread import VkClientThread
from LoginWidget import LoginWidget
from Registry import Registry
#from VkClient import VkClient
from Config import Config
from ChatWindow import ChatWindow

class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent = None):
		QtGui.QMainWindow.__init__(self, parent)
		self.ui = uic.loadUi(("./ui/mainwindow.ui"), self)
		# init
		
		self.registry = Registry()
		self.registry.objects['config'] = Config()
		
		# connect widgets and slots
		self.loginButton.clicked.connect(self.loginButton_clicked)
                self.contactList.itemDoubleClicked.connect (self.contactListEntry_doubleclicked)

		if self.registry.objects['config'].isLogin():
			self.hide_loginButton()
		
	# widgets handlers
	def loginButton_clicked(self):
		self.loginWidget = LoginWidget(self)
		self.loginWidget.show()
		self.loginWidget.raise_()
	# other methods
	def hide_loginButton(self):
 		self.loginButton.hide()
                self.ui.layout().update()
	
	def server_connection_init(self):
		self.registry.objects['vk'] = VkClientThread(self.registry.objects['config'].config['token'])
		vk = self.registry.objects['vk']
		
		vk.start()
		
		self.connect(vk, vk.updateOnlineForMainWindow, self.UpdateContactList)
		self.connect(vk, vk.recieveMessagesForMainWindow, self.RecieveNewMessages)
		
		#contacts = vk.getAllFriends()
 		#contacts_name = vk.getUsersInfo(contacts)
	
		#for user in contacts_name:
		#	self.contactList.addItem(user['first_name'] + ' ' + user['last_name'])
	
	def UpdateContactList(self, names):
		self.contactList.clear()
		for user in names:
			self.contactList.addItem(user)

	def RecieveNewMessages(self, msgs):
		vk = self.registry.objects['vk']
		msgs.pop(0)
		mark_as_read = []
		for msg in reversed(msgs):
			if hasattr(self, 'ChatWindow') and msg['uid'] in self.ChatWindow.tabs:
				uid = msg['uid']
				name = vk.id_to_name[uid]
				self.ChatWindow.getTab(msg['uid']).add_message(msg['body'], name)
				# mark as read?
				mark_as_read.append(msg['mid'])
			else:
				pass
				#Change icon in contact list
				#print "Chat doesn't open"
				#print msg
		if mark_as_read:
			vk.markAsRead(mark_as_read)
	
        # proof of concept
        def contactListEntry_doubleclicked (self, entry):
                name = entry.text()
                if 'chatwindow' not in self.registry.objects:
                    self.registry.objects['chatwindow'] = ChatWindow()
                self.ChatWindow = self.registry.objects['chatwindow']
                id = self.registry.objects['vk'].name_to_id[unicode (name)]
                self.ChatWindow.addChatTab (id, name)
                self.ChatWindow.show()

def main():
	app = QtGui.QApplication(sys.argv)
	w = MainWindow()
	w.show()
	w.raise_()
	# TODO: Use threads? Gevent?
	if w.registry.objects['config'].isLogin():
 		w.server_connection_init()
  	
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
