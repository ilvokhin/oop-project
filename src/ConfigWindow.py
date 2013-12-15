#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import string

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic

from VkClientThread import VkClientThread
from LoginWidget import LoginWidget
from Registry import Registry
#from VkClient import VkClient
from Config import Config
from ChatWindow import ChatWindow

def isColor (s):
	s = str (s)
	hd = set (string.hexdigits)
	for i in s:
		if i not in hd:
			return False
	return len(s) == 6

class ConfigWindow (QtGui.QWidget):
	def __init__ (self, parent = None):
		QtGui.QWidget.__init__(self, None)
		self.parent = parent
		Registry().objects['config'] = Config()
		self.conf = Registry().objects['config']
		self.ui = uic.loadUi(("./ui/configWindow.ui"), self)
		self.setWindowFlags (QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
		self.colorHelp.linkActivated.connect (self.open_browser)

		self.local = self.conf.config
		# flags first
		self.enableSound.setChecked (self.conf.config['enableSound'])
		self.showOffline.setChecked (self.conf.config['showOffline'])
		self.loadHistory.setChecked (self.conf.config['loadHistory'])

		# input fields second
		self.contactsTimeout.setValue (self.conf.config['contactsTimeout'])
		self.messagesTimeout.setValue (self.conf.config['messagesTimeout'])
		self.historyCount.setValue (self.conf.config['historyCount'])

		if isColor (self.conf.config['myColor']):
			self.myColor.setText (self.conf.config['myColor'])
		else:
			self.myColor.setText ('000000')
		if isColor (self.conf.config['friendsColor']):
			self.friendsColor.setText (self.conf.config['friendsColor'])
		else:
			self.friendsColor.setText ('000000')

		# finally, setting whether some widgets are active
		self.historyCount.setEnabled (self.loadHistory.isChecked())

		self.apply.accepted.connect (self.save)
		self.apply.rejected.connect (self.close)
		self.enableSound.toggled.connect (self.enableSoundSave)
		self.showOffline.toggled.connect (self.showOfflineSave)
		self.loadHistory.toggled.connect (self.loadHistorySave)
		self.contactsTimeout.valueChanged.connect (self.contactsTimeoutSave)
		self.messagesTimeout.valueChanged.connect (self.messagesTimeoutSave)
		self.historyCount.valueChanged.connect (self.historyCountSave)
		self.myColor.textChanged.connect (self.myColorSave)
		self.friendsColor.textChanged.connect (self.friendsColorSave)

	def enableSoundSave(self):
		self.local['enableSound'] = self.enableSound.isChecked()
	def showOfflineSave(self):
		self.local['showOffline'] = self.showOffline.isChecked()
	def loadHistorySave(self):
		self.local['loadHistory'] = self.loadHistory.isChecked()
		self.historyCount.setEnabled (self.loadHistory.isChecked())

	def contactsTimeoutSave(self):
		self.local['contactsTimeout'] = self.contactsTimeout.value()
	def messagesTimeoutSave(self):
		self.local['messagesTimeout'] = self.messagesTimeout.value()
	def historyCountSave(self):
		self.local['historyCount'] = self.historyCount.value()
	def myColorSave(self, value):
		if isColor(value):
			self.local['myColor'] = str (value)

	def friendsColorSave(self, value):
		if isColor(value):
			self.local['friendsColor'] = str (value)

	def open_browser (self, s):
		QtGui.QDesktopServices.openUrl (QtCore.QUrl (s))

	def save (self):
		self.conf.config = self.local
		self.conf.save()
		self.parent.updateConfig()
		self.close()

def main():
	app = QtGui.QApplication(sys.argv)
	w = ConfigWindow()
	w.show()
	w.raise_()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
