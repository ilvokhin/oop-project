#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic

from Registry import Registry
from VkClientThread import VkClientThread

def markUrl (msg, proto):
	msg = QtCore.QString (msg)
	pos = 0
	while msg.indexOf (proto, pos) != -1:
		urlStart = msg.indexOf (proto, pos)
		urlEnd = msg.indexOf (" ", urlStart)
		if urlEnd == -1:
			urlEnd = msg.size()
		url = msg.mid (urlStart, urlEnd - urlStart)
		msg.insert (urlEnd, "\">" + url + "</a>")
		msg.insert (urlStart, "<a href=\"")
		pos = 15 + urlStart + 2*url.size() # 15 is the length of <a href=""></a>
	return msg

class ChatTab (QtGui.QWidget):
	def __init__(self, id):
		QtGui.QWidget.__init__(self, None)
		self.ui = uic.loadUi ("./ui/chatTab.ui", self)
		self.closeButton.clicked.connect (self.closeButton_clicked)
		self.messageField.textChanged.connect (self.text_changed)
		self.sendButton.clicked.connect (self.send_message)
		self.id = id
		self.reg = Registry()
		self.vk = self.reg.objects['vk']

		# I know no other way to redefine childrens' functions. If someone does, please tell
		self.chatLog.mouseReleaseEvent = lambda ev: self.open_url (QtCore.QPoint (ev.x(), ev.y()))
		self.resetIcon = QtCore.SIGNAL ('resetIcon')

	def open_url (self, click):
		s = self.chatLog.anchorAt (click)
		if s:
			QtGui.QDesktopServices.openUrl (QtCore.QUrl (s))

	def closeButton_clicked (self):
		self.close()

	def text_changed (self):
		st = self.messageField.toPlainText()
		self.sendButton.setEnabled (st.size() > 0)

	def add_message(self, msg, name = "me"):
		msg = markUrl (markUrl (msg, "http://"), "https://")

		conf = self.reg.objects['config']
		if name == "me":
			color = conf.config['myColor']
		else:
			color = conf.config['friendsColor']
		self.chatLog.append ("<b><font color=\"#" + color + "\">" + name + ":</font></b> " + msg)

	def send_message (self):
		msg = self.messageField.toPlainText()
		if msg:
			self.vk.sendMessage (self.id, unicode(msg))
			self.messageField.clear()
			self.add_message(msg)
			self.messageField.setFocus()

	def load_history (self, uid, count = 3):
		msgs = self.vk.getHistory(uid, count)
		name = self.vk.id_to_name[uid]
	
		for msg in msgs:
			if msg['uid'] == uid:
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
