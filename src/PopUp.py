#! /usr/bin/env python

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic

class PopUp(QtGui.QWidget):
	def __init__(self, id, mid, msg, count, time = 2000, parent = None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = uic.loadUi(("./ui/PopUp.ui"), self)
		self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		self.setFocusPolicy(QtCore.Qt.NoFocus)
		self.timer = QtCore.QTimer
		self.count = count
		self.time = time
		self.id = id
		self.mid = mid
		self.signal = QtCore.SIGNAL("openTab")
		
		if len(msg) > 50:
			msg = msg[0:50] + "..."
 		self.ui.messageLabel.setText(msg)

	def showEvent(self, event):
		geom = self.frameGeometry()
		screen = QtGui.QDesktopWidget().screenGeometry()
		indent = 5 # magic constant for good looking
		self.setGeometry(screen.width() - self.width() - indent, indent + self.count * (self.height() + indent), self.width(), self.height())
		self.timer.singleShot(self.time, self.close)
	
	def mousePressEvent(self, event):
		if event.button() == QtCore.Qt.LeftButton:
			print "event" # open dialog window send signal self.id
			self.emit(self.signal, self.id, self.mid)
		self.close()

class PopUpMan(QtCore.QThread):
	def __init__(self):
		QtCore.QThread.__init__(self)
		self.popups = {}
		self.signal = self.signal = QtCore.SIGNAL("openTabMainWindow")
	
	def create(self, id, mid, msg, count, time = 3000):
		self.popups[(id, mid)] = PopUp(id, mid, msg, count, time)
		self.popups[(id, mid)].show()
		#self.popups[(id, mid)].raise_()
		self.connect(self.popups[(id, mid)], self.popups[(id, mid)].signal, self.openChatTab)

	def openChatTab(self, id, mid):
		print id
		del self.popups[(id, mid)]
		self.emit(self.signal, id)

if __name__ == "__main__":

	app = QtGui.QApplication([])
	man = PopUpMan()

	for i in xrange(5):
		man.create(0, i, "test" * 30, i)
	
	app.exec_()
