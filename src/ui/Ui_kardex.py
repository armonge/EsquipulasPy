# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/kardex.ui'
#
# Created: Fri Jul 23 16:23:53 2010
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmKardex(object):
    def setupUi(self, frmKardex):
        frmKardex.setObjectName("frmKardex")
        frmKardex.resize(800, 600)
        self.centralwidget = QtGui.QWidget(frmKardex)
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
        self.label_3 = QtGui.QLabel(self.tabdetails)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.txtParentPrintedDocumentNumber = QtGui.QLineEdit(self.tabdetails)
        self.txtParentPrintedDocumentNumber.setReadOnly(True)
        self.txtParentPrintedDocumentNumber.setObjectName("txtParentPrintedDocumentNumber")
        self.horizontalLayout_2.addWidget(self.txtParentPrintedDocumentNumber)
        self.label_6 = QtGui.QLabel(self.tabdetails)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.txtPrintedDocumentNumber = QtGui.QLineEdit(self.tabdetails)
        self.txtPrintedDocumentNumber.setReadOnly(True)
        self.txtPrintedDocumentNumber.setObjectName("txtPrintedDocumentNumber")
        self.horizontalLayout_2.addWidget(self.txtPrintedDocumentNumber)
        self.label_7 = QtGui.QLabel(self.tabdetails)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.txtWarehouse = QtGui.QLineEdit(self.tabdetails)
        self.txtWarehouse.setReadOnly(True)
        self.txtWarehouse.setObjectName("txtWarehouse")
        self.horizontalLayout_2.addWidget(self.txtWarehouse)
        self.label_2 = QtGui.QLabel(self.tabdetails)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.dtPicker = QtGui.QDateTimeEdit(self.tabdetails)
        self.dtPicker.setReadOnly(True)
        self.dtPicker.setCalendarPopup(True)
        self.dtPicker.setObjectName("dtPicker")
        self.horizontalLayout_2.addWidget(self.dtPicker)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 2)
        self.tabledetails = QtGui.QTableView(self.tabdetails)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.tabledetails.sizePolicy().hasHeightForWidth())
        self.tabledetails.setSizePolicy(sizePolicy)
        self.tabledetails.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tabledetails.setObjectName("tabledetails")
        self.tabledetails.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tabledetails, 1, 0, 1, 2)
        self.label_5 = QtGui.QLabel(self.tabdetails)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 1, 1, 1)
        self.txtKardexObservation = QtGui.QPlainTextEdit(self.tabdetails)
        self.txtKardexObservation.setReadOnly(True)
        self.txtKardexObservation.setObjectName("txtKardexObservation")
        self.gridLayout.addWidget(self.txtKardexObservation, 4, 0, 1, 1)
        self.txtDocObservation = QtGui.QPlainTextEdit(self.tabdetails)
        self.txtDocObservation.setReadOnly(True)
        self.txtDocObservation.setObjectName("txtDocObservation")
        self.gridLayout.addWidget(self.txtDocObservation, 4, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.tabdetails)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/document-edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabdetails, icon, "")
        self.tabnavigation = QtGui.QWidget()
        self.tabnavigation.setObjectName("tabnavigation")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabnavigation)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tablenavigation = QtGui.QTableView(self.tabnavigation)
        self.tablenavigation.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tablenavigation.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tablenavigation.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tablenavigation.setSortingEnabled(True)
        self.tablenavigation.setObjectName("tablenavigation")
        self.tablenavigation.horizontalHeader().setStretchLastSection(True)
        self.tablenavigation.verticalHeader().setVisible(False)
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
        frmKardex.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(frmKardex)
        self.statusbar.setObjectName("statusbar")
        frmKardex.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(frmKardex)
        self.toolBar.setObjectName("toolBar")
        frmKardex.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.actionNew = QtGui.QAction(frmKardex)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/res/document-new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon2)
        self.actionNew.setObjectName("actionNew")
        self.actionPreview = QtGui.QAction(frmKardex)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/res/document-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPreview.setIcon(icon3)
        self.actionPreview.setObjectName("actionPreview")
        self.actionGoFirst = QtGui.QAction(frmKardex)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/res/go-first.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGoFirst.setIcon(icon4)
        self.actionGoFirst.setObjectName("actionGoFirst")
        self.actionGoPrevious = QtGui.QAction(frmKardex)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/res/go-previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGoPrevious.setIcon(icon5)
        self.actionGoPrevious.setObjectName("actionGoPrevious")
        self.actionGoNext = QtGui.QAction(frmKardex)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/res/go-next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGoNext.setIcon(icon6)
        self.actionGoNext.setObjectName("actionGoNext")
        self.actionGoLast = QtGui.QAction(frmKardex)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/res/go-last.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGoLast.setIcon(icon7)
        self.actionGoLast.setObjectName("actionGoLast")
        self.actionSave = QtGui.QAction(frmKardex)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/res/document-save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon8)
        self.actionSave.setObjectName("actionSave")
        self.actionPrint = QtGui.QAction(frmKardex)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/res/document-print.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrint.setIcon(icon9)
        self.actionPrint.setObjectName("actionPrint")
        self.actionCancel = QtGui.QAction(frmKardex)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/res/dialog-cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCancel.setIcon(icon10)
        self.actionCancel.setObjectName("actionCancel")
        self.actionEditar = QtGui.QAction(frmKardex)
        self.actionEditar.setIcon(icon)
        self.actionEditar.setObjectName("actionEditar")
        self.actionDelete = QtGui.QAction(frmKardex)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/res/edit-delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon11)
        self.actionDelete.setObjectName("actionDelete")
        self.actionCopy = QtGui.QAction(frmKardex)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/res/edit-copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(icon12)
        self.actionCopy.setObjectName("actionCopy")
        self.actionCut = QtGui.QAction(frmKardex)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/icons/res/edit-cut.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCut.setIcon(icon13)
        self.actionCut.setObjectName("actionCut")
        self.actionPaste = QtGui.QAction(frmKardex)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/icons/res/edit-paste.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaste.setIcon(icon14)
        self.actionPaste.setObjectName("actionPaste")
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionCancel)
        self.toolBar.addAction(self.actionPreview)
        self.toolBar.addAction(self.actionPrint)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCopy)
        self.toolBar.addAction(self.actionPaste)
        self.toolBar.addAction(self.actionCut)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionGoFirst)
        self.toolBar.addAction(self.actionGoPrevious)
        self.toolBar.addAction(self.actionGoNext)
        self.toolBar.addAction(self.actionGoLast)
        self.label_2.setBuddy(self.dtPicker)
        self.label.setBuddy(self.lineEdit)

        self.retranslateUi(frmKardex)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(frmKardex)

    def retranslateUi(self, frmKardex):
        frmKardex.setWindowTitle(QtGui.QApplication.translate("frmKardex", "Kardex", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("frmKardex", "Documento: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("frmKardex", "Kardex: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("frmKardex", "Bodega", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("frmKardex", "&Fecha", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("frmKardex", "Observaciones del Documento", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("frmKardex", "Observaciones de Kardex", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabdetails), None)
        self.label.setText(QtGui.QApplication.translate("frmKardex", "&Buscar", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabnavigation), None)
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("frmKardex", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setText(QtGui.QApplication.translate("frmKardex", "Confirmar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setToolTip(QtGui.QApplication.translate("frmKardex", "Confirmar el documento", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setShortcut(QtGui.QApplication.translate("frmKardex", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreview.setText(QtGui.QApplication.translate("frmKardex", "Previsualizar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoFirst.setText(QtGui.QApplication.translate("frmKardex", "Ir al Primer Registro", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoPrevious.setText(QtGui.QApplication.translate("frmKardex", "Ir al Registro Anterior", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoNext.setText(QtGui.QApplication.translate("frmKardex", "Ir al siguiente registro", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoLast.setText(QtGui.QApplication.translate("frmKardex", "Ir al ultimo registro", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("frmKardex", "Guardar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPrint.setText(QtGui.QApplication.translate("frmKardex", "Imprimir", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCancel.setText(QtGui.QApplication.translate("frmKardex", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditar.setText(QtGui.QApplication.translate("frmKardex", "Editar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditar.setShortcut(QtGui.QApplication.translate("frmKardex", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete.setText(QtGui.QApplication.translate("frmKardex", "Borrar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setText(QtGui.QApplication.translate("frmKardex", "Copiar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setShortcut(QtGui.QApplication.translate("frmKardex", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setText(QtGui.QApplication.translate("frmKardex", "Cortar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setShortcut(QtGui.QApplication.translate("frmKardex", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setText(QtGui.QApplication.translate("frmKardex", "Pegar", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmKardex = QtGui.QMainWindow()
    ui = Ui_frmKardex()
    ui.setupUi(frmKardex)
    frmKardex.show()
    sys.exit(app.exec_())

