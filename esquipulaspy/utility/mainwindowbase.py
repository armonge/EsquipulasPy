# -*- coding: utf-8 -*-
'''
Created on 11/06/2010

@author: Andrés Reyes Monge
'''

import sys
from PyQt4.QtCore import SIGNAL, QSettings, pyqtSlot, QSize, QProcess
from PyQt4.QtGui import QDialog, QMessageBox, QIcon, QWidget, QVBoxLayout, \
QPushButton, qApp, QMainWindow
from PyQt4.QtSql import QSqlDatabase

import utility.user

class MainWindowBase( QMainWindow ):
    '''
    Esta clase implementa la funcionalidad que es común a todas las ventanas
    principales del sistema.
    '''
    def __init__( self , parent ):
        '''
        Constructor
        '''
        super( MainWindowBase, self ).__init__( parent )
        self.process = QProcess()
        """
        @ivar: Este es el proceso en el que se llamara la ayuda
        @type:QProcess
        """

        self.user = utility.user.LoggedUser
        """
        @type: User
        """
    def startUi( self ):
        self.setupUi( self )
        dockaction = self.dockWidget.toggleViewAction()
        dockaction.setIcon( QIcon( ":/icons/res/utilities-desktop-extra.png" ) )
        self.toolBar.addAction( dockaction )


        self.woptions = QWidget()

        self.btnPasswd = QPushButton( QIcon( ":/images/res/dialog-password.png" ), u"Cambiar\nContraseña" )
        self.btnPasswd.setMinimumSize( QSize( 0, 70 ) )
        self.btnPasswd.setIconSize( QSize( 64, 64 ) )

        self.btnHelp = QPushButton( QIcon( ":/images/res/system-help.png" ), u"Ayuda" )
        self.btnHelp.setMinimumSize( QSize( 0, 70 ) )
        self.btnHelp.setIconSize( QSize( 64, 64 ) )

        self.btnAbout = QPushButton( QIcon( ":/images/res/help-about.png" ), "Acerca de" )
        self.btnAbout.setMinimumSize( QSize( 0, 70 ) )
        self.btnAbout.setIconSize( QSize( 64, 64 ) )

        self.btnLogOut = QPushButton( u"Cerrar Sesión" )
        self.btnLogOut.setMinimumSize( QSize( 0, 70 ) )
        self.btnLogOut.setIconSize( QSize( 64, 64 ) )


        layout = QVBoxLayout()
        layout.addWidget( self.btnPasswd )
        layout.addWidget( self.btnHelp )
        layout.addWidget( self.btnAbout )
        layout.addWidget( self.btnLogOut )

        self.woptions.setLayout( layout )
        self.toolBox.addItem( self.woptions, "Opciones" )


        settings = QSettings()
        self.restoreGeometry( settings.value( "MainWindow/Geometry" ).toByteArray() )
        #self.mdiArea.subWindowActivated[QMdiSubWindow].connect(self.showtoolbar)
        self.connect( self.mdiArea, SIGNAL( "subWindowActivated(QMdiSubWindow *)" )\
                      , self.showtoolbar )

        self.btnLogOut.clicked.connect( self.logOut )
        self.btnAbout.clicked.connect( self.about )
        self.btnHelp.clicked.connect( self.help )
        self.btnPasswd.clicked.connect( self.changePassword )


        self.setWindowTitle( u"%s %s: Usuario %s conectado a %s@%s" % ( qApp.organizationName(), \
            qApp.applicationName(), \
            self.user.user, \
            QSqlDatabase.database().databaseName() , \
            QSqlDatabase.database().hostName() )
        )


    def logOut( self ):
        self.setVisible( False )

        for hijo in self.mdiArea.subWindowList():
            if not hijo.close():
                return

        dlguser = utility.user.dlgUserLogin()
        dlguser.txtPassword.setText( "" )
        if dlguser.exec_() == QDialog.Accepted:
            user = dlguser.user
            if user.valid:
                if user.hasRole( self.module ):
                    self.user = user
                    self.setWindowTitle( u"%s %s: Usuario %s conectado a %s@%s" % ( qApp.organizationName(), \
                            qApp.applicationName(), \
                            self.user.user, \
                            QSqlDatabase.database().databaseName() , \
                            QSqlDatabase.database().hostName() )
                        )
                    self.init()
                    self.setVisible( True )
                    return
                else:
                    QMessageBox.critical( None,
                    qApp.organizationName(),
                    u"Usted no tiene permiso para acceder a este modulo",
                    QMessageBox.StandardButtons( QMessageBox.Ok ) )
            else:
                QMessageBox.critical( None,
                qApp.organizationName(),
                user.error,
                QMessageBox.StandardButtons( QMessageBox.Ok ) )

        self.close()

    def init( self ):
        raise NotImplementedError()

    def about( self ):
        QMessageBox.about( self, qApp.organizationName(),
        "<b>%s: %s</b><br />" % ( qApp.organizationName(), qApp.applicationName() ) + \
        "Este programa ha sido desarrollado por Cusuco Software y se distribuye bajo" \
        "una licencia GPL, usted deberia de haber recibido una copia de esta licencia " + \
        "junto con el programa." )

    def help( self ):
        if sys.platform == "linux2":
            self.process.setWorkingDirectory( "/usr/share/doc/packages/misesquipulas/manual/" )
        elif sys.platform == "win32":
            self.process.setWorkingDirectory( r"C:\Archivos de programa\Esquipulas\manual" )

        self.process.start( "assistant -collectionFile esquipulashelpcollection.qhc" )


    def changePassword( self ):
        dlg = utility.user.dlgPasswordChange( self.user )
        if dlg.exec_() == QDialog.Accepted:
            QMessageBox.information( self, qApp.organizationName(), u"La contraseña se ha cambiado exitorsamente" )


    def showtoolbar( self, *args ):
        """
        mostrar la toolbar de la ventana que se acaba de mostrar
        """
        for window in self.mdiArea.subWindowList():
            window.widget().toolBar.setVisible( False )
        for window in args:
            if not window is None:
                window.widget().toolBar.setVisible( True )


    def _setStatus( self, status ):
        self.__status = status
        self.setControls( self.__status )
    def _getStatus( self ):
        return self.__status
    status = property( _getStatus, _setStatus )

    def setControls( self, status ):
        raise NotImplementedError()

    def closeEvent( self, _event ):
        settings = QSettings()
        settings.setValue( "MainWindow/Geometry", self.saveGeometry() )

    @pyqtSlot()
    def on_actionLockSession_triggered( self ):
        self.status = False

    @pyqtSlot()
    def on_actionUnlockSession_triggered( self ):
        dlg = utility.user.dlgSmallUserLogin( self )
        if dlg.exec_() == QDialog.Accepted:
            tmpuser = utility.user.User( dlg.txtUser.text(), dlg.txtPassword.text() )
            if tmpuser.valid:
                if tmpuser.uid == self.user.uid or tmpuser.hasRole( 'root' ):
                    self.status = True
                else:
                    QMessageBox.critical( self, \
                                         qApp.organizationName(), \
                                         u"Usted esta intentando desbloquear " + \
                                         " una sesión que no le pertenece", \
                                         QMessageBox.Ok, \
                                         QMessageBox.Ok )
            else:
                QMessageBox.critical( self, \
                                         qApp.organizationName(), \
                                         u"No ha sido posible autenticarle", \
                                         QMessageBox.Ok, \
                                         QMessageBox.Ok )



