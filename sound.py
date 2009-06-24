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
Created on Jun 6, 2009

@author: daniel
'''
try:
    import sndobj
except:
    import win32sndobj as sndobj

import sys

options = sys.argv[1:]

class Sound(object):
    def __init__(self, interface='system'):
        self.tab = sndobj.HarmTable()
        self.saw = sndobj.HarmTable(1024, 25, sndobj.SAW)
        self.buzz = sndobj.HarmTable(1024, 20, sndobj.BUZZ)
        self.ham = sndobj.HammingTable(1024, 20.54)
        self.thread = sndobj.SndThread()
        self.mixer_left = sndobj.Mixer()
        self.mixer_right = sndobj.Mixer()
	self.thread.AddObj(self.mixer_left)
	self.thread.AddObj(self.mixer_right)
        if interface == 'jack': 
            self.gain_left = sndobj.Gain(0., self.mixer_left)
            self.gain_left.SetGainM(1./32768)
            self.gain_right = sndobj.Gain(0., self.mixer_right)
            self.gain_right.SetGainM(1./32768)
            
            self.output = sndobj.SndJackIO('vizi')
            self.input = self.output
            
            self.output.SetOutput(1, self.gain_left)
            self.output.SetOutput(2, self.gain_right)
            
            self.thread.AddObj(self.gain_left)
            self.thread.AddObj(self.gain_right)
            
        elif interface == 'system':
            self.output = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)
            self.output.SetOutput(1, self.mixer_left)
            self.output.SetOutput(2, self.mixer_right)
            self.input = sndobj.SndRTIO(1, sndobj.SND_INPUT)
        
        self.thread.AddObj(self.output, sndobj.SNDIO_OUT)
        self.thread.AddObj(self.input, sndobj.SNDIO_IN)
        #self.thread.AddObj(self.mixer)


# initialize sound object that will be shared among modules
if len(options) > 0:
    interface = options[0]
    sound = Sound(interface)
else:
    sound = Sound(interface='system')
