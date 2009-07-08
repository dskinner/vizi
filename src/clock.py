'''
Created on Jul 7, 2009

@author: daniel
'''
from __future__ import division
from PyQt4 import QtCore

class Clock(object):
    def __init__(self):
        self.timer = QtCore.QTimer()
        self.time = QtCore.QTime()
        self.time.start()
    
    def tick(self):
        return self.time.restart()/1000


clock = Clock()