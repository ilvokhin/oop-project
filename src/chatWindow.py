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

        # test
        for i in xrange (1, 10):
            s = QString ("%1").arg (i)
            w = self.createTab()
            w.closeButton.clicked.connect(self.closeButton_clicked)
            self.addTab (w, s)


    def createTab (self):
        return ChatTab()

    def closeButton_clicked (self):
        self.removeTab (self.currentIndex())
        if (self.count() == 0):
            self.close()


def main():
        app = QtGui.QApplication(sys.argv)
        w = ChatWindow()
        w.show()
        w.raise_()
        sys.exit(app.exec_())

if __name__ == "__main__":
        main()
