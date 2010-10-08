# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/catgeneric.ui'
#
# Created: Mon Oct  4 22:38:07 2010
#      by: PyQt4 UI code generator 4.7.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FrmCatGeneric(object):
    def setupUi(self, FrmCatGeneric):
        FrmCatGeneric.setObjectName(_fromUtf8("FrmCatGeneric"))
        FrmCatGeneric.resize(800, 587)
        self.centralwidget = QtGui.QWidget(FrmCatGeneric)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tableview = QtGui.QTableView(self.centralwidget)
        self.tableview.setSizeIncrement(QtCore.QSize(0, 2))
        self.tableview.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tableview.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableview.setAlternatingRowColors(True)
        self.tableview.setSortingEnabled(True)
        self.tableview.setObjectName(_fromUtf8("tableview"))
        self.tableview.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.tableview, 0, 0, 1, 2)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.txtSearch = QtGui.QLineEdit(self.centralwidget)
        self.txtSearch.setObjectName(_fromUtf8("txtSearch"))
        self.gridLayout.addWidget(self.txtSearch, 1, 1, 1, 1)
        FrmCatGeneric.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(FrmCatGeneric)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        FrmCatGeneric.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(FrmCatGeneric)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        FrmCatGeneric.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.actionNew = QtGui.QAction(FrmCatGeneric)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/res/document-new.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionSave = QtGui.QAction(FrmCatGeneric)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/res/document-save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon1)
        self.actionSave.setVisible(True)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionEdit = QtGui.QAction(FrmCatGeneric)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/res/document-edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEdit.setIcon(icon2)
        self.actionEdit.setVisible(False)
        self.actionEdit.setObjectName(_fromUtf8("actionEdit"))
        self.actionDelete = QtGui.QAction(FrmCatGeneric)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/res/edit-delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon3)
        self.actionDelete.setObjectName(_fromUtf8("actionDelete"))
        self.actionCancel = QtGui.QAction(FrmCatGeneric)
        self.actionCancel.setEnabled(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/res/dialog-cancel.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCancel.setIcon(icon4)
        self.actionCancel.setVisible(True)
        self.actionCancel.setObjectName(_fromUtf8("actionCancel"))
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionEdit)
        self.toolBar.addAction(self.actionCancel)
        self.label.setBuddy(self.txtSearch)

        self.retranslateUi(FrmCatGeneric)
        QtCore.QMetaObject.connectSlotsByName(FrmCatGeneric)

    def retranslateUi(self, FrmCatGeneric):
        FrmCatGeneric.setWindowTitle(QtGui.QApplication.translate("FrmCatGeneric", "Catalogo Generico", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FrmCatGeneric", "&Buscar", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("FrmCatGeneric", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setText(QtGui.QApplication.translate("FrmCatGeneric", "Nuevo", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setShortcut(QtGui.QApplication.translate("FrmCatGeneric", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("FrmCatGeneric", "Guardar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("FrmCatGeneric", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit.setText(QtGui.QApplication.translate("FrmCatGeneric", "Editar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit.setShortcut(QtGui.QApplication.translate("FrmCatGeneric", "F2", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete.setText(QtGui.QApplication.translate("FrmCatGeneric", "Borrar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCancel.setText(QtGui.QApplication.translate("FrmCatGeneric", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    FrmCatGeneric = QtGui.QMainWindow()
    ui = Ui_FrmCatGeneric()
    ui.setupUi(FrmCatGeneric)
    FrmCatGeneric.show()
    sys.exit(app.exec_())

