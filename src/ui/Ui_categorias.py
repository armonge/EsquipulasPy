# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/categorias.ui'
#
# Created: Mon Oct  4 22:37:48 2010
#      by: PyQt4 UI code generator 4.7.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FrmCategorias(object):
    def setupUi(self, FrmCategorias):
        FrmCategorias.setObjectName(_fromUtf8("FrmCategorias"))
        FrmCategorias.resize(465, 468)
        self.centralwidget = QtGui.QWidget(FrmCategorias)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.view = QtGui.QTreeView(self.centralwidget)
        self.view.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.view.setAlternatingRowColors(True)
        self.view.setObjectName(_fromUtf8("view"))
        self.gridLayout.addWidget(self.view, 0, 0, 1, 2)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.txtSearch = QtGui.QLineEdit(self.centralwidget)
        self.txtSearch.setObjectName(_fromUtf8("txtSearch"))
        self.gridLayout.addWidget(self.txtSearch, 1, 1, 1, 1)
        FrmCategorias.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(FrmCategorias)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        FrmCategorias.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(FrmCategorias)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        FrmCategorias.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.actionAdd = QtGui.QAction(FrmCategorias)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/res/list-add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd.setIcon(icon)
        self.actionAdd.setObjectName(_fromUtf8("actionAdd"))
        self.actionDelete = QtGui.QAction(FrmCategorias)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/res/list-remove.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon1)
        self.actionDelete.setObjectName(_fromUtf8("actionDelete"))
        self.actionEditar = QtGui.QAction(FrmCategorias)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/res/document-edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEditar.setIcon(icon2)
        self.actionEditar.setObjectName(_fromUtf8("actionEditar"))
        self.actionAddSub = QtGui.QAction(FrmCategorias)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/res/format-add-node.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAddSub.setIcon(icon3)
        self.actionAddSub.setObjectName(_fromUtf8("actionAddSub"))
        self.toolBar.addAction(self.actionAdd)
        self.toolBar.addAction(self.actionAddSub)
        self.toolBar.addAction(self.actionEditar)
        self.label.setBuddy(self.txtSearch)

        self.retranslateUi(FrmCategorias)
        QtCore.QMetaObject.connectSlotsByName(FrmCategorias)

    def retranslateUi(self, FrmCategorias):
        FrmCategorias.setWindowTitle(QtGui.QApplication.translate("FrmCategorias", "Categorias", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FrmCategorias", "&Buscar", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("FrmCategorias", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd.setText(QtGui.QApplication.translate("FrmCategorias", "Añadir", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd.setToolTip(QtGui.QApplication.translate("FrmCategorias", "Añadir Categoria", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd.setShortcut(QtGui.QApplication.translate("FrmCategorias", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete.setText(QtGui.QApplication.translate("FrmCategorias", "Borrar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditar.setText(QtGui.QApplication.translate("FrmCategorias", "Editar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddSub.setText(QtGui.QApplication.translate("FrmCategorias", "Añadir Subcategoria", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    FrmCategorias = QtGui.QMainWindow()
    ui = Ui_FrmCategorias()
    ui.setupUi(FrmCategorias)
    FrmCategorias.show()
    sys.exit(app.exec_())

