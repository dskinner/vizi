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
@todo:  * Ditched ADSR design, come up with a new one
        * PVBlur crashes on update
        * PVMorph is broke
        * Wave, Loop, and all that stuff is probably broke
        * OrbMultiConnects are not handling pluggin default_in's back automagically
'''

import numpy
import pyglet
try:
    import sndobj
except:
    import win32sndobj as sndobj

from orb2 import *
from sound import *
import space

class ADSR(Orb3):
    def __init__(self, *args, **kwargs):
        super(ADSR, self).__init__(*args, **kwargs)
        self.snd = sndobj.ADSR(self.attack, self.maxamp, self.decay, self.sustain, self.release, self.duration)
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Attack: \n MaxAmp: \n Decay: \n Sustain: \n Release: \n Duration: \n {font_name 'Flotsam smart'}{bold False}ADSR'''
        self._infobox_layout.width = 400
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
    
    def update(self, dt):
        maxamp, sustain = self.body.position.x, self.body.position.y
        self.maxamp, self.sustain = maxamp/4, sustain/4
        attack, decay, release, duration = self.four_in_one_control.vals
        self.snd.SetMaxAmp(self.maxamp)
        self.snd.SetADSR(attack, decay, self.sustain, release)
        self.snd.SetDur(duration)
        
        if self.hovering:
            self.update_infobox([attack, self.maxamp, decay, self.sustain, release, duration])
        
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class Balance(OrbMultiConnect):
    def __init__(self, *args, **kwargs):
        super(Balance, self).__init__(*args, **kwargs)
        self.default_in1 = sndobj.SndIn()
        self.default_in2 = sndobj.SndIn()
        self.links = [self.default_in1, self.default_in2]
        self.snd = sndobj.Balance(*self.links)
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}First Input: \n Second Input: \n {font_name 'Flotsam smart'}{bold False}Balance'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
    
    def on_connect_input(self, from_obj, x, y):
        x1, y1 = self.body.position
        w = self.base.image.width/2
        
        if x1-w <= x <= x1:
            self.links[0] = from_obj.snd
        elif x1 <= x <= x1+w:
            self.links[1] = from_obj.snd
        
        l, r = repr(self.links[0]), repr(self.links[1])
        self.update_infobox([l[8:l.index(';')], r[8:r.index(';')]])
        self.snd.SetInput(*self.links)
        from_obj._output = self
    
    def update(self, dt):
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class Buzz(Orb2):
    def __init__(self, *args, **kwargs):
        super(Buzz, self).__init__(*args, **kwargs)
        
        self.snd = sndobj.Buzz(100., 16000., 30)
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Frequency: \n Amplitude: \n {font_name 'Flotsam smart'}{bold False}OsCiLi'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
    
    def update(self, dt):
        frequency = determine_constrained_value(min=0, max=940, \
            val=abs(degrees(self.body.angle)))
        amplitude = abs(self.blue.rotation)
        
        if self.hovering:
            self.update_infobox([frequency, amplitude])
        
        self.snd.SetFreq(frequency)
        self.snd.SetAmp(amplitude)
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class Filter(Orb2):
    def __init__(self, *args, **kwargs):
        super(Filter, self).__init__(*args, **kwargs)
        self.default_in = sndobj.SndIn()
        self.snd = sndobj.Filter(1000, 10, self.default_in)
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Frequency: \n Bandwidth: \n {font_name 'Flotsam smart'}{bold False}Filter'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
    
    def update(self, dt):
        freq = determine_constrained_value(min=0, max=2000, \
                                          val=abs(degrees(self.body.angle)))
        
        bw = abs(self.blue.rotation)
        
        if self.hovering:
            self.update_infobox([freq, bw])
        
        self.snd.SetFreq(freq)
        self.snd.SetBW(bw)
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class FFT(Orb2):
    def __init__(self, *args, **kwargs):
        super(FFT, self).__init__(*args, **kwargs)
        self.default_in = sndobj.SndIn()
        self.snd = sndobj.FFT(sound.tab, self.default_in)
        self.in_mixer = False
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Scale: \n {font_name 'Flotsam smart'}{bold False}FFT'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
        
        self.orange = None # disable orange control
        self.blue.rotation = 0
    
    def update(self, dt):
        scale = determine_constrained_value(0, 1, self.blue.rotation/1000)
        self.snd.SetScale(scale)
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])
        if self.hovering:
            self.update_infobox([scale])


