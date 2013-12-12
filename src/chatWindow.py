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

class chatWindow (QTabWidget):
    def __init__(self, parent = None):
        QTabWidget.__init__(self, parent)
        self.ui = uic.loadUi(("./ui/chatWindow.ui"), self)

        """for i in xrange (1, 10):
            s = QString ("%1").arg (i)
            self.addTab (self.createTab(), s)"""

    def createTab (self):
        newTab = QtGui.QWidget()
        newTab.ui = uic.loadUi (("./ui/chatTab.ui"), newTab)
        return newTab

    # TODO: connect with an actual close button from a tab widget, just like this:
    # self.closeTabButton.clicked.connect(self.closeTabButton_clicked)
    def closeTabButton_clicked (self):
        self.removeTab (self.currentIndex())
        if (self.count() == 0):
            self.close()
        self.closeTabButton.raise_()


def main():
        app = QtGui.QApplication(sys.argv)
        w = chatWindow()
        w.show()
        w.raise_()
        sys.exit(app.exec_())

if __name__ == "__main__":
        main()
