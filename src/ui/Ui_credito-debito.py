# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/marcos/workspace/EsquipulasPy/src/ui/credito-debito.ui'
#
# Created by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmCreditoDebito(object):
    def setupUi(self, frmCreditoDebito):
        frmCreditoDebito.setObjectName("frmCreditoDebito")
        frmCreditoDebito.resize(800, 600)
        frmCreditoDebito.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtGui.QWidget(frmCreditoDebito)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        self.tabdetails = QtGui.QWidget()
        self.tabdetails.setObjectName("tabdetails")
        self.gridLayout = QtGui.QGridLayout(self.tabdetails)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.txtDocumentNumber = QtGui.QLineEdit(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtDocumentNumber.sizePolicy().hasHeightForWidth())
        self.txtDocumentNumber.setSizePolicy(sizePolicy)
        self.txtDocumentNumber.setReadOnly(True)
        self.txtDocumentNumber.setObjectName("txtDocumentNumber")
        self.horizontalLayout_2.addWidget(self.txtDocumentNumber)
        self.label_3 = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.stackedWidget = QtGui.QStackedWidget(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_5 = QtGui.QWidget()
        self.page_5.setObjectName("page_5")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.page_5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.cbClient = QtGui.QComboBox(self.page_5)
        self.cbClient.setObjectName("cbClient")
        self.verticalLayout_3.addWidget(self.cbClient)
        self.stackedWidget.addWidget(self.page_5)
        self.page_6 = QtGui.QWidget()
        self.page_6.setObjectName("page_6")
        self.txtClient = QtGui.QLineEdit(self.page_6)
        self.txtClient.setGeometry(QtCore.QRect(4, 4, 105, 25))
        self.txtClient.setReadOnly(True)
        self.txtClient.setObjectName("txtClient")
        self.stackedWidget.addWidget(self.page_6)
        self.horizontalLayout_2.addWidget(self.stackedWidget)
        self.label_4 = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.txtBill = QtGui.QLineEdit(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtBill.sizePolicy().hasHeightForWidth())
        self.txtBill.setSizePolicy(sizePolicy)
        self.txtBill.setReadOnly(True)
        self.txtBill.setObjectName("txtBill")
        self.horizontalLayout_2.addWidget(self.txtBill)
        self.label_5 = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.dtPicker = QtGui.QDateTimeEdit(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dtPicker.sizePolicy().hasHeightForWidth())
        self.dtPicker.setSizePolicy(sizePolicy)
        self.dtPicker.setReadOnly(True)
        self.dtPicker.setCalendarPopup(True)
        self.dtPicker.setObjectName("dtPicker")
        self.horizontalLayout_2.addWidget(self.dtPicker)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 2)
        self.tabledetails = QtGui.QTableView(self.tabdetails)
        self.tabledetails.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tabledetails.setObjectName("tabledetails")
        self.tabledetails.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.tabledetails, 1, 0, 1, 2)
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
        self.gridLayout.addWidget(self.groupBox_2, 2, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(self.tabdetails)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_11 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 0, 0, 1, 1)
        self.label_14 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 1, 0, 1, 1)
        self.lblTaxes = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTaxes.sizePolicy().hasHeightForWidth())
        self.lblTaxes.setSizePolicy(sizePolicy)
        self.lblTaxes.setObjectName("lblTaxes")
        self.gridLayout_2.addWidget(self.lblTaxes, 1, 1, 1, 1)
        self.label_12 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 2, 0, 1, 1)
        self.lblCost = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCost.sizePolicy().hasHeightForWidth())
        self.lblCost.setSizePolicy(sizePolicy)
        self.lblCost.setObjectName("lblCost")
        self.gridLayout_2.addWidget(self.lblCost, 2, 1, 1, 1)
        self.label_13 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 3, 0, 1, 1)
        self.lblTotal = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTotal.sizePolicy().hasHeightForWidth())
        self.lblTotal.setSizePolicy(sizePolicy)
        self.lblTotal.setObjectName("lblTotal")
        self.gridLayout_2.addWidget(self.lblTotal, 3, 1, 1, 1)
        self.lblSubtotal = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSubtotal.sizePolicy().hasHeightForWidth())
        self.lblSubtotal.setSizePolicy(sizePolicy)
        self.lblSubtotal.setObjectName("lblSubtotal")
        self.gridLayout_2.addWidget(self.lblSubtotal, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 2, 1, 1, 1)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/document-edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabdetails, icon, "")
        self.tabnavigation = QtGui.QWidget()
        self.tabnavigation.setObjectName("tabnavigation")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabnavigation)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tablenavigation = QtGui.QTableView(self.tabnavigation)
        self.tablenavigation.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tablenavigation.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tablenavigation.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tablenavigation.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tablenavigation.setSortingEnabled(True)
        self.tablenavigation.setObjectName("tablenavigation")
        self.tablenavigation.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.tablenavigation)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.tabnavigation)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.txtSearch = QtGui.QLineEdit(self.tabnavigation)
        self.txtSearch.setObjectName("txtSearch")
        self.horizontalLayout.addWidget(self.txtSearch)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/res/table.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabnavigation, icon1, "")
        self.verticalLayout.addWidget(self.tabWidget)
        frmCreditoDebito.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(frmCreditoDebito)
        self.statusbar.setObjectName("statusbar")
        frmCreditoDebito.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(frmCreditoDebito)
        self.toolBar.setObjectName("toolBar")
        frmCreditoDebito.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.actionNew = QtGui.QAction(frmCreditoDebito)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/res/document-new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon2)
        self.actionNew.setObjectName("actionNew")
        self.actionPreview = QtGui.QAction(frmCreditoDebito)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/res/document-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPreview.setIcon(icon3)
        self.actionPreview.setObjectName("actionPreview")
        self.actionGoFirst = QtGui.QAction(frmCreditoDebito)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/res/go-first.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGoFirst.setIcon(icon4)
        self.actionGoFirst.setObjectName("actionGoFirst")
        self.actionGoPrevious = QtGui.QAction(frmCreditoDebito)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/res/go-previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGoPrevious.setIcon(icon5)
        self.actionGoPrevious.setObjectName("actionGoPrevious")
        self.actionGoNext = QtGui.QAction(frmCreditoDebito)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/res/go-next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGoNext.setIcon(icon6)
        self.actionGoNext.setObjectName("actionGoNext")
        self.actionGoLast = QtGui.QAction(frmCreditoDebito)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/res/go-last.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGoLast.setIcon(icon7)
        self.actionGoLast.setObjectName("actionGoLast")
        self.actionSave = QtGui.QAction(frmCreditoDebito)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/res/document-save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon8)
        self.actionSave.setObjectName("actionSave")
        self.actionCancel = QtGui.QAction(frmCreditoDebito)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/res/dialog-cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCancel.setIcon(icon9)
        self.actionCancel.setObjectName("actionCancel")
        self.actionEditar = QtGui.QAction(frmCreditoDebito)
        self.actionEditar.setIcon(icon)
        self.actionEditar.setObjectName("actionEditar")
        self.actionDelete = QtGui.QAction(frmCreditoDebito)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/res/edit-delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon10)
        self.actionDelete.setObjectName("actionDelete")
        self.actionCopy = QtGui.QAction(frmCreditoDebito)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/res/edit-copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(icon11)
        self.actionCopy.setObjectName("actionCopy")
        self.actionCut = QtGui.QAction(frmCreditoDebito)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/res/edit-cut.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCut.setIcon(icon12)
        self.actionCut.setObjectName("actionCut")
        self.actionPaste = QtGui.QAction(frmCreditoDebito)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/icons/res/edit-paste.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaste.setIcon(icon13)
        self.actionPaste.setObjectName("actionPaste")
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionCancel)
        self.toolBar.addAction(self.actionPreview)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCopy)
        self.toolBar.addAction(self.actionPaste)
        self.toolBar.addAction(self.actionCut)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionGoFirst)
        self.toolBar.addAction(self.actionGoPrevious)
        self.toolBar.addAction(self.actionGoNext)
        self.toolBar.addAction(self.actionGoLast)
        self.label_2.setBuddy(self.txtDocumentNumber)
        self.label_3.setBuddy(self.txtBill)
        self.label_4.setBuddy(self.txtClient)
        self.label_5.setBuddy(self.dtPicker)
        self.label.setBuddy(self.txtSearch)

        self.retranslateUi(frmCreditoDebito)
        self.tabWidget.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(frmCreditoDebito)
        frmCreditoDebito.setTabOrder(self.txtDocumentNumber, self.dtPicker)
        frmCreditoDebito.setTabOrder(self.dtPicker, self.tabledetails)
        frmCreditoDebito.setTabOrder(self.tabledetails, self.txtObservations)
        frmCreditoDebito.setTabOrder(self.txtObservations, self.txtBill)
        frmCreditoDebito.setTabOrder(self.txtBill, self.txtClient)
        frmCreditoDebito.setTabOrder(self.txtClient, self.cbClient)
        frmCreditoDebito.setTabOrder(self.cbClient, self.tabWidget)
        frmCreditoDebito.setTabOrder(self.tabWidget, self.tablenavigation)
        frmCreditoDebito.setTabOrder(self.tablenavigation, self.txtSearch)

    def retranslateUi(self, frmCreditoDebito):
        frmCreditoDebito.setWindowTitle(QtGui.QApplication.translate("frmCreditoDebito", "Devoluciones", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("frmCreditoDebito", "# Documento", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("frmCreditoDebito", "Cliente", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("frmCreditoDebito", "# Devolucion", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("frmCreditoDebito", "Fecha", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("frmCreditoDebito", "Observaciones", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("frmCreditoDebito", "Totales", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("frmCreditoDebito", "Subtotal: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("frmCreditoDebito", "Impuesto: ", None, QtGui.QApplication.UnicodeUTF8))
        self.lblTaxes.setText(QtGui.QApplication.translate("frmCreditoDebito", "C$ 0.00", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("frmCreditoDebito", "Costo Total: ", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCost.setText(QtGui.QApplication.translate("frmCreditoDebito", "C$ 0.00", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("frmCreditoDebito", "Total Devolución: ", None, QtGui.QApplication.UnicodeUTF8))
        self.lblTotal.setText(QtGui.QApplication.translate("frmCreditoDebito", "C$ 0.00", None, QtGui.QApplication.UnicodeUTF8))
        self.lblSubtotal.setText(QtGui.QApplication.translate("frmCreditoDebito", "C$ 0.00", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabdetails), None)
        self.label.setText(QtGui.QApplication.translate("frmCreditoDebito", "&Buscar", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabnavigation), None)
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("frmCreditoDebito", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setText(QtGui.QApplication.translate("frmCreditoDebito", "Nuevo", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setShortcut(QtGui.QApplication.translate("frmCreditoDebito", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreview.setText(QtGui.QApplication.translate("frmCreditoDebito", "Previsualizar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoFirst.setText(QtGui.QApplication.translate("frmCreditoDebito", "Ir al Primer Registro", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoPrevious.setText(QtGui.QApplication.translate("frmCreditoDebito", "Ir al Registro Anterior", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoNext.setText(QtGui.QApplication.translate("frmCreditoDebito", "Ir al siguiente registro", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoLast.setText(QtGui.QApplication.translate("frmCreditoDebito", "Ir al ultimo registro", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("frmCreditoDebito", "Guardar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCancel.setText(QtGui.QApplication.translate("frmCreditoDebito", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditar.setText(QtGui.QApplication.translate("frmCreditoDebito", "Editar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditar.setShortcut(QtGui.QApplication.translate("frmCreditoDebito", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete.setText(QtGui.QApplication.translate("frmCreditoDebito", "Borrar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setText(QtGui.QApplication.translate("frmCreditoDebito", "Copiar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setShortcut(QtGui.QApplication.translate("frmCreditoDebito", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setText(QtGui.QApplication.translate("frmCreditoDebito", "Cortar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setShortcut(QtGui.QApplication.translate("frmCreditoDebito", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setText(QtGui.QApplication.translate("frmCreditoDebito", "Pegar", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmCreditoDebito = QtGui.QMainWindow()
    ui = Ui_frmCreditoDebito()
    ui.setupUi(frmCreditoDebito)
    frmCreditoDebito.show()
    sys.exit(app.exec_())

