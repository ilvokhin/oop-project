#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal
from Registry import Registry
from VkClientThread import VkClientThread

def markUrl(msg, proto):
	pos = 0
	while msg.find(proto, pos) != -1:
		start = msg.find(proto, pos)
		end = msg.find(" ", start)
		if end == -1:
			end = len(msg)
		url = msg[start : end]
		msg = msg[:end] + "\">" + url + "</a>" + msg[end:]
		msg = msg[:start] + "<a href=\"" + msg[start:]
		pos = 15 + start + 2*len(url) # 15 is the length of <a href=""></a>
	return msg

class ChatTab(QtWidgets.QWidget):
	resetIcon = pyqtSignal()
	def __init__(self, id):
		QtWidgets.QWidget.__init__(self, None)
		self.ui = uic.loadUi("./ui/chatTab.ui", self)
		self.closeButton.clicked.connect(self.closeButton_clicked)
		self.messageField.textChanged.connect(self.text_changed)
		self.sendButton.clicked.connect(self.send_message)
		self.id = id
		self.reg = Registry()
		self.vk = self.reg.objects['vk']

		self.chatLog.mouseReleaseEvent = lambda ev: self.open_url(QtCore.QPoint(ev.x(), ev.y()))

	def open_url(self, click):
		s = self.chatLog.anchorAt(click)
		if s:
			QtGui.QDesktopServices.openUrl(QtCore.QUrl(s))

	def closeButton_clicked(self):
		self.close()

	def text_changed(self):
		st = self.messageField.toPlainText()
		self.sendButton.setEnabled(st.size() > 0)

	def add_message(self, msg, name = "me"):
		msg = markUrl(markUrl(msg, "http://"), "https://")

		conf = self.reg.objects['config']
		if name == "me":
			color = conf.config['myColor']
		else:
			color = conf.config['friendsColor']
		self.chatLog.append("<b><font color=\"#" + color + "\">" + name + ":</font></b> " + msg)

	def send_message(self):
		msg = self.messageField.toPlainText()
		if msg:
			self.vk.sendMessage(self.id, unicode(msg))
			self.messageField.clear()
			self.add_message(msg)
			self.messageField.setFocus()

	def load_history(self, user_id, count = 3):
		msgs = self.vk.getHistory(user_id, count)
		name = self.vk.id_to_name[user_id]
		for msg in msgs:
			if msg['from_id'] == user_id:
				self.add_message(msg['body'], name)
			else:
				self.add_message(msg['body'])

	def keyPressEvent(self, event):
		if event.modifiers() and QtCore.Qt.ControlModifier:
			if event.key() == QtCore.Qt.Key_Return:
				self.send_message()
			elif event.key() == QtCore.Qt.Key_W:
				self.closeButton.click()

def main():
		app = QtGui.QApplication(sys.argv)
		w = ChatTab()
		w.show()
		w.raise_()
		sys.exit(app.exec_())

if __name__ == "__main__":
		main()
