# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/entradacompra.ui'
#
# Created: Mon Aug 23 02:21:25 2010
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmEntradaCompra(object):
    def setupUi(self, frmEntradaCompra):
        frmEntradaCompra.setObjectName("frmEntradaCompra")
        frmEntradaCompra.resize(828, 600)
        frmEntradaCompra.setStyleSheet("None")
        self.centralwidget = QtGui.QWidget(frmEntradaCompra)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.tabdetails = QtGui.QWidget()
        self.tabdetails.setObjectName("tabdetails")
        self.gridLayout_2 = QtGui.QGridLayout(self.tabdetails)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.txtDocumentNumber = QtGui.QLineEdit(self.tabdetails)
        self.txtDocumentNumber.setEnabled(True)
        self.txtDocumentNumber.setReadOnly(True)
        self.txtDocumentNumber.setObjectName("txtDocumentNumber")
        self.gridLayout_2.addWidget(self.txtDocumentNumber, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.tabdetails)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 5, 1, 1)
        self.dtPicker = QtGui.QDateTimeEdit(self.tabdetails)
        self.dtPicker.setEnabled(True)
        self.dtPicker.setReadOnly(True)
        self.dtPicker.setCalendarPopup(True)
        self.dtPicker.setObjectName("dtPicker")
        self.gridLayout_2.addWidget(self.dtPicker, 0, 6, 1, 1)
        self.tabledetails = QtGui.QTableView(self.tabdetails)
        self.tabledetails.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabledetails.sizePolicy().hasHeightForWidth())
        self.tabledetails.setSizePolicy(sizePolicy)
        self.tabledetails.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tabledetails.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tabledetails.setAlternatingRowColors(True)
        self.tabledetails.setSortingEnabled(True)
        self.tabledetails.setObjectName("tabledetails")
        self.tabledetails.horizontalHeader().setStretchLastSection(True)
        self.tabledetails.verticalHeader().setVisible(False)
        self.gridLayout_2.addWidget(self.tabledetails, 2, 0, 1, 7)
        self.groupBox_2 = QtGui.QGroupBox(self.tabdetails)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.txtObservations = QtGui.QPlainTextEdit(self.groupBox_2)
        self.txtObservations.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtObservations.sizePolicy().hasHeightForWidth())
        self.txtObservations.setSizePolicy(sizePolicy)
        self.txtObservations.setReadOnly(True)
        self.txtObservations.setObjectName("txtObservations")
        self.gridLayout_3.addWidget(self.txtObservations, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_2, 3, 0, 1, 5)
        self.groupBox = QtGui.QGroupBox(self.tabdetails)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignCenter)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_6 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_6)
        self.lblSubtotal = QtGui.QLabel(self.groupBox)
        self.lblSubtotal.setObjectName("lblSubtotal")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.lblSubtotal)
        self.label_8 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_8)
        self.lblIVA = QtGui.QLabel(self.groupBox)
        self.lblIVA.setObjectName("lblIVA")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.lblIVA)
        self.label_11 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_11)
        self.lblTotal = QtGui.QLabel(self.groupBox)
        self.lblTotal.setObjectName("lblTotal")
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.lblTotal)
        self.label_5 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_5)
        self.lblTotalD = QtGui.QLabel(self.groupBox)
        self.lblTotalD.setObjectName("lblTotalD")
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.lblTotalD)
        self.gridLayout_2.addWidget(self.groupBox, 3, 5, 1, 2)
        self.gbRadios = QtGui.QGroupBox(self.tabdetails)
        self.gbRadios.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbRadios.sizePolicy().hasHeightForWidth())
        self.gbRadios.setSizePolicy(sizePolicy)
        self.gbRadios.setFlat(False)
        self.gbRadios.setCheckable(False)
        self.gbRadios.setObjectName("gbRadios")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.gbRadios)
        self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.rbCash = QtGui.QRadioButton(self.gbRadios)
        self.rbCash.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbCash.sizePolicy().hasHeightForWidth())
        self.rbCash.setSizePolicy(sizePolicy)
        self.rbCash.setChecked(True)
        self.rbCash.setObjectName("rbCash")
        self.horizontalLayout_3.addWidget(self.rbCash)
        self.rbCredit = QtGui.QRadioButton(self.gbRadios)
        self.rbCredit.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbCredit.sizePolicy().hasHeightForWidth())
        self.rbCredit.setSizePolicy(sizePolicy)
        self.rbCredit.setObjectName("rbCredit")
        self.horizontalLayout_3.addWidget(self.rbCredit)
        self.rbCheck = QtGui.QRadioButton(self.gbRadios)
        self.rbCheck.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbCheck.sizePolicy().hasHeightForWidth())
        self.rbCheck.setSizePolicy(sizePolicy)
        self.rbCheck.setObjectName("rbCheck")
        self.horizontalLayout_3.addWidget(self.rbCheck)
        self.gridLayout_2.addWidget(self.gbRadios, 1, 5, 1, 2)
        self.label_3 = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.swProvider = QtGui.QStackedWidget(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.swProvider.sizePolicy().hasHeightForWidth())
        self.swProvider.setSizePolicy(sizePolicy)
        self.swProvider.setObjectName("swProvider")
        self.page = QtGui.QWidget()
        self.page.setObjectName("page")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.page)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cbProvider = QtGui.QComboBox(self.page)
        self.cbProvider.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbProvider.sizePolicy().hasHeightForWidth())
        self.cbProvider.setSizePolicy(sizePolicy)
        self.cbProvider.setEditable(True)
        self.cbProvider.setObjectName("cbProvider")
        self.horizontalLayout_2.addWidget(self.cbProvider)
        self.swProvider.addWidget(self.page)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.page_2)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.txtProvider = QtGui.QLineEdit(self.page_2)
        self.txtProvider.setEnabled(True)
        self.txtProvider.setReadOnly(True)
        self.txtProvider.setObjectName("txtProvider")
        self.horizontalLayout_5.addWidget(self.txtProvider)
        self.swProvider.addWidget(self.page_2)
        self.gridLayout_2.addWidget(self.swProvider, 1, 1, 1, 1)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/document-edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabdetails, icon, "")
        self.tabnavigation = QtGui.QWidget()
        self.tabnavigation.setObjectName("tabnavigation")
        self.verticalLayout = QtGui.QVBoxLayout(self.tabnavigation)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tablenavigation = QtGui.QTableView(self.tabnavigation)
        self.tablenavigation.setAlternatingRowColors(True)
        self.tablenavigation.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tablenavigation.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tablenavigation.setObjectName("tablenavigation")
        self.tablenavigation.horizontalHeader().setStretchLastSection(True)
        self.tablenavigation.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tablenavigation)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtGui.QLabel(self.tabnavigation)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.txtSearch = QtGui.QLineEdit(self.tabnavigation)
        self.txtSearch.setObjectName("txtSearch")
        self.horizontalLayout.addWidget(self.txtSearch)
        self.verticalLayout.addLayout(self.horizontalLayout)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/res/table.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabnavigation, icon1, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
        frmEntradaCompra.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(frmEntradaCompra)
        self.statusbar.setObjectName("statusbar")
        frmEntradaCompra.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(frmEntradaCompra)
        self.toolBar.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar.setObjectName("toolBar")
        frmEntradaCompra.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.toolBar.addSeparator()
        self.toolBar.addSeparator()
        self.label_2.setBuddy(self.txtDocumentNumber)
        self.label.setBuddy(self.dtPicker)
        self.label_3.setBuddy(self.txtProvider)
        self.label_4.setBuddy(self.txtSearch)

        self.retranslateUi(frmEntradaCompra)
        self.tabWidget.setCurrentIndex(1)
        self.swProvider.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(frmEntradaCompra)
        frmEntradaCompra.setTabOrder(self.txtDocumentNumber, self.txtProvider)
        frmEntradaCompra.setTabOrder(self.txtProvider, self.dtPicker)
        frmEntradaCompra.setTabOrder(self.dtPicker, self.tabledetails)
        frmEntradaCompra.setTabOrder(self.tabledetails, self.txtObservations)
        frmEntradaCompra.setTabOrder(self.txtObservations, self.tabWidget)
        frmEntradaCompra.setTabOrder(self.tabWidget, self.cbProvider)
        frmEntradaCompra.setTabOrder(self.cbProvider, self.tablenavigation)
        frmEntradaCompra.setTabOrder(self.tablenavigation, self.txtSearch)

    def retranslateUi(self, frmEntradaCompra):
        frmEntradaCompra.setWindowTitle(QtGui.QApplication.translate("frmEntradaCompra", "Entrada Compra", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("frmEntradaCompra", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\"># Compra:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmEntradaCompra", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Fecha:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("frmEntradaCompra", "Observaciones", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("frmEntradaCompra", "Subtotal: ", None, QtGui.QApplication.UnicodeUTF8))
        self.lblSubtotal.setText(QtGui.QApplication.translate("frmEntradaCompra", "0.00", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("frmEntradaCompra", "IVA: ", None, QtGui.QApplication.UnicodeUTF8))
        self.lblIVA.setText(QtGui.QApplication.translate("frmEntradaCompra", "0.00", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("frmEntradaCompra", "Total C$: ", None, QtGui.QApplication.UnicodeUTF8))
        self.lblTotal.setText(QtGui.QApplication.translate("frmEntradaCompra", "0.00", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("frmEntradaCompra", "Total US$:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblTotalD.setText(QtGui.QApplication.translate("frmEntradaCompra", "0.00", None, QtGui.QApplication.UnicodeUTF8))
        self.gbRadios.setTitle(QtGui.QApplication.translate("frmEntradaCompra", "Tipo de Pago", None, QtGui.QApplication.UnicodeUTF8))
        self.rbCash.setText(QtGui.QApplication.translate("frmEntradaCompra", "Contado", None, QtGui.QApplication.UnicodeUTF8))
        self.rbCredit.setText(QtGui.QApplication.translate("frmEntradaCompra", "Credito", None, QtGui.QApplication.UnicodeUTF8))
        self.rbCheck.setText(QtGui.QApplication.translate("frmEntradaCompra", "Cheque", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("frmEntradaCompra", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Proveedor:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabdetails), None)
        self.label_4.setText(QtGui.QApplication.translate("frmEntradaCompra", "&Buscar", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabnavigation), None)
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("frmEntradaCompra", "toolBar", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmEntradaCompra = QtGui.QMainWindow()
    ui = Ui_frmEntradaCompra()
    ui.setupUi(frmEntradaCompra)
    frmEntradaCompra.show()
    sys.exit(app.exec_())

