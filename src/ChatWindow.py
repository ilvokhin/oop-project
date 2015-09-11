#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
from Registry import Registry
from VkClientThread import VkClientThread
from ChatTab import ChatTab

class ChatWindow(QTabWidget):
	triggered = pyqtSignal()
	def __init__(self):
		QTabWidget.__init__(self, None)
		self.ui = uic.loadUi("./ui/chatWindow.ui", self)
		self.currentChanged.connect(self.resetTitle)
		self.triggered.connect(self.closeEvent)
		# user ID -> tab number
		self.tabs = {}

	def addChatTab(self, id, name, history_cnt = 3):
		if id not in self.tabs:
			tab = ChatTab(id)
			tab.closeButton.clicked.connect(self.closeButton_clicked)
			self.tabs[id] = self.count()
			self.addTab(tab, name)
			tab.load_history(id, history_cnt)

			# yes, I am cheating on you
			tab.chatLog.mousePressEvent = lambda ev: tab.resetIcon.emit
			tab.messageField.mousePressEvent = lambda ev: tab.resetIcon.emit
			tab.resetIcon.connect(self.resetTabIcon)

		self.setCurrentIndex(self.tabs[id])
		if self.isMinimized():
			self.showNormal()
		self.activateWindow()
		self.widget(self.tabs[id]).messageField.setFocus()

	def resetTabIcon(self):
		self.setTabIcon(self.currentIndex(), QtGui.QIcon())

	def getTab(self, uid):
		return self.widget(self.tabs[uid])

	def currentIndexChanged(self, idx):
		self.setTabIcon(idx, QtGui.QIcon())

	def closeButton_clicked(self):
		idx = self.currentIndex()
		id = self.widget(idx).id
		self.removeTab(idx)
		del self.tabs[id]
		if(self.count() == 0):
			self.close()
		else:
			self.widget(self.currentIndex()).messageField.setFocus()

	def resetTitle(self, id):
		self.setWindowTitle(self.tabText(id))

	def closeEvent(self, event):
		for tab in self.tabs:
			self.removeTab(self.tabs[tab])
		self.tabs = {}
		self.close()

def main():
		app = QtGui.QApplication(sys.argv)
		w = ChatWindow()
		w.show()
		w.raise_()
		sys.exit(app.exec_())

if __name__ == "__main__":
		main()
