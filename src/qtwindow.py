#! /usr/bin/env python

import os
import sys

from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.QtOpenGL import *

from pyglet.gl import *
import pyglet

from sound import *

from objmenu import Ui_Form

class MyForm(QGLWidget):
    def __init__(self, parent=None):
        super(MyForm, self).__init__(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers), parent)
        self.setAutoFillBackground(False)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
    
    def initializeGL(self):
        glClearColor(0., 0., 0., 1.)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    def paintEvent(self, event):
        self.makeCurrent()
        painter = QtGui.QPainter(self)
        painter.end()
    
    def animate(self):
        self.update()
    
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        self.updateGL()


class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers), parent)
        self.setGeometry(10, 10, 800, 600)
        self.my_form = MyForm(self)
        
        
        self.clock = QtCore.QTimer()
        self.clock.setSingleShot(False)
        self.clock.timeout.connect(self.animate)
        self.clock.timeout.connect(self.my_form.animate)
        self.clock.start()
        
        self.time = QtCore.QTime()
        
        self.setAutoFillBackground(False)
        
        self.draw_handlers = []
        self.menu_handlers = []
        self.update_handlers = []
        
        self.frames = 0
        self.last_pos = (0, 0)
    
    def __del__(self):
        sound.thread.ProcOff()
    
    def initializeGL(self):
        glClearColor(0., 0., 0., 1.)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    def keyPressEvent(self, event):
        import space
        from viziobj import Oscili
        #space.manage.active.add_body(Oscili(position=(150, 150)))
        if event.key() == 80:
            space.manage.active.step = not space.manage.active.step
    
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
        if (self.frames % 100) is 0:
            self.time.start()
            self.frames = 0
        
        self.makeCurrent()
        
        glClear(GL_COLOR_BUFFER_BIT)
        
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.save()
        fps = QtCore.QString()
        elapsed = self.time.elapsed()
        if elapsed == 0.0:
            elapsed = 0.0000001
        fps.setNum(self.frames/(elapsed/1000.0), 'f', 2)
        self.dt = self.frames/(elapsed/1000.0)
        painter.setPen(QtGui.QColor('white'))
        painter.drawText(20, 40, fps + " fps")
        painter.restore()
        
        # draw
        for handler in self.draw_handlers:
            handler(painter)
        
        painter.end()
        
        self.frames += 1
    
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        self.updateGL()
    
    def animate(self):
        for handler in self.update_handlers:
            handler(self.dt)
        self.update()


app = QtGui.QApplication(sys.argv)
window=GLWidget()
