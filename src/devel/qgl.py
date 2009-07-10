from OpenGL.GL import *
from PyQt4 import QtCore, QtGui, QtOpenGL

from timer import *
from window import *

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent):
        super(GLWidget, self).__init__(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers), parent)
        self.setGeometry(0, 0, parent.width(), parent.height())
        self.setAutoFillBackground(False)
        
        self.draw_handlers = []
    
    def initializeGL(self):
        glClearColor(0., 0., 0., 1.)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        self.i = QtGui.QPixmap('../res/orb_white.png')
        self.t = self.bindTexture(self.i.scaledToWidth(self.i.width()/2.))
    
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        painter = QtGui.QPainter(self)
        
        fps = QtCore.QString()
        fps.setNum(time.dt, 'f', 3)
        self.renderText(20, 30, fps)
        
        w1, h1 = self.width()/2., self.height()/2.
        w2, h2 = self.i.width()/4., self.i.height()/4.
        self.drawTexture(QtCore.QPointF(w1-w2, h1-h2), self.t)
        
        for handler in self.draw_handlers:
            handler(painter)
        
        painter.end()
    
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        self.updateGL()


glwidget = GLWidget(window.drawarea)
timer.timeout.connect(glwidget.updateGL)

