from __future__ import division
from PyQt4 import QtCore, QtGui

import space
from viziobj import *
from window import *

class ShowMenuButton(QtGui.QPushButton):
    def __init__(self, *args):
        super(ShowMenuButton, self).__init__(*args)
        self.setGeometry(10, 100, 100, 25)
    
    def mousePressEvent(self, event):
        super(ShowMenuButton, self).mousePressEvent(event)
        menu._menu.tab.show()


class Menu(QtGui.QTabWidget):
    def __init__(self, *args):
        super(Menu, self).__init__(*args)
        self._menu = uic.loadUi('menu.ui', self)
        self.connect(self._menu.listWidget, SIGNAL('clicked(QModelIndex)'), \
                     self.clicked)
    
    def clicked(self, index):
        obj = index.data().toString()
        space.manage.active.add_body(globals()[str(obj)](position=(150, 150)))
        print 'index:', obj


class SndObjs(QtGui.QFrame):
    def __init__(self, *args):
        super(SndObjs, self).__init__(*args)
        self._sndobjs = uic.loadUi('sndobjs.ui', self)
        self.connect(self._sndobjs.sndobjs, SIGNAL('clicked(QModelIndex)'), \
                     self.clicked)
    
    def clicked(self, index):
        obj = index.data().toString()
        space.manage.active.add_body(globals()[str(obj)](position=(550, 150)))
        print 'index:', obj
        

show_menu = ShowMenuButton('Show Menu', window)
menu = SndObjs(window)

window.connect(show_menu, QtCore.SIGNAL('clicked()'), menu, \
               QtCore.SLOT('show()'))

