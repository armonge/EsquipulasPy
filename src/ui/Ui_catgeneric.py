# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/marcos/workspace/EsquipulasPy/src/ui/catgeneric.ui'
#
# Created: Wed Jul 28 00:27:02 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmCatGeneric(object):
    def setupUi(self, frmCatGeneric):
        frmCatGeneric.setObjectName("frmCatGeneric")
        frmCatGeneric.resize(800, 587)
        self.centralwidget = QtGui.QWidget(frmCatGeneric)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tableview = QtGui.QTableView(self.centralwidget)
        self.tableview.setSizeIncrement(QtCore.QSize(0, 2))
        self.tableview.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tableview.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableview.setAlternatingRowColors(True)
        self.tableview.setSortingEnabled(True)
        self.tableview.setObjectName("tableview")
        self.tableview.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.tableview, 0, 0, 1, 2)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.txtSearch = QtGui.QLineEdit(self.centralwidget)
        self.txtSearch.setObjectName("txtSearch")
        self.gridLayout.addWidget(self.txtSearch, 1, 1, 1, 1)
        frmCatGeneric.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(frmCatGeneric)
        self.statusbar.setObjectName("statusbar")
        frmCatGeneric.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(frmCatGeneric)
        self.toolBar.setObjectName("toolBar")
        frmCatGeneric.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.actionNew = QtGui.QAction(frmCatGeneric)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/document-new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtGui.QAction(frmCatGeneric)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/res/document-save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon1)
        self.actionSave.setVisible(True)
        self.actionSave.setObjectName("actionSave")
        self.actionEdit = QtGui.QAction(frmCatGeneric)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/res/document-edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEdit.setIcon(icon2)
        self.actionEdit.setVisible(False)
        self.actionEdit.setObjectName("actionEdit")
        self.actionDelete = QtGui.QAction(frmCatGeneric)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/res/edit-delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon3)
        self.actionDelete.setObjectName("actionDelete")
        self.actionCancel = QtGui.QAction(frmCatGeneric)
        self.actionCancel.setEnabled(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/res/dialog-cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCancel.setIcon(icon4)
        self.actionCancel.setVisible(True)
        self.actionCancel.setObjectName("actionCancel")
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionEdit)
        self.toolBar.addAction(self.actionCancel)
        self.label.setBuddy(self.txtSearch)

        self.retranslateUi(frmCatGeneric)
        QtCore.QMetaObject.connectSlotsByName(frmCatGeneric)

    def retranslateUi(self, frmCatGeneric):
        frmCatGeneric.setWindowTitle(QtGui.QApplication.translate("frmCatGeneric", "Catalogo Generico", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmCatGeneric", "&Buscar", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("frmCatGeneric", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setText(QtGui.QApplication.translate("frmCatGeneric", "Nuevo", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setShortcut(QtGui.QApplication.translate("frmCatGeneric", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("frmCatGeneric", "Guardar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("frmCatGeneric", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit.setText(QtGui.QApplication.translate("frmCatGeneric", "Editar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit.setShortcut(QtGui.QApplication.translate("frmCatGeneric", "F2", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete.setText(QtGui.QApplication.translate("frmCatGeneric", "Borrar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCancel.setText(QtGui.QApplication.translate("frmCatGeneric", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmCatGeneric = QtGui.QMainWindow()
    ui = Ui_frmCatGeneric()
    ui.setupUi(frmCatGeneric)
    frmCatGeneric.show()
    sys.exit(app.exec_())

