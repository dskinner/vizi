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
Created on May 26, 2009

@author: Daniel Skinner
@todo: * make revolutes follow physics engine
       * make color controls be a tuple index to control and abstract get_control better
       * review set_output in relation to its subclasses
       * make draw_waveform scale better to visually represent sound db level more accurately
       * provide hover descriptions for actions getting ready to take place on mouse drag,
         "connect to first input", "connect to second input", "select magnitude output", etc
       * fix infobox problem where long label will cause line wraps which will cause error with metrics
       * dont set center sprite colors with every draw
'''
from __future__ import division
from Box2D import *
import math
from math import atan2, degrees, radians, sqrt, sin, cos
import numpy
from OpenGL.GL import *

import b2
import qcontrol as control
from utils import *
from window import *
import space

from PyQt4 import QtGui

class SoundObject(object):
    def __init__(self):
        self._output = None
        self.links = []
        self.inputs = []
        self.linking = False
        self.hovering = False
        self.destory = False
        self.processing = True
        self.in_mixer = True
    
    def draw_waveform(self, painter):
        if not hasattr(self, 'popout'):
            return
        glLoadIdentity()
        x, y = self.body.position.x, self.body.position.y
        
        if self.output is not None:
            x2, y2 = self.output.body.position.x, self.output.body.position.y
        else:
            x2, y2 = space.manage.active.master.body.position.x, space.manage.active.master.body.position.y
        
        length = len(self.popout)
        
        # get median of data set and subtract to all to "center"
        self.popout -= self.popout.mean()
        
        # scale the height of waveform output
        a = abs(self.popout.max())
        i = abs(self.popout.min())
        scale = a >= i and a/20 or i/20
        self.popout /= scale
        
        # determine distance from self to output
        distance = abs(sqrt((x2-x)**2 + (y2-y)**2))
        
        if int(distance) is 0:
            return
        
        # dont know which is faster but i imagine the first
        vertices = numpy.arange(0, distance, distance/length, dtype='float32').repeat(2, axis=0)
        #vertices = numpy.arange(0, distance, distance/2/length, dtype='float32')
        
        vertices[0:-1:2] = self.popout
        vertices.shape = [vertices.size/2., 2]
        
        glTranslatef(x, y, 1)
        #determine angle from current orb to master and rotate as such
        r = -degrees(atan2(x2-x, y2-y))
        glRotatef(r, 0, 0, 1)
        
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, vertices)
        glDrawArrays(GL_LINE_STRIP, 0, len(vertices))
        glDisableClientState(GL_VERTEX_ARRAY)
    
    def get_output(self):
        return self._output
    
    def on_destroy(self):
        self.snd = None
    
    def set_output(self, obj):
        # remove old links
        if self.output is not None:
            if self in self.output.inputs:
                self.output.inputs.remove(self)
            if hasattr(self.output, 'snd'):
                if hasattr(self.output, 'default_in') and self.output.snd:
                    self.output.snd.SetInput(self.output.default_in)
                elif self.output.snd:
                    self.output.snd.SetInput(None)
        
        # create new links
        self._output = obj
        if self.output is not None:
            self.output.inputs.append(self)
        
        if hasattr(obj, 'snd'):
            self.output.snd.SetInput(self.snd)
        
        # weirdness
        if obj in self.inputs:
            self.inputs.remove(obj)
            
        # create new joint
        if hasattr(self, 'joint') and self.joint is not None:
            space.manage.active.world.DestroyJoint(self.joint)
            self.joint = None
        self.joint_def = None
        if self.output is not None:
            self.joint_def = b2DistanceJointDef()
            self.joint_def.Initialize(self.body, self.output.body, (self.body.position.x, self.body.position.y), (self.output.body.position.x, self.output.body.position.y))
            self.joint = space.manage.active.world.CreateJoint(self.joint_def)
    output = property(get_output, set_output)


class Orb2(SoundObject):
    ''' Base class for an orb with two dial controls '''
    
    def __init__(self, position):
        super(Orb2, self).__init__()
        self.position = position
        
        # pointer to control designated active
        self.active_control = None
        
        # the orb controls
        self.base = control.Base()
        self.orange = control.Orange()
        self.blue = control.Blue()
        self.center = control.Center()
        
        # create physics body
        self.init_body(position)
        
        # update physics body based on control value
        self.map_physics = {'orange rotation': 'body angle'}
        
        # useful for debugging during draw
        '''
        self.vertices = create_circle_vertices(16, self.circle_def().radius)
        self.vertex_list = pyglet.graphics.vertex_list(16,
            ('v2f/stream', self.vertices),
            ('c3B/static', (255, 0, 0, 0)*12))
        '''
    
    def init_body(self, position):
        self.body_def = b2.BodyDef(position=position)
        self.body = space.manage.active.world.CreateBody(self.body_def())
        
        self.circle_def = b2.CircleDef(2., (self.base.pixmap.width()-30)/2,
                                       0.3, 0.7)
        
        self.body.CreateShape(self.circle_def())
        self.body.SetMassFromShapes()
        self.body.userData = {'destroy': False, 'name': 'orb'}
    
    def draw(self, painter):
        x, y = self.body.position.x, self.body.position.y
        
        self.base.draw(painter, x, y)
        if self.orange: # for handling disabled orange controls in some subclasses, for now
            self.orange.draw(painter, x, y)
        if self.blue:
            self.blue.draw(painter, x, y)
        self.center.draw(painter, x, y)
        '''
        if self.in_mixer:
            self.center.sprite.color = (255, 255, 255)
        else:
            self.center.sprite.color = (50, 50, 50)
        '''
        
    def mouse_press(self, event):
        x, y = event.x(), event.y()
        
        self.active_control = self.get_control(x, y)
        if hasattr(self.active_control, 'mouse_press'):
            self.active_control.mouse_press(event, self.body)
    
    def mouse_release(self, x, y, symbol, modifiers):
        self.active_control = None
    
    def mouse_move(self, event):
        if hasattr(self.active_control, 'mouse_move'):
            self.active_control.mouse_move(event, self.body)
        
        for k, v in self.map_physics.items():
            k = k.split()
            v = v.split()
            if hasattr(self, v[0]) and getattr(self, k[0]):
                setattr(getattr(self, v[0]), v[1], -radians(getattr(getattr(self, k[0]), k[1])))
            
    def get_control(self, x, y):
        # read pixels
        ww, wh = window.width(), window.height()
        pixels = [0., 0., 0., 0.]
        rgba = (GLfloat*len(pixels))(*pixels)
        glReadPixels(x, wh-y, 1, 1, GL_RGBA, GL_FLOAT, rgba)
        red, green, blue, alpha = rgba[0], rgba[1], rgba[2], rgba[3]
        
        # determine control clicked by color
        if .55 < red < .88 and \
            .18 < green < .28 and \
            .1 > blue > .05 :
            return self.orange
        elif .15 < red < .21 and \
            .38 < green < .47 and \
            .47 < blue < .61:
            return self.blue
        elif alpha > .05:
            return self.base
    
    def update(self, dt):
        for k, v in self.map_physics.items():
            k = k.split()
            v = v.split()
            if hasattr(self, k[0]):
                setattr(getattr(self, k[0]), k[1], -degrees(getattr(getattr(self, v[0]), v[1])))
    
    def hit_test(self, x, y):
        x2, y2 = self.body.position.x, self.body.position.y
        w, h = self.base.pixmap.width()/2, self.base.pixmap.height()/2
        if (x2-w) <= x <= (x2+w) and (y2-h) <= y <= (y2+h):
            return True
        return False


class OrbMultiConnect(SoundObject):
    def __init__(self, position):
        super(OrbMultiConnect, self).__init__()
        
        self.base = control.Base(batch=space.manage.active.batch, group=space.manage.active.layer0)
        self.multi_connect = control.MultiConnect(batch=space.manage.active.batch, group=space.manage.active.layer1)
        self.center = control.Center2(batch=space.manage.active.batch, group=space.manage.active.layer2)
        
        self.init_body(position)
    
    def draw(self):
        x, y = self.body.position.x, self.body.position.y
        
        self.base.draw(x, y)
        self.multi_connect.sprite.set_position(x, y)
        self.center.sprite.set_position(x, y)
    
    def hit_test(self, x, y):
        x2, y2 = self.body.position.x, self.body.position.y
        w, h = self.base.image.width/2, self.base.image.height/2
        if (x2-w) <= x <= (x2+w) and (y2-h) <= y <= (y2+h):
            return True
        return False
    
    def init_body(self, position):
        self.body_def = b2.BodyDef(position=position)
        self.body = space.manage.active.world.CreateBody(self.body_def())
        
        self.circle_def = b2.CircleDef(2., (self.base.image.width-30)/2,
                                       0.3, 0.7)
        
        self.body.CreateShape(self.circle_def())
        self.body.SetMassFromShapes()
        self.body.userData = {'destroy': False, 'name': 'orb'}

    def mouse_press(self, x, y, symbol, modifiers):
        self.active_control = self.get_control(x, y)
        if hasattr(self.active_control, 'mouse_press'):
            self.active_control.mouse_press(x, y, symbol, modifiers, self.body)
    
    def mouse_release(self, x, y, symbol, modifiers):
        self.active_control = None
    
    def mouse_drag(self, x, y, dx, dy, symbol, modifiers):
        if hasattr(self.active_control, 'mouse_drag'):
            self.active_control.mouse_drag(x, y, dx, dy, symbol, modifiers, self.body)
    
    def get_control(self, x, y):
        # read pixels
        pixels = [0., 0., 0., 0.]
        rgba = (GLfloat*len(pixels))(*pixels)
        glReadPixels(x, y, 1, 1, GL_RGBA, GL_FLOAT, rgba)
        red, green, blue, alpha = rgba[0], rgba[1], rgba[2], rgba[3]
        
        # determine control clicked by color
        if alpha > .05:
            return self.base
    
    def hit_test(self, x, y):
        x2, y2 = self.body.position.x, self.body.position.y
        w, h = self.base.image.width/2, self.base.image.height/2
        if (x2-w) <= x <= (x2+w) and (y2-h) <= y <= (y2+h):
            return True
        return False


class OrbMixer(SoundObject):
    def __init__(self, position):
        super(OrbMixer, self).__init__()
        
        self.base = control.MixerBase()
        self.init_body(position)
    
    def draw(self, painter):
        x, y = self.body.position.x, self.body.position.y
        self.base.draw(painter, x, y)
    
    def hit_test(self, x, y):
        x2, y2 = self.body.position.x, self.body.position.y
        w, h = self.base.pixmap.width()/2, self.base.pixmap.height()/2
        if (x2-w) <= x <= (x2+w) and (y2-h) <= y <= (y2+h):
            return True
        return False
    
    def init_body(self, position):
        self.body_def = b2.BodyDef(position=position)
        self.body = space.manage.active.world.CreateBody(self.body_def())
        
        self.circle_def = b2.CircleDef(2., (self.base.pixmap.width()-30)/2,
                                       0.3, 0.7)
        
        self.body.CreateShape(self.circle_def())
        self.body.SetMassFromShapes()
        self.body.userData = {'destroy': False, 'name': 'orb'}

    def mouse_press(self, x, y, symbol, modifiers):
        self.active_control = self.get_control(x, y)
        if hasattr(self.active_control, 'mouse_press'):
            self.active_control.mouse_press(x, y, symbol, modifiers, self.body)
    
    def mouse_release(self, x, y, symbol, modifiers):
        self.active_control = None
    
    def mouse_drag(self, x, y, dx, dy, symbol, modifiers):
        if hasattr(self.active_control, 'mouse_drag'):
            self.active_control.mouse_drag(x, y, dx, dy, symbol, modifiers, self.body)
    
    def get_control(self, x, y):
        # read pixels
        pixels = [0., 0., 0., 0.]
        rgba = (GLfloat*len(pixels))(*pixels)
        glReadPixels(x, y, 1, 1, GL_RGBA, GL_FLOAT, rgba)
        red, green, blue, alpha = rgba[0], rgba[1], rgba[2], rgba[3]
        
        # determine control clicked by color
        if alpha > .05:
            return self.base
    
    def hit_test(self, x, y):
        x2, y2 = self.body.position.x, self.body.position.y
        w, h = self.base.pixmap.width()/2, self.base.pixmap.height()/2
        if (x2-w) <= x <= (x2+w) and (y2-h) <= y <= (y2+h):
            return True
        return False


class Orb3(object):
    pass