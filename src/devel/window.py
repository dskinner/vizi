from PyQt4 import QtCore, QtGui, uic

from timer import *

class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uic.loadUi('main.ui', self)


window = Window()