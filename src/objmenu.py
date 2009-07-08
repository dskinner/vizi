# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'objmenu.ui'
#
# Created: Tue Jul  7 00:55:13 2009
#      by: PyQt4 UI code generator 4.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(158, 224)
        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 121, 192))
        self.listWidget.setFrameShape(QtGui.QFrame.NoFrame)
        self.listWidget.setFrameShadow(QtGui.QFrame.Plain)
        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.listWidget.setObjectName("listWidget")
        QtGui.QListWidgetItem(self.listWidget)
        QtGui.QListWidgetItem(self.listWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.item(0).setText(QtGui.QApplication.translate("Form", "FFT", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.item(1).setText(QtGui.QApplication.translate("Form", "Oscili", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.setSortingEnabled(__sortingEnabled)

