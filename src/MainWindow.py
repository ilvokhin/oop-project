#! /usr/bin/env python
# -*- coding: utf-8 -*

# Windows requires some weird kind of workaround to show the application icon in the taskbar
import ctypes
import platform
if platform.system() == 'Windows':
	myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
	ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

import sys

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
from VkClientThread import VkClientThread
from LoginWidget import LoginWidget
from Registry import Registry
from Config import Config
from ChatWindow import ChatWindow
from PopUp import PopUpMan
from ConfigWindow import ConfigWindow

class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent = None):
		QtGui.QMainWindow.__init__(self, parent)
		self.ui = uic.loadUi("./ui/mainwindow.ui", self)
		
		self.registry = Registry()
		self.registry.objects['config'] = Config()
		self.conf = self.registry.objects['config']
		self.new_messages = {}
		self.popup_man = PopUpMan()
		
		self.sound = QtGui.QSound(r"./data/sounds/bb2.wav")
		self.online_icon = QtGui.QIcon(r"./data/pics/online.png")
		self.offline_icon = QtGui.QIcon(r"./data/pics/offline.png") 
		self.mail_icon = QtGui.QIcon(r"./data/pics/mail.png")
		
		# connect signals and slots
		self.actionLogin.triggered.connect(self.login)
		self.actionExit.triggered.connect (self.close)
		self.actionOptions.triggered.connect(self.openConfigWindow)
		self.contactList.itemDoubleClicked.connect (self.openChatWindow)
		self.connect (self.popup_man, self.popup_man.signal, self.openChatTabFromPopUp)

		if self.registry.objects['config'].isLoggedIn():
			self.actionLogin.setEnabled (False)
		
	# widgets handlers
	def login (self):
		if not hasattr (self, 'loginWidget') or not self.loginWidget.isVisible():
			self.loginWidget = LoginWidget(self)
			self.loginWidget.show()
			self.loginWidget.raise_()
		else:
			self.loginWidget.activateWindow()

	def openConfigWindow (self):
		if not hasattr (self, 'w') or not self.w.isVisible():
			self.w = ConfigWindow(self)
			self.w.show()
			self.w.raise_()
		else:
			self.w.activateWindow()

	''' I will uncomment this whenever I find a way to make application quit instead of folding when X is pressed
	def hideEvent (self, e):
		self.trayIcon = QtGui.QSystemTrayIcon (QtGui.QIcon (r"./data/pics/icon.png"))
		self.trayIcon.setToolTip ("VPythonte messenger")
		self.trayIcon.activated.connect (self.unfold)
		self.trayIcon.show()
		self.hide()
		self.setWindowFlags (QtCore.Qt.Tool)
		print e.type()

	def unfold (self, e):
		self.trayIcon.hide()
		self.setWindowFlags (QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint )
		self.show()
		self.showNormal()
		self.activateWindow()
	'''

	# other methods
	def updateConfig (self):
		self.conf = self.registry.objects['config']
		if 'vk' in self.registry.objects:
			vk = self.registry.objects['vk']
			self.UpdateContactList(vk.online)

	def server_connection_init(self):
		self.registry.objects['vk'] = VkClientThread(self.conf.config['token'])
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
			item.setIcon(self.mail_icon)
			self.contactList.addItem(item)
			showed.add(user)
		
		for user in names:
			if user not in showed:
				item = QtGui.QListWidgetItem(vk.id_to_name[user])
				item.setIcon(self.online_icon)
				self.contactList.addItem(item)
				showed.add(user)

		conf = Registry().objects['config']
		if conf.config['showOffline']:
			for id in vk.id_to_name:
				if id not in showed:
					item = QtGui.QListWidgetItem(vk.id_to_name[id])
					item.setIcon(self.offline_icon)
					self.contactList.addItem(item)

	def RecieveNewMessages(self, msgs):
		vk = self.registry.objects['vk']
		msgs.pop(0)
		mark_as_read = []
		old_messages = self.new_messages
		cnt = 0

		self.new_messages = {}
		for msg in reversed(msgs):
			if hasattr(self, 'ChatWindow') and msg['uid'] in self.ChatWindow.tabs:
				uid = msg['uid']
				name = vk.id_to_name[uid]
				cur_idx = self.ChatWindow.currentIndex()
				if self.ChatWindow.tabs[uid] == cur_idx:
 					self.ChatWindow.getTab(msg['uid']).add_message(msg['body'], name)
 	 				mark_as_read.append(msg['mid'])
				if not self.ChatWindow.widget(self.ChatWindow.tabs[uid]).isActiveWindow():
					self.sound.play()

			else:
				if (msg['uid'] not in old_messages or
					(msg['uid'] in old_messages 
					and msg['mid'] not in old_messages[msg['uid']])
				   ):
					self.popup_man.create(msg['uid'], msg['mid'], msg['body'], cnt)
					if self.conf.config['enableSound']:
						self.sound.play()
					cnt += 1
				if msg['uid'] in self.new_messages:
 					self.new_messages[msg['uid']].append(msg['mid'])
				else:
					self.new_messages[msg['uid']] = [msg['mid']]
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
		print "open chattab from popup", id
	
	def openChatWindow (self, entry):
		name = entry.text()
		vk = self.registry.objects['vk']
		id = vk.name_to_id[unicode (name)]

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
	app = QtGui.QApplication(sys.argv)
	w = MainWindow()
	w.show()
	w.raise_()
	# TODO: Use threads? Gevent?
	if w.registry.objects['config'].isLoggedIn():
 		w.server_connection_init()
  	
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
