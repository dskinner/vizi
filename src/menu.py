# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL, QObject

import viziobj
import space
from qgl import glwidget
from app import app

import random
import yaml

class MyFilter(QtCore.QObject):
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.HoverEnter:
            left_panel.label_help.setText(obj.help_text)
        return QtGui.QWidget.eventFilter(self, obj, event)

class MenuLabel(QtGui.QPushButton):
    def __init__(self, text, tooltip, description):
        QtGui.QPushButton.__init__(self, text)
        self.setToolTip(tooltip)
        self.help_text = description
        
        self.setFlat(True)
        self.setStyleSheet('text-align: left;')
        self.event_filter = MyFilter()
        self.installEventFilter(self.event_filter)
    
    def mouseReleaseEvent(self, event):
        space.manage.active.add_body(getattr(viziobj, str(self.text()))(position=(350, 150)))
        space_menu.update_label()


class Menu(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.labels = []
        for k, v in sorted(yaml.load(open('sound_objects.yaml')).items()):
            self.labels.append(MenuLabel(k, v[0], v[1]))
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
        self.label.setStyleSheet('font-size: 12pt; font-weight: bold; margin: 0 0 0 10px; padding: 0;')
        self.total = QtGui.QLabel(' of {0}'.format('1'))
        self.total.setStyleSheet('margin: 0; padding: 0;')
        
        self.left_button = QtGui.QPushButton('L')
        self.connect(self.left_button, SIGNAL('clicked(bool)'), self.left_click)
        
        self.right_button = QtGui.QPushButton('R')
        self.connect(self.right_button, SIGNAL('clicked(bool)'), self.right_click)
        
        self.physics_sim = QtGui.QCheckBox('Physics')
        self.connect(self.physics_sim, SIGNAL('stateChanged(int)'), self.set_physics_sim)
        
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.left_button)
        layout.addWidget(self.label)
        layout.addWidget(self.total)
        layout.addWidget(self.right_button)
        layout.addWidget(self.physics_sim)
        self.setLayout(layout)
    
    def set_physics_sim(self, i):
        space.manage.active.step = i and True or False
    
    def left_click(self, b):
        space.manage.activate_space(space.manage.spaces.index(space.manage.active) - 1)
        self.update_label()
    
    def right_click(self, b):
        space.manage.activate_space(space.manage.spaces.index(space.manage.active) + 1)
        self.update_label()
    
    def update_label(self, b=True):
        self.label.setText('Mixer {0}'.format((space.manage.spaces.index(space.manage.active)+1)))
        self.total.setText(' of {0}'.format(space.Space.i))


menu = Menu()
scroll_area = QtGui.QScrollArea()
scroll_area.setWidget(menu)


tabs = QtGui.QTabWidget()
tabs.setTabPosition(2)
tabs.addTab(scroll_area, 'Sound Objects')
tabs.addTab(QtGui.QWidget(), 'Filesystem')
tabs.addTab(QtGui.QWidget(), 'Projects')
tabs.addTab(QtGui.QWidget(), 'Mixer States')


class LeftPanel(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setStyleSheet('background-color: #242424; color: white;')
        self.setGeometry(0, 0, 190, 700)
        
        self.label_container = QtGui.QWidget()
        self.label_container.setFixedHeight(150)
        self.label_container.setStyleSheet(':focus { border: none; }')
        self.label_help = QtGui.QLabel('this is a test', parent=self.label_container)
        self.label_help.setMinimumSize(170, 140)
        self.label_help.setWordWrap(True)
        self.label_help.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabs)
        layout.addWidget(self.label_container)
        self.setLayout(layout)


left_panel = LeftPanel(glwidget)

space_menu = MenuSpace(glwidget)