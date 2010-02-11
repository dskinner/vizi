# -*- coding: utf-8 -*-
#!/usr/bin/env python

from app import *
from timer import *
from qgl import *

import space
from viziobj import *
import menu
from sound import *

if __name__ == '__main__':
    glwidget.show()
    sound.thread.ProcOn()
    sys.exit(app.exec_())