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
		self.new_messages = {}
		
		# connect widgets and slots
		self.loginButton.clicked.connect(self.loginButton_clicked)
                self.contactList.itemDoubleClicked.connect (self.contactListEntry_doubleclicked)

                # TODO: add a button for configuration window
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
		
	def UpdateContactList(self, names):
		self.contactList.clear()
		
 		vk = self.registry.objects['vk']
		
		showed = set()
		
		# TODO: fix if user is not friend
		for user in self.new_messages:
			item = QtGui.QListWidgetItem(vk.id_to_name[user])
                        item.setIcon(QtGui.QIcon(r"./data/pics/mail.png"))
                        self.contactList.addItem(item)
                        showed.add(user)
		
		for user in names:
			if user not in showed:
				item = QtGui.QListWidgetItem(vk.id_to_name[user])
				item.setIcon(QtGui.QIcon(r"./data/pics/online.png"))
				self.contactList.addItem(item)
				showed.add(user)
		for id in vk.id_to_name:
			if id not in showed:
				item = QtGui.QListWidgetItem(vk.id_to_name[id])
                                item.setIcon(QtGui.QIcon(r"./data/pics/offline.png"))
                                self.contactList.addItem(item)

	def RecieveNewMessages(self, msgs):
		vk = self.registry.objects['vk']
		msgs.pop(0)
		mark_as_read = []
		self.new_messages.clear()
		for msg in reversed(msgs):
			if hasattr(self, 'ChatWindow') and msg['uid'] in self.ChatWindow.tabs:
				uid = msg['uid']
				name = vk.id_to_name[uid]
				cur_idx = self.ChatWindow.currentIndex()
				if self.ChatWindow.tabs[uid] == cur_idx:
 					self.ChatWindow.getTab(msg['uid']).add_message(msg['body'], name)
 	 				mark_as_read.append(msg['mid'])
			else:
				#Change icon in contact list
  				print "Chat doesn't open"
				print msg
				if msg['uid'] in self.new_messages:
 					self.new_messages[msg['uid']].append(msg['mid'])
				else:
					self.new_messages[msg['uid']] = [msg['mid']]
		if mark_as_read:
			vk.markAsRead(mark_as_read)
		if self.new_messages or mark_as_read:
			self.UpdateContactList(vk.online)

        def contactListEntry_doubleclicked (self, entry):
                name = entry.text()
		vk = self.registry.objects['vk']
		if not hasattr(self, 'ChatWindow'):
			self.ChatWindow = ChatWindow()
                id = vk.name_to_id[unicode (name)]
		if id in self.new_messages:
			self.ChatWindow.addChatTab (id, name, len(self.new_messages[id]))
			vk.markAsRead(self.new_messages[id])
			del self.new_messages[id]
			self.UpdateContactList(vk.online)
		else:
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
