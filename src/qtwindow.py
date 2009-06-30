#! /usr/bin/env python

import os
import sys

from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.QtOpenGL import *

from pyglet.gl import *
import pyglet

from sound import *


class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers), parent)
        
        self.clock = QtCore.QTimer()
        self.clock.setSingleShot(False)
        self.clock.timeout.connect(self.update)
        self.clock.start()
        
        self.setAutoFillBackground(False)
        
        self.draw_handlers = []
        self.menu_handlers = []
        self.update_handlers = []
    
    def __del__(self):
        sound.thread.ProcOff()
    
    def initializeGL(self):
        glClearColor(0., 0., 0., 1.)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    def keyPressEvent(self, event):
        import space
        from viziobj import *
        space.manage.active.add_body(Oscili(position=(150, 150)))
    
    def mousePressEvent(self, event):
        self.lastPos = event.pos()
        import space
        space.manage.active.mouse_press(event)
    
    def mouseMoveEvent(self, event):
        import space
        space.manage.active.mouse_move(event)
    
    def paintEvent(self, event):
        for handler in self.update_handlers:
            handler()
        
        self.makeCurrent()
        
        glClear(GL_COLOR_BUFFER_BIT)
        
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # draw
        for handler in self.draw_handlers:
            handler(painter)
        
        painter.end()
    
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        self.updateGL()
    
    def update(self):
        super(GLWidget, self).update()


app = QtGui.QApplication(sys.argv)
window=GLWidget()
