# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'products.ui'
#
# Created: Wed Jul 14 17:10:38 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmProducts(object):
    def setupUi(self, frmProducts):
        frmProducts.setObjectName("frmProducts")
        frmProducts.resize(262, 292)
        self.centralwidget = QtGui.QWidget(frmProducts)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.txtComission = QtGui.QLineEdit(self.centralwidget)
        self.txtComission.setObjectName("txtComission")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.txtComission)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.txtISC = QtGui.QLineEdit(self.centralwidget)
        self.txtISC.setObjectName("txtISC")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.txtISC)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.txtDAI_2 = QtGui.QLineEdit(self.centralwidget)
        self.txtDAI_2.setObjectName("txtDAI_2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.txtDAI_2)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.txtProfit = QtGui.QLineEdit(self.centralwidget)
        self.txtProfit.setObjectName("txtProfit")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.txtProfit)
        self.verticalLayout.addLayout(self.formLayout)
        self.columnView = QtGui.QColumnView(self.centralwidget)
        self.columnView.setObjectName("columnView")
        self.verticalLayout.addWidget(self.columnView)
        self.buttonBox = QtGui.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        frmProducts.setCentralWidget(self.centralwidget)
        self.toolBar = QtGui.QToolBar(frmProducts)
        self.toolBar.setObjectName("toolBar")
        frmProducts.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)

        self.retranslateUi(frmProducts)
        QtCore.QMetaObject.connectSlotsByName(frmProducts)

    def retranslateUi(self, frmProducts):
        frmProducts.setWindowTitle(QtGui.QApplication.translate("frmProducts", "Añadir Articulos", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmProducts", "Comisión", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("frmProducts", "ISC", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("frmProducts", "DAI", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("frmProducts", "Ganancia", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("frmProducts", "toolBar", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmProducts = QtGui.QMainWindow()
    ui = Ui_frmProducts()
    ui.setupUi(frmProducts)
    frmProducts.show()
    sys.exit(app.exec_())

