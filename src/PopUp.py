#! /usr/bin/env python

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets
from PyQt5 import uic

class PopUp(QtWidgets.QWidget):
	openTab = pyqtSignal(int, int)
	def __init__(self, user_id, id, msg, count, time = 2000, parent = None):
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = uic.loadUi(("./ui/PopUp.ui"), self)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.Tool)
		self.setFocusPolicy(QtCore.Qt.NoFocus)
		self.timer = QtCore.QTimer
		self.count = count
		self.time = time
		self.user_id = user_id
		self.id = id

		if len(msg) > 50:
			msg = msg[0:50] + "..."
		self.ui.messageLabel.setText(msg)

	def showEvent(self, event):
		geom = self.frameGeometry()
		screen = QtWidgets.QDesktopWidget().screenGeometry()
		indent = 5 # magic constant for good looking
		self.setGeometry(screen.width() - self.width() - indent, indent + self.count * (self.height() + indent), self.width(), self.height())
		self.timer.singleShot(self.time, self.close)
	
	def mousePressEvent(self, event):
		if event.button() == QtCore.Qt.LeftButton:
			self.openTab.emit(self.user_id, self.id)
		self.close()

class PopUpMan(QtCore.QThread):
	openTabMainWindow = pyqtSignal(int)
	def __init__(self):
		QtCore.QThread.__init__(self)
		self.popups = {}

	def create(self, user_id, id, msg, count, time = 3000):
		self.popups[(user_id, id)] = PopUp(user_id, id, msg, count, time)
		self.popups[(user_id, id)].show()
		self.popups[(user_id, id)].openTab.connect(self.openChatTab)

	def openChatTab(self, user_id, id):
		#print(user_id)
		del self.popups[(user_id, id)]
		self.openTabMainWindow.emit(user_id)

if __name__ == "__main__":
	app = QtGui.QApplication([])
	man = PopUpMan()
	app.exec_()
