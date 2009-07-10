#! /usr/bin/env python

import os
import sys

from PyQt4 import QtCore, QtGui, QtOpenGL, uic
from PyQt4.QtCore import *
from PyQt4.QtOpenGL import *

from pyglet.gl import *
import pyglet

from sound import *


class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers), parent)
        self.setGeometry(10, 10, 800, 600)
        
        self.clock = QtCore.QTimer()
        self.clock.setSingleShot(False)
        self.clock.timeout.connect(self.animate)
        self.clock.start()
        
        self.time = QtCore.QTime()
        
        self.setAutoFillBackground(False)
        
        self.draw_handlers = []
        self.menu_handlers = []
        self.update_handlers = []
        
        self.frames = 0
        self.last_pos = (0, 0)
        self.dt = 0.00001
    
    def __del__(self):
        sound.thread.ProcOff()
    
    def initializeGL(self):
        glClearColor(0., 0., 0., 1.)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    def keyPressEvent(self, event):
        import space
        space.manage.active.key_press(event)
    
    def mousePressEvent(self, event):
        self.lastPos = event.pos()
        import space
        space.manage.active.mouse_press(event)
        self.last_pos = (event.x(), event.y())
    
    def mouseMoveEvent(self, event):
        import space
        space.manage.active.mouse_move(event)
        self.last_pos = (event.x(), event.y())
    
    def mouseReleaseEvent(self, event):
        import space
        space.manage.active.mouse_release(event)
    
    def paintEvent(self, event):
        self.makeCurrent()
        
        glClear(GL_COLOR_BUFFER_BIT)
        
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.save()
        
        fps = QtCore.QString()
        fps.setNum(1./self.dt, 'f', 3)
        
        painter.setPen(QtGui.QColor('white'))
        painter.drawText(20, 40, fps + " fps")
        painter.restore()
        
        # draw
        for handler in self.draw_handlers:
            handler(painter)
        
        painter.end()
    
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        self.updateGL()
    
    def animate(self):
        self.dt = self.time.restart()/1000.
        if self.dt == 0.0:
            self.dt = 0.0000001
            
        for handler in self.update_handlers:
            handler(self.dt)
        self.update()


app = QtGui.QApplication(sys.argv)
window=GLWidget()
