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
import pyglet
from pyglet.window import key, mouse
from PyQt4 import QtCore
from PyQt4.QtGui import QPixmap
try:
    import sndobj
except:
    import win32sndobj as sndobj


from sound import *
from qtwindow import *

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
    
    def draw(self, painter):
        pass


class ManageSpace(object):
    def __init__(self):
        self.active = None
        self.spaces = []
        
        self.spaces.append(Space())
        self.activate_space(0)
        
        self.line_in_port = 0
        
        #window.push_handlers(self)
        
    def activate_space(self, i):
        if self.active is not None:
            #window.remove_handlers(self.active)
            window.draw_handlers.remove(self.active.draw)
        
        self.active = self.spaces[i%len(self.spaces)]
        
        window.draw_handlers.append(self.active.draw)
        window.update_handlers.append(self.active.update)
        #window.push_handlers(self.active)
        
    def on_key_press(self, symbol, modifiers):
        if symbol == key.COMMA:
            self.activate_space(self.spaces.index(self.active) - 1)
        elif symbol == key.PERIOD:
            self.activate_space(self.spaces.index(self.active) +1) 
        
        if self.active is None:
            return


class Master(object):
    '''A decoration to represent master channel of local mixer'''
    def __init__(self, world):
        self.pixmap = QPixmap('res/orb_white.png')
        self.scale = 0.5
        
        self.body_def = b2BodyDef()
        self.body_def.position = (window.width()/2, window.height()/2)
        self.body = world.world.CreateBody(self.body_def)
        
        self.circle_def = b2CircleDef()
        self.circle_def.friction = 0.9
        self.circle_def.radius = (self.pixmap.width()/2/2)-13
        self.circle = self.body.CreateShape(self.circle_def)
        
        self.inputs = []
        self.output = None
    
    def draw(self, painter):
        x, y = self.body.position.x, self.body.position.y
        w, h = self.pixmap.width(), self.pixmap.height()
        painter.save()
        painter.translate(x-(w/2/2), y-(h/2/2))
        painter.rotate(degrees(self.body.angle))
        painter.scale(0.5, 0.5)
        painter.drawPixmap(0, 0, self.pixmap)
        painter.restore()
    
    def hit_test(self, x, y):
        x2, y2 = self.body.position.x, self.body.position.y
        w, h = self.pixmap.width()/2, self.pixmap.height()/2
        if x in range(int(x2-w), int(x2+w)) and y in range(int(y2-h), int(y2+h)):
            return True
        return False


