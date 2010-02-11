# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

class Time(QtCore.QTime):
    def __init__(self):
        super(Time, self).__init__()
        self.dt = 0.001
    
    def update(self):
        dt = self.restart()/1000.
        if dt <= 0.:
            dt = 0.001
        self.dt = dt
    
    def draw_fps(self, painter, x=10, y=10, color=QtGui.QColor(0, 0, 0)):
        painter.save()
        fps = QtCore.QString()
        fps.setNum(1000./(self.dt*1000.), 'f', 3)
        painter.setPen(color)
        painter.drawText(x, y, fps)
        painter.restore()


timer = QtCore.QTimer()
time = Time()
timer.timeout.connect(time.update)
timer.start(1/60.)