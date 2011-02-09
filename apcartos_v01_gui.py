# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'apcartos_v01_gui.ui'
#
# Created: Wed Feb 09 17:29:53 2011
#      by: PyQt4 UI code generator 4.5.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(544, 705)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.mapArea = QtGui.QMdiArea(self.centralwidget)
        self.mapArea.setObjectName("mapArea")
        self.gridLayout.addWidget(self.mapArea, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 544, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuWindows = QtGui.QMenu(self.menubar)
        self.menuWindows.setObjectName("menuWindows")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionTile = QtGui.QAction(MainWindow)
        self.actionTile.setObjectName("actionTile")
        self.actionLink = QtGui.QAction(MainWindow)
        self.actionLink.setObjectName("actionLink")
        self.actionStart_editing = QtGui.QAction(MainWindow)
        self.actionStart_editing.setObjectName("actionStart_editing")
        self.actionAdd_new_window = QtGui.QAction(MainWindow)
        self.actionAdd_new_window.setObjectName("actionAdd_new_window")
        self.menuWindows.addAction(self.actionAdd_new_window)
        self.menuWindows.addAction(self.actionTile)
        self.menuEdit.addAction(self.actionStart_editing)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuWindows.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuWindows.setTitle(QtGui.QApplication.translate("MainWindow", "Windows", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Add new window", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTile.setText(QtGui.QApplication.translate("MainWindow", "Tile", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLink.setText(QtGui.QApplication.translate("MainWindow", "Link", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStart_editing.setText(QtGui.QApplication.translate("MainWindow", "Start editing", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_new_window.setText(QtGui.QApplication.translate("MainWindow", "Add new window", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_new_window.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+W", None, QtGui.QApplication.UnicodeUTF8))

