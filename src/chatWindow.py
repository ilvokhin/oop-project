#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic

from PyQt4.QtGui import QTabWidget
from PyQt4.QtCore import QString
from Registry import Registry
from VkClientThread import VkClientThread
from ChatTab import ChatTab

class ChatWindow (QTabWidget):
    def __init__(self, parent = None):
        QTabWidget.__init__(self, parent)
        self.ui = uic.loadUi(("./ui/chatWindow.ui"), self)
        self.currentChanged.connect (self.resetTitle)

        # user ID -> tab number
        self.tabs = {}

    def addChatTab (self, id, name):
        if id not in self.tabs:
            tab = ChatTab(id)
            tab.closeButton.clicked.connect(self.closeButton_clicked)
            # TODO: connect 'send' button and some slot

            self.tabs[id] = self.count()
            self.addTab (tab, name)
        self.setCurrentIndex (self.tabs[id])
        self.activateWindow()

    def closeButton_clicked (self):
        idx = self.currentIndex()
        id = self.widget (idx).id
        self.removeTab (idx)
        del self.tabs[id]
        if (self.count() == 0):
            self.names = {}
            self.close()

    def resetTitle (self, id):
        self.setWindowTitle (self.tabText (id))


def main():
        app = QtGui.QApplication(sys.argv)
        w = ChatWindow()
        w.show()
        w.raise_()
        sys.exit(app.exec_())

if __name__ == "__main__":
        main()