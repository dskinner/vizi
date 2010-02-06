# -*- coding: utf-8 -*-
#!/usr/bin/env python

from app import *
from timer import *
from qgl import *
import qspace
from qviziobj import *
from sound import *

if __name__ == '__main__':
    glwidget.show()
    sound.thread.ProcOn()
    space.manage.active.add_body(Oscili(position=(150, 150)))
    space.manage.active.add_body(Oscili(position=(130, 130)))
    sys.exit(app.exec_())