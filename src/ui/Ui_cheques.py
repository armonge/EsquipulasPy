# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/cheques.ui'
#
# Created: Mon Aug 23 03:19:13 2010
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmCheques(object):
    def setupUi(self, frmCheques):
        frmCheques.setObjectName("frmCheques")
        frmCheques.resize(769, 665)
        self.centralwidget = QtGui.QWidget(frmCheques)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        self.tabdetails = QtGui.QWidget()
        self.tabdetails.setObjectName("tabdetails")
        self.gridLayout_4 = QtGui.QGridLayout(self.tabdetails)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_9 = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 0, 0, 1, 1)
        self.lblncheque = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(18)
        sizePolicy.setHeightForWidth(self.lblncheque.sizePolicy().hasHeightForWidth())
        self.lblncheque.setSizePolicy(sizePolicy)
        self.lblncheque.setStyleSheet("border:1px solid #000")
        self.lblncheque.setText("")
        self.lblncheque.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblncheque.setObjectName("lblncheque")
        self.gridLayout_2.addWidget(self.lblncheque, 0, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 0, 2, 1, 1)
        self.dtPicker = QtGui.QDateEdit(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(18)
        sizePolicy.setHeightForWidth(self.dtPicker.sizePolicy().hasHeightForWidth())
        self.dtPicker.setSizePolicy(sizePolicy)
        self.dtPicker.setCalendarPopup(True)
        self.dtPicker.setObjectName("dtPicker")
        self.gridLayout_2.addWidget(self.dtPicker, 0, 3, 1, 1)
        self.label_11 = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 1, 0, 1, 1)
        self.beneficiariowidget = QtGui.QStackedWidget(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.beneficiariowidget.sizePolicy().hasHeightForWidth())
        self.beneficiariowidget.setSizePolicy(sizePolicy)
        self.beneficiariowidget.setObjectName("beneficiariowidget")
        self.page = QtGui.QWidget()
        self.page.setObjectName("page")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.page)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lblbeneficiario = QtGui.QLabel(self.page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblbeneficiario.sizePolicy().hasHeightForWidth())
        self.lblbeneficiario.setSizePolicy(sizePolicy)
        self.lblbeneficiario.setFrameShape(QtGui.QFrame.Box)
        self.lblbeneficiario.setText("")
        self.lblbeneficiario.setObjectName("lblbeneficiario")
        self.horizontalLayout_4.addWidget(self.lblbeneficiario)
        self.beneficiariowidget.addWidget(self.page)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.page_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.cbobeneficiario = QtGui.QComboBox(self.page_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbobeneficiario.sizePolicy().hasHeightForWidth())
        self.cbobeneficiario.setSizePolicy(sizePolicy)
        self.cbobeneficiario.setEditable(True)
        self.cbobeneficiario.setObjectName("cbobeneficiario")
        self.verticalLayout_4.addWidget(self.cbobeneficiario)
        self.beneficiariowidget.addWidget(self.page_2)
        self.gridLayout_2.addWidget(self.beneficiariowidget, 1, 1, 1, 1)
        self.retencionwidget = QtGui.QStackedWidget(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.retencionwidget.sizePolicy().hasHeightForWidth())
        self.retencionwidget.setSizePolicy(sizePolicy)
        self.retencionwidget.setObjectName("retencionwidget")
        self.page_9 = QtGui.QWidget()
        self.page_9.setObjectName("page_9")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.page_9)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lblretencion = QtGui.QLabel(self.page_9)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblretencion.sizePolicy().hasHeightForWidth())
        self.lblretencion.setSizePolicy(sizePolicy)
        self.lblretencion.setFrameShape(QtGui.QFrame.Box)
        self.lblretencion.setObjectName("lblretencion")
        self.horizontalLayout_5.addWidget(self.lblretencion)
        self.retencionwidget.addWidget(self.page_9)
        self.page_10 = QtGui.QWidget()
        self.page_10.setObjectName("page_10")
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.page_10)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.cboretencion = QtGui.QComboBox(self.page_10)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboretencion.sizePolicy().hasHeightForWidth())
        self.cboretencion.setSizePolicy(sizePolicy)
        self.cboretencion.setObjectName("cboretencion")
        self.cboretencion.addItem("")
        self.horizontalLayout_6.addWidget(self.cboretencion)
        self.retencionwidget.addWidget(self.page_10)
        self.gridLayout_2.addWidget(self.retencionwidget, 1, 3, 1, 1)
        self.label_12 = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 2, 0, 1, 1)
        self.cuentawidget = QtGui.QStackedWidget(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cuentawidget.sizePolicy().hasHeightForWidth())
        self.cuentawidget.setSizePolicy(sizePolicy)
        self.cuentawidget.setObjectName("cuentawidget")
        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName("page_3")
        self.verticalLayout = QtGui.QVBoxLayout(self.page_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblcuenta = QtGui.QLabel(self.page_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblcuenta.sizePolicy().hasHeightForWidth())
        self.lblcuenta.setSizePolicy(sizePolicy)
        self.lblcuenta.setStyleSheet("margin:0")
        self.lblcuenta.setFrameShape(QtGui.QFrame.Box)
        self.lblcuenta.setText("")
        self.lblcuenta.setObjectName("lblcuenta")
        self.verticalLayout.addWidget(self.lblcuenta)
        self.cuentawidget.addWidget(self.page_3)
        self.page_4 = QtGui.QWidget()
        self.page_4.setObjectName("page_4")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.page_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cbocuenta = QtGui.QComboBox(self.page_4)
        self.cbocuenta.setEditable(True)
        self.cbocuenta.setObjectName("cbocuenta")
        self.horizontalLayout_3.addWidget(self.cbocuenta)
        self.cuentawidget.addWidget(self.page_4)
        self.gridLayout_2.addWidget(self.cuentawidget, 2, 1, 1, 1)
        self.Concepto = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Concepto.sizePolicy().hasHeightForWidth())
        self.Concepto.setSizePolicy(sizePolicy)
        self.Concepto.setObjectName("Concepto")
        self.gridLayout_2.addWidget(self.Concepto, 2, 2, 1, 1)
        self.conceptowidget = QtGui.QStackedWidget(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.conceptowidget.sizePolicy().hasHeightForWidth())
        self.conceptowidget.setSizePolicy(sizePolicy)
        self.conceptowidget.setObjectName("conceptowidget")
        self.page_5 = QtGui.QWidget()
        self.page_5.setObjectName("page_5")
        self.gridLayout_5 = QtGui.QGridLayout(self.page_5)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.lblconcepto = QtGui.QLabel(self.page_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblconcepto.sizePolicy().hasHeightForWidth())
        self.lblconcepto.setSizePolicy(sizePolicy)
        self.lblconcepto.setFrameShape(QtGui.QFrame.Box)
        self.lblconcepto.setText("")
        self.lblconcepto.setObjectName("lblconcepto")
        self.gridLayout_5.addWidget(self.lblconcepto, 0, 0, 1, 1)
        self.conceptowidget.addWidget(self.page_5)
        self.page_6 = QtGui.QWidget()
        self.page_6.setObjectName("page_6")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.page_6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cboconcepto = QtGui.QComboBox(self.page_6)
        self.cboconcepto.setEditable(True)
        self.cboconcepto.setObjectName("cboconcepto")
        self.horizontalLayout_2.addWidget(self.cboconcepto)
        self.conceptowidget.addWidget(self.page_6)
        self.gridLayout_2.addWidget(self.conceptowidget, 2, 3, 1, 1)
        self.label_16 = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 3, 0, 1, 1)
        self.lbltipocambio = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbltipocambio.sizePolicy().hasHeightForWidth())
        self.lbltipocambio.setSizePolicy(sizePolicy)
        self.lbltipocambio.setFrameShape(QtGui.QFrame.Panel)
        self.lbltipocambio.setText("")
        self.lbltipocambio.setObjectName("lbltipocambio")
        self.gridLayout_2.addWidget(self.lbltipocambio, 3, 1, 1, 1)
        self.ckretencion = QtGui.QCheckBox(self.tabdetails)
        self.ckretencion.setObjectName("ckretencion")
        self.gridLayout_2.addWidget(self.ckretencion, 1, 2, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.frame_2 = QtGui.QFrame(self.tabdetails)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtGui.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.tabledetails = QtGui.QTableView(self.frame_2)
        self.tabledetails.setAlternatingRowColors(True)
        self.tabledetails.setObjectName("tabledetails")
        self.gridLayout.addWidget(self.tabledetails, 0, 0, 1, 3)
        self.label_15 = QtGui.QLabel(self.frame_2)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 1, 0, 1, 1)
        self.txtobservaciones = QtGui.QPlainTextEdit(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtobservaciones.sizePolicy().hasHeightForWidth())
        self.txtobservaciones.setSizePolicy(sizePolicy)
        self.txtobservaciones.setMaximumSize(QtCore.QSize(16777215, 100))
        self.txtobservaciones.setReadOnly(False)
        self.txtobservaciones.setObjectName("txtobservaciones")
        self.gridLayout.addWidget(self.txtobservaciones, 2, 0, 4, 1)
        self.lblsub = QtGui.QLabel(self.frame_2)
        self.lblsub.setObjectName("lblsub")
        self.gridLayout.addWidget(self.lblsub, 2, 1, 1, 1)
        self.lbliva = QtGui.QLabel(self.frame_2)
        self.lbliva.setObjectName("lbliva")
        self.gridLayout.addWidget(self.lbliva, 3, 1, 1, 1)
        self.iva = QtGui.QLabel(self.frame_2)
        self.iva.setObjectName("iva")
        self.gridLayout.addWidget(self.iva, 3, 2, 1, 1)
        self.lblret = QtGui.QLabel(self.frame_2)
        self.lblret.setObjectName("lblret")
        self.gridLayout.addWidget(self.lblret, 4, 1, 1, 1)
        self.retencion = QtGui.QLabel(self.frame_2)
        self.retencion.setObjectName("retencion")
        self.gridLayout.addWidget(self.retencion, 4, 2, 1, 1)
        self.lbltotal = QtGui.QLabel(self.frame_2)
        self.lbltotal.setObjectName("lbltotal")
        self.gridLayout.addWidget(self.lbltotal, 5, 1, 1, 1)
        self.total = QtGui.QLabel(self.frame_2)
        self.total.setObjectName("total")
        self.gridLayout.addWidget(self.total, 5, 2, 1, 1)
        self.subtotal = QtGui.QDoubleSpinBox(self.frame_2)
        self.subtotal.setReadOnly(False)
        self.subtotal.setDecimals(4)
        self.subtotal.setMaximum(9999999.0)
        self.subtotal.setObjectName("subtotal")
        self.gridLayout.addWidget(self.subtotal, 2, 2, 1, 1)
        self.gridLayout_4.addWidget(self.frame_2, 1, 0, 1, 1)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/document-edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabdetails, icon, "")
        self.tabnavigation = QtGui.QWidget()
        self.tabnavigation.setObjectName("tabnavigation")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabnavigation)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tablenavigation = QtGui.QTableView(self.tabnavigation)
        self.tablenavigation.setAlternatingRowColors(True)
        self.tablenavigation.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tablenavigation.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tablenavigation.setObjectName("tablenavigation")
        self.tablenavigation.horizontalHeader().setStretchLastSection(True)
        self.tablenavigation.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.tablenavigation)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtGui.QLabel(self.tabnavigation)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.txtSearch = QtGui.QLineEdit(self.tabnavigation)
        self.txtSearch.setObjectName("txtSearch")
        self.horizontalLayout.addWidget(self.txtSearch)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/res/table.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabnavigation, icon1, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
        frmCheques.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(frmCheques)
        self.statusbar.setObjectName("statusbar")
        frmCheques.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(frmCheques)
        self.toolBar.setObjectName("toolBar")
        frmCheques.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.label_4.setBuddy(self.txtSearch)

        self.retranslateUi(frmCheques)
        self.tabWidget.setCurrentIndex(0)
        self.beneficiariowidget.setCurrentIndex(0)
        self.retencionwidget.setCurrentIndex(0)
        self.cboretencion.setCurrentIndex(-1)
        self.cuentawidget.setCurrentIndex(0)
        self.conceptowidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(frmCheques)
        frmCheques.setTabOrder(self.dtPicker, self.cbobeneficiario)
        frmCheques.setTabOrder(self.cbobeneficiario, self.ckretencion)
        frmCheques.setTabOrder(self.ckretencion, self.cboretencion)
        frmCheques.setTabOrder(self.cboretencion, self.cbocuenta)
        frmCheques.setTabOrder(self.cbocuenta, self.cboconcepto)
        frmCheques.setTabOrder(self.cboconcepto, self.subtotal)
        frmCheques.setTabOrder(self.subtotal, self.txtobservaciones)
        frmCheques.setTabOrder(self.txtobservaciones, self.tabledetails)
        frmCheques.setTabOrder(self.tabledetails, self.tabWidget)
        frmCheques.setTabOrder(self.tabWidget, self.txtSearch)
        frmCheques.setTabOrder(self.txtSearch, self.tablenavigation)

    def retranslateUi(self, frmCheques):
        frmCheques.setWindowTitle(QtGui.QApplication.translate("frmCheques", "Elaboración de Cheques", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("frmCheques", "Cheque No.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("frmCheques", "Fecha:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("frmCheques", "Beneficiario:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblretencion.setText(QtGui.QApplication.translate("frmCheques", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.cboretencion.setItemText(0, QtGui.QApplication.translate("frmCheques", "5", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("frmCheques", "Cuenta Bancaria:", None, QtGui.QApplication.UnicodeUTF8))
        self.Concepto.setText(QtGui.QApplication.translate("frmCheques", "En Concepto de:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("frmCheques", "Tipo de Cambio:", None, QtGui.QApplication.UnicodeUTF8))
        self.ckretencion.setText(QtGui.QApplication.translate("frmCheques", "Retencion", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("frmCheques", "Observaciones", None, QtGui.QApplication.UnicodeUTF8))
        self.lblsub.setText(QtGui.QApplication.translate("frmCheques", "Subtotal Factura", None, QtGui.QApplication.UnicodeUTF8))
        self.lbliva.setText(QtGui.QApplication.translate("frmCheques", "IVA", None, QtGui.QApplication.UnicodeUTF8))
        self.iva.setText(QtGui.QApplication.translate("frmCheques", "0.0000", None, QtGui.QApplication.UnicodeUTF8))
        self.lblret.setText(QtGui.QApplication.translate("frmCheques", "Retencion", None, QtGui.QApplication.UnicodeUTF8))
        self.retencion.setText(QtGui.QApplication.translate("frmCheques", "0.0000", None, QtGui.QApplication.UnicodeUTF8))
        self.lbltotal.setText(QtGui.QApplication.translate("frmCheques", "Total", None, QtGui.QApplication.UnicodeUTF8))
        self.total.setText(QtGui.QApplication.translate("frmCheques", "0.0000", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabdetails), None)
        self.label_4.setText(QtGui.QApplication.translate("frmCheques", "&Buscar", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabnavigation), None)
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("frmCheques", "toolBar", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmCheques = QtGui.QMainWindow()
    ui = Ui_frmCheques()
    ui.setupUi(frmCheques)
    frmCheques.show()
    sys.exit(app.exec_())

