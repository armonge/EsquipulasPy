# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/marcos/workspace/EsquipulasPy/src/ui/cierre.ui'
#
# Created by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmCierreContable(object):
    def setupUi(self, FrmCierreContable):
        FrmCierreContable.setObjectName("frmCierreContable")
        FrmCierreContable.resize(828, 623)
        FrmCierreContable.setStyleSheet("None")
        self.centralwidget = QtGui.QWidget(FrmCierreContable)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.lbltitulo = QtGui.QLabel(self.centralwidget)
        self.lbltitulo.setFrameShape(QtGui.QFrame.NoFrame)
        self.lbltitulo.setScaledContents(False)
        self.lbltitulo.setAlignment(QtCore.Qt.AlignCenter)
        self.lbltitulo.setObjectName("lbltitulo")
        self.gridLayout.addWidget(self.lbltitulo, 0, 0, 1, 1)
        self.dtPicker = QtGui.QDateTimeEdit(self.centralwidget)
        self.dtPicker.setAlignment(QtCore.Qt.AlignCenter)
        self.dtPicker.setObjectName("dtPicker")
        self.gridLayout.addWidget(self.dtPicker, 1, 0, 1, 1)
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
        self.gridLayout.addWidget(self.splitter_2, 2, 0, 1, 1)
        FrmCierreContable.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(FrmCierreContable)
        self.statusbar.setObjectName("statusbar")
        FrmCierreContable.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(FrmCierreContable)
        self.toolBar.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar.setObjectName("toolBar")
        FrmCierreContable.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.actionSave = QtGui.QAction(FrmCierreContable)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/document-save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon)
        self.actionSave.setObjectName("actionSave")

        self.retranslateUi(FrmCierreContable)
        QtCore.QMetaObject.connectSlotsByName(FrmCierreContable)

    def retranslateUi(self, FrmCierreContable):
        FrmCierreContable.setWindowTitle(QtGui.QApplication.translate("frmCierreContable", "Cierre Contable", None, QtGui.QApplication.UnicodeUTF8))
        self.lbltitulo.setText(QtGui.QApplication.translate("frmCierreContable", "<h2><b>Documentos pertenecientes a cierre contable Mensual", None, QtGui.QApplication.UnicodeUTF8))
        self.dtPicker.setDisplayFormat(QtGui.QApplication.translate("frmCierreContable", "MMMM yyyy", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("frmCierreContable", "Estado de Resultado", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("frmCierreContable", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("frmCierreContable", "save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setToolTip(QtGui.QApplication.translate("frmCierreContable", "Guardar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("frmCierreContable", "Ctrl+G", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    FrmCierreContable = QtGui.QMainWindow()
    ui = Ui_frmCierreContable()
    ui.setupUi(FrmCierreContable)
    FrmCierreContable.show()
    sys.exit(app.exec_())

