#!/usr/bin/env python

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

#  by David Skinner
#  and Daniel Skinner
#  on June 
#
#  read a midi file and map it to sound effects.

import pyglet
from pyglet import clock
from midi import MidiFile

import math
import time

try:
    import sndobj
except:
    import win32sndobj as sndobj

class ViziMidiFreq(object):
    def __init__ (self, midi_note = 69, base_freq = 440):
        self.COUNT_MIDI_NOTE = 128
        self.freq = []
        assert midi_note >= 0
        assert midi_note < self.COUNT_MIDI_NOTE
        assert base_freq > 0.0
        for note in range(-midi_note, self.COUNT_MIDI_NOTE - midi_note):
            my_freq = base_freq * pow(pow(10, math.log10(2) / 12), note)
            self.freq.append(my_freq)
            
    def pitch(self, midi_note):
        assert midi_note >= 0
        assert midi_note < self.COUNT_MIDI_NOTE
        return self.freq[midi_note]
        
        
#  Global Array
midi_map = []

class ViziMidiEvents(object):
    def __init__(self, event_type, my_tick, track, channel = 0, pitch = 0, velocity = 0):
        self.event_type = event_type
        self.my_tick = my_tick
        self.track = track
        self.channel = channel
        self.pitch = pitch
        self.velocity = velocity

    def DoProcess(self, last_tick):
        if self.event_type == delta_time:
            return last_tick + self.my_tick    
        elif event_type == NOTE_ON:
            if self.my_tick > last_tick:
                return self.my_tick
            else:
                for my_map in midi_map:
                    if self.track != my_map.track:
                        pass
                    elif self.channel != my_map.channel:
                        pass
                    elif self.pitch != my_map.pitch:
                        pass
                    elif self.velocity == 0:
                        my_map.note_off()
                    else:
                        my_map.note_on()
                        

class ViziMidiTracks(object):
    def __init__(self):
        self.my_midiEvents = []
        self.count_events
        self.next_tick = 0
        self.next_event_index = 0
    
    def Append(self, this_event):
        self.my_midiEvents.append(this_event)
        self.count_events += 1
        
    def Restart(self, restart_tick):
        self.next_tick = restart_tick
        self.next_event_index = 0
        
    def DoProcess(self, tick_counter): # on each track will determine if it is time to process next element
        ret_value = False
        while tick_counter <= next_tick:
            if next_event_index < self.count_events:
                next_tick = my_midiEvent[next_event_index].DoProcess(next_tick)
                next_event_index += 1    
            else:
                ret_value = False
                break
        return ret_value


class ViziMidiFile(object):
    def __init__(self, infile):
        self.my_tracks = []  #read from file
        self.my_midiMap = [] # matches MidiSndObj.note_event() with NoteEvents  
        self.next_time = 0.0
        self.tempo = 120.0     
        self.tick_counter = 0
        self.each_time = (60.0 / self.tempo) / 96.0
        self.m = MidiFile()
        self.m.open(infile)
        self.m.read()
        self.m.close()
    
    def __repr__(self):
        return `self.__dict__`
    
    def Print(self):
        print self.m

    def Restart(self, restart_tick = 0):
        for my_track in self.my_tracks:
            my_track.Restart(restart_tick)
        self.tick_counter = restart_tick
        self.next_time = restart_tick * self.each_time
        
    def DoProcess(self, this_time): # increments the tick counter when the time is right
        if self.next_time >= this_time:
            return True
        else:
            ret_value = 0
            self.next_time += self.each_time
            self.tick_counter += 1
            for this_track in self.my_tracks:
                ret_value += this_track.DoProcess(self.tick_counter)
            return ret_value
    
class ViziMidiMap(object):
    def __init__ (self, midiSndObj, track, channel, pitch):
        self.MidiSndObj = midiSndObj
        self.track = track
        self.channel = channel
        self.pitch = pitch
        
    def note_on(self,velocity):
        self.MidiSndObj.note_on(velocity)
    
    def note_off(self):
        self.MidiSndObj.note_off()
        
#  Vizi Sound Objects can go in a different file maybe



class ViziADSR(sndobj.ADSR):
    def __init__(self, *args, **kwargs):
        super(ViziADSR, self).__init__(*args, **kwargs)
        
    def note_on(self, velocity):
        self.SetMaxAmp(velocity / 128)
        self.Restart()

    def note_off(self):
        self.Release()

        
