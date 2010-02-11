# -*- coding: utf-8 -*-
from OpenGL.GL import *
from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QPixmap

from timer import *

fmt = QtOpenGL.QGLFormat()
fmt.setAlpha(True)
fmt.setSampleBuffers(True)

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(fmt, parent)
        self.setGeometry(0, 0, 1224, 700)
        self.setAutoFillBackground(False)
        self.setWindowTitle('VIZI 0.2')
        
        self.draw_handlers = []
        self.draw_gl_handlers = []
        self.update_handlers = []
        
        timer.timeout.connect(self.updateGL)
    
    def initializeGL(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width(), 0, self.height(), -1, 1)
        glMatrixMode(GL_MODELVIEW)
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    def paintGL(self):
        self.update()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        for handler in self.draw_gl_handlers:
            handler()
        
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        
        time.draw_fps(painter, 300, 30, QtGui.QColor(255, 255, 255))
        
        for handler in self.draw_handlers:
            handler(painter)
        
        painter.end()
    
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
    
    def update(self):
        for handler in self.update_handlers:
            handler()
    
    def keyPressEvent(self, event):
        import space
        space.manage.active.key_press(event)
    
    def mousePressEvent(self, event):
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


glwidget = GLWidget()

