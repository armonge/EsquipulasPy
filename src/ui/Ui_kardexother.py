# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/kardexother.ui'
#
# Created by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmKardexOther(object):
    def setupUi(self, frmKardexOther):
        frmKardexOther.setObjectName("frmKardexOther")
        frmKardexOther.resize(644, 600)
        self.centralwidget = QtGui.QWidget(frmKardexOther)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        self.tabdetails = QtGui.QWidget()
        self.tabdetails.setObjectName("tabdetails")
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.tabdetails)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_2 = QtGui.QLabel(self.tabdetails)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        self.txtPrintedDocumentNumber = QtGui.QLineEdit(self.tabdetails)
        self.txtPrintedDocumentNumber.setReadOnly(True)
        self.txtPrintedDocumentNumber.setObjectName("txtPrintedDocumentNumber")
        self.horizontalLayout_6.addWidget(self.txtPrintedDocumentNumber)
        self.label_5 = QtGui.QLabel(self.tabdetails)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.dtPicker = QtGui.QDateTimeEdit(self.tabdetails)
        self.dtPicker.setReadOnly(True)
        self.dtPicker.setCalendarPopup(True)
        self.dtPicker.setObjectName("dtPicker")
        self.horizontalLayout_6.addWidget(self.dtPicker)
        self.verticalLayout_8.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtGui.QLabel(self.tabdetails)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.swConcept = QtGui.QStackedWidget(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.swConcept.sizePolicy().hasHeightForWidth())
        self.swConcept.setSizePolicy(sizePolicy)
        self.swConcept.setObjectName("swConcept")
        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName("page_3")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.page_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.txtConcept = QtGui.QLineEdit(self.page_3)
        self.txtConcept.setReadOnly(True)
        self.txtConcept.setObjectName("txtConcept")
        self.horizontalLayout_3.addWidget(self.txtConcept)
        self.swConcept.addWidget(self.page_3)
        self.page_4 = QtGui.QWidget()
        self.page_4.setObjectName("page_4")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.page_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.cbConcept = QtGui.QComboBox(self.page_4)
        self.cbConcept.setEditable(True)
        self.cbConcept.setObjectName("cbConcept")
        self.verticalLayout_3.addWidget(self.cbConcept)
        self.swConcept.addWidget(self.page_4)
        self.horizontalLayout_2.addWidget(self.swConcept)
        self.label_4 = QtGui.QLabel(self.tabdetails)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.swWarehouse = QtGui.QStackedWidget(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.swWarehouse.sizePolicy().hasHeightForWidth())
        self.swWarehouse.setSizePolicy(sizePolicy)
        self.swWarehouse.setObjectName("swWarehouse")
        self.page_5 = QtGui.QWidget()
        self.page_5.setObjectName("page_5")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.page_5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.txtWarehouse = QtGui.QLineEdit(self.page_5)
        self.txtWarehouse.setReadOnly(True)
        self.txtWarehouse.setObjectName("txtWarehouse")
        self.verticalLayout_5.addWidget(self.txtWarehouse)
        self.swWarehouse.addWidget(self.page_5)
        self.page_6 = QtGui.QWidget()
        self.page_6.setObjectName("page_6")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.page_6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.cbWarehouse = QtGui.QComboBox(self.page_6)
        self.cbWarehouse.setEditable(True)
        self.cbWarehouse.setObjectName("cbWarehouse")
        self.verticalLayout_4.addWidget(self.cbWarehouse)
        self.swWarehouse.addWidget(self.page_6)
        self.horizontalLayout_2.addWidget(self.swWarehouse)
        self.verticalLayout_8.addLayout(self.horizontalLayout_2)
        self.splitter_2 = QtGui.QSplitter(self.tabdetails)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setOpaqueResize(True)
        self.splitter_2.setChildrenCollapsible(False)
        self.splitter_2.setObjectName("splitter_2")
        self.tabledetails = QtGui.QTableView(self.splitter_2)
        self.tabledetails.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tabledetails.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tabledetails.setAlternatingRowColors(True)
        self.tabledetails.setObjectName("tabledetails")
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_6 = QtGui.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_7.addWidget(self.label_6)
        self.txtObservations = QtGui.QPlainTextEdit(self.layoutWidget)
        self.txtObservations.setObjectName("txtObservations")
        self.verticalLayout_7.addWidget(self.txtObservations)
        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lblaccounts = QtGui.QLabel(self.layoutWidget1)
        self.lblaccounts.setObjectName("lblaccounts")
        self.verticalLayout_6.addWidget(self.lblaccounts)
        self.tableaccounts = QtGui.QTableView(self.layoutWidget1)
        self.tableaccounts.setObjectName("tableaccounts")
        self.verticalLayout_6.addWidget(self.tableaccounts)
        self.verticalLayout_8.addWidget(self.splitter_2)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/document-edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabdetails, icon, "")
        self.tabnavigation = QtGui.QWidget()
        self.tabnavigation.setObjectName("tabnavigation")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabnavigation)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tablenavigation = QtGui.QTableView(self.tabnavigation)
        self.tablenavigation.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tablenavigation.setAlternatingRowColors(True)
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
        self.lineEdit = QtGui.QLineEdit(self.tabnavigation)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/res/table.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabnavigation, icon1, "")
        self.verticalLayout.addWidget(self.tabWidget)
        frmKardexOther.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(frmKardexOther)
        self.statusbar.setObjectName("statusbar")
        frmKardexOther.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(frmKardexOther)
        self.toolBar.setObjectName("toolBar")
        frmKardexOther.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.label_2.setBuddy(self.txtPrintedDocumentNumber)
        self.label_5.setBuddy(self.dtPicker)
        self.label_3.setBuddy(self.cbConcept)
        self.label_4.setBuddy(self.cbWarehouse)
        self.label_6.setBuddy(self.txtObservations)
        self.lblaccounts.setBuddy(self.tableaccounts)
        self.label.setBuddy(self.lineEdit)

        self.retranslateUi(frmKardexOther)
        self.tabWidget.setCurrentIndex(1)
        self.swConcept.setCurrentIndex(0)
        self.swWarehouse.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(frmKardexOther)
        frmKardexOther.setTabOrder(self.txtPrintedDocumentNumber, self.dtPicker)
        frmKardexOther.setTabOrder(self.dtPicker, self.cbConcept)
        frmKardexOther.setTabOrder(self.cbConcept, self.cbWarehouse)
        frmKardexOther.setTabOrder(self.cbWarehouse, self.tabledetails)
        frmKardexOther.setTabOrder(self.tabledetails, self.txtObservations)
        frmKardexOther.setTabOrder(self.txtObservations, self.tableaccounts)
        frmKardexOther.setTabOrder(self.tableaccounts, self.tabWidget)
        frmKardexOther.setTabOrder(self.tabWidget, self.txtWarehouse)
        frmKardexOther.setTabOrder(self.txtWarehouse, self.txtConcept)
        frmKardexOther.setTabOrder(self.txtConcept, self.tablenavigation)
        frmKardexOther.setTabOrder(self.tablenavigation, self.lineEdit)

    def retranslateUi(self, frmKardexOther):
        frmKardexOther.setWindowTitle(QtGui.QApplication.translate("frmKardexOther", "Otros Movimientos de Kardex", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("frmKardexOther", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">&amp;Numero de Ajuste de Bodega:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("frmKardexOther", "<b>&Fecha</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("frmKardexOther", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">&amp;Concepto:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("frmKardexOther", "<b>&Bodega</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("frmKardexOther", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Comentario&amp;s</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lblaccounts.setText(QtGui.QApplication.translate("frmKardexOther", "<b>&Movimientos</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabdetails), None)
        self.label.setText(QtGui.QApplication.translate("frmKardexOther", "&Buscar", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabnavigation), None)
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("frmKardexOther", "toolBar", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmKardexOther = QtGui.QMainWindow()
    ui = Ui_frmKardexOther()
    ui.setupUi(frmKardexOther)
    frmKardexOther.show()
    sys.exit(app.exec_())