class ViziPluck(sndobj.Pluck):
    def __init__(self, *args, **kwargs):
        super(ViziPluck, self).__init__(*args, **kwargs)
    
    def note_on(self, velocity):
        #self.Enable()
        self.SetAmp(velocity * 32767 / 128)

    def note_off(self):
        pass#self.Disable()
  
  
if __name__ == '__main__':
    #try:
    if True:
        thread = sndobj.SndThread()
        doit = []
        
        #  Define Mixers
        mixerLeft = sndobj.Mixer()
        doit.append(mixerLeft)
        
        mixerRight = sndobj.Mixer()
        doit.append(mixerRight)
        
        midi_freq = ViziMidiFreq()
        
        #  Create each string.
        count = 128
        
        OBOE = False
        if OBOE:
            oboe = []
            
            #  Triangle wave table.
            tri_ints = range(-256,256,1) + range(256,-256,-1)
            tri_amps = sndobj.floatArray(len(tri_ints))
            for i, x in enumerate(tri_ints):
                tri_amps[i] = 10000.0 * x / 256
            tri_tab = sndobj.UsrHarmTable(1024, 1, tri_amps)
            
            for note in range(count):
                freq = midi_freq.pitch(note)
                osc = sndobj.Oscili(tri_tab, freq, 32767)
                doit.append(osc)
        
                #  ADSR(attackTime,maxAmp,decayTime,sustainAmp,releaseTime,durationTime,InObj)
                env = ViziADSR(.2, 0.0, .2, .1, .05, 12.0, osc)
                oboe.append(env)
                doit.append(env)
                p = (2.0 * note / (count - 1)) - 1.0
                pan = sndobj.Pan(p,env)
                doit.append(pan)
        
                # Mix the signals for each channel
                mixerLeft.AddObj(pan.left)
                mixerRight.AddObj(pan.right)
        
        HARP = True
        if HARP:
            harp = []
            for note in range(count):
                freq = midi_freq.pitch(note)
                p = (2.0 * note / (count - 1)) - 1.0
                osc = ViziPluck(freq, 0.)
                harp.append(osc)
                doit.append(osc)
                pan = sndobj.Pan(p,osc)
                doit.append(pan)
                mixerLeft.AddObj(pan.left)
                mixerRight.AddObj(pan.right)
                
        #  Hear the chime.
        import sys
        jack = 'jack' in sys.argv[-1] and True or False
        if not jack:
            outp = sndobj.SndRTIO(2, sndobj.SND_OUTPUT)
            outp.SetOutput(1, mixerLeft)
            outp.SetOutput(2, mixerRight)
        else:
            outp = sndobj.SndJackIO('vizimidi_test')
            gainl = sndobj.Gain(0., mixerLeft)
            gainl.SetGainM(1./3276)
            gainr = sndobj.Gain(0., mixerRight)
            gainr.SetGainM(1./3276)
            thread.AddObj(gainl)
            thread.AddObj(gainr)
            outp.SetOutput(1, gainl)
            outp.SetOutput(2, gainr)
        
        for i, x in enumerate(doit):
            thread.AddObj(x)
        thread.AddObj(outp, sndobj.SNDIO_OUT)
 
        #testViziMidi = ViziMidiFile("ISawHerStandingThere.mid")
       
        print "Begin Playing song"
        myTime = 0.0
        #clock.tick()
        #testViziMidi.Restart(myTime)
        thread.ProcOn()
        
        strings = len(harp)
        string = 0
        
        def update(dt):
            pass

        clock.schedule(update)
        clock.set_fps_limit(30)
        window = pyglet.window.Window()
        
        def pluck_harp(dt):
            global strings, string
            #print 'playing harp[%s]' % string
            harp[string].note_on(.9)
            string += 1
            if string >= strings:
                string = 0
        
        clock.schedule_interval(pluck_harp, .1)
        pyglet.app.run() # main loop
        
        '''
        def tick_tock(dt):
            global myTime
            myTime += dt
            print myTime, testViziMidi.DoProcess(myTime)
            if testViziMidi.DoProcess(myTime) == False:
                clock.unschedule(tick_tock)
                
        clock.schedule_interval(tick_tock, testViziMidi.each_time)
        #time.sleep(4)
        #time.sleep(54600 * testViziMidi.each_time)
        thread.ProcOff()
        testViziMidi.Print()
        '''
    #except Exception as e:
    else:
        print 'Exception: ', e
        
