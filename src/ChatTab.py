#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic

from PyQt4.QtCore import QString
from Registry import Registry
from VkClientThread import VkClientThread

class ChatTab (QtGui.QWidget):
    def __init__(self, id, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = uic.loadUi (("./ui/chatTab.ui"), self)
        self.closeButton.clicked.connect(self.closeButton_clicked)
        self.messageField.textChanged.connect (self.text_changed)
        self.sendButton.clicked.connect(self.send_message)
        self.id = id
	
	reg = Registry()
        self.vk = reg.objects['vk']

    def closeButton_clicked (self):
        self.close()
        self.closeButton.raise_()

    def text_changed (self):
        st = self.messageField.toPlainText()
        if st.size() > 0:
            self.sendButton.setEnabled (True)
        else:
            self.sendButton.setEnabled (False)

    def add_message(self, msg, name = "me"):
        self.chatLog.append("<b>" + name + ":</b> " + msg)

    def send_message (self):
        msg = self.messageField.toPlainText()
	if( msg):
		self.vk.sendMessage(self.id, unicode(msg))
		self.messageField.clear()
		self.add_message(msg)
		self.messageField.setFocus()

    def load_history(self, uid, count = 3):
	reg = Registry()
	self.vk = reg.objects['vk']
	msgs = self.vk.getHistory(uid)
	
	name = self.vk.id_to_name[uid]
	
	for msg in msgs:
		if msg['uid'] == uid:
			self.add_message(msg['body'], name)
		else:
			self.add_message(msg['body'])
    def keyPressEvent(self, event):
        if event.modifiers() and QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Return:
		self.send_message()

def main():
        app = QtGui.QApplication(sys.argv)
        w = ChatTab()
        w.show()
        w.raise_()
        sys.exit(app.exec_())

if __name__ == "__main__":
        main()
