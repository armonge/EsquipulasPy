# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/mainwindowinventario.ui'
#
# Created: Mon Aug 30 13:15:33 2010
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
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.mdiArea = QtGui.QMdiArea(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mdiArea.sizePolicy().hasHeightForWidth())
        self.mdiArea.setSizePolicy(sizePolicy)
        brush = QtGui.QBrush(QtGui.QColor(121, 116, 113))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.mdiArea.setBackground(brush)
        self.mdiArea.setViewMode(QtGui.QMdiArea.TabbedView)
        self.mdiArea.setTabShape(QtGui.QTabWidget.Rounded)
        self.mdiArea.setTabPosition(QtGui.QTabWidget.North)
        self.mdiArea.setObjectName("mdiArea")
        self.gridLayout.addWidget(self.mdiArea, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtGui.QDockWidget(MainWindow)
        self.dockWidget.setMinimumSize(QtCore.QSize(230, 183))
        self.dockWidget.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolBox = QtGui.QToolBox(self.dockWidgetContents_2)
        self.toolBox.setObjectName("toolBox")
        self.page_2 = QtGui.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 214, 541))
        self.page_2.setObjectName("page_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.page_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btnLiquidations = QtGui.QPushButton(self.page_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnLiquidations.sizePolicy().hasHeightForWidth())
        self.btnLiquidations.setSizePolicy(sizePolicy)
        self.btnLiquidations.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.btnLiquidations.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/res/simbolo-dolar-300x245.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnLiquidations.setIcon(icon1)
        self.btnLiquidations.setIconSize(QtCore.QSize(64, 64))
        self.btnLiquidations.setFlat(False)
        self.btnLiquidations.setObjectName("btnLiquidations")
        self.verticalLayout_2.addWidget(self.btnLiquidations)
        self.btnEntries = QtGui.QPushButton(self.page_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnEntries.sizePolicy().hasHeightForWidth())
        self.btnEntries.setSizePolicy(sizePolicy)
        self.btnEntries.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.btnEntries.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/res/skrooge_merge_import2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnEntries.setIcon(icon2)
        self.btnEntries.setIconSize(QtCore.QSize(64, 64))
        self.btnEntries.setFlat(False)
        self.btnEntries.setObjectName("btnEntries")
        self.verticalLayout_2.addWidget(self.btnEntries)
        self.toolBox.addItem(self.page_2, "")
        self.widget = QtGui.QWidget()
        self.widget.setGeometry(QtCore.QRect(0, 0, 143, 226))
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btnKEntries = QtGui.QPushButton(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnKEntries.sizePolicy().hasHeightForWidth())
        self.btnKEntries.setSizePolicy(sizePolicy)
        self.btnKEntries.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.btnKEntries.setFont(font)
        self.btnKEntries.setIconSize(QtCore.QSize(64, 64))
        self.btnKEntries.setFlat(False)
        self.btnKEntries.setObjectName("btnKEntries")
        self.verticalLayout_3.addWidget(self.btnKEntries)
        self.btnKExits = QtGui.QPushButton(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnKExits.sizePolicy().hasHeightForWidth())
        self.btnKExits.setSizePolicy(sizePolicy)
        self.btnKExits.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.btnKExits.setFont(font)
        self.btnKExits.setIconSize(QtCore.QSize(64, 64))
        self.btnKExits.setFlat(False)
        self.btnKExits.setObjectName("btnKExits")
        self.verticalLayout_3.addWidget(self.btnKExits)
        self.btnKOther = QtGui.QPushButton(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnKOther.sizePolicy().hasHeightForWidth())
        self.btnKOther.setSizePolicy(sizePolicy)
        self.btnKOther.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.btnKOther.setFont(font)
        self.btnKOther.setIconSize(QtCore.QSize(64, 64))
        self.btnKOther.setFlat(False)
        self.btnKOther.setObjectName("btnKOther")
        self.verticalLayout_3.addWidget(self.btnKOther)
        self.toolBox.addItem(self.widget, "")
        self.page = QtGui.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 190, 300))
        self.page.setObjectName("page")
        self.gridLayout_2 = QtGui.QGridLayout(self.page)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btnArticles = QtGui.QPushButton(self.page)
        self.btnArticles.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.btnArticles.setFont(font)
        self.btnArticles.setAutoFillBackground(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/res/llanta.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnArticles.setIcon(icon3)
        self.btnArticles.setIconSize(QtCore.QSize(64, 64))
        self.btnArticles.setFlat(False)
        self.btnArticles.setObjectName("btnArticles")
        self.gridLayout_2.addWidget(self.btnArticles, 0, 0, 1, 1)
        self.btnCategories = QtGui.QPushButton(self.page)
        self.btnCategories.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.btnCategories.setFont(font)
        self.btnCategories.setAutoFillBackground(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/images/res/estante.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCategories.setIcon(icon4)
        self.btnCategories.setIconSize(QtCore.QSize(64, 64))
        self.btnCategories.setFlat(False)
        self.btnCategories.setObjectName("btnCategories")
        self.gridLayout_2.addWidget(self.btnCategories, 1, 0, 1, 1)
        self.btnBrands = QtGui.QPushButton(self.page)
        self.btnBrands.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.btnBrands.setFont(font)
        self.btnBrands.setAutoFillBackground(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/images/res/marca.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnBrands.setIcon(icon5)
        self.btnBrands.setIconSize(QtCore.QSize(64, 64))
        self.btnBrands.setFlat(False)
        self.btnBrands.setObjectName("btnBrands")
        self.gridLayout_2.addWidget(self.btnBrands, 2, 0, 1, 1)
        self.btnProviders = QtGui.QPushButton(self.page)
        self.btnProviders.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.btnProviders.setFont(font)
        self.btnProviders.setAutoFillBackground(False)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/images/res/resource-group.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnProviders.setIcon(icon6)
        self.btnProviders.setIconSize(QtCore.QSize(64, 64))
        self.btnProviders.setFlat(False)
        self.btnProviders.setObjectName("btnProviders")
        self.gridLayout_2.addWidget(self.btnProviders, 3, 0, 1, 1)
        self.toolBox.addItem(self.page, "")
        self.verticalLayout.addWidget(self.toolBox)
        self.dockWidget.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.actionLockSession = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/res/object-locked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLockSession.setIcon(icon7)
        self.actionLockSession.setObjectName("actionLockSession")
        self.actionUnlockSession = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/res/object-unlocked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUnlockSession.setIcon(icon8)
        self.actionUnlockSession.setVisible(False)
        self.actionUnlockSession.setObjectName("actionUnlockSession")
        self.toolBar.addAction(self.actionLockSession)
        self.toolBar.addAction(self.actionUnlockSession)

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Llantera Esquipulas Inventario", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Inventario", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLiquidations.setText(QtGui.QApplication.translate("MainWindow", "Liquidaciones", None, QtGui.QApplication.UnicodeUTF8))
        self.btnEntries.setText(QtGui.QApplication.translate("MainWindow", "Entradas", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QtGui.QApplication.translate("MainWindow", "Movimientos", None, QtGui.QApplication.UnicodeUTF8))
        self.btnKEntries.setText(QtGui.QApplication.translate("MainWindow", "Entradas\n"
"Locales,\n"
"Importaciones y\n"
"Devoluciones", None, QtGui.QApplication.UnicodeUTF8))
        self.btnKExits.setText(QtGui.QApplication.translate("MainWindow", "Salida por\n"
"Factura", None, QtGui.QApplication.UnicodeUTF8))
        self.btnKOther.setText(QtGui.QApplication.translate("MainWindow", "Otros\n"
"Movimientos", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.widget), QtGui.QApplication.translate("MainWindow", "Kardex", None, QtGui.QApplication.UnicodeUTF8))
        self.btnArticles.setText(QtGui.QApplication.translate("MainWindow", "Articulos", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCategories.setText(QtGui.QApplication.translate("MainWindow", "Categorias", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrands.setText(QtGui.QApplication.translate("MainWindow", "Marcas", None, QtGui.QApplication.UnicodeUTF8))
        self.btnProviders.setText(QtGui.QApplication.translate("MainWindow", "Proveedores", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QtGui.QApplication.translate("MainWindow", "Catalogos", None, QtGui.QApplication.UnicodeUTF8))
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

