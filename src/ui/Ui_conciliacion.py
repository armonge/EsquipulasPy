# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/conciliacion.ui'
#
# Created: Mon Aug 23 03:29:58 2010
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmConciliacion(object):
    def setupUi(self, frmConciliacion):
        frmConciliacion.setObjectName("frmConciliacion")
        frmConciliacion.resize(723, 545)
        frmConciliacion.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget = QtGui.QWidget(frmConciliacion)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        self.tabdetails = QtGui.QWidget()
        self.tabdetails.setObjectName("tabdetails")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.tabdetails)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.splitter_2 = QtGui.QSplitter(self.tabdetails)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.groupBox = QtGui.QGroupBox(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 150))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.lblfecha = QtGui.QLabel(self.groupBox)
        self.lblfecha.setMinimumSize(QtCore.QSize(0, 15))
        self.lblfecha.setText("")
        self.lblfecha.setAlignment(QtCore.Qt.AlignCenter)
        self.lblfecha.setObjectName("lblfecha")
        self.verticalLayout_7.addWidget(self.lblfecha)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.txtbanco = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtbanco.sizePolicy().hasHeightForWidth())
        self.txtbanco.setSizePolicy(sizePolicy)
        self.txtbanco.setReadOnly(True)
        self.txtbanco.setObjectName("txtbanco")
        self.gridLayout.addWidget(self.txtbanco, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 4, 1, 1)
        self.txtcuentabanco = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtcuentabanco.sizePolicy().hasHeightForWidth())
        self.txtcuentabanco.setSizePolicy(sizePolicy)
        self.txtcuentabanco.setReadOnly(True)
        self.txtcuentabanco.setObjectName("txtcuentabanco")
        self.gridLayout.addWidget(self.txtcuentabanco, 0, 5, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.txtmoneda = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtmoneda.sizePolicy().hasHeightForWidth())
        self.txtmoneda.setSizePolicy(sizePolicy)
        self.txtmoneda.setReadOnly(True)
        self.txtmoneda.setObjectName("txtmoneda")
        self.gridLayout.addWidget(self.txtmoneda, 0, 3, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 6, 1, 1)
        self.txtcuenta = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtcuenta.sizePolicy().hasHeightForWidth())
        self.txtcuenta.setSizePolicy(sizePolicy)
        self.txtcuenta.setReadOnly(True)
        self.txtcuenta.setObjectName("txtcuenta")
        self.gridLayout.addWidget(self.txtcuenta, 0, 7, 1, 1)
        self.verticalLayout_7.addLayout(self.gridLayout)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.tabledetails = QtGui.QTableView(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabledetails.sizePolicy().hasHeightForWidth())
        self.tabledetails.setSizePolicy(sizePolicy)
        self.tabledetails.setMinimumSize(QtCore.QSize(200, 70))
        self.tabledetails.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tabledetails.setObjectName("tabledetails")
        self.horizontalLayout_11.addWidget(self.tabledetails)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btnNotasCD = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnNotasCD.sizePolicy().hasHeightForWidth())
        self.btnNotasCD.setSizePolicy(sizePolicy)
        self.btnNotasCD.setMaximumSize(QtCore.QSize(22, 16777215))
        self.btnNotasCD.setStyleSheet("background: url(:/icons/res/list-add.png) no-repeat;")
        self.btnNotasCD.setText("")
        self.btnNotasCD.setObjectName("btnNotasCD")
        self.verticalLayout_3.addWidget(self.btnNotasCD)
        self.btnremove = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnremove.sizePolicy().hasHeightForWidth())
        self.btnremove.setSizePolicy(sizePolicy)
        self.btnremove.setMaximumSize(QtCore.QSize(22, 16777215))
        self.btnremove.setStyleSheet("background:url(:/icons/res/arrow-right.png)  no-repeat;")
        self.btnremove.setText("")
        self.btnremove.setObjectName("btnremove")
        self.verticalLayout_3.addWidget(self.btnremove)
        self.horizontalLayout_11.addLayout(self.verticalLayout_3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_7.addLayout(self.horizontalLayout_4)
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setMinimumSize(QtCore.QSize(0, 0))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.groupBox_2 = QtGui.QGroupBox(self.splitter)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 240))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.spbsaldobanco = QtGui.QDoubleSpinBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbsaldobanco.sizePolicy().hasHeightForWidth())
        self.spbsaldobanco.setSizePolicy(sizePolicy)
        self.spbsaldobanco.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spbsaldobanco.setMinimum(-1000000000.0)
        self.spbsaldobanco.setMaximum(1000000000.0)
        self.spbsaldobanco.setProperty("value", 0.0)
        self.spbsaldobanco.setObjectName("spbsaldobanco")
        self.horizontalLayout_2.addWidget(self.spbsaldobanco)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lbltotallibro_2 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbltotallibro_2.sizePolicy().hasHeightForWidth())
        self.lbltotallibro_2.setSizePolicy(sizePolicy)
        self.lbltotallibro_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbltotallibro_2.setObjectName("lbltotallibro_2")
        self.horizontalLayout_5.addWidget(self.lbltotallibro_2)
        self.txtdeposito = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtdeposito.sizePolicy().hasHeightForWidth())
        self.txtdeposito.setSizePolicy(sizePolicy)
        self.txtdeposito.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtdeposito.setReadOnly(True)
        self.txtdeposito.setObjectName("txtdeposito")
        self.horizontalLayout_5.addWidget(self.txtdeposito)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.tablalibromas = QtGui.QTableView(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tablalibromas.sizePolicy().hasHeightForWidth())
        self.tablalibromas.setSizePolicy(sizePolicy)
        self.tablalibromas.setMinimumSize(QtCore.QSize(0, 50))
        self.tablalibromas.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tablalibromas.setObjectName("tablalibromas")
        self.verticalLayout_4.addWidget(self.tablalibromas)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.lbltotallibro_3 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbltotallibro_3.sizePolicy().hasHeightForWidth())
        self.lbltotallibro_3.setSizePolicy(sizePolicy)
        self.lbltotallibro_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbltotallibro_3.setObjectName("lbltotallibro_3")
        self.horizontalLayout_7.addWidget(self.lbltotallibro_3)
        self.txtcheque = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtcheque.sizePolicy().hasHeightForWidth())
        self.txtcheque.setSizePolicy(sizePolicy)
        self.txtcheque.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtcheque.setReadOnly(True)
        self.txtcheque.setObjectName("txtcheque")
        self.horizontalLayout_7.addWidget(self.txtcheque)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.tablalibromenos = QtGui.QTableView(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tablalibromenos.sizePolicy().hasHeightForWidth())
        self.tablalibromenos.setSizePolicy(sizePolicy)
        self.tablalibromenos.setMinimumSize(QtCore.QSize(0, 50))
        self.tablalibromenos.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tablalibromenos.setObjectName("tablalibromenos")
        self.verticalLayout_4.addWidget(self.tablalibromenos)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.lbltotallibro = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbltotallibro.sizePolicy().hasHeightForWidth())
        self.lbltotallibro.setSizePolicy(sizePolicy)
        self.lbltotallibro.setMinimumSize(QtCore.QSize(0, 8))
        self.lbltotallibro.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbltotallibro.setObjectName("lbltotallibro")
        self.horizontalLayout_10.addWidget(self.lbltotallibro)
        self.txttotallibro = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txttotallibro.sizePolicy().hasHeightForWidth())
        self.txttotallibro.setSizePolicy(sizePolicy)
        self.txttotallibro.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txttotallibro.setReadOnly(True)
        self.txttotallibro.setObjectName("txttotallibro")
        self.horizontalLayout_10.addWidget(self.txttotallibro)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.groupBox_3 = QtGui.QGroupBox(self.splitter)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 240))
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_7 = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.txtsaldolibro = QtGui.QLineEdit(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtsaldolibro.sizePolicy().hasHeightForWidth())
        self.txtsaldolibro.setSizePolicy(sizePolicy)
        self.txtsaldolibro.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtsaldolibro.setReadOnly(True)
        self.txtsaldolibro.setObjectName("txtsaldolibro")
        self.horizontalLayout_3.addWidget(self.txtsaldolibro)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lbltotallibro_4 = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbltotallibro_4.sizePolicy().hasHeightForWidth())
        self.lbltotallibro_4.setSizePolicy(sizePolicy)
        self.lbltotallibro_4.setMinimumSize(QtCore.QSize(0, 8))
        self.lbltotallibro_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbltotallibro_4.setObjectName("lbltotallibro_4")
        self.horizontalLayout_6.addWidget(self.lbltotallibro_4)
        self.txtnotacredito = QtGui.QLineEdit(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtnotacredito.sizePolicy().hasHeightForWidth())
        self.txtnotacredito.setSizePolicy(sizePolicy)
        self.txtnotacredito.setMinimumSize(QtCore.QSize(0, 0))
        self.txtnotacredito.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtnotacredito.setReadOnly(True)
        self.txtnotacredito.setObjectName("txtnotacredito")
        self.horizontalLayout_6.addWidget(self.txtnotacredito)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.tablabancomas = QtGui.QTableView(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tablabancomas.sizePolicy().hasHeightForWidth())
        self.tablabancomas.setSizePolicy(sizePolicy)
        self.tablabancomas.setMinimumSize(QtCore.QSize(0, 50))
        self.tablabancomas.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tablabancomas.setObjectName("tablabancomas")
        self.verticalLayout_5.addWidget(self.tablabancomas)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.lbltotallibro_5 = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbltotallibro_5.sizePolicy().hasHeightForWidth())
        self.lbltotallibro_5.setSizePolicy(sizePolicy)
        self.lbltotallibro_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbltotallibro_5.setObjectName("lbltotallibro_5")
        self.horizontalLayout_8.addWidget(self.lbltotallibro_5)
        self.txtnotadebito = QtGui.QLineEdit(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtnotadebito.sizePolicy().hasHeightForWidth())
        self.txtnotadebito.setSizePolicy(sizePolicy)
        self.txtnotadebito.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtnotadebito.setReadOnly(True)
        self.txtnotadebito.setObjectName("txtnotadebito")
        self.horizontalLayout_8.addWidget(self.txtnotadebito)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)
        self.tablabancomenos = QtGui.QTableView(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tablabancomenos.sizePolicy().hasHeightForWidth())
        self.tablabancomenos.setSizePolicy(sizePolicy)
        self.tablabancomenos.setMinimumSize(QtCore.QSize(0, 50))
        self.tablabancomenos.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tablabancomenos.setObjectName("tablabancomenos")
        self.verticalLayout_5.addWidget(self.tablabancomenos)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.lbltotalbanco = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbltotalbanco.sizePolicy().hasHeightForWidth())
        self.lbltotalbanco.setSizePolicy(sizePolicy)
        self.lbltotalbanco.setMinimumSize(QtCore.QSize(0, 8))
        self.lbltotalbanco.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbltotalbanco.setObjectName("lbltotalbanco")
        self.horizontalLayout_9.addWidget(self.lbltotalbanco)
        self.txttotalbanco = QtGui.QLineEdit(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txttotalbanco.sizePolicy().hasHeightForWidth())
        self.txttotalbanco.setSizePolicy(sizePolicy)
        self.txttotalbanco.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txttotalbanco.setReadOnly(True)
        self.txttotalbanco.setObjectName("txttotalbanco")
        self.horizontalLayout_9.addWidget(self.txttotalbanco)
        self.verticalLayout_5.addLayout(self.horizontalLayout_9)
        self.verticalLayout_6.addWidget(self.splitter_2)
        self.lbldiferencia = QtGui.QLabel(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbldiferencia.sizePolicy().hasHeightForWidth())
        self.lbldiferencia.setSizePolicy(sizePolicy)
        self.lbldiferencia.setMinimumSize(QtCore.QSize(0, 10))
        self.lbldiferencia.setAlignment(QtCore.Qt.AlignCenter)
        self.lbldiferencia.setObjectName("lbldiferencia")
        self.verticalLayout_6.addWidget(self.lbldiferencia)
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
        self.verticalLayout.addWidget(self.tabWidget)
        frmConciliacion.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(frmConciliacion)
        self.statusbar.setObjectName("statusbar")
        frmConciliacion.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(frmConciliacion)
        self.toolBar.setObjectName("toolBar")
        frmConciliacion.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.label_4.setBuddy(self.txtSearch)

        self.retranslateUi(frmConciliacion)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(frmConciliacion)
        frmConciliacion.setTabOrder(self.tablenavigation, self.txtSearch)

    def retranslateUi(self, frmConciliacion):
        frmConciliacion.setWindowTitle(QtGui.QApplication.translate("frmConciliacion", "Conciliacion Bancaria", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("frmConciliacion", "Libro Mayor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmConciliacion", "Banco", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("frmConciliacion", "Cuenta Bancaria", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("frmConciliacion", "Moneda", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("frmConciliacion", "Cuenta Contable", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNotasCD.setToolTip(QtGui.QApplication.translate("frmConciliacion", "Agregar notas de crédito o débito", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNotasCD.setShortcut(QtGui.QApplication.translate("frmConciliacion", "Ctrl+A", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("frmConciliacion", "Libro", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("frmConciliacion", "Saldo del banco", None, QtGui.QApplication.UnicodeUTF8))
        self.lbltotallibro_2.setText(QtGui.QApplication.translate("frmConciliacion", "MÁS: DEPOSITOS EN TRANSITO", None, QtGui.QApplication.UnicodeUTF8))
        self.lbltotallibro_3.setText(QtGui.QApplication.translate("frmConciliacion", "MENOS: CHEQUES EN  EN TRANSITO", None, QtGui.QApplication.UnicodeUTF8))
        self.lbltotallibro.setText(QtGui.QApplication.translate("frmConciliacion", "Total Disponible:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("frmConciliacion", "Banco", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("frmConciliacion", "Saldo del auxiliar de la empresa", None, QtGui.QApplication.UnicodeUTF8))
        self.lbltotallibro_4.setText(QtGui.QApplication.translate("frmConciliacion", "MÁS: NOTAS DE CREDITO", None, QtGui.QApplication.UnicodeUTF8))
        self.lbltotallibro_5.setText(QtGui.QApplication.translate("frmConciliacion", "MENOS: NOTAS DE DEBITO", None, QtGui.QApplication.UnicodeUTF8))
        self.lbltotalbanco.setText(QtGui.QApplication.translate("frmConciliacion", "Total Disponible:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbldiferencia.setText(QtGui.QApplication.translate("frmConciliacion", "Diferencia C$ 0.0000", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabdetails), None)
        self.label_4.setText(QtGui.QApplication.translate("frmConciliacion", "&Buscar", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabnavigation), None)
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("frmConciliacion", "toolBar", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmConciliacion = QtGui.QMainWindow()
    ui = Ui_frmConciliacion()
    ui.setupUi(frmConciliacion)
    frmConciliacion.show()
    sys.exit(app.exec_())

