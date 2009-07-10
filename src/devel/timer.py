#!/usr/bin/env python
from PyQt4 import QtCore, QtGui

from app import *

timer = QtCore.QTimer()
time = QtCore.QTime()
time.dt = 0.001

def update():
    time.dt = time.restart()/1000.

timer.timeout.connect(update)
timer.start(1/60.)