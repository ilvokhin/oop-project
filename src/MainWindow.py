#! /usr/bin/env python
# -*- coding: utf-8 -*

import sys

from PyQt4 import QtGui
from PyQt4 import uic

from LoginWidget import LoginWidget
from Registry import Registry
from VkClient import VkClient
from Config import Config

class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent = None):
		QtGui.QMainWindow.__init__(self, parent)
		self.ui = uic.loadUi(("./ui/mainwindow.ui"), self)
		# init
		
		self.registry = Registry()
		self.registry.objects['config'] = Config()
		
		# connect widgets
		self.loginButton.clicked.connect(self.loginButton_clicked)
		
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
	
	def contact_list_init(self):
		self.registry.objects['vk'] = VkClient(self.registry.objects['config'].config['token'])
		vk = self.registry.objects['vk']
		contacts = vk.getAllFriends()
 		contacts_name = vk.getUsersInfo(contacts)
	
		for user in contacts_name:
			self.contactList.addItem(user['first_name'] + ' ' + user['last_name'])

def main():
	app = QtGui.QApplication(sys.argv)
	w = MainWindow()
	w.show()
	w.raise_()
	# TODO: Use threads? Gevent?
	w.contact_list_init()
  	
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
