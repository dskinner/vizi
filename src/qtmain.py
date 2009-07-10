'''
Created on Jun 30, 2009

@author: daniel
'''
from __future__ import division
from window import *
from menu import *

from Box2D import *
from math import atan, atan2, cos, degrees, pi, sin, sqrt

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
import space


if __name__ == '__main__':
    sound.thread.ProcOn()
    window.show()
    space.manage.active.add_body(Oscili(position=(150, 150)))
    space.manage.active.add_body(Oscili(position=(130, 130)))
    sys.exit(app.exec_())