class Gain(Orb2):
    def __init__(self, *args, **kwargs):
        super(Gain, self).__init__(*args, **kwargs)
        self.default_in = sndobj.SndIn()
        self.snd = sndobj.Gain(0.0, self.default_in)
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Multiplier: \n {font_name 'Flotsam smart'}{bold False}Gain'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
        
        self.orange = None #disable orange control
        self.blue.rotation = 0
    
    def update(self, dt):
        multiplier = self.blue.rotation/2
        
        if multiplier <= 0:
            multiplier += 1000
            multiplier /= 1000 
        
        if self.hovering:
            self.update_infobox([multiplier])
        self.snd.SetGainM(multiplier)
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class Hilb(Orb2):
    def __init__(self, *args, **kwargs):
        super(Hilb, self).__init__(*args, **kwargs)
        self.default_in = sndobj.SndIn()
        self.snd = sndobj.Hilb(self.default_in)
        
        self.infobox = ''' {color (255,255,255,255)}{font_name 'Flotsam smart'}Hilb'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
        
        self.orange = None
        self.blue = None
    
    def update(self, dt):
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class HiPass(Orb2):
    def __init__(self, *args, **kwargs):
        super(HiPass, self).__init__(*args, **kwargs)
        self.blue.rotation = 3060. # set for upcoming hipass init
        self.blue.revolutions = 8
        self.default_in = sndobj.SndIn()
        self.snd = sndobj.HiPass(self.blue.rotation, self.default_in)
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Cutoff Freq: \n {font_name 'Flotsam smart'}{bold False}HiPass'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
        
        self.orange = None
    
    def update(self, dt):
        cutoff = abs(self.blue.rotation)
        self.snd.SetFreq(cutoff)
        
        if self.hovering:
            self.update_infobox([cutoff])
        
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class IFFT(Orb2):
    def __init__(self, *args, **kwargs):
        super(IFFT, self).__init__(*args, **kwargs)
        self.default_in = sndobj.SndIn()
        self.snd = sndobj.IFFT(sound.tab, self.default_in)
        
        self.infobox = ''' {color (255,255,255,255)}{font_name 'Flotsam smart'}IFFT'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
        self.orange = None
        self.blue = None
    
    def update(self, dt):
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class LineIn(Orb2):
    def __init__(self, *args, **kwargs):
        super(LineIn, self).__init__(*args, **kwargs)
        space.manage.line_in_port += 1
        self.sndio_in = True
        self.snd = sndobj.SndIn(sound.input, space.manage.line_in_port)
        
        self.infobox = ''' {color (255,255,255,255)}{font_name 'Flotsam smart'}LineIn'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
        self.orange = None
        self.blue = None
    
    def update(self, dt):
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class Loop(Orb2):
    def __init__(self, *args, **kwargs):
        super(Loop, self).__init__(*args, **kwargs)
        self.default_in = sndobj.SndIn()
        self.snd = sndobj.SndLoop(0.05, 5., self.default_in, 1.)
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Semitone: \n {font_name 'Flotsam smart'}{bold False}SnDlooP'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
        
        self.orange = None
    
    def set_output(self, obj):
        super(Loop, self).set_output(obj)
        self.snd.ReSample()
    
    def update(self, dt):
        semitone = int(self.blue.rotation/12)
        
        self.snd.SetPitch(semitone)
        self.label_looptime.text = 'Loop Time: {0}'.format(semitone)
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class LoPass(Orb2):
    def __init__(self, *args, **kwargs):
        super(LoPass, self).__init__(*args, **kwargs)
        self.default_in = sndobj.SndIn()
        self.snd = sndobj.LoPass(self.blue.rotation, self.default_in)
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Cutoff Freq: \n {font_name 'Flotsam smart'}{bold False}LoPass'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
        
        self.orange = None
    
    def update(self, dt):
        cutoff = abs(self.blue.rotation)
        self.snd.SetFreq(cutoff)
        
        if self.hovering:
            self.update_infobox([cutoff])
        
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class Mixer(OrbMixer):
    def __init__(self, *args, **kwargs):
        super(Mixer, self).__init__(*args, **kwargs)
        
        self.space = space.Space()
        space.manage.spaces.append(self.space)
        
        self.snd = self.space.mixer
        
        self.infobox = ''' {color (255,255,255,255)}{font_name 'Flotsam smart'}MiXer'''
        
        self.popout = numpy.zeros(self.space.mixer.GetVectorSize(), dtype='float32')
    
    def update(self, dt):
        self.space.mixer.PopOut(self.popout[0:self.space.mixer.GetVectorSize()])


class Oscili(Orb2):
    def __init__(self, *args, **kwargs):
        super(Oscili, self).__init__(*args, **kwargs)
        
        self.snd = sndobj.Oscili(sound.tab, 0, 9900)
        self.blue.rotation = 9900
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Frequency: \n Amplitude: \n {font_name 'Flotsam smart'}{bold False}OsCiLi'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
    
    def update(self, dt):
        frequency = determine_constrained_value(min=0, max=940, \
            val=abs(degrees(self.body.angle)))
        amplitude = abs(self.blue.rotation)
        
        if self.hovering:
            self.update_infobox([frequency, amplitude])
        
        self.snd.SetFreq(frequency)
        self.snd.SetAmp(amplitude)
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class OsciliHam(Orb2):
    def __init__(self, *args, **kwargs):
        super(OsciliHam, self).__init__(*args, **kwargs)
        
        self.snd = sndobj.Oscili(sound.ham, 0, 9900)
        self.blue.rotation = 9900
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Frequency: \n Amplitude: \n {font_name 'Flotsam smart'}{bold False}OsCiLi'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
    
    def update(self, dt):
        frequency = determine_constrained_value(min=0, max=940, \
            val=abs(degrees(self.body.angle)))
        amplitude = abs(self.blue.rotation)
        
        if self.hovering:
            self.update_infobox([frequency, amplitude])
        
        self.snd.SetFreq(frequency)
        self.snd.SetAmp(amplitude)
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class OsciliSaw(Orb2):
    def __init__(self, *args, **kwargs):
        super(OsciliSaw, self).__init__(*args, **kwargs)
        
        self.snd = sndobj.Oscili(sound.saw, 0, 9900)
        self.blue.rotation = 9900
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Frequency: \n Amplitude: \n {font_name 'Flotsam smart'}{bold False}OsCiLi'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
    
    def update(self, dt):
        frequency = determine_constrained_value(min=0, max=940, \
            val=abs(degrees(self.body.angle)))
        amplitude = abs(self.blue.rotation)
        
        if self.hovering:
            self.update_infobox([frequency, amplitude])
        
        self.snd.SetFreq(frequency)
        self.snd.SetAmp(amplitude)
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class OsciliBuzz(Orb2):
    def __init__(self, *args, **kwargs):
        super(OsciliBuzz, self).__init__(*args, **kwargs)
        
        self.snd = sndobj.Oscili(sound.buzz, 0, 9900)
        self.blue.rotation = 9900
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Frequency: \n Amplitude: \n {font_name 'Flotsam smart'}{bold False}OsCiLi'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
    
    def update(self, dt):
        frequency = determine_constrained_value(min=0, max=940, \
            val=abs(degrees(self.body.angle)))
        amplitude = abs(self.blue.rotation)
        
        if self.hovering:
            self.update_infobox([frequency, amplitude])
        
        self.snd.SetFreq(frequency)
        self.snd.SetAmp(amplitude)
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class Phase(Orb2):
    def __init__(self, *args, **kwargs):
        super(Phase, self).__init__(*args, **kwargs)
        
        self.snd = sndobj.Phase(440.)
        self.snd.SetFreq(0)
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Frequency: \n Phase: \n {font_name 'Flotsam smart'}{bold False}Phase'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
    
    def update(self, dt):
        freq = determine_constrained_value(min=0, max=440, \
                                          val=abs(self.body.angle*(180/pi)))
        
        phase = abs(self.blue.rotation)
        
        if self.hovering:
            self.update_infobox([freq, phase])
        
        self.snd.SetFreq(freq)
        self.snd.SetPhase(phase)
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class Pitch(Orb2):
    def __init__(self, *args, **kwargs):
        super(Pitch, self).__init__(*args, **kwargs)
        self.default_in = sndobj.SndIn()
        self.snd = sndobj.Pitch(0.1, self.default_in, 0)
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Semitone: \n {font_name 'Flotsam smart'}{bold False}Pitch'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
        
        self.orange = None #disable orange control
    
    def update(self, dt):
        semitone = int(self.blue.rotation/12)
        
        self.snd.SetPitch(semitone)
        if self.hovering:
            self.update_infobox([semitone])
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class PVA(Orb2):
    def __init__(self, *args, **kwargs):
        super(PVA, self).__init__(*args, **kwargs)
        self.default_in = sndobj.SndIn()
        self.links = []
        self.snd = sndobj.PVA(sound.ham, self.default_in)
        self.in_mixer = False
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Scale: \n {font_name 'Flotsam smart'}{bold False}PVA'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
    
    def update(self, dt):
        scale = determine_constrained_value(0, 1, self.blue.rotation/1000)
        self.snd.SetScale(scale)
        if self.hovering:
            self.update_infobox([scale])
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class PVBlur(Orb2):
    def __init__(self, *args, **kwargs):
        super(PVBlur, self).__init__(*args, **kwargs)
        self.default_in = sndobj.PVA(sound.ham, sndobj.SndIn())
        self.snd = sndobj.PVBlur(self.default_in, 0.1)
        self.in_mixer = False
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Blur: \n {font_name 'Flotsam smart'}{bold False}PVBlur'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
    
    def update(self, dt):
        blur = determine_constrained_value(0, 1, self.blue.rotation/1000)
        #self.snd.SetBlurTime(blur)
        if self.hovering:
            self.update_infobox([blur])
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class PVMorph(Orb2):
    def __init__(self, *args, **kwargs):
        super(PVMorph, self).__init__(*args, **kwargs)
        self.default_in1 = sndobj.SndIn()
        self.default_in2 = sndobj.SndIn()
        self.links = [self.default_in1, self.default_in2]
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Frequency: \n Amplitude: \n {font_name 'Flotsam smart'}{bold False}PVMorph'''
        
        self.popout = numpy.zeros(256, dtype='float32')
    
    def on_connect_input(self, from_obj, x, y):
        x1, y1 = self.body.position
        w = self.base.image.width/2
        
        if x1-w <= x <= x1:
            self.links[0] = from_obj.snd
        elif x1 <= x <= x1+w:
            self.links[1] = from_obj.snd
        
        #l, r = repr(self.links[0]), repr(self.links[1])
        #self.update_infobox([l[8:l.index(';')], r[8:r.index(';')]])
        #self.snd.SetInput(*self.links)
    
    def create(self):
        self.snd = sndobj.PVMorph(0.1, 0.1, self.inputs[0], self.inputs[1])
        self.in_mixer = False
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
    
    def update(self, dt):
        freq = determine_constrained_value(min=0, max=440, \
                                          val=abs(self.body.angle*(180/pi)))
        
        amp = abs(self.blue.rotation)
        if hasattr(self, 'snd'):
            self.snd.SetFreqMorph(freq)
            self.snd.SetAmpMorph(amp)
            self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])
        
        if self.hovering:
            self.update_infobox([freq, amp])


