# -*- coding: utf-8 -*-
#!/usr/bin/env python

from app import *
from timer import *
from qgl import *
import space
from viziobj import *
import menu
from sound import *
from vobj import *

if __name__ == '__main__':
    glwidget.show()
    sound.thread.ProcOn()
    #space.manage.active.add_body(Oscili(position=(150, 150)))
    #space.manage.active.add_body(Oscili(position=(130, 130)))
    sys.exit(app.exec_())