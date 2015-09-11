#! /usr/bin/env python
# -*- coding: utf-8 -*

# Windows requires some weird kind of workaround to show application's icon in taskbar
import ctypes
import platform
if platform.system() == 'Windows':
	myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
	ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

import sys

from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtMultimedia import QSound
from VkClientThread import VkClientThread
from LoginWidget import LoginWidget
from Registry import Registry
from Config import Config
from ChatWindow import ChatWindow
from PopUp import PopUpMan
from ConfigWindow import ConfigWindow

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent = None):
		QtWidgets.QMainWindow.__init__(self, parent)
		self.ui = uic.loadUi("./ui/mainwindow.ui", self)
		
		self.registry = Registry()
		self.registry.objects['config'] = Config()
		self.conf = self.registry.objects['config']
		self.new_messages = {}
		self.popup_man = PopUpMan()
		
		self.sound = QSound(r"./data/sounds/bb2.wav")
		self.online_icon = QtGui.QIcon(r"./data/pics/online.png")
		self.offline_icon = QtGui.QIcon(r"./data/pics/offline.png") 
		self.mail_icon = QtGui.QIcon(r"./data/pics/mail.png")
		
		# connect signals and slots
		self.actionLogin.triggered.connect(self.login)
		self.actionExit.triggered.connect(self.close)
		self.actionOptions.triggered.connect(self.openConfigWindow)
		self.contactList.itemDoubleClicked.connect(self.openChatWindow)
		self.popup_man.openTabMainWindow.connect(self.openChatTabFromPopUp)

		if self.registry.objects['config'].isLoggedIn():
			self.actionLogin.setEnabled(False)
		
	# widgets handlers
	def login(self):
		if not hasattr(self, 'loginWidget') or not self.loginWidget.isVisible():
			self.loginWidget = LoginWidget(self)
			self.loginWidget.show()
			self.loginWidget.raise_()
		else:
			self.loginWidget.activateWindow()

	def openConfigWindow(self):
		if not hasattr(self, 'w') or not self.w.isVisible():
			self.w = ConfigWindow(self)
			self.w.show()
			self.w.raise_()
		else:
			self.w.activateWindow()

	# other methods
	def updateConfig(self):
		self.conf = self.registry.objects['config']
		if 'vk' in self.registry.objects:
			vk = self.registry.objects['vk']
			self.UpdateContactList(vk.online)

	def server_connection_init(self):
		self.registry.objects['vk'] = VkClientThread(self.conf.config['token'])
		vk = self.registry.objects['vk']
		vk.start()
		vk.updateOnlineForMainWindow.connect(self.UpdateContactList)
		vk.receiveMessagesForMainWindow.connect(self.ReceiveNewMessages)
		
	def UpdateContactList(self, names):
		self.contactList.clear()
		vk = self.registry.objects['vk']
		showed = set()

		# TODO: fix if user is not friend
		for user in self.new_messages:
			item = QtWidgets.QListWidgetItem(vk.id_to_name[user])
			item.setIcon(self.mail_icon)
			self.contactList.addItem(item)
			showed.add(user)
		
		for user in names:
			if user not in showed:
				item = QtWidgets.QListWidgetItem(vk.id_to_name[user])
				item.setIcon(self.online_icon)
				self.contactList.addItem(item)
				showed.add(user)

		conf = Registry().objects['config']
		if conf.config['showOffline']:
			for id in vk.id_to_name:
				if id not in showed:
					item = QtWidgets.QListWidgetItem(vk.id_to_name[id])
					item.setIcon(self.offline_icon)
					self.contactList.addItem(item)

	def ReceiveNewMessages(self, msgs):
		vk = self.registry.objects['vk']
		msgs.pop(0)
		mark_as_read = []
		old_messages = self.new_messages
		cnt = 0

		self.new_messages = {}
		for msg in reversed(msgs):
			if hasattr(self, 'ChatWindow') and msg['user_id'] in self.ChatWindow.tabs:
				uid = msg['user_id']
				name = vk.id_to_name[uid]
				cur_idx = self.ChatWindow.currentIndex()
				if self.ChatWindow.tabs[uid] == cur_idx:
 					self.ChatWindow.getTab(msg['user_id']).add_message(msg['body'], name)
 					mark_as_read.append(msg['id'])
				if not self.ChatWindow.widget(self.ChatWindow.tabs[uid]).isActiveWindow():
					self.ChatWindow.setTabIcon(self.ChatWindow.tabs[uid], self.mail_icon)
					self.popup_man.create(msg['user_id'], msg['id'], msg['body'], cnt)
					if self.conf.config['enableSound']:
						self.sound.play()

			else:
				if(msg['user_id'] not in old_messages or
					(msg['user_id'] in old_messages 
					and msg['id'] not in old_messages[msg['user_id']])
				   ):
					self.popup_man.create(msg['user_id'], msg['id'], msg['body'], cnt)
					if self.conf.config['enableSound']:
						self.sound.play()
					cnt += 1
				if msg['user_id'] in self.new_messages:
 					self.new_messages[msg['user_id']].append(msg['id'])
				else:
					self.new_messages[msg['user_id']] = [msg['id']]
		if mark_as_read:
			vk.markAsRead(mark_as_read)
		if self.new_messages or mark_as_read:
			self.UpdateContactList(vk.online)
	
	def openChatTab(self, id, show_history_mes = 3):
		if not hasattr(self, 'ChatWindow'):
			self.ChatWindow = ChatWindow()
		vk = self.registry.objects['vk']
		name = vk.id_to_name[id]
		self.ChatWindow.addChatTab(id, name, show_history_mes)
		self.ChatWindow.show()
	
	def openChatTabFromPopUp(self, id):
		vk = self.registry.objects['vk']
		vk.markAsRead(self.new_messages[id])

		reg = Registry()
		loadHistory = reg.objects['config'].config['loadHistory']
		if loadHistory:
			historyCount = reg.objects['config'].config['historyCount']
		else:
			historyCount = 0

		self.openChatTab(id, len(self.new_messages[id]) + historyCount)
		del self.new_messages[id]
		self.UpdateContactList(vk.online)
	
	def openChatWindow(self, entry):
		name = entry.text()
		vk = self.registry.objects['vk']
		id = vk.name_to_id[name]

		reg = Registry()
		loadHistory = reg.objects['config'].config['loadHistory']
		if loadHistory:
			historyCount = reg.objects['config'].config['historyCount']
		else:
			historyCount = 0
		if id in self.new_messages:
			vk.markAsRead(self.new_messages[id])
			self.openChatTab(id, len(self.new_messages[id]) + historyCount)
			del self.new_messages[id]
			self.UpdateContactList(vk.online)
		else:
			self.openChatTab(id, historyCount)
 

def main():
	app = QtWidgets.QApplication(sys.argv)
	w = MainWindow()
	w.show()
	w.raise_()
	# TODO: Use threads? Gevent?
	if w.registry.objects['config'].isLoggedIn():
 		w.server_connection_init()
  	
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