class PVS(Orb2):
    def __init__(self, *args, **kwargs):
        super(PVS, self).__init__(*args, **kwargs)
        self.default_in = sndobj.SndIn()
        self.snd = sndobj.PVS(sound.ham, self.default_in)
        
        self.infobox = ''' {color (255,255,255,255)}{font_name 'Flotsam smart'}PVS'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
        self.orange = None
        self.blue = None
    
    def update(self, dt):
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class Ring(OrbMultiConnect):
    def __init__(self, *args, **kwargs):
        super(Ring, self).__init__(*args, **kwargs)
        self.default_in1 = sndobj.SndIn()
        self.default_in2 = sndobj.SndIn()
        self.links = [self.default_in1, self.default_in2]
        self.snd = sndobj.Ring(*self.links)
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}First Input: \n Second Input: \n {font_name 'Flotsam smart'}{bold False}RinG'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
    
    def on_connect_input(self, from_obj, x, y):
        x1, y1 = self.body.position
        w = self.base.image.width/2
        
        if x1-w <= x <= x1:
            print 'one'
            self.links[0] = from_obj.snd
            self.snd.SetInput1(self.links[0])
            from_obj._output = self
        elif x1 <= x <= x1+w:
            print 'two'
            self.links[1] = from_obj.snd
            self.snd.SetInput2(self.links[1])
            from_obj._output = self
        
        l, r = repr(self.links[0]), repr(self.links[1])
        self.update_infobox([l[8:l.index(';')], r[8:r.index(';')]])
    
    def update(self, dt):
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class SndRead(Orb2):
    def __init__(self, *args, **kwargs):
        super(SndRead, self).__init__(*args, **kwargs)
        self.snd = sndobj.SndRead('frompysndobj.wav', 1.)
        
        self.infobox = ''' {color (255,255,255,255)}{font_name 'Flotsam smart'}SnDReaD'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
    
    def update(self, dt):
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class SpecMult(OrbMultiConnect):
    def __init__(self, *args, **kwargs):
        super(SpecMult, self).__init__(*args, **kwargs)
        self.default_in1 = sndobj.FFT(sound.ham, sndobj.SndIn())
        self.default_in2 = sndobj.FFT(sound.ham, sndobj.SndIn())
        self.links = [self.default_in1, self.default_in2]
        self.snd = sndobj.SpecVoc(*self.links)
        self.in_mixer = False
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}First Input: \n Second Input: \n {font_name 'Flotsam smart'}{bold False}SPeCMuLt'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
    
    def on_connect_input(self, from_obj, x, y):
        x1, y1 = self.body.position
        w = self.base.image.width/2
        
        if x1-w <= x <= x1:
            print 'one'
            self.links[0] = from_obj.snd
            self.snd.SetInput(self.links[0])
        elif x1 <= x <= x1+w:
            print 'two'
            self.links[1] = from_obj.snd
            self.snd.SetInput2(self.links[1])
        
        l, r = repr(self.links[0]), repr(self.links[1])
        self.update_infobox([l[8:l.index(';')], r[8:r.index(';')]])
        from_obj._output = self
    
    def update(self, dt):
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class SpecThresh(Orb2):
    def __init__(self, *args, **kwargs):
        super(SpecThresh, self).__init__(*args, **kwargs)
        self.default_in = sndobj.SndIn()
        self.snd = sndobj.SpecThresh(0.0, self.default_in)
        self.in_mixer = False
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Threshold: \n {font_name 'Flotsam smart'}{bold False}SPeCThresh'''        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
        
        self.orange = None # disable orange control
        self.blue.rotation = 0
    
    def update(self, dt):
        threshold = determine_constrained_value(0, 1, self.blue.rotation/1000)
        self.snd.SetThreshold(threshold)
        
        if self.hovering:
            self.update_infobox([threshold])
        
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class SpecVoc(OrbMultiConnect):
    def __init__(self, *args, **kwargs):
        super(SpecVoc, self).__init__(*args, **kwargs)
        self.default_in1 = sndobj.FFT(sound.ham, sndobj.SndIn())
        self.default_in2 = sndobj.FFT(sound.ham, sndobj.SndIn())
        self.links = [self.default_in1, self.default_in2]
        self.snd = sndobj.SpecVoc(*self.links)
        self.in_mixer = False
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}First Input: \n Second Input: \n {font_name 'Flotsam smart'}{bold False}SpecVoc'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
    
    def on_connect_input(self, from_obj, x, y):
        x1, y1 = self.body.position
        w = self.base.image.width/2
        
        if x1-w <= x <= x1:
            print 'one'
            self.links[0] = from_obj.snd
            self.snd.SetInput(self.links[0])
        elif x1 <= x <= x1+w:
            print 'two'
            self.links[1] = from_obj.snd
            self.snd.SetInput2(self.links[1])
        
        l, r = repr(self.links[0]), repr(self.links[1])
        self.update_infobox([l[8:l.index(';')], r[8:r.index(';')]])
        from_obj._output = self
    
    def update(self, dt):
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])


class VDelay(Orb2):
    def __init__(self, *args, **kwargs):
        super(VDelay, self).__init__(*args, **kwargs)
        
        self.default_in = sndobj.SndIn()
        self.snd = sndobj.VDelay(.999, .2, .3, .3, .3, self.default_in)
        
        self.infobox = ''' {color (255,255,255,255)}{bold True}Delay: \n Feedback Gain: \n Forward Gain: \n Direct Gain: \n {font_name 'Flotsam smart'}{bold False}vDeLay'''        
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
    
    def update(self, dt):
        d = abs(self.body.angle)*.1
        if str(self.snd.GetDelayTime())[:5] != str(d)[:5]:
            if d == 0.:
                d = 0.001
            self.snd.SetDelayTime(d)
        
        
        feedback_val = abs(self.blue.rotation*.001)
        feedback = determine_constrained_value(min=0, max=.999, val=feedback_val)
        self.snd.SetFdbgain(feedback)
        
        forward_val, direct_val = self.body.position.x, self.body.position.y
        forward = determine_constrained_value(0, .999, abs(forward_val)/1024)
        direct = determine_constrained_value(0, .999, abs(direct_val)/700)
        
        self.snd.SetFwdgain(forward)
        self.snd.SetDirgain(direct)
        
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])
        
        if self.hovering:
            self.update_infobox([d, feedback, forward, direct])


class Wave(Orb2):
    def __init__(self, *args, **kwargs):
        super(Wave, self).__init__(*args, **kwargs)
        self.default_in = sndobj.SndIn()
        self.snd = sndobj.SndWave("frompysndobj.wav", sndobj.OVERWRITE)
        self.snd.SetOutput(1, self.default_in)
        sound.thread.AddObj(self.snd, sndobj.SNDIO_OUT)
        
        self.infobox = ''' {color (255,255,255,255)}{font_name 'Flotsam smart'}Wave'''
        
        self.popout = numpy.zeros(self.snd.GetVectorSize(), dtype='float32')
    
    def on_destroy(self):
        sound.thread.DeleteObj(self.snd, sndobj.SNDIO_OUT)
        self.snd = None
    
    def on_connect(self, to_obj):
        self.snd.SetOutput(1, to_obj.snd)
    
    def update(self, dt):
        self.snd.PopOut(self.popout[0:self.snd.GetVectorSize()])

