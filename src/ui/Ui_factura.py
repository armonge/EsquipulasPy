# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\workspace\EsquipulasPy\src\ui\factura.ui'
#
# Created: Thu Aug 05 23:05:17 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmFactura(object):
    def setupUi(self, frmFactura):
        frmFactura.setObjectName("frmFactura")
        frmFactura.resize(730, 583)
        self.centralwidget = QtGui.QWidget(frmFactura)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        self.tabdetails = QtGui.QWidget()
        self.tabdetails.setObjectName("tabdetails")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tabdetails)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)
        self.dtPicker = QtGui.QDateTimeEdit(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dtPicker.sizePolicy().hasHeightForWidth())
        self.dtPicker.setSizePolicy(sizePolicy)
        self.dtPicker.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dtPicker.setReadOnly(True)
        self.dtPicker.setCalendarPopup(True)
        self.dtPicker.setObjectName("dtPicker")
        self.gridLayout.addWidget(self.dtPicker, 0, 3, 1, 1)
        self.label = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.swcliente = QtGui.QStackedWidget(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.swcliente.sizePolicy().hasHeightForWidth())
        self.swcliente.setSizePolicy(sizePolicy)
        self.swcliente.setObjectName("swcliente")
        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName("page_3")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.page_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.cbcliente = QtGui.QComboBox(self.page_3)
        self.cbcliente.setEditable(True)
        self.cbcliente.setObjectName("cbcliente")
        self.horizontalLayout_4.addWidget(self.cbcliente)
        self.swcliente.addWidget(self.page_3)
        self.page_4 = QtGui.QWidget()
        self.page_4.setObjectName("page_4")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.page_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.txtcliente = QtGui.QLineEdit(self.page_4)
        self.txtcliente.setReadOnly(True)
        self.txtcliente.setObjectName("txtcliente")
        self.horizontalLayout_3.addWidget(self.txtcliente)
        self.swcliente.addWidget(self.page_4)
        self.gridLayout.addWidget(self.swcliente, 1, 1, 1, 3)
        self.label_11 = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 2, 0, 1, 1)
        self.swvendedor = QtGui.QStackedWidget(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.swvendedor.sizePolicy().hasHeightForWidth())
        self.swvendedor.setSizePolicy(sizePolicy)
        self.swvendedor.setObjectName("swvendedor")
        self.page_7 = QtGui.QWidget()
        self.page_7.setObjectName("page_7")
        self.horizontalLayout_8 = QtGui.QHBoxLayout(self.page_7)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.cbvendedor = QtGui.QComboBox(self.page_7)
        self.cbvendedor.setEditable(True)
        self.cbvendedor.setObjectName("cbvendedor")
        self.horizontalLayout_8.addWidget(self.cbvendedor)
        self.swvendedor.addWidget(self.page_7)
        self.page_8 = QtGui.QWidget()
        self.page_8.setObjectName("page_8")
        self.horizontalLayout_9 = QtGui.QHBoxLayout(self.page_8)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.txtvendedor = QtGui.QLineEdit(self.page_8)
        self.txtvendedor.setReadOnly(True)
        self.txtvendedor.setObjectName("txtvendedor")
        self.horizontalLayout_9.addWidget(self.txtvendedor)
        self.swvendedor.addWidget(self.page_8)
        self.gridLayout.addWidget(self.swvendedor, 2, 1, 1, 3)
        self.label_6 = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
        self.swbodega = QtGui.QStackedWidget(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.swbodega.sizePolicy().hasHeightForWidth())
        self.swbodega.setSizePolicy(sizePolicy)
        self.swbodega.setObjectName("swbodega")
        self.page_5 = QtGui.QWidget()
        self.page_5.setObjectName("page_5")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.page_5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.cbbodega = QtGui.QComboBox(self.page_5)
        self.cbbodega.setEditable(True)
        self.cbbodega.setObjectName("cbbodega")
        self.horizontalLayout_5.addWidget(self.cbbodega)
        self.swbodega.addWidget(self.page_5)
        self.page_6 = QtGui.QWidget()
        self.page_6.setObjectName("page_6")
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.page_6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.txtbodega = QtGui.QLineEdit(self.page_6)
        self.txtbodega.setDragEnabled(True)
        self.txtbodega.setReadOnly(True)
        self.txtbodega.setObjectName("txtbodega")
        self.horizontalLayout_6.addWidget(self.txtbodega)
        self.swbodega.addWidget(self.page_6)
        self.gridLayout.addWidget(self.swbodega, 3, 1, 1, 3)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.rbcontado = QtGui.QRadioButton(self.tabdetails)
        self.rbcontado.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbcontado.sizePolicy().hasHeightForWidth())
        self.rbcontado.setSizePolicy(sizePolicy)
        self.rbcontado.setChecked(True)
        self.rbcontado.setObjectName("rbcontado")
        self.horizontalLayout_7.addWidget(self.rbcontado)
        self.rbcredito = QtGui.QRadioButton(self.tabdetails)
        self.rbcredito.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbcredito.sizePolicy().hasHeightForWidth())
        self.rbcredito.setSizePolicy(sizePolicy)
        self.rbcredito.setObjectName("rbcredito")
        self.horizontalLayout_7.addWidget(self.rbcredito)
        self.gridLayout.addLayout(self.horizontalLayout_7, 4, 2, 1, 2)
        self.lblnfac = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblnfac.sizePolicy().hasHeightForWidth())
        self.lblnfac.setSizePolicy(sizePolicy)
        self.lblnfac.setStyleSheet("border:1px solid #000")
        self.lblnfac.setText("")
        self.lblnfac.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblnfac.setObjectName("lblnfac")
        self.gridLayout.addWidget(self.lblnfac, 0, 1, 1, 1)
        self.lblanulado = QtGui.QLabel(self.tabdetails)
        self.lblanulado.setStyleSheet("font: 75 20pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 0, 0);")
        self.lblanulado.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblanulado.setObjectName("lblanulado")
        self.gridLayout.addWidget(self.lblanulado, 4, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.tabledetails = QtGui.QTableView(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabledetails.sizePolicy().hasHeightForWidth())
        self.tabledetails.setSizePolicy(sizePolicy)
        self.tabledetails.setMinimumSize(QtCore.QSize(0, 100))
        self.tabledetails.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tabledetails.setObjectName("tabledetails")
        self.verticalLayout_3.addWidget(self.tabledetails)
        self.label_7 = QtGui.QLabel(self.tabdetails)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_3.addWidget(self.label_7)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.txtobservaciones = QtGui.QPlainTextEdit(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtobservaciones.sizePolicy().hasHeightForWidth())
        self.txtobservaciones.setSizePolicy(sizePolicy)
        self.txtobservaciones.setMinimumSize(QtCore.QSize(0, 40))
        self.txtobservaciones.setMaximumSize(QtCore.QSize(16777215, 80))
        self.txtobservaciones.setReadOnly(True)
        self.txtobservaciones.setObjectName("txtobservaciones")
        self.gridLayout_2.addWidget(self.txtobservaciones, 0, 0, 3, 1)
        self.label_3 = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 1, 1, 1)
        self.lblsubtotal = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblsubtotal.sizePolicy().hasHeightForWidth())
        self.lblsubtotal.setSizePolicy(sizePolicy)
        self.lblsubtotal.setMinimumSize(QtCore.QSize(60, 0))
        self.lblsubtotal.setMaximumSize(QtCore.QSize(300, 16777215))
        self.lblsubtotal.setStyleSheet("None")
        self.lblsubtotal.setText("")
        self.lblsubtotal.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblsubtotal.setObjectName("lblsubtotal")
        self.gridLayout_2.addWidget(self.lblsubtotal, 0, 2, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_8 = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.lbltasaiva = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbltasaiva.sizePolicy().hasHeightForWidth())
        self.lbltasaiva.setSizePolicy(sizePolicy)
        self.lbltasaiva.setText("")
        self.lbltasaiva.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbltasaiva.setObjectName("lbltasaiva")
        self.horizontalLayout_2.addWidget(self.lbltasaiva)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)
        self.lbliva = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbliva.sizePolicy().hasHeightForWidth())
        self.lbliva.setSizePolicy(sizePolicy)
        self.lbliva.setMinimumSize(QtCore.QSize(60, 0))
        self.lbliva.setMaximumSize(QtCore.QSize(300, 16777215))
        self.lbliva.setStyleSheet("None")
        self.lbliva.setText("")
        self.lbliva.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbliva.setObjectName("lbliva")
        self.gridLayout_2.addWidget(self.lbliva, 1, 2, 1, 1)
        self.label_9 = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 2, 1, 1, 1)
        self.lbltotal = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbltotal.sizePolicy().hasHeightForWidth())
        self.lbltotal.setSizePolicy(sizePolicy)
        self.lbltotal.setMinimumSize(QtCore.QSize(60, 0))
        self.lbltotal.setMaximumSize(QtCore.QSize(300, 16777215))
        self.lbltotal.setStyleSheet("None")
        self.lbltotal.setText("")
        self.lbltotal.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbltotal.setObjectName("lbltotal")
        self.gridLayout_2.addWidget(self.lbltotal, 2, 2, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
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
        self.btnAnular = QtGui.QPushButton(self.tabnavigation)
        self.btnAnular.setObjectName("btnAnular")
        self.horizontalLayout.addWidget(self.btnAnular)
        self.cboFiltro = QtGui.QComboBox(self.tabnavigation)
        self.cboFiltro.setObjectName("cboFiltro")
        self.cboFiltro.addItem("")
        self.cboFiltro.addItem("")
        self.cboFiltro.addItem("")
        self.horizontalLayout.addWidget(self.cboFiltro)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/res/table.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabnavigation, icon1, "")
        self.verticalLayout.addWidget(self.tabWidget)
        frmFactura.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(frmFactura)
        self.statusbar.setObjectName("statusbar")
        frmFactura.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(frmFactura)
        self.toolBar.setObjectName("toolBar")
        frmFactura.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.actionNew = QtGui.QAction(frmFactura)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/res/document-new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon2)
        self.actionNew.setObjectName("actionNew")
        self.actionPreview = QtGui.QAction(frmFactura)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/res/document-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPreview.setIcon(icon3)
        self.actionPreview.setObjectName("actionPreview")
        self.actionGoFirst = QtGui.QAction(frmFactura)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/res/go-first.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGoFirst.setIcon(icon4)
        self.actionGoFirst.setObjectName("actionGoFirst")
        self.actionGoPrevious = QtGui.QAction(frmFactura)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/res/go-previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGoPrevious.setIcon(icon5)
        self.actionGoPrevious.setObjectName("actionGoPrevious")
        self.actionGoNext = QtGui.QAction(frmFactura)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/res/go-next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGoNext.setIcon(icon6)
        self.actionGoNext.setObjectName("actionGoNext")
        self.actionGoLast = QtGui.QAction(frmFactura)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/res/go-last.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGoLast.setIcon(icon7)
        self.actionGoLast.setObjectName("actionGoLast")
        self.actionSave = QtGui.QAction(frmFactura)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/res/document-save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon8)
        self.actionSave.setObjectName("actionSave")
        self.actionCancel = QtGui.QAction(frmFactura)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/res/dialog-cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCancel.setIcon(icon9)
        self.actionCancel.setObjectName("actionCancel")
        self.actionEditCell = QtGui.QAction(frmFactura)
        self.actionEditCell.setIcon(icon)
        self.actionEditCell.setObjectName("actionEditCell")
        self.actionDeleteRow = QtGui.QAction(frmFactura)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/res/edit-delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDeleteRow.setIcon(icon10)
        self.actionDeleteRow.setObjectName("actionDeleteRow")
        self.actionCopy = QtGui.QAction(frmFactura)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/res/edit-copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(icon11)
        self.actionCopy.setObjectName("actionCopy")
        self.actionCut = QtGui.QAction(frmFactura)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/res/edit-cut.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCut.setIcon(icon12)
        self.actionCut.setObjectName("actionCut")
        self.actionPaste = QtGui.QAction(frmFactura)
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
        self.label_5.setBuddy(self.dtPicker)
        self.label.setBuddy(self.txtcliente)
        self.label_11.setBuddy(self.txtcliente)
        self.label_6.setBuddy(self.txtbodega)
        self.lbltasaiva.setBuddy(self.txtbodega)
        self.label_4.setBuddy(self.txtSearch)

        self.retranslateUi(frmFactura)
        self.tabWidget.setCurrentIndex(0)
        self.swcliente.setCurrentIndex(1)
        self.swvendedor.setCurrentIndex(1)
        self.swbodega.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(frmFactura)
        frmFactura.setTabOrder(self.cbcliente, self.cbvendedor)
        frmFactura.setTabOrder(self.cbvendedor, self.cbbodega)
        frmFactura.setTabOrder(self.cbbodega, self.rbcontado)
        frmFactura.setTabOrder(self.rbcontado, self.rbcredito)
        frmFactura.setTabOrder(self.rbcredito, self.tabledetails)
        frmFactura.setTabOrder(self.tabledetails, self.txtobservaciones)
        frmFactura.setTabOrder(self.txtobservaciones, self.tabWidget)
        frmFactura.setTabOrder(self.tabWidget, self.dtPicker)
        frmFactura.setTabOrder(self.dtPicker, self.txtvendedor)
        frmFactura.setTabOrder(self.txtvendedor, self.txtSearch)
        frmFactura.setTabOrder(self.txtSearch, self.tablenavigation)
        frmFactura.setTabOrder(self.tablenavigation, self.txtcliente)
        frmFactura.setTabOrder(self.txtcliente, self.txtbodega)

    def retranslateUi(self, frmFactura):
        frmFactura.setWindowTitle(QtGui.QApplication.translate("frmFactura", "Factura", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("frmFactura", "<b>Facturar No.</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("frmFactura", "<b>Fecha</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.dtPicker.setDisplayFormat(QtGui.QApplication.translate("frmFactura", "dd/MM/yyyy", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmFactura", "&<b>Facturar a:</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("frmFactura", "<b>Vendedor:</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("frmFactura", "&<b>Bodega:<.b>", None, QtGui.QApplication.UnicodeUTF8))
        self.rbcontado.setText(QtGui.QApplication.translate("frmFactura", "Contado", None, QtGui.QApplication.UnicodeUTF8))
        self.rbcredito.setText(QtGui.QApplication.translate("frmFactura", "Crédito", None, QtGui.QApplication.UnicodeUTF8))
        self.lblanulado.setText(QtGui.QApplication.translate("frmFactura", "ANULADA", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("frmFactura", "<b>Observaciones</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("frmFactura", "<b>Subtotal</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("frmFactura", "<b>Iva</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("frmFactura", "<b>Total</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabdetails), None)
        self.label_4.setText(QtGui.QApplication.translate("frmFactura", "&Buscar", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAnular.setText(QtGui.QApplication.translate("frmFactura", "Anular Factura", None, QtGui.QApplication.UnicodeUTF8))
        self.cboFiltro.setItemText(0, QtGui.QApplication.translate("frmFactura", "Ambas", None, QtGui.QApplication.UnicodeUTF8))
        self.cboFiltro.setItemText(1, QtGui.QApplication.translate("frmFactura", "Anuladas", None, QtGui.QApplication.UnicodeUTF8))
        self.cboFiltro.setItemText(2, QtGui.QApplication.translate("frmFactura", "No Anuladas", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabnavigation), None)
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("frmFactura", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setText(QtGui.QApplication.translate("frmFactura", "Nuevo", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setShortcut(QtGui.QApplication.translate("frmFactura", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreview.setText(QtGui.QApplication.translate("frmFactura", "Previsualizar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreview.setShortcut(QtGui.QApplication.translate("frmFactura", "Ctrl+P", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoFirst.setText(QtGui.QApplication.translate("frmFactura", "Ir al Primer Registro", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoPrevious.setText(QtGui.QApplication.translate("frmFactura", "Ir al Registro Anterior", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoNext.setText(QtGui.QApplication.translate("frmFactura", "Ir al siguiente registro", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoLast.setText(QtGui.QApplication.translate("frmFactura", "Ir al ultimo registro", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("frmFactura", "Guardar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("frmFactura", "Ctrl+G", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCancel.setText(QtGui.QApplication.translate("frmFactura", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditCell.setText(QtGui.QApplication.translate("frmFactura", "Editar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditCell.setShortcut(QtGui.QApplication.translate("frmFactura", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeleteRow.setText(QtGui.QApplication.translate("frmFactura", "Borrar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setText(QtGui.QApplication.translate("frmFactura", "Copiar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setShortcut(QtGui.QApplication.translate("frmFactura", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setText(QtGui.QApplication.translate("frmFactura", "Cortar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setShortcut(QtGui.QApplication.translate("frmFactura", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setText(QtGui.QApplication.translate("frmFactura", "Pegar", None, QtGui.QApplication.UnicodeUTF8))

import res_rc
