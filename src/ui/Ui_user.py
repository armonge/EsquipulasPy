# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/user.ui'
#
# Created: Sat Aug  7 17:54:01 2010
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dlgUserLogin(object):
    def setupUi(self, dlgUserLogin):
        dlgUserLogin.setObjectName("dlgUserLogin")
        dlgUserLogin.resize(519, 311)
        dlgUserLogin.setMinimumSize(QtCore.QSize(519, 311))
        dlgUserLogin.setMaximumSize(QtCore.QSize(519, 311))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dlgUserLogin.setWindowIcon(icon)
        dlgUserLogin.setStyleSheet(".QFrame{\n"
"    background-image: url(:/images/res/passwd-bg.png);\n"
"    background-repeat:no-repeat;\n"
"    margin:0;\n"
"    padding:0;\n"
"}\n"
"")
        self.horizontalLayout = QtGui.QHBoxLayout(dlgUserLogin)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtGui.QFrame(dlgUserLogin)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 5)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.txtUser = QtGui.QLineEdit(self.frame)
        self.txtUser.setObjectName("txtUser")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.txtUser)
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.txtPassword = QtGui.QLineEdit(self.frame)
        self.txtPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.txtPassword.setObjectName("txtPassword")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.txtPassword)
        self.gridLayout.addLayout(self.formLayout, 5, 3, 1, 1)
        self.buttonbox = QtGui.QDialogButtonBox(self.frame)
        self.buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonbox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonbox.setObjectName("buttonbox")
        self.gridLayout.addWidget(self.buttonbox, 7, 0, 1, 5)
        spacerItem = QtGui.QSpacerItem(60, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 6)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 6, 0, 1, 6)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 5, 4, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 5, 2, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 3, 0, 1, 6)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem6, 0, 0, 1, 6)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem7, 5, 5, 1, 1)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem8, 5, 1, 1, 1)
        spacerItem9 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem9, 8, 0, 1, 6)
        self.horizontalLayout.addWidget(self.frame)
        self.label_2.setBuddy(self.txtPassword)
        self.label_3.setBuddy(self.txtUser)

        self.retranslateUi(dlgUserLogin)
        QtCore.QObject.connect(self.buttonbox, QtCore.SIGNAL("accepted()"), dlgUserLogin.accept)
        QtCore.QObject.connect(self.buttonbox, QtCore.SIGNAL("rejected()"), dlgUserLogin.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgUserLogin)

    def retranslateUi(self, dlgUserLogin):
        dlgUserLogin.setWindowTitle(QtGui.QApplication.translate("dlgUserLogin", "Iniciar Sesión", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("dlgUserLogin", "Llantera Esquipulas", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("dlgUserLogin", "&Usuario", None, QtGui.QApplication.UnicodeUTF8))
        self.txtUser.setWhatsThis(QtGui.QApplication.translate("dlgUserLogin", "Escriba aca su usuario", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("dlgUserLogin", "&Contraseña", None, QtGui.QApplication.UnicodeUTF8))
        self.txtPassword.setWhatsThis(QtGui.QApplication.translate("dlgUserLogin", "Escriba aca su contraseña, tenga en cuenta que el sistema hace diferencia entre minusculas y mayusculas", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dlgUserLogin = QtGui.QDialog()
    ui = Ui_dlgUserLogin()
    ui.setupUi(dlgUserLogin)
    dlgUserLogin.show()
    sys.exit(app.exec_())

