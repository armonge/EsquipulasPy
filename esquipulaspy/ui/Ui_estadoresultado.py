# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\workspace\EsquipulasPy\src\ui\estadoresultado.ui'
#
# Created: Wed Jul 21 13:33:05 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmEstadoResultado(object):
    def setupUi(self, FrmEstadoResultado):
        FrmEstadoResultado.setObjectName("frmEstadoResultado")
        FrmEstadoResultado.resize(800, 600)
        self.centralwidget = QtGui.QWidget(FrmEstadoResultado)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.dtPicker = QtGui.QDateTimeEdit(self.centralwidget)
        self.dtPicker.setAlignment(QtCore.Qt.AlignCenter)
        self.dtPicker.setObjectName("dtPicker")
        self.verticalLayout_2.addWidget(self.dtPicker)
        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtGui.QSplitter(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.groupBox_3 = QtGui.QGroupBox(self.splitter)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 240))
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabledetails = QtGui.QTableView(self.groupBox_3)
        self.tabledetails.setObjectName("tabledetails")
        self.verticalLayout.addWidget(self.tabledetails)
        self.verticalLayout_2.addWidget(self.splitter_2)
        FrmEstadoResultado.setCentralWidget(self.centralwidget)
        self.toolBar = QtGui.QToolBar(FrmEstadoResultado)
        self.toolBar.setObjectName("toolBar")
        FrmEstadoResultado.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)

        self.retranslateUi(FrmEstadoResultado)
        QtCore.QMetaObject.connectSlotsByName(FrmEstadoResultado)

    def retranslateUi(self, FrmEstadoResultado):
        FrmEstadoResultado.setWindowTitle(QtGui.QApplication.translate("frmEstadoResultado", "Estado de Resultados", None, QtGui.QApplication.UnicodeUTF8))
        self.dtPicker.setDisplayFormat(QtGui.QApplication.translate("frmEstadoResultado", "MMMM yyyy", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("frmEstadoResultado", "Estado de Resultado", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("frmEstadoResultado", "toolBar", None, QtGui.QApplication.UnicodeUTF8))

import res_rc
