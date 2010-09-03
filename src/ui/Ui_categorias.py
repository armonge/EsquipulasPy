# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/categorias.ui'
#
# Created by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmCategorias(object):
    def setupUi(self, frmCategorias):
        frmCategorias.setObjectName("frmCategorias")
        frmCategorias.resize(465, 468)
        self.centralwidget = QtGui.QWidget(frmCategorias)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.view = QtGui.QTreeView(self.centralwidget)
        self.view.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.view.setAlternatingRowColors(True)
        self.view.setObjectName("view")
        self.gridLayout.addWidget(self.view, 0, 0, 1, 2)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.txtSearch = QtGui.QLineEdit(self.centralwidget)
        self.txtSearch.setObjectName("txtSearch")
        self.gridLayout.addWidget(self.txtSearch, 1, 1, 1, 1)
        frmCategorias.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(frmCategorias)
        self.statusbar.setObjectName("statusbar")
        frmCategorias.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(frmCategorias)
        self.toolBar.setObjectName("toolBar")
        frmCategorias.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.actionAdd = QtGui.QAction(frmCategorias)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/list-add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd.setIcon(icon)
        self.actionAdd.setObjectName("actionAdd")
        self.actionDelete = QtGui.QAction(frmCategorias)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/res/list-remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon1)
        self.actionDelete.setObjectName("actionDelete")
        self.actionEditar = QtGui.QAction(frmCategorias)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/res/document-edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEditar.setIcon(icon2)
        self.actionEditar.setObjectName("actionEditar")
        self.actionAddSub = QtGui.QAction(frmCategorias)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/res/format-add-node.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAddSub.setIcon(icon3)
        self.actionAddSub.setObjectName("actionAddSub")
        self.toolBar.addAction(self.actionAdd)
        self.toolBar.addAction(self.actionAddSub)
        self.toolBar.addAction(self.actionEditar)
        self.label.setBuddy(self.txtSearch)

        self.retranslateUi(frmCategorias)
        QtCore.QMetaObject.connectSlotsByName(frmCategorias)

    def retranslateUi(self, frmCategorias):
        frmCategorias.setWindowTitle(QtGui.QApplication.translate("frmCategorias", "Categorias", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmCategorias", "&Buscar", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("frmCategorias", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd.setText(QtGui.QApplication.translate("frmCategorias", "Añadir", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd.setToolTip(QtGui.QApplication.translate("frmCategorias", "Añadir Categoria", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd.setShortcut(QtGui.QApplication.translate("frmCategorias", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete.setText(QtGui.QApplication.translate("frmCategorias", "Borrar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditar.setText(QtGui.QApplication.translate("frmCategorias", "Editar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddSub.setText(QtGui.QApplication.translate("frmCategorias", "Añadir Subcategoria", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmCategorias = QtGui.QMainWindow()
    ui = Ui_frmCategorias()
    ui.setupUi(frmCategorias)
    frmCategorias.show()
    sys.exit(app.exec_())

