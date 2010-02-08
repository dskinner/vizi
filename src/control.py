# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
#
#    Copyright (C) 2009  Daniel Skinner
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#-----------------------------------------------------------------------------

'''
Created on May 31, 2009

@author: daniel
@todo: review approach to diff's
'''
from __future__ import division
from math import atan2, degrees, radians, sqrt, sin, cos
import pyglet
from pyglet.gl import *
from PyQt4.QtGui import QPixmap, QWidget
from utils import *
from qgl import *

class ControlDecorative(object):
    pass


class ControlPosition(object):
    def mouse_move(self, event, body):
        x, y = event.x(), event.y()
        x2, y2 = glwidget.last_pos
        dx, dy = x-x2, y-y2
        body.position = (x+dx, y+dy)


class ControlRotate(object):
    def __init__(self):
        self.rotation = 0
        self.revolutions = 0
        self.history = [0, 0]
    
    def adjust_angle(self, r, body):
        '''used by subclasses to determine what to do on angle change'''
        pass
    
    def mouse_press(self, event, body):
        x, y = event.x(), event.y()
        '''provides initial data in history for comparative operators later'''
        x2, y2 = body.position.x, body.position.y
        
        # calculate angle from center of orb to mouse
        r = -degrees(atan2(x-x2, y-y2))
        
        # adjust and clip history
        self.history.append(r)
        self.history = self.history[-2:]
    
    def mouse_move(self, event, body):
        x, y = event.x(), event.y()
        h = self.history
        x2, y2 = body.position.x, body.position.y
        
        # calculate angle from center of orb to mouse
        r = -degrees(atan2(x-x2, y-y2))
        
        # counting revolutions
        if self.history[-1] > -134 and r < 44:
            self.revolutions += 1
        elif self.history[-1] < 44 and r > -134:
            self.revolutions -= 1
        
        # adjust and clip history
        self.history.append(r)
        self.history = self.history[-2:]
        
        # set adjusted angle
        self.adjust_angle(r, body)


class Base(ControlPosition):
    pixmap = QPixmap('res/orb2_base.png')
    
    def __init__(self):
        super(Base, self).__init__()
    
    def draw(self, painter, x, y):
        glLoadIdentity()
        w, h = self.pixmap.width()/2., self.pixmap.height()/2.
        painter.drawPixmap(x-w, y-h, self.pixmap)


class MixerBase(Base):
    pixmap = QPixmap('res/orb_white_sm.png')


class Blue(ControlRotate):
    pixmap = QPixmap('res/orb2_blue_control_r.png')
    
    def __init__(self):
        super(Blue, self).__init__()
    
    def draw(self, painter, x, y):
        w, h = self.pixmap.width(), self.pixmap.height()
        
        painter.save()
        painter.translate(x, y)
        painter.rotate(self.rotation)
        painter.translate(-6, -6)
        painter.drawPixmap(0, 0, self.pixmap)
        painter.restore()

    def adjust_angle(self, r, body):
        diff = self.history[-1] - self.history[-2]
        if diff <= -180:
            diff += 360
        elif diff >= 180:
            diff -= 360
        self.rotation += diff


class Center(ControlDecorative):
    pixmap = QPixmap('res/orb2_center.png')
    
    def __init__(self):
        super(Center, self).__init__()
    
    def draw(self, painter, x, y):
        w, h = self.pixmap.width()/2., self.pixmap.height()/2.
        painter.drawPixmap(x-w, y-h, self.pixmap)


class Center2(ControlDecorative):
    pixmap = QPixmap('res/orb2_center2.png')
    
    def __init__(self):
        super(Center2, self).__init__()


class Orange(ControlRotate):
    pixmap = QPixmap('res/orb2_orange_control_r.png')
    
    def __init__(self):
        super(Orange, self).__init__()
    
    def draw(self, painter, x, y):
        w, h = self.pixmap.width(), self.pixmap.height()
        
        #glTranslatef(x, y, 1)
        #glRotatef(self.rotation, 0, 0, 1)
        #glTranslatef(-6, -6, 1)
        
        painter.save()
        painter.translate(x, y)
        painter.rotate(self.rotation)
        painter.translate(-6, -6)
        painter.drawPixmap(0, 0, self.pixmap)
        painter.restore()
    
    def adjust_angle(self, r, body):
        diff = self.history[-1] - self.history[-2]
        if diff <= -180:
            diff += 360
        elif diff >= 180:
            diff -= 360
        self.rotation += diff


class MultiConnect(ControlDecorative):
    image = pyglet.image.load('res/orb_multi_connect.png')
    
    def __init__(self, batch, group):
        super(MultiConnect, self).__init__()
        w, h = self.image.width, self.image.height
        self.image.anchor_x = int(w/2)
        self.image.anchor_y = int(h/2)
        self.sprite = pyglet.sprite.Sprite(self.image, batch=batch, group=group)


class FourInOne(ControlRotate):
    def __init__(self):
        super(FourInOne, self).__init__()
        self.rotation = 45
        self.c = 0
        self.vals = [0, 0, 0, 0]
    
    def adjust_angle(self, r, body):
        diff = self.history[-1] - self.history[-2]
        if diff <= -180:
            diff += 360
        elif diff >= 180:
            diff -= 360
        v = self.vals[self.c] + (diff*.001)
        if self.c is not 3:
            self.vals[self.c] = determine_constrained_value(0., 1., v)
        else:
            self.vals[self.c] = determine_constrained_value(0., 5., v)
        self.rotation += diff

