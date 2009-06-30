'''
Created on Jun 29, 2009

@author: daniel
'''

import pyglet
import space
from window import *

class Options(object):
    def __init__(self):
        pass
    
    def draw(self):
        ww = window.width
        x1, x2, y1, y2 = 50, ww-50, 0, 200
        pyglet.graphics.draw(4, GL_QUADS,
            ('v2f', (x1, y1,
                     x2, y1,
                     x2, y2,
                     x1, y2)),
            ('c4B', (39, 118, 153, 50)*4))
        if space.manage.active.active_control is not None:
            active_control = space.manage.active.active_control
            label = pyglet.text.Label(repr(active_control))
            label.x = 50
            label.y = 100
            label.color = (255, 255, 255, 255)
            label.draw()
    
    def update(self):
        pass


options = Options()
window.draw_handlers.append(options.draw)