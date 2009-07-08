# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu.ui'
#
# Created: Wed Jul  8 01:12:24 2009
#      by: PyQt4 UI code generator 4.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TabWidget(object):
    def setupUi(self, TabWidget):
        TabWidget.setObjectName("TabWidget")
        TabWidget.resize(267, 322)
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.listWidget = QtGui.QListWidget(self.tab)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 256, 192))
        self.listWidget.setObjectName("listWidget")
        QtGui.QListWidgetItem(self.listWidget)
        QtGui.QListWidgetItem(self.listWidget)
        QtGui.QListWidgetItem(self.listWidget)
        self.pushButton = QtGui.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(130, 220, 96, 24))
        self.pushButton.setObjectName("pushButton")
        TabWidget.addTab(self.tab, "")
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName("tab1")
        TabWidget.addTab(self.tab1, "")

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)

    def retranslateUi(self, TabWidget):
        TabWidget.setWindowTitle(QtGui.QApplication.translate("TabWidget", "TabWidget", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.item(0).setText(QtGui.QApplication.translate("TabWidget", "Gain", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.item(1).setText(QtGui.QApplication.translate("TabWidget", "Mixer", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.item(2).setText(QtGui.QApplication.translate("TabWidget", "Oscili", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(QtGui.QApplication.translate("TabWidget", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        TabWidget.setTabText(TabWidget.indexOf(self.tab), QtGui.QApplication.translate("TabWidget", "Tab 1", None, QtGui.QApplication.UnicodeUTF8))
        TabWidget.setTabText(TabWidget.indexOf(self.tab1), QtGui.QApplication.translate("TabWidget", "Tab 2", None, QtGui.QApplication.UnicodeUTF8))

