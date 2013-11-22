#! /usr/bin/env python
# -*- coding: utf-8 -*

import sys

from PyQt4 import QtGui
from PyQt4 import uic

from LoginWidget import LoginWidget

class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent = None):
		QtGui.QMainWindow.__init__(self, parent)
		uic.loadUi(("./ui/mainwindow.ui"), self)
		# connect widgets
		self.loginButton.clicked.connect(self.loginButton_clicked)
	# widgets handlers
	def loginButton_clicked(self):
		self.loginWidget = LoginWidget()
		self.loginWidget.show()
		self.loginWidget.raise_()
		print "Login"
	# other methods

def main():
	app = QtGui.QApplication(sys.argv)
	w = MainWindow()
	w.show()
	w.raise_()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
