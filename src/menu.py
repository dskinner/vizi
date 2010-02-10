# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL

import viziobj
import space
from qgl import glwidget

class MenuLabel(QtGui.QLabel):
    def mouseReleaseEvent(self, event):
        space.manage.active.add_body(getattr(viziobj, str(self.text()))(position=(150, 150)))


class Menu(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.labels = [ 'ADSR',
                        'Balance',
                        'Buzz',
                        'FFT',
                        'Filter',
                        'Gain',
                        'HarmTable',
                        'HiPass',
                        'Hilb',
                        'IFFT',
                        'LineIn',
                        'LoPass',
                        'Loop',
                        'Mixer',
                        'Oscili',
                        'OsciliSaw',
                        'OsciliBuzz',
                        'OsciliHam',
                        'PVA',
                        'PVBlur',
                        'PVMorph',
                        'PVS',
                        'Phase',
                        'Pitch',
                        'Ring',
                        'SndRead',
                        'SpecMult',
                        'SpecThresh',
                        'SpecVoc',
                        'VDelay',
                        'Wave']
        self.labels = [MenuLabel(x) for x in self.labels]
        layout = QtGui.QVBoxLayout()
        for l in self.labels:
            layout.addWidget(l)
        self.setLayout(layout)
    

class MenuSpace(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setStyleSheet('margin: 0px; padding: 10px; background-color: #242424; color: white;')
        self.move((1224/2)-(190/2.), 0)
        
        self.label = QtGui.QLabel('Mixer {0}'.format('1'))
        self.total = QtGui.QLabel(' of {0}'.format('1'))
        
        self.left_button = QtGui.QPushButton('L')
        self.connect(self.left_button, SIGNAL('clicked(bool)'), self.left_click)
        
        self.right_button = QtGui.QPushButton('R')
        self.connect(self.right_button, SIGNAL('clicked(bool)'), self.right_click)
        
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.left_button)
        layout.addWidget(self.label)
        layout.addWidget(self.total)
        layout.addWidget(self.right_button)
        self.setLayout(layout)
    
    def left_click(self, b):
        space.manage.activate_space(space.manage.spaces.index(space.manage.active) - 1)
        self.update_label()
    
    def right_click(self, b):
        space.manage.activate_space(space.manage.spaces.index(space.manage.active) + 1)
        self.update_label()
    
    def update_label(self, b=True):
        print 'calling update_label'
        self.label.setText('Mixer {0}'.format((space.manage.spaces.index(space.manage.active)+1)))
        self.total.setText(' of {0}'.format(space.Space.i))


menu = Menu()
tabs = QtGui.QTabWidget(glwidget)
tabs.setStyleSheet('background-color: #242424; color: white;')
tabs.setTabPosition(2)
tabs.addTab(menu, 'Sound Objects')

space_menu = MenuSpace(glwidget)
space_menu.connect(menu.labels[5], SIGNAL('clicked(bool)'), space_menu.update_label)
print menu.labels[5].text()