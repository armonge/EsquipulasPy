# -*- coding: utf-8 -*-
'''
Created on 11/06/2010

@author: Andrés Reyes Monge
'''
from PyQt4.QtCore import SIGNAL, QSettings, pyqtSlot, QSize, QUrl
from PyQt4.QtGui import QDialog, QMessageBox, QIcon, QWidget, QVBoxLayout, \
QPushButton, qApp, QDesktopServices, QMdiSubWindow, qApp
from PyQt4.QtSql import QSqlDatabase

import utility.user

class MainWindowBase( object ):
    '''
    classdocs
    '''
    def __init__( self ):
        '''
        Constructor
        '''
        
        self.user = utility.user.LoggedUser
        
        dockaction  = self.dockWidget.toggleViewAction()
        dockaction.setIcon(QIcon(":/icons/res/utilities-desktop-extra.png"))
        self.toolBar.addAction(dockaction)
        
        
        self.woptions = QWidget()
        
        self.btnPasswd = QPushButton(QIcon(":/images/res/dialog-password.png"),u"Cambiar\nContraseña")
        self.btnPasswd.setMinimumSize(QSize(0, 70))
        self.btnPasswd.setIconSize(QSize(64, 64))
        
        self.btnHelp = QPushButton( QIcon(":/images/res/system-help.png"), u"Ayuda")
        self.btnHelp.setMinimumSize(QSize(0, 70))
        self.btnHelp.setIconSize(QSize(64, 64))
        
        self.btnAbout = QPushButton(QIcon(":/images/res/help-about.png"), "Acerca de")
        self.btnAbout.setMinimumSize(QSize(0, 70))
        self.btnAbout.setIconSize(QSize(64, 64))

        self.btnLogOut = QPushButton(u"Cerrar Sesión")
        self.btnLogOut.setMinimumSize(QSize(0, 70))
        self.btnLogOut.setIconSize(QSize(64, 64))        
        
        
        layout = QVBoxLayout()
        layout.addWidget(self.btnPasswd)
        layout.addWidget(self.btnHelp)
        layout.addWidget(self.btnAbout)
        layout.addWidget(self.btnLogOut)
        
        self.woptions.setLayout(layout)
        self.toolBox.addItem(self.woptions, "Opciones")
        
        
        settings = QSettings()
        self.restoreGeometry( settings.value( "MainWindow/Geometry" ).toByteArray() )
        #self.mdiArea.subWindowActivated[QMdiSubWindow].connect(self.showtoolbar)
        self.connect( self.mdiArea, SIGNAL( "subWindowActivated(QMdiSubWindow *)" )\
                      , self.showtoolbar )
        
        self.btnLogOut.clicked.connect(self.logOut)
        self.btnAbout.clicked.connect(self.about)
        self.btnHelp.clicked.connect(self.help)
        self.btnPasswd.clicked.connect(self.changePassword)
        

        self.setWindowTitle(u"%s %s: Usuario %s conectado a %s@%s" % (qApp.organizationName(), \
            qApp.applicationName(),\
            self.user.user, \
            QSqlDatabase.database().databaseName() , \
            QSqlDatabase.database().hostName())
        )
    
        
    def logOut(self):
        self.setVisible(False)

        for hijo in self.mdiArea.subWindowList():
            if not hijo.close():
                return

        dlguser = utility.user.dlgUserLogin()
        cont = 0
        valido = False
        dlguser.txtPassword.setText("")
        if dlguser.exec_() == QDialog.Accepted:
            user = dlguser.user
            if user.valid:
                if user.hasRole( self.module ):
                    self.user = user
                    self.setWindowTitle(u"%s %s: Usuario %s conectado a %s@%s" % (qApp.organizationName(), \
                            qApp.applicationName(),\
                            self.user.user, \
                            QSqlDatabase.database().databaseName() , \
                            QSqlDatabase.database().hostName())
                        )
                    self.init()
                    self.setVisible(True)
                    return 
                else:
                    QtGui.QMessageBox.critical( None,
                    QtGui.qApp.organizationName(),
                    u"Usted no tiene permiso para acceder a este modulo",
                    QtGui.QMessageBox.StandardButtons( QtGui.QMessageBox.Ok ) )
            else:
                QtGui.QMessageBox.critical( None,
                QtGui.qApp.organizationName(),
                user.error,
                QtGui.QMessageBox.StandardButtons( QtGui.QMessageBox.Ok ) )
        
        self.close()

    def init(self):
        raise NotImplementedError()
        
    def about(self):
        QMessageBox.about(self, qApp.organizationName(),
        "<b>%s: %s</b><br />" % ( qApp.organizationName(), qApp.applicationName() )  + \
        "Este programa ha sido desarrollado por Cusuco Software y se distribuye bajo" \
        "una licencia GPL, usted deberia de haber recibido una copia de esta licencia " +\
        "junto con el programa."  )
        
    def help(self):
        pass
        #settings = QSettings()
        #base = settings.value( "Reports/base" ).toString()
        
        #ds = QDesktopServices()
        #ds.openUrl(QUrl(base + "../help/"))
        
    def changePassword(self):
        dlg = utility.user.dlgPasswordChange(self.user)
        if dlg.exec_() == QDialog.Accepted:
            QMessageBox.information(self, qApp.organizationName(), u"La contraseña se ha cambiado exitorsamente")
    
    
    def showtoolbar( self, *args ):
        """
        mostrar la toolbar de la ventana que se acaba de mostrar
        """
        for window in self.mdiArea.subWindowList():
            window.widget().toolBar.setVisible( False )
        for window in args:
            if not window is None:
                window.widget().toolBar.setVisible( True )
        

    def setStatus( self, status ):
        self.__status = status
        self.setControls( self.__status )
    def getStatus( self ):
        return self.__status
    status = property( getStatus, setStatus )

    def setControls( self, status ):
        raise NotImplementedError()

    def closeEvent( self, event ):
        settings = QSettings()
        settings.setValue( "MainWindow/Geometry", self.saveGeometry() )

    @pyqtSlot(  )
    def on_actionLockSession_triggered( self ):
        self.status = False

    @pyqtSlot(  )
    def on_actionUnlockSession_triggered( self ):
        dlg = utility.user.dlgUserLogin( self )
        if dlg.exec_() == QDialog.Accepted:
            tmpuser = utility.user.User( dlg.txtUser.text(), dlg.txtPassword.text() )
            if tmpuser.valid:
                if tmpuser.uid == self.user.uid or tmpuser.hasRole( 'root' ):
                    self.status = True
                else:
                    QMessageBox.critical( self, \
                                         qApp.organizationName(), \
                                         u"Usted esta intentando desbloquear "+\
                                         " una sesión que no le pertenece", \
                                         QMessageBox.Ok, \
                                         QMessageBox.Ok )
            else:
                QMessageBox.critical( self, \
                                         qApp.organizationName(), \
                                         u"No ha sido posible autenticarle", \
                                         QMessageBox.Ok, \
                                         QMessageBox.Ok )



