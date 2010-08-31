# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/articulos.ui'
#
# Created by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmArticlesNew(object):
    def setupUi(self, frmArticlesNew):
        frmArticlesNew.setObjectName("frmArticlesNew")
        frmArticlesNew.resize(702, 338)
        self.gridLayout = QtGui.QGridLayout(frmArticlesNew)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtGui.QLabel(frmArticlesNew)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtGui.QLabel(frmArticlesNew)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.btnAgregarMarca = QtGui.QPushButton(frmArticlesNew)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAgregarMarca.sizePolicy().hasHeightForWidth())
        self.btnAgregarMarca.setSizePolicy(sizePolicy)
        self.btnAgregarMarca.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/list-add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAgregarMarca.setIcon(icon)
        self.btnAgregarMarca.setObjectName("btnAgregarMarca")
        self.horizontalLayout_3.addWidget(self.btnAgregarMarca)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(frmArticlesNew)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.label_3 = QtGui.QLabel(frmArticlesNew)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_2 = QtGui.QLabel(frmArticlesNew)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(0, QtGui.QFormLayout.LabelRole, spacerItem)
        self.label_4 = QtGui.QLabel(frmArticlesNew)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.sbComission = QtGui.QDoubleSpinBox(frmArticlesNew)
        self.sbComission.setMinimumSize(QtCore.QSize(88, 0))
        self.sbComission.setObjectName("sbComission")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.sbComission)
        self.sbProfit = QtGui.QDoubleSpinBox(frmArticlesNew)
        self.sbProfit.setMinimumSize(QtCore.QSize(88, 0))
        self.sbProfit.setObjectName("sbProfit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.sbProfit)
        self.sbISC = QtGui.QDoubleSpinBox(frmArticlesNew)
        self.sbISC.setMinimumSize(QtCore.QSize(88, 0))
        self.sbISC.setObjectName("sbISC")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.sbISC)
        self.sbDAI = QtGui.QDoubleSpinBox(frmArticlesNew)
        self.sbDAI.setMinimumSize(QtCore.QSize(88, 0))
        self.sbDAI.setObjectName("sbDAI")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.sbDAI)
        self.gridLayout.addLayout(self.formLayout, 0, 2, 2, 1)
        self.categoriesview = QtGui.QTreeView(frmArticlesNew)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.categoriesview.sizePolicy().hasHeightForWidth())
        self.categoriesview.setSizePolicy(sizePolicy)
        self.categoriesview.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.categoriesview.setAlternatingRowColors(True)
        self.categoriesview.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.categoriesview.setObjectName("categoriesview")
        self.gridLayout.addWidget(self.categoriesview, 1, 0, 1, 1)
        self.brandsview = QtGui.QListView(frmArticlesNew)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.brandsview.sizePolicy().hasHeightForWidth())
        self.brandsview.setSizePolicy(sizePolicy)
        self.brandsview.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.brandsview.setAlternatingRowColors(True)
        self.brandsview.setObjectName("brandsview")
        self.gridLayout.addWidget(self.brandsview, 1, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_7 = QtGui.QLabel(frmArticlesNew)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)
        self.txtCategorySearch = QtGui.QLineEdit(frmArticlesNew)
        self.txtCategorySearch.setObjectName("txtCategorySearch")
        self.horizontalLayout.addWidget(self.txtCategorySearch)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_8 = QtGui.QLabel(frmArticlesNew)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.txtBrandSearch = QtGui.QLineEdit(frmArticlesNew)
        self.txtBrandSearch.setObjectName("txtBrandSearch")
        self.horizontalLayout_2.addWidget(self.txtBrandSearch)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(frmArticlesNew)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 2, 1, 1)
        self.label_7.setBuddy(self.txtCategorySearch)
        self.label_8.setBuddy(self.txtBrandSearch)

        self.retranslateUi(frmArticlesNew)
        QtCore.QMetaObject.connectSlotsByName(frmArticlesNew)
        frmArticlesNew.setTabOrder(self.categoriesview, self.brandsview)
        frmArticlesNew.setTabOrder(self.brandsview, self.btnAgregarMarca)
        frmArticlesNew.setTabOrder(self.btnAgregarMarca, self.txtCategorySearch)
        frmArticlesNew.setTabOrder(self.txtCategorySearch, self.txtBrandSearch)
        frmArticlesNew.setTabOrder(self.txtBrandSearch, self.buttonBox)

    def retranslateUi(self, frmArticlesNew):
        frmArticlesNew.setWindowTitle(QtGui.QApplication.translate("frmArticlesNew", "Añadir Articulos", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("frmArticlesNew", "<b>Categoria</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("frmArticlesNew", "<b>Marca</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAgregarMarca.setToolTip(QtGui.QApplication.translate("frmArticlesNew", "Agregar Marca", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmArticlesNew", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Comisión</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("frmArticlesNew", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">ISC</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("frmArticlesNew", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">DAI</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("frmArticlesNew", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Ganancia</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.sbComission.setPrefix(QtGui.QApplication.translate("frmArticlesNew", "US$ ", None, QtGui.QApplication.UnicodeUTF8))
        self.sbProfit.setSuffix(QtGui.QApplication.translate("frmArticlesNew", " %", None, QtGui.QApplication.UnicodeUTF8))
        self.sbISC.setSuffix(QtGui.QApplication.translate("frmArticlesNew", " %", None, QtGui.QApplication.UnicodeUTF8))
        self.sbDAI.setSuffix(QtGui.QApplication.translate("frmArticlesNew", " %", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("frmArticlesNew", "Buscar", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("frmArticlesNew", "Buscar", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmArticlesNew = QtGui.QDialog()
    ui = Ui_frmArticlesNew()
    ui.setupUi(frmArticlesNew)
    frmArticlesNew.show()
    sys.exit(app.exec_())

