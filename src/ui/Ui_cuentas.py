# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/cuentas.ui'
#
# Created: Thu Aug  5 12:56:05 2010
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmAccounts(object):
    def setupUi(self, frmAccounts):
        frmAccounts.setObjectName("frmAccounts")
        frmAccounts.resize(800, 600)
        self.centralwidget = QtGui.QWidget(frmAccounts)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.accountsTree = QtGui.QTreeView(self.centralwidget)
        self.accountsTree.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.accountsTree.setObjectName("accountsTree")
        self.gridLayout.addWidget(self.accountsTree, 0, 0, 1, 3)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setIndent(15)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.txtSearch = QtGui.QLineEdit(self.centralwidget)
        self.txtSearch.setObjectName("txtSearch")
        self.gridLayout.addWidget(self.txtSearch, 1, 1, 1, 1)
        self.btnAdd = QtGui.QPushButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/list-add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAdd.setIcon(icon)
        self.btnAdd.setObjectName("btnAdd")
        self.gridLayout.addWidget(self.btnAdd, 1, 2, 1, 1)
        frmAccounts.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(frmAccounts)
        self.statusbar.setObjectName("statusbar")
        frmAccounts.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(frmAccounts)
        self.toolBar.setObjectName("toolBar")
        frmAccounts.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.label.setBuddy(self.txtSearch)

        self.retranslateUi(frmAccounts)
        QtCore.QMetaObject.connectSlotsByName(frmAccounts)

    def retranslateUi(self, frmAccounts):
        frmAccounts.setWindowTitle(QtGui.QApplication.translate("frmAccounts", "Cuentas Contables", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmAccounts", "&Buscar:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAdd.setText(QtGui.QApplication.translate("frmAccounts", "&Añadir", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("frmAccounts", "toolBar", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmAccounts = QtGui.QMainWindow()
    ui = Ui_frmAccounts()
    ui.setupUi(frmAccounts)
    frmAccounts.show()
    sys.exit(app.exec_())

