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
@todo:  * Work on draw routines, theyve become a bit weird with the addition
          of multiple workspaces.
        * clean up labels for spaces
'''

from __future__ import division
from Box2D import *
from math import degrees
from PyQt4 import QtCore
from PyQt4.QtCore import Qt, SIGNAL, QObject
from PyQt4.QtGui import QPixmap

try:
    import sndobj
except:
    import win32sndobj as sndobj

from sound import *
from qgl import * # glwidget

class BoundingBox(object):
    def __init__(self, world, position, size):
        self.body_def = b2BodyDef()
        self.body_def.position = position
        self.body = world.world.CreateBody(self.body_def)
        self.body.userData = {'name': 'bounding_box'}
        
        self.shape_def = b2PolygonDef()
        self.shape_def.SetAsBox(*size)
        self.shape_def.friction = 0.9
        self.shape = self.body.CreateShape(self.shape_def)
        l = self.shape.asPolygon().vertices
        self.vertices = [y for x in l for y in x]
        '''
        self.vertex_list = pyglet.graphics.vertex_list(4,
            ('v2f/stream', self.vertices),
            ('c3B/static', (255, 0, 0, 0)*3))
        '''
    
    def draw(self, painter):
        x, y = self.body.position.x, self.body.position.y
        pass
        '''
        glPushMatrix()
        glTranslatef(x, y, 0)
        glRotatef(degrees(self.body.angle), 0, 0, 1)
        self.vertex_list.draw(GL_LINE_LOOP)
        glPopMatrix()
        '''


class ManageSpace(object):
    def __init__(self):
        self.active = None
        self.spaces = []
        
        self.spaces.append(Space())
        self.activate_space(0)
        
        self.line_in_port = 0
        
    def activate_space(self, i):
        if self.active is not None:
            #self.active.labels.hide()
            glwidget.draw_handlers.remove(self.active.draw)
            glwidget.draw_gl_handlers.remove(self.active.draw_gl)
        
        self.active = self.spaces[i%len(self.spaces)]
        
        #self.active.labels.show()
        glwidget.draw_handlers.append(self.active.draw)
        glwidget.draw_gl_handlers.append(self.active.draw_gl)
        
    def key_press(self, event):
        if event.key() == Qt.Key_Comma:
            self.activate_space(self.spaces.index(self.active) - 1)
        elif event.key() == Qt.Key_Period:
            self.activate_space(self.spaces.index(self.active) + 1)
        
        if self.active is None:
            return


class Master(object):
    '''A decoration to represent master channel of local mixer'''
    pixmap = QPixmap('res/orb_white.png')
    
    def __init__(self, world):
        self.pixmap = self.pixmap.scaledToWidth(self.pixmap.width()/2.)
        
        self.body_def = b2BodyDef()
        self.body_def.position = (glwidget.width()/2, glwidget.height()/2)
        self.body = world.world.CreateBody(self.body_def)
        
        self.circle_def = b2CircleDef()
        self.circle_def.friction = 0.9
        self.circle_def.radius = (self.pixmap.width()/2)-13
        self.circle = self.body.CreateShape(self.circle_def)
        
        self.inputs = []
        self.output = None
    
    def draw(self, painter):
        x, y = self.body.position.x, self.body.position.y
        w, h = self.pixmap.width()/2, self.pixmap.height()/2
        painter.drawPixmap(x-w, y-h, self.pixmap)
    
    def hit_test(self, x, y):
        x2, y2 = self.body.position.x, self.body.position.y
        w, h = self.pixmap.width(), self.pixmap.height()
        if x in range(int(x2-w), int(x2+w)) and y in range(int(y2-h), int(y2+h)):
            return True
        return False


class Space(object):
    pixmap = QPixmap('res/space_info_2.png')
    i = 0
    
    def __init__(self):
        Space.i += 1
        
        ### space label
        '''
        self.label = QtCore.QString('Mixer {0}'.format(self.i))
        '''
        self.font = QtGui.QFont()
        self.font.setPointSize(12)
        self.font.setBold(True)
        #self.menu_space = MenuSpace(glwidget)
        '''
        self.labels = QtGui.QWidget(parent=glwidget)
        self.labels.setStyleSheet('margin: 0px; padding: 10px; background-color: #242424; color: white;')
        self.left_button = QtGui.QPushButton('L')
        self.right_button = QtGui.QPushButton('R')
        layout = QtGui.QHBoxLayout()
        label = QtGui.QLabel('Mixer {0}'.format(self.i))
        label.setFont(self.font)
        label.setStyleSheet('padding-right: 0px;')
        layout.addWidget(self.left_button)
        layout.addWidget(label)
        
        self.label_total = QtGui.QLabel('of {0}'.format(self.i))
        self.label_total.setStyleSheet('padding-left: -3px; padding-top: 12px;')
        layout.addWidget(self.label_total)
        layout.addWidget(self.right_button)
        
        self.labels.setLayout(layout)
        self.labels.move((1224/2)-(190/2.), 0)
        '''
        ###
        
        self.bodies = []
        timer.timeout.connect(self.update)
        
        ### setup Mixer
        self.mixer = sndobj.Mixer()
        self.default_in = sndobj.SndIn()
        self.mixer.AddObj(self.default_in) # prevent error out if workspace is empty
        
        self.pan_val = 0.0
        self.pan = sndobj.Pan(self.pan_val, self.mixer)
        self.pan.GetError()
        
        sound.mixer_left.AddObj(self.pan.left)
        sound.mixer_right.AddObj(self.pan.right)
        sound.thread.AddObj(self.mixer)
        sound.thread.AddObj(self.pan)
        ###
        
        ### setup physics space
        w, h = glwidget.width(), glwidget.height()
        
        self.worldAABB = b2AABB()
        self.worldAABB.lowerBound = (0, 0)
        self.worldAABB.upperBound = (w, h)
        self.gravity = (0, 0)
        self.sleep = True
        self.world = b2World(self.worldAABB, self.gravity, self.sleep)
        self.step = True
        
        self.add_body(BoundingBox(self, (w/2, 10), (w/2, 5)))
        self.add_body(BoundingBox(self, (w/2, h-10), (w/2, 5)))
        self.add_body(BoundingBox(self, (10, h/2), (5, h/2)))
        self.add_body(BoundingBox(self, (w-10, h/2), (5, h/2)))
        ###
        
        self.master = Master(self) # decoratively the master channel for the local mixer
        self.add_body(self.master)
        
    def add_body(self, body):
        self.bodies.append(body)
        
        if hasattr(body, 'snd') and not isinstance(body.snd, sndobj.Mixer) \
            and not isinstance(body.snd, sndobj.SndWave):
            sound.thread.AddObj(body.snd)
            self.mixer.AddObj(body.snd)
    
    def draw(self, painter):
        # draw vizi objects
        for body in self.bodies:
            if hasattr(body, 'draw'):
                body.draw(painter)
        # draw space_info
        #self.label_total.setText('of {0}'.format(self.i))
        painter.save()
        painter.restore()
    
    def draw_gl(self):
        for body in self.bodies:
            if hasattr(body, 'draw_gl'):
                body.draw_gl()
    
    def update(self):
        if self.step:
            self.world.Step(time.dt*2.5, 10, 8)
        
        for body in self.bodies:
            if hasattr(body, 'update'):
                body.update()
        
        # cant delete objects from an inactive workspace, atm anyway
        if manage.active is not self:
            return
        
        for body in self.bodies:
            if hasattr(body, 'destroy') and body.destroy:
                if hasattr(body, 'in_mixer') and body.in_mixer:
                    self.mixer.DeleteObj(body.snd)
                
                self.world.DestroyBody(body.body)
                
                if hasattr(body, 'on_destroy'):
                    body.on_destroy()
                
                self.bodies.remove(body)

    def key_press(self, event):
        if event.key() == QtCore.Qt.Key_QuoteLeft:
            print 'worked!'
            for body in self.bodies:
                if hasattr(body, 'hovering') and body.hovering:
                    print 'even further!'
                    if body.processing:
                        body.snd.Disable()
                        body.processing = False
                    else:
                        body.snd.Enable()
                        body.processing = True
        if event.key() == QtCore.Qt.Key_AsciiTilde:
            for body in self.bodies:
                if hasattr(body, 'hovering') and body.hovering:
                    if body.in_mixer:
                        self.mixer.DeleteObj(body.snd)
                        body.in_mixer = False
                    else:
                        self.mixer.AddObj(body.snd)
                        body.in_mixer = True
        if event.key() == QtCore.Qt.Key_F11:
            glwidget.set_fullscreen(not glwidget.fullscreen)
        if event.key() == QtCore.Qt.Key_P:
            print 'whatup!'
            self.step = not self.step
        if event.key() == QtCore.Qt.Key_Delete:
            for body in self.bodies:
                if hasattr(body, 'hovering') and body.hovering:
                    body.destroy = True
        if event.key() == QtCore.Qt.Key_K:
            self.pan_val -= 1
            self.pan.SetPan((self.pan_val/10)+.01)
            print 'set pan to: ', (self.pan_val/10)+.01
            print self.pan.GetError()
        if event.key() == QtCore.Qt.Key_L:
            self.pan_val += 1
            self.pan.SetPan((self.pan_val/10)-.01)
            print 'set pan to: ', (self.pan_val/10)-.01
            print self.pan.GetError()
    
    def mouse_press(self, event):
        x, y = event.x(), event.y()
        y = 700-y
        if event.buttons() & QtCore.Qt.MidButton:
            for body in self.bodies:
                if hasattr(body, 'hit_test') and body.hit_test(x, y):
                    print('links: ', body.links)
                    print('error: ', body.snd.GetError(), body.snd.ErrorMessage())
                    body.snd.GetInput()
        if event.buttons() & QtCore.Qt.LeftButton:
            for body in self.bodies:
                if hasattr(body, 'hit_test') and body.hit_test(x, y):
                    if self.step:
                        md = b2MouseJointDef()
                        md.body1   = self.world.GetGroundBody()
                        md.body2   = body.body
                        md.target  = (x, y)
                        md.maxForce= 1000.0 * body.body.GetMass()
                        body.mouseJoint = self.world.CreateJoint(md).getAsType()
                        body.body.WakeUp()
                    else:
                        if hasattr(body, 'mouse_press'):
                            body.mouse_press(event)
                        body.mouseJoint = True
        if event.buttons() & QtCore.Qt.RightButton:
            for body in self.bodies:
                if hasattr(body, 'hit_test') and body.hit_test(x, y):
                    # prepare to relink to something else
                    body.linking = True
    
    def mouse_release(self, event):
        x, y = event.x(), event.y()
        y = 700-y
        if int(event.button()) == int(QtCore.Qt.LeftButton):
            for body in self.bodies:
                if hasattr(body, 'mouseJoint') and body.mouseJoint:
                    if self.step:
                        self.world.DestroyJoint(body.mouseJoint)
                        body.mouseJoint = None
                    else:
                        body.mouseJoint = False
                        if hasattr(body, 'control') and body.control is not None:
                            body.control = None
        if int(event.button()) == int(QtCore.Qt.RightButton):
            linking = []
            dest = None
            for body in self.bodies:
                if hasattr(body, 'linking') and body.linking:
                    linking.append(body)
                if hasattr(body, 'hit_test') and body.hit_test(x, y):
                    dest = body
            
            if dest is None:
                print('No destination, stopped linking')
                for l in linking:
                    l.linking = False
                return False
            
            if len(linking) is 0:
                print('Found no objects to link, stopped linking')
                return False
            
            for l in linking:
                if hasattr(dest, 'on_connect_input'):
                    dest.on_connect_input(l, x, y)
                    l.linking = False
                    continue
                if hasattr(l, 'on_connect'):
                    l.on_connect(dest)
                    l.linking = False
                    continue
                l.output = dest
                l.linking = False
    
    def mouse_move(self, event):
        x, y = event.x(), event.y()
        y = 700-y # TODO stop hacking upside-down Qt Canvas
        dx, dy = glwidget.last_pos
        
        for body in self.bodies:
            if hasattr(body, 'mouseJoint') and body.mouseJoint:
                if self.step:
                    body.mouseJoint.SetTarget((x, y))
                else:
                    if hasattr(body, 'active_control') and body.active_control is not None:
                        body.mouse_move(event)
                        
            if hasattr(body, 'hit_test') and body.hit_test(x, 700-y):
                pixels = [0.]
                alpha = (GLfloat*len(pixels))(*pixels)
                glReadPixels(x, y, 1, 1, GL_ALPHA, GL_FLOAT, alpha)
                if alpha[0] > .05:
                    body.hovering = True
            elif hasattr(body, 'hit_test') and hasattr(body, 'hovering') and body.hovering is True:
                body.hovering = False


# init world to be shared among modules
manage = ManageSpace()
