# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/armonge/workspace/EsquipulasPy/src/ui/frmApertura.ui'
#
# Created: Mon Jun 21 20:19:47 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmApertura(object):
    def setupUi(self, frmApertura):
        frmApertura.setObjectName("frmApertura")
        frmApertura.setWindowModality(QtCore.Qt.ApplicationModal)
        frmApertura.resize(237, 245)
        self.txtMonto = QtGui.QDoubleSpinBox(frmApertura)
        self.txtMonto.setGeometry(QtCore.QRect(60, 100, 161, 22))
        self.txtMonto.setDecimals(4)
        self.txtMonto.setMaximum(1000000000.0)
        self.txtMonto.setObjectName("txtMonto")
        self.label = QtGui.QLabel(frmApertura)
        self.label.setGeometry(QtCore.QRect(10, 70, 31, 16))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(frmApertura)
        self.label_2.setGeometry(QtCore.QRect(10, 100, 41, 16))
        self.label_2.setObjectName("label_2")
        self.label_4 = QtGui.QLabel(frmApertura)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 41, 16))
        self.label_4.setObjectName("label_4")
        self.txtUsuario = QtGui.QLineEdit(frmApertura)
        self.txtUsuario.setGeometry(QtCore.QRect(60, 10, 161, 20))
        self.txtUsuario.setReadOnly(False)
        self.txtUsuario.setObjectName("txtUsuario")
        self.label_3 = QtGui.QLabel(frmApertura)
        self.label_3.setGeometry(QtCore.QRect(10, 40, 41, 16))
        self.label_3.setObjectName("label_3")
        self.cboCaja = QtGui.QComboBox(frmApertura)
        self.cboCaja.setGeometry(QtCore.QRect(60, 70, 161, 22))
        self.cboCaja.setObjectName("cboCaja")
        self.dtFechaTime = QtGui.QDateTimeEdit(frmApertura)
        self.dtFechaTime.setGeometry(QtCore.QRect(60, 40, 161, 22))
        self.dtFechaTime.setObjectName("dtFechaTime")
        self.groupBox = QtGui.QGroupBox(frmApertura)
        self.groupBox.setGeometry(QtCore.QRect(0, 130, 231, 80))
        self.groupBox.setObjectName("groupBox")
        self.txtUser = QtGui.QLineEdit(self.groupBox)
        self.txtUser.setGeometry(QtCore.QRect(80, 20, 141, 20))
        self.txtUser.setReadOnly(False)
        self.txtUser.setObjectName("txtUser")
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 20, 41, 16))
        self.label_5.setObjectName("label_5")
        self.txtPassword = QtGui.QLineEdit(self.groupBox)
        self.txtPassword.setGeometry(QtCore.QRect(80, 50, 141, 20))
        self.txtPassword.setReadOnly(False)
        self.txtPassword.setObjectName("txtPassword")
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 50, 61, 16))
        self.label_6.setObjectName("label_6")
        self.buttonBox = QtGui.QDialogButtonBox(frmApertura)
        self.buttonBox.setGeometry(QtCore.QRect(70, 210, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(frmApertura)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), frmApertura.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), frmApertura.reject)
        QtCore.QMetaObject.connectSlotsByName(frmApertura)
        frmApertura.setTabOrder(self.txtUsuario, self.dtFechaTime)
        frmApertura.setTabOrder(self.dtFechaTime, self.cboCaja)
        frmApertura.setTabOrder(self.cboCaja, self.txtMonto)
        frmApertura.setTabOrder(self.txtMonto, self.buttonBox)

    def retranslateUi(self, frmApertura):
        frmApertura.setWindowTitle(QtGui.QApplication.translate("frmApertura", "Apertura de Caja", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmApertura", "Caja", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("frmApertura", "Monto", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("frmApertura", "Usuario", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("frmApertura", "Fecha", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("frmApertura", "Autorizacion", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("frmApertura", "Usuario", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("frmApertura", "Contraseña", None, QtGui.QApplication.UnicodeUTF8))