class Space(object):
    i = 0
    
    def __init__(self):
        ### label
        self.label = pyglet.text.Label(text='SPACE {0}'.format(self.i), \
            color=(255,255,255,255), font_size=14)
        Space.i += 1
        w1, h1 = window.width(), window.height()
        w2, h2 = self.label.content_width, self.label.content_height
        
        x, y = (w1/2)-(w2/2), h1-h2-10
        
        self.label.x = x
        self.label.y = y
        ###
        
        self.bodies = []
        
        self.batch = pyglet.graphics.Batch()
        self.layer0 = pyglet.graphics.OrderedGroup(0)
        self.layer1 = pyglet.graphics.OrderedGroup(1)
        self.layer2 = pyglet.graphics.OrderedGroup(2)
        self.layer3 = pyglet.graphics.OrderedGroup(3)
        
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
        
        self.worldAABB = b2AABB()
        self.worldAABB.lowerBound = (0, 0)
        self.worldAABB.upperBound = (window.width(), window.height())
        self.gravity = (0, 0)
        self.sleep = True
        self.world = b2World(self.worldAABB, self.gravity, self.sleep)
        self.master = None
        self.step = True
        
        self.master = Master(self) # decoratively the master channel for the local mixer
        self.add_body(self.master)
        
        w, h = window.width(), window.height()
        self.add_body(BoundingBox(self, (w/2, 10), (w/2, 5)))
        self.add_body(BoundingBox(self, (w/2, h-10), (w/2, 5)))
        self.add_body(BoundingBox(self, (10, h/2), (5, h/2)))
        self.add_body(BoundingBox(self, (w-10, h/2), (5, h/2)))
        
        self.active_control = None
        
    def add_body(self, body):
        self.bodies.append(body)
        
        if hasattr(body, 'draw'):
            pass#window.draw_handlers.append(body.draw)
        if hasattr(body, 'update'):
            window.update_handlers.append(body.update)
        #window.push_handlers(body)
        
        if hasattr(body, 'snd') and not isinstance(body.snd, sndobj.Mixer):
            sound.thread.AddObj(body.snd)
            self.mixer.AddObj(body.snd)
    
    def draw(self, painter):
        for body in self.bodies:
            if hasattr(body, 'draw_waveform'):
                body.draw_waveform(painter)
            if hasattr(body, 'draw'):
                body.draw(painter)
        
        '''
        for body in self.bodies:
            if hasattr(body, 'draw_waveform'):
                body.draw_waveform(painter)
            if hasattr(body, 'draw'):
                body.draw(painter)
        #self.batch.draw()
        for body in self.bodies:
            if hasattr(body, 'draw_infobox') and body.hovering:
                body.draw_infobox(painter)
        '''
        
        #self.label.draw()
    
    def update(self, dt):
        if self.step:
            self.world.Step(1/60., 10, 8)
        
        for body in self.bodies:
            if hasattr(body, 'destroy') and body.destroy:
                if hasattr(body, 'draw'):
                    pass#window.draw_handlers.remove(body.draw)
                if hasattr(body, 'update'):
                    window.update_handlers.remove(body.update)
                window.remove_handlers(body)
                
                if hasattr(body, 'in_mixer') and body.in_mixer:
                    self.mixer.DeleteObj(body.snd)
                sound.thread.DeleteObj(body.snd)
                
                self.world.DestroyBody(body.body)
                
                if hasattr(body, 'on_destroy'):
                    body.on_destroy()
                
                self.bodies.remove(body)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.QUOTELEFT:
            for body in self.bodies:
                if hasattr(body, 'hovering') and body.hovering:
                    if body.processing:
                        body.snd.Disable()
                        body.processing = False
                    else:
                        body.snd.Enable()
                        body.processing = True
        if symbol == key.ASCIITILDE:
            for body in self.bodies:
                if hasattr(body, 'hovering') and body.hovering:
                    if body.in_mixer:
                        self.mixer.DeleteObj(body.snd)
                        body.in_mixer = False
                    else:
                        self.mixer.AddObj(body.snd)
                        body.in_mixer = True
        if symbol == key.F11:
            window.set_fullscreen(not window.fullscreen)
        if symbol == key.P:
            self.step = not self.step
        if symbol == key.DELETE:
            for body in self.bodies:
                if hasattr(body, 'hovering') and body.hovering:
                    body.destroy = True
        if symbol == key.K:
            self.pan_val -= 1
            self.pan.SetPan((self.pan_val/10)+.01)
            print 'set pan to: ', (self.pan_val/10)+.01
            print self.pan.GetError()
        if symbol == key.L:
            self.pan_val += 1
            self.pan.SetPan((self.pan_val/10)-.01)
            print 'set pan to: ', (self.pan_val/10)-.01
            print self.pan.GetError()
    
    def mouse_press(self, event):
        x, y = event.x(), event.y()
        if event.buttons() & QtCore.Qt.MidButton:
            for body in self.bodies:
                if hasattr(body, 'hit_test') and body.hit_test(x, y):
                    print('links: ', body.links)
                    print('error: ', body.snd.GetError(), body.snd.ErrorMessage())
                    body.snd.GetInput()
        if event.buttons() & QtCore.Qt.LeftButton:
            self.active_control = None
            for body in self.bodies:
                if hasattr(body, 'hit_test') and body.hit_test(x, y):
                    self.active_control = body
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
        dx, dy = window.lastPos.x(), window.lastPos.y()
        for body in self.bodies:
            if hasattr(body, 'mouseJoint') and body.mouseJoint:
                if self.step:
                    body.mouseJoint.SetTarget((x, y))
                else:
                    if hasattr(body, 'active_control') and body.active_control is not None:
                        body.mouse_move(event)
    
    def on_mouse_motion(self, x, y, dx, dy):
        for body in self.bodies:
            if hasattr(body, 'hit_test') and body.hit_test(x, y):
                pixels = [0.]
                alpha = (GLfloat*len(pixels))(*pixels)
                glReadPixels(x, y, 1, 1, GL_ALPHA, GL_FLOAT, alpha)
                if alpha[0] > .05:
                    body.hovering = True
            elif hasattr(body, 'hit_test') and hasattr(body, 'hovering') and body.hovering is True:
                body.hovering = False


# init world to be shared among modules
manage = ManageSpace()
