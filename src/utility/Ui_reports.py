# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/armonge/workspace/EsquipulasPy/utility/reports.ui'
#
# Created: Tue May 18 09:48:41 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmReportes(object):
    def setupUi(self, frmReportes):
        frmReportes.setObjectName("frmReportes")
        frmReportes.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmReportes.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(frmReportes)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.webView = QtWebKit.QWebView(self.centralwidget)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.horizontalLayout.addWidget(self.webView)
        self.verticalSlider = QtGui.QSlider(self.centralwidget)
        self.verticalSlider.setMinimum(1)
        self.verticalSlider.setMaximum(10)
        self.verticalSlider.setSingleStep(1)
        self.verticalSlider.setPageStep(1)
        self.verticalSlider.setProperty("value", 5)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setInvertedControls(True)
        self.verticalSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.verticalSlider.setTickInterval(1)
        self.verticalSlider.setObjectName("verticalSlider")
        self.horizontalLayout.addWidget(self.verticalSlider)
        frmReportes.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(frmReportes)
        self.statusbar.setObjectName("statusbar")
        frmReportes.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(frmReportes)
        self.toolBar.setObjectName("toolBar")
        frmReportes.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.actionPrint = QtGui.QAction(frmReportes)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/res/document-print.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrint.setIcon(icon1)
        self.actionPrint.setObjectName("actionPrint")
        self.actionCopy = QtGui.QAction(frmReportes)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/res/edit-copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(icon2)
        self.actionCopy.setObjectName("actionCopy")
        self.actionCut = QtGui.QAction(frmReportes)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/res/edit-cut.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCut.setIcon(icon3)
        self.actionCut.setObjectName("actionCut")
        self.actionPaste = QtGui.QAction(frmReportes)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/res/edit-paste.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaste.setIcon(icon4)
        self.actionPaste.setObjectName("actionPaste")
        self.toolBar.addAction(self.actionPrint)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCopy)
        self.toolBar.addAction(self.actionPaste)
        self.toolBar.addAction(self.actionCut)
        self.toolBar.addSeparator()

        self.retranslateUi(frmReportes)
        QtCore.QMetaObject.connectSlotsByName(frmReportes)

    def retranslateUi(self, frmReportes):
        frmReportes.setWindowTitle(QtGui.QApplication.translate("frmReportes", "Reporte", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("frmReportes", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPrint.setText(QtGui.QApplication.translate("frmReportes", "Imprimir", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPrint.setShortcut(QtGui.QApplication.translate("frmReportes", "Ctrl+P", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setText(QtGui.QApplication.translate("frmReportes", "Copiar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setShortcut(QtGui.QApplication.translate("frmReportes", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setText(QtGui.QApplication.translate("frmReportes", "Cortar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setShortcut(QtGui.QApplication.translate("frmReportes", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setText(QtGui.QApplication.translate("frmReportes", "Pegar", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
