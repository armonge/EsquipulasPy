# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\workspace\EsquipulasPy\src\inventario\subcategorias.ui'
#
# Created: Wed Jun 02 23:38:40 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmSubcategorias(object):
    def setupUi(self, frmSubcategorias):
        frmSubcategorias.setObjectName("frmSubcategorias")
        frmSubcategorias.resize(442, 125)
        self.cboCategoria = QtGui.QComboBox(frmSubcategorias)
        self.cboCategoria.setGeometry(QtCore.QRect(90, 20, 341, 22))
        self.cboCategoria.setObjectName("cboCategoria")
        self.label_2 = QtGui.QLabel(frmSubcategorias)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(frmSubcategorias)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.txtSubcategoria = QtGui.QLineEdit(frmSubcategorias)
        self.txtSubcategoria.setGeometry(QtCore.QRect(90, 60, 341, 20))
        self.txtSubcategoria.setObjectName("txtSubcategoria")
        self.btnCancelar = QtGui.QPushButton(frmSubcategorias)
        self.btnCancelar.setGeometry(QtCore.QRect(400, 90, 31, 31))
        self.btnCancelar.setStyleSheet("background-image: url(:/icons/res/edit-delete.png);\n"
"background-repeat:no-repeat;")
        self.btnCancelar.setText("")
        self.btnCancelar.setFlat(True)
        self.btnCancelar.setObjectName("btnCancelar")
        self.btnAceptar = QtGui.QPushButton(frmSubcategorias)
        self.btnAceptar.setGeometry(QtCore.QRect(360, 90, 31, 31))
        self.btnAceptar.setStyleSheet("background-image: url(:/icons/res/document-save.png);\n"
"background-repeat:no-repeat;")
        self.btnAceptar.setText("")
        self.btnAceptar.setFlat(True)
        self.btnAceptar.setObjectName("btnAceptar")

        self.retranslateUi(frmSubcategorias)
        QtCore.QMetaObject.connectSlotsByName(frmSubcategorias)

    def retranslateUi(self, frmSubcategorias):
        frmSubcategorias.setWindowTitle(QtGui.QApplication.translate("frmSubcategorias", "Nueva Subcategoria", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("frmSubcategorias", "Categoria", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("frmSubcategorias", "Subcategoria", None, QtGui.QApplication.UnicodeUTF8))

import res_rc
