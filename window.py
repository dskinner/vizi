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

import pyglet
from pyglet.gl import *

from sound import *

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.draw_handlers = []
        self.menu_handlers = []
        self.update_handlers = []
        pyglet.clock.schedule(self.update)
        self.batch = pyglet.graphics.Batch()
        self.layer0 = pyglet.graphics.OrderedGroup(0)
        self.layer1 = pyglet.graphics.OrderedGroup(1)
        self.layer2 = pyglet.graphics.OrderedGroup(2)
        self.layer3 = pyglet.graphics.OrderedGroup(3)
        
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        self.clock = pyglet.clock.ClockDisplay()
    
    def on_draw(self):
        self.clear()
        self.clock.draw()
        
        for handler in self.draw_handlers:
            handler()
        
        self.batch.draw()
        
        for handler in self.menu_handlers:
            handler()
    
    def on_exit(self):
        sound.thread.ProcOff()
        sound.thread = None
        pyglet.app.exit()
    
    def update(self, dt):
        for handler in self.update_handlers:
            handler(dt)


# init window to be shared among modules
window = Window(width=1224, height=700, resizable=True, vsync=True, caption='VIZI 0.1')
