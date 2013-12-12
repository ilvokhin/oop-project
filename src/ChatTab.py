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
        self.id = id

    def closeButton_clicked (self):
        self.close()
        self.closeButton.raise_()

    def text_changed (self):
        st = self.messageField.toPlainText()
        if st.size() > 0:
            self.sendButton.setEnabled (True)
        else:
            self.sendButton.setEnabled (False)

def main():
        app = QtGui.QApplication(sys.argv)
        w = ChatTab()
        w.show()
        w.raise_()
        sys.exit(app.exec_())

if __name__ == "__main__":
        main()
