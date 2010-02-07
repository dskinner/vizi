# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.QtGui import QPixmap

from timer import *

class MenuLabel(QtGui.QLabel):
    def mouseReleaseEvent(self, event):
        print 'from label', self.text()


class Menu(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.labels = [ 'ADSR',
                        'Balance',
                        'Buzz',
                        'FFT',
                        'Filter',
                        'Gain',
                        'HarmTable',
                        'HiPass',
                        'Hilb',
                        'IFFT',
                        'LineIn',
                        'LoPass',
                        'Loop',
                        'Mixer',
                        'Oscili',
                        'OsciliSaw',
                        'OsciliBuzz',
                        'OsciliHam',
                        'PVA',
                        'PVBlur',
                        'PVMorph',
                        'PVS',
                        'Phase',
                        'Pitch',
                        'Ring',
                        'SndRead',
                        'SpecMult',
                        'SpecThresh',
                        'SpecVoc',
                        'VDelay',
                        'Wave']
        self.labels = [MenuLabel(x) for x in self.labels]
        layout = QtGui.QVBoxLayout()
        for l in self.labels:
            layout.addWidget(l)
        self.setLayout(layout)
    
    def get_text(self):
        print 'hi'


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
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width(), 0, self.height(), -1, 1)
        glMatrixMode(GL_MODELVIEW)
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        #glShadeModel(GL_SMOOTH)
        glClearColor(0., 0., 0., 1.)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    def paintGL(self):
        for handler in self.update_handlers:
            handler(time.dt)
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        painter = QtGui.QPainter()
        
        for handler in self.draw_gl_handlers:
            handler()
        
        painter.begin(self)
        
        fps = QtCore.QString()
        fps.setNum(1000./(time.dt*1000.), 'f', 3)
        
        painter.setPen(QtGui.QColor(255, 255, 255))
        painter.drawText(20, 670, fps)
        
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
menu = Menu(glwidget)

