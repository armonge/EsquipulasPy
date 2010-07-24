# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'articulos.ui'
#
# Created: Wed Jul 14 18:23:45 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmArticlesNew(object):
    def setupUi(self, frmArticlesNew):
        frmArticlesNew.setObjectName("frmArticlesNew")
        frmArticlesNew.resize(581, 375)
        self.horizontalLayout = QtGui.QHBoxLayout(frmArticlesNew)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_5 = QtGui.QLabel(frmArticlesNew)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.categoriesview = QtGui.QTreeView(frmArticlesNew)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.categoriesview.sizePolicy().hasHeightForWidth())
        self.categoriesview.setSizePolicy(sizePolicy)
        self.categoriesview.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.categoriesview.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.categoriesview.setObjectName("categoriesview")
        self.verticalLayout_2.addWidget(self.categoriesview)
        self.label_6 = QtGui.QLabel(frmArticlesNew)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.brandsview = QtGui.QListView(frmArticlesNew)
        self.brandsview.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.brandsview.setObjectName("brandsview")
        self.verticalLayout_2.addWidget(self.brandsview)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(frmArticlesNew)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.txtComission = QtGui.QLineEdit(frmArticlesNew)
        self.txtComission.setObjectName("txtComission")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.txtComission)
        self.label_3 = QtGui.QLabel(frmArticlesNew)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.txtISC = QtGui.QLineEdit(frmArticlesNew)
        self.txtISC.setObjectName("txtISC")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.txtISC)
        self.label_2 = QtGui.QLabel(frmArticlesNew)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.txtDAI = QtGui.QLineEdit(frmArticlesNew)
        self.txtDAI.setObjectName("txtDAI")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.txtDAI)
        self.label_4 = QtGui.QLabel(frmArticlesNew)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.txtProfit = QtGui.QLineEdit(frmArticlesNew)
        self.txtProfit.setObjectName("txtProfit")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.txtProfit)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(frmArticlesNew)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(frmArticlesNew)
        QtCore.QMetaObject.connectSlotsByName(frmArticlesNew)

    def retranslateUi(self, frmArticlesNew):
        frmArticlesNew.setWindowTitle(QtGui.QApplication.translate("frmArticlesNew", "Añadir Articulos", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("frmArticlesNew", "Categoria", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("frmArticlesNew", "Marca", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmArticlesNew", "Comisión", None, QtGui.QApplication.UnicodeUTF8))
        self.txtComission.setText(QtGui.QApplication.translate("frmArticlesNew", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("frmArticlesNew", "ISC", None, QtGui.QApplication.UnicodeUTF8))
        self.txtISC.setText(QtGui.QApplication.translate("frmArticlesNew", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("frmArticlesNew", "DAI", None, QtGui.QApplication.UnicodeUTF8))
        self.txtDAI.setText(QtGui.QApplication.translate("frmArticlesNew", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("frmArticlesNew", "Ganancia", None, QtGui.QApplication.UnicodeUTF8))
        self.txtProfit.setText(QtGui.QApplication.translate("frmArticlesNew", "0", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmArticlesNew = QtGui.QDialog()
    ui = Ui_frmArticlesNew()
    ui.setupUi(frmArticlesNew)
    frmArticlesNew.show()
    sys.exit(app.exec_())

