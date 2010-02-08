# -*- coding: utf-8 -*-
from __future__ import division
from PyQt4.QtGui import QWidget, QPixmap, QPainter
from PyQt4.QtCore import QObject
from PyQt4.QtOpenGL import QGLWidget
from PyQt4 import QtOpenGL

from Box2D import *
import math
from math import atan2, degrees, radians, sqrt, sin, cos
import numpy
from OpenGL.GL import *

from timer import timer
from qgl import glwidget
import space
import b2

class VObj(QWidget):
    base = QPixmap('res/orb2_base.png')
    center = QPixmap('res/orb2_center.png')
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(200, 200, self.base.width(), self.base.height())
        self.setAutoFillBackground(False)
        self.init_body((self.x(), 700-self.y()))
        #glwidget.draw_handlers.append(self.draw)
        glwidget.update_handlers.append(self.update)
    
    def init_body(self, position):
        self.body_def = b2.BodyDef(position=position)
        self.body = space.manage.active.world.CreateBody(self.body_def())
        
        self.circle_def = b2.CircleDef(2., (self.base.width()-30)/2,
                                       0.3, 0.7)
        
        self.body.CreateShape(self.circle_def())
        self.body.SetMassFromShapes()
        self.body.userData = {'destroy': False, 'name': 'orb'}
    
    def update(self, dt):
        print dt
        self.move(self.body.position.x, 700-self.body.position.y)
    
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.base)
        painter.drawPixmap(0, 0, self.center)
        painter.end()
    
    def mousePressEvent(self, event):
        print 'you clicked me!'
