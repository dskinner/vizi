# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.QtGui import QPixmap
from timer import *

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers), parent)
        self.setGeometry(0, 0, 1224, 700)
        self.setAutoFillBackground(False)
        
        self.pixmap = QPixmap('res/orb_white.png')
        
        self.draw_handlers = []
        self.draw_gl_handlers = []
        self.update_handlers = []
    
    def initializeGL(self):
        '''
        glShadeModel(GL_SMOOTH)
        glClearColor(0., 0., 0., 1.)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        '''
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width(), 0, self.height(), -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glClearColor(0.0, 0.0, 0.0, 1.0)
    
    def animate(self):
        self.repaint()
    
    def paintGL(self):
        for handler in self.update_handlers:
            handler(time.dt)
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        painter = QtGui.QPainter()
        
        for handler in self.draw_gl_handlers:
            handler()
        
        painter.begin(self)
        
        fps = QtCore.QString()
        fps.setNum(time.dt*1000, 'f', 2)
        
        painter.setPen(QtGui.QColor(255, 255, 255))
        painter.drawText(20, 30, fps)
        
        for handler in self.draw_handlers:
            glLoadIdentity()
            handler(painter)
        
        painter.end()
    
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
    
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
glwidget.setWindowTitle('VIZI 0.2')
timer.timeout.connect(glwidget.updateGL)

