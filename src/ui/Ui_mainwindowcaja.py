# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/mainwindowcaja.ui'
#
# Created: Sat Aug  7 00:14:32 2010
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(1151, 713)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mdiArea = QtGui.QMdiArea(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mdiArea.sizePolicy().hasHeightForWidth())
        self.mdiArea.setSizePolicy(sizePolicy)
        self.mdiArea.setViewMode(QtGui.QMdiArea.TabbedView)
        self.mdiArea.setTabShape(QtGui.QTabWidget.Rounded)
        self.mdiArea.setTabPosition(QtGui.QTabWidget.North)
        self.mdiArea.setObjectName("mdiArea")
        self.horizontalLayout.addWidget(self.mdiArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtGui.QDockWidget(MainWindow)
        self.dockWidget.setMinimumSize(QtCore.QSize(230, 175))
        self.dockWidget.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolBox = QtGui.QToolBox(self.dockWidgetContents_2)
        self.toolBox.setEnabled(True)
        self.toolBox.setObjectName("toolBox")
        self.page = QtGui.QWidget()
        self.page.setEnabled(True)
        self.page.setGeometry(QtCore.QRect(0, 0, 214, 567))
        self.page.setObjectName("page")
        self.gridLayout = QtGui.QGridLayout(self.page)
        self.gridLayout.setObjectName("gridLayout")
        self.btnClients = QtGui.QPushButton(self.page)
        self.btnClients.setEnabled(False)
        self.btnClients.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.btnClients.setFont(font)
        self.btnClients.setAutoFillBackground(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/res/preferences-desktop-personal.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnClients.setIcon(icon1)
        self.btnClients.setIconSize(QtCore.QSize(64, 64))
        self.btnClients.setFlat(False)
        self.btnClients.setObjectName("btnClients")
        self.gridLayout.addWidget(self.btnClients, 0, 0, 1, 1)
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtGui.QWidget()
        self.page_2.setEnabled(True)
        self.page_2.setGeometry(QtCore.QRect(0, 0, 214, 567))
        self.page_2.setObjectName("page_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.page_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btnApertura = QtGui.QPushButton(self.page_2)
        self.btnApertura.setEnabled(True)
        self.btnApertura.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.btnApertura.setFont(font)
        self.btnApertura.setAutoFillBackground(False)
        self.btnApertura.setIconSize(QtCore.QSize(64, 64))
        self.btnApertura.setFlat(False)
        self.btnApertura.setObjectName("btnApertura")
        self.verticalLayout_2.addWidget(self.btnApertura)
        self.btnfactura = QtGui.QPushButton(self.page_2)
        self.btnfactura.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnfactura.sizePolicy().hasHeightForWidth())
        self.btnfactura.setSizePolicy(sizePolicy)
        self.btnfactura.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.btnfactura.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/res/simbolo-dolar-300x245.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnfactura.setIcon(icon2)
        self.btnfactura.setIconSize(QtCore.QSize(64, 64))
        self.btnfactura.setFlat(False)
        self.btnfactura.setObjectName("btnfactura")
        self.verticalLayout_2.addWidget(self.btnfactura)
        self.btnAnnulments = QtGui.QPushButton(self.page_2)
        self.btnAnnulments.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAnnulments.sizePolicy().hasHeightForWidth())
        self.btnAnnulments.setSizePolicy(sizePolicy)
        self.btnAnnulments.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.btnAnnulments.setFont(font)
        self.btnAnnulments.setIconSize(QtCore.QSize(64, 64))
        self.btnAnnulments.setFlat(False)
        self.btnAnnulments.setObjectName("btnAnnulments")
        self.verticalLayout_2.addWidget(self.btnAnnulments)
        self.btnrecibo = QtGui.QPushButton(self.page_2)
        self.btnrecibo.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnrecibo.sizePolicy().hasHeightForWidth())
        self.btnrecibo.setSizePolicy(sizePolicy)
        self.btnrecibo.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.btnrecibo.setFont(font)
        self.btnrecibo.setIconSize(QtCore.QSize(32, 32))
        self.btnrecibo.setFlat(False)
        self.btnrecibo.setObjectName("btnrecibo")
        self.verticalLayout_2.addWidget(self.btnrecibo)
        self.btnArqueo = QtGui.QPushButton(self.page_2)
        self.btnArqueo.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnArqueo.sizePolicy().hasHeightForWidth())
        self.btnArqueo.setSizePolicy(sizePolicy)
        self.btnArqueo.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.btnArqueo.setFont(font)
        self.btnArqueo.setIcon(icon2)
        self.btnArqueo.setIconSize(QtCore.QSize(64, 64))
        self.btnArqueo.setFlat(False)
        self.btnArqueo.setObjectName("btnArqueo")
        self.verticalLayout_2.addWidget(self.btnArqueo)
        self.toolBox.addItem(self.page_2, "")
        self.verticalLayout.addWidget(self.toolBox)
        self.dockWidget.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.actionLockSession = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/res/object-locked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLockSession.setIcon(icon3)
        self.actionLockSession.setObjectName("actionLockSession")
        self.actionUnlockSession = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/res/object-unlocked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUnlockSession.setIcon(icon4)
        self.actionUnlockSession.setVisible(False)
        self.actionUnlockSession.setObjectName("actionUnlockSession")
        self.toolBar.addAction(self.actionLockSession)
        self.toolBar.addAction(self.actionUnlockSession)

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Llantera Esquipulas Caja", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Caja", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClients.setText(QtGui.QApplication.translate("MainWindow", "Clientes", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QtGui.QApplication.translate("MainWindow", "Catalogos", None, QtGui.QApplication.UnicodeUTF8))
        self.btnApertura.setText(QtGui.QApplication.translate("MainWindow", "Apertura de Caja", None, QtGui.QApplication.UnicodeUTF8))
        self.btnApertura.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+1", None, QtGui.QApplication.UnicodeUTF8))
        self.btnfactura.setText(QtGui.QApplication.translate("MainWindow", "Facturas", None, QtGui.QApplication.UnicodeUTF8))
        self.btnfactura.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+2", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAnnulments.setText(QtGui.QApplication.translate("MainWindow", "Anulaciones \n"
"de Factura", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAnnulments.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+3", None, QtGui.QApplication.UnicodeUTF8))
        self.btnrecibo.setText(QtGui.QApplication.translate("MainWindow", "Recibos", None, QtGui.QApplication.UnicodeUTF8))
        self.btnrecibo.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+4", None, QtGui.QApplication.UnicodeUTF8))
        self.btnArqueo.setText(QtGui.QApplication.translate("MainWindow", "Arqueo", None, QtGui.QApplication.UnicodeUTF8))
        self.btnArqueo.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+5", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QtGui.QApplication.translate("MainWindow", "Movimientos", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLockSession.setText(QtGui.QApplication.translate("MainWindow", "Bloquear Sesión", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUnlockSession.setText(QtGui.QApplication.translate("MainWindow", "Desbloquear Sesión", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

