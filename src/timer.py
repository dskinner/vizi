#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

from app import *

class Time(QtCore.QTime):
    def __init__(self):
        super(Time, self).__init__()
        self.dt = 0.001
    
    def update(self):
        self.dt = self.restart()/1000.


timer = QtCore.QTimer()
time = Time()
timer.timeout.connect(time.update)
timer.start(1/60.)