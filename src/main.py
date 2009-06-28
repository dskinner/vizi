#! /usr/bin/env python
#-----------------------------------------------------------------------------
#
#    Vizi is an aspiring and unconventional digital-audio-workstation
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
Created on May 5, 2009

@author: daniel
@todo:  * Allow for changing between audio interfaces
        * Step Time Backwards for physics
        * gui for min/max limits on orb controls, fix min bug with determine_c
        * If pybox2d is not installed, then disable physics instead of failing (use skeleton for box2d)
        * implement creating and linking tables to objects like oscili
        * display helpbox for sndobj descriptions and examples
'''
from __future__ import division
from Box2D import *
from math import atan, atan2, cos, degrees, pi, sin, sqrt
import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
try:
    import sndobj
except:
    import win32sndobj as sndobj

from numpy import *

import b2
from orb2 import *
from sound import *
from utils import *
from viziobj import *
from window import *
import space

#world.add_body(Oscili((150, 150)))

######
class Menu(object):
    def __init__(self):
        self._text = '''{color (255,255,255,255)}{bold True}{font_size 10} ADSR
 Balance
 Buzz
 FFT
 Filter
 Gain
 HarmTable
 HiPass
 Hilb
 IFFT
 LineIn
 LoPass
 Loop
 Mixer
 Oscili
 OsciliSaw
 OsciliBuzz
 OsciliHam
 PVA
 PVBlur
 PVMorph
 PVS
 Phase
 Pitch
 Ring
 SndRead
 SpecMult
 SpecThresh
 SpecVoc
 VDelay
 Wave
'''
        self._document = pyglet.text.decode_attributed(self._text)
        self._layout = pyglet.text.layout.IncrementalTextLayout(self._document, width=330, height=window.height, multiline=True)
        self.hover_vertices = None
    
    def draw(self):
        if self.hover_vertices is not None:
            pyglet.graphics.draw(4, GL_QUADS,
                ('v2f', self.hover_vertices),
                ('c4B', (39, 118, 153, 50)*4))
        self._layout.draw()
        
    def hit_test(self, x, y):
        w, h = self._layout.content_width, self._layout.content_height
        x1, y1 = self._layout.x, self._layout.y+self._layout.height-h
        if x1 <= x <= x1+w and y1 <= y <= y1+h:
            return True
        return False
    
    def on_mouse_press(self, x, y, symbol, modifiers):
        if self.hit_test(x, y):
            line = self._layout.get_line_from_point(x, y)
            position = self._layout.get_position_from_line(line)
            end = self._document.get_paragraph_end(position)
            obj = self._document.text[position:end].strip()
            space.manage.active.add_body(globals()[obj](position=(150, 150)))
    
    def on_mouse_motion(self, x, y, dx, dy):
        if self.hit_test(x, y):
            line = self._layout.get_line_from_point(x, y)
            x1, y1 = self._layout.get_point_from_line(line)
            y1 -= 6
            w, h = 120, 20
            self.hover_vertices = (x1, y1, x1+w, y1, x1+w, y1+h, x1, y1+h)
        else:
            self.hover_vertices = None

menu = Menu()
window.menu_handlers.append(menu.draw)
window.push_handlers(menu)
######

if __name__ == '__main__':
    sound.thread.ProcOn()
    pyglet.app.run()



'''
import sndobj

class Osc(sndobj.Oscili):
    def __init__(self, *args, **kwargs):
        super(Osc, self).__init__(*args, **kwargs)


### Master Out
mixer_left = sndobj.Mixer()
gain_left = sndobj.Gain(0., mixer_left)
gain_left.SetGainM(1./32768)

mixer_right = sndobj.Mixer()
gain_right = sndobj.Gain(0., mixer_right)
gain_right.SetGainM(1./32768)

outp = sndobj.SndJackIO('vizi_test')
outp.SetOutput(1, gain_left)
outp.SetOutput(2, gain_right)

thread = sndobj.SndThread()
thread.AddObj(mixer_left)
thread.AddObj(mixer_right)
thread.AddObj(gain_left)
thread.AddObj(gain_right)
thread.AddObj(outp, sndobj.SNDIO_OUT)
###


tab = sndobj.HarmTable()

osc1 = Osc(tab, 400, 10000)
osc2 = sndobj.Oscili(tab, 100, 10000)

mix1 = sndobj.Mixer()
mix1.AddObj(osc1)
pan1 = sndobj.Pan(-1.0, mix1)

mix2 = sndobj.Mixer()
mix2.AddObj(osc2)
pan2 = sndobj.Pan(1.0, mix2)

mixer_left.AddObj(pan1.left)
mixer_right.AddObj(pan1.right)

mixer_left.AddObj(pan2.left)
mixer_right.AddObj(pan2.right)

thread.AddObj(mix1)
thread.AddObj(mix2)
thread.AddObj(pan1)
thread.AddObj(pan2)
thread.AddObj(osc1)
thread.AddObj(osc2)

thread.ProcOn()
'''
