# -*- coding: utf-8 -*-
from OpenGL.GL import *
from PyQt4 import QtCore, QtGui, QtOpenGL

from timer import *

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers))
        self.setGeometry(0, 0, 1224, 700)
        self.setAutoFillBackground(False)
        
        self.draw_handlers = []
        self.update_handlers = []
        
    def initializeGL(self):
        glClearColor(0., 0., 0., 1.)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    def paintGL(self):
        # update all relevant objects before drawing
        for handler in self.update_handlers:
            handler(time.dt)
        
        #
        glClear(GL_COLOR_BUFFER_BIT)
        painter = QtGui.QPainter(self)
        
        fps = QtCore.QString()
        fps.setNum(time.dt, 'f', 3)
        self.renderText(20, 30, fps)
        
        for handler in self.draw_handlers:
            pass#handler(painter)
        
        painter.end()
    
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        self.updateGL()
    
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



glwidget = GLWidget()
timer.timeout.connect(glwidget.updateGL)

