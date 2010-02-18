# -*- coding: utf-8 -*-
from Box2D import *
from OpenGL.GL import *
from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QPixmap

import b2
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
        
        self.last_pos = [0, 0]
        self.update_handlers = []
        
        timer.timeout.connect(self.updateGL)
    
    def initializeGL(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width(), self.height(), 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    def paintGL(self):
        import space
        self.update()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        space.manage.active.draw_gl()
        
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        
        time.draw_fps(painter, 300, 30, QtGui.QColor(255, 255, 255))
        
        space.manage.active.draw(painter)
        
        painter.end()
    
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
    
    def update(self):
        for handler in self.update_handlers:
            handler()

    def keyPressEvent(self, event):
        import space
        if event.key() == QtCore.Qt.Key_QuoteLeft:
            for body in space.manage.active.bodies:
                if hasattr(body, 'hovering') and body.hovering:
                    if body.processing:
                        body.snd.Disable()
                        body.processing = False
                    else:
                        body.snd.Enable()
                        body.processing = True
        if event.key() == QtCore.Qt.Key_AsciiTilde:
            for body in space.manage.active.bodies:
                if hasattr(body, 'hovering') and body.hovering:
                    if body.in_mixer:
                        space.manage.active.mixer.DeleteObj(body.snd)
                        body.in_mixer = False
                    else:
                        space.manage.active.mixer.AddObj(body.snd)
                        body.in_mixer = True
        if event.key() == QtCore.Qt.Key_Delete:
            for body in space.manage.active.bodies:
                if hasattr(body, 'hovering') and body.hovering:
                    body.destroy = True
        if event.key() == QtCore.Qt.Key_K:
            space.manage.active.pan_val -= 1
            space.manage.active.pan.SetPan((space.manage.active.pan_val/10)+.01)
            print 'set pan to: ', (space.manage.active.pan_val/10)+.01
            print space.manage.active.pan.GetError()
        if event.key() == QtCore.Qt.Key_L:
            space.manage.active.pan_val += 1
            space.manage.active.pan.SetPan((space.manage.active.pan_val/10)-.01)
            print 'set pan to: ', (space.manage.active.pan_val/10)-.01
            print space.manage.active.pan.GetError()
    
    def mousePressEvent(self, event):
        import space
        x, y = event.x(), event.y()
        if event.buttons() & QtCore.Qt.MidButton:
            for body in space.manage.active.bodies:
                if hasattr(body, 'hit_test') and body.hit_test(x, y):
                    print('links: ', body.links)
                    print('error: ', body.snd.GetError(), body.snd.ErrorMessage())
                    body.snd.GetInput()
        if event.buttons() & QtCore.Qt.LeftButton:
            for body in space.manage.active.bodies:
                if hasattr(body, 'hit_test') and body.hit_test(x, y):
                    if space.manage.active.step:
                        md = b2MouseJointDef()
                        md.body1   = space.manage.active.world.GetGroundBody()
                        md.body2   = body.body
                        md.target  = (x, y)
                        md.maxForce= 1000.0 * body.body.GetMass()
                        body.mouseJoint = space.manage.active.world.CreateJoint(md).getAsType()
                        body.body.WakeUp()
                    else:
                        print 'running otherwise', hasattr(body, 'mouse_press')
                        if hasattr(body, 'mouse_press'):
                            body.mouse_press(event)
                        body.mouseJoint = True
        if event.buttons() & QtCore.Qt.RightButton:
            for body in space.manage.active.bodies:
                if hasattr(body, 'hit_test') and body.hit_test(x, y):
                    # prepare to relink to something else
                    body.linking = True
        
        self.last_pos = (event.x(), event.y())
    
    def mouseReleaseEvent(self, event):
        import space
        x, y = event.x(), event.y()
        if int(event.button()) == int(QtCore.Qt.LeftButton):
            for body in space.manage.active.bodies:
                if hasattr(body, 'mouseJoint') and body.mouseJoint:
                    if space.manage.active.step:
                        space.manage.active.world.DestroyJoint(body.mouseJoint)
                        body.mouseJoint = None
                    else:
                        body.mouseJoint = False
                        if hasattr(body, 'control') and body.control is not None:
                            body.control = None
        if int(event.button()) == int(QtCore.Qt.RightButton):
            linking = []
            dest = None
            for body in space.manage.active.bodies:
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
    
    def mouseMoveEvent(self, event):
        import space
        x, y = event.x(), event.y()
        dx, dy = self.last_pos
        
        for body in space.manage.active.bodies:
            if hasattr(body, 'mouseJoint') and body.mouseJoint:
                if space.manage.active.step:
                    body.mouseJoint.SetTarget((x, y))
                else:
                    if hasattr(body, 'active_control') and body.active_control is not None:
                        body.mouse_move(event)
                        
            if hasattr(body, 'hit_test') and body.hit_test(x, y):
                pixels = [0.]
                alpha = (GLfloat*len(pixels))(*pixels)
                glReadPixels(x, y, 1, 1, GL_ALPHA, GL_FLOAT, alpha)
                if alpha[0] > .05:
                    body.hovering = True
            elif hasattr(body, 'hit_test') and hasattr(body, 'hovering') and body.hovering is True:
                body.hovering = False
        
        self.last_pos = (event.x(), event.y())


glwidget = GLWidget()

