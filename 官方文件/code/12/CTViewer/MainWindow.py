# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(833, 706)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.vtk_window_1 = QVTKRenderWindowInteractor(self.centralwidget)
        self.vtk_window_1.setObjectName("vtk_window_1")
        self.gridLayout.addWidget(self.vtk_window_1, 0, 0, 1, 1)
        self.vtk_window_3 = QVTKRenderWindowInteractor(self.centralwidget)
        self.vtk_window_3.setObjectName("vtk_window_3")
        self.gridLayout.addWidget(self.vtk_window_3, 1, 0, 1, 1)
        self.vtk_window_4 = QVTKRenderWindowInteractor(self.centralwidget)
        self.vtk_window_4.setObjectName("vtk_window_4")
        self.gridLayout.addWidget(self.vtk_window_4, 1, 1, 1, 1)
        self.vtk_window_2 = QVTKRenderWindowInteractor(self.centralwidget)
        self.vtk_window_2.setObjectName("vtk_window_2")
        self.gridLayout.addWidget(self.vtk_window_2, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 833, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ImageViewDemo"))

