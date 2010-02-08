# -*- coding: utf-8 -*-
from PyQt4 import QtGui

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
    

menu = Menu(glwidget)