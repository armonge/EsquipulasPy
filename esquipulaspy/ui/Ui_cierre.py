# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Workspace\EsquipulasPy\esquipulaspy\ui\cierre.ui'
#
# Created: Tue Oct 19 00:11:03 2010
#      by: PyQt4 UI code generator 4.7.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmCierreContable(object):
    def setupUi(self, frmCierreContable):
        frmCierreContable.setObjectName(_fromUtf8("frmCierreContable"))
        frmCierreContable.resize(828, 623)
        frmCierreContable.setStyleSheet(_fromUtf8(""))
        self.centralwidget = QtGui.QWidget(frmCierreContable)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lbltitulo = QtGui.QLabel(self.centralwidget)
        self.lbltitulo.setFrameShape(QtGui.QFrame.NoFrame)
        self.lbltitulo.setScaledContents(False)
        self.lbltitulo.setAlignment(QtCore.Qt.AlignCenter)
        self.lbltitulo.setObjectName(_fromUtf8("lbltitulo"))
        self.gridLayout.addWidget(self.lbltitulo, 0, 0, 1, 1)
        self.dtPicker = QtGui.QDateTimeEdit(self.centralwidget)
        self.dtPicker.setAlignment(QtCore.Qt.AlignCenter)
        self.dtPicker.setCurrentSection(QtGui.QDateTimeEdit.MonthSection)
        self.dtPicker.setObjectName(_fromUtf8("dtPicker"))
        self.gridLayout.addWidget(self.dtPicker, 1, 0, 1, 1)
        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.splitter = QtGui.QSplitter(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.groupBox_3 = QtGui.QGroupBox(self.splitter)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 240))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabledetails = QtGui.QTableView(self.groupBox_3)
        self.tabledetails.setObjectName(_fromUtf8("tabledetails"))
        self.verticalLayout.addWidget(self.tabledetails)
        self.gridLayout.addWidget(self.splitter_2, 2, 0, 1, 1)
        frmCierreContable.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(frmCierreContable)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        frmCierreContable.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(frmCierreContable)
        self.toolBar.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        frmCierreContable.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.actionSave = QtGui.QAction(frmCierreContable)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/res/document-save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))

        self.retranslateUi(frmCierreContable)
        QtCore.QMetaObject.connectSlotsByName(frmCierreContable)

    def retranslateUi(self, frmCierreContable):
        frmCierreContable.setWindowTitle(QtGui.QApplication.translate("frmCierreContable", "Cierre Contable", None, QtGui.QApplication.UnicodeUTF8))
        self.lbltitulo.setText(QtGui.QApplication.translate("frmCierreContable", "<h2><b>Documentos pertenecientes a cierre contable", None, QtGui.QApplication.UnicodeUTF8))
        self.dtPicker.setDisplayFormat(QtGui.QApplication.translate("frmCierreContable", "MMMM yyyy", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("frmCierreContable", "Cierre Contable", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("frmCierreContable", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("frmCierreContable", "save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setToolTip(QtGui.QApplication.translate("frmCierreContable", "Guardar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("frmCierreContable", "Ctrl+G", None, QtGui.QApplication.UnicodeUTF8))

import res_rc
