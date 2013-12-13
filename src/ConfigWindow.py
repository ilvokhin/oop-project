#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic

from VkClientThread import VkClientThread
from LoginWidget import LoginWidget
from Registry import Registry
#from VkClient import VkClient
from Config import Config
from ChatWindow import ChatWindow

class ConfigWindow (QtGui.QWidget):
        def __init__ (self, parent = None):
            QtGui.QWidget.__init__(self, parent)
            # self.conf = Registry().objects['config']
            self.ui = uic.loadUi(("./ui/ConfigWindow.ui"), self)
            self.colorHelp.linkActivated.connect (self.open_browser)

            # load everything we have in config into spinboxes and input fields
            # don't forget to gray out unneeded widgets, if respective checkboxes are unchecked

        def open_browser (self, s):
            QtGui.QDesktopServices.openUrl (QtCore.QUrl (s))

def main():
        app = QtGui.QApplication(sys.argv)
        w = ConfigWindow()
        w.show()
        w.raise_()
        sys.exit(app.exec_())

if __name__ == "__main__":
        main()
