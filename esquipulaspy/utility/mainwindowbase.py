# -*- coding: utf-8 -*-
'''
Created on 11/06/2010

@author: Andrés Reyes Monge
'''

import sys
from PyQt4.QtCore import  QSettings, pyqtSlot, QSize, QProcess
from PyQt4.QtGui import QDialog, QMessageBox, QIcon, QWidget, QVBoxLayout, \
QPushButton, qApp, QMainWindow, QMdiSubWindow
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
        self.__status = False

    def startUi( self ):
        self.setupUi( self )
        dockaction = self.dockWidget.toggleViewAction()
        dockaction.setIcon( QIcon( ":/icons/res/utilities-desktop-extra.png" ) )
        self.toolBar.addAction( dockaction )


        woptions = QWidget()

        btn_passwd = QPushButton( QIcon( 
                                        ":/images/res/dialog-password.png" ),
                                       u"Cambiar\nContraseña" )
        btn_passwd.setMinimumSize( QSize( 0, 70 ) )
        btn_passwd.setIconSize( QSize( 64, 64 ) )

        btn_help = QPushButton( QIcon( ":/images/res/system-help.png" ),
                                    u"Ayuda" )
        btn_help.setMinimumSize( QSize( 0, 70 ) )
        btn_help.setIconSize( QSize( 64, 64 ) )

        btn_about = QPushButton( QIcon( ":/images/res/help-about.png" ),
                                     "Acerca de" )
        btn_about.setMinimumSize( QSize( 0, 70 ) )
        btn_about.setIconSize( QSize( 64, 64 ) )

        btn_logout = QPushButton( u"Cerrar Sesión" )
        btn_logout.setMinimumSize( QSize( 0, 70 ) )
        btn_logout.setIconSize( QSize( 64, 64 ) )


        layout = QVBoxLayout()
        layout.addWidget( btn_passwd )
        layout.addWidget( btn_help )
        layout.addWidget( btn_about )
        layout.addWidget( btn_logout )

        woptions.setLayout( layout )
        self.toolBox.addItem( woptions, "Opciones" )


        settings = QSettings()
        self.restoreGeometry( 
                     settings.value( "MainWindow/Geometry" ).toByteArray() )

        self.mdiArea.subWindowActivated[ QMdiSubWindow  ].connect( self.showtoolbar )

        btn_logout.clicked.connect( self.logOut )
        btn_about.clicked.connect( self.about )
        btn_help.clicked.connect( self.help )
        btn_passwd.clicked.connect( self.changePassword )


        self.setWindowTitle( u"%s %s: Usuario %s conectado a %s@%s" % ( 
            qApp.organizationName(), \
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
                    self.setWindowTitle( 
                            u"%s %s: Usuario %s conectado a %s@%s" %
                            ( qApp.organizationName(),
                            qApp.applicationName(),
                            self.user.user,
                            QSqlDatabase.database().databaseName() ,
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
        "<b>%s: %s</b><br />" % ( qApp.organizationName(),
                                  qApp.applicationName() ) + \
        "Este programa ha sido desarrollado por Cusuco Software y se "\
        + "distribuye bajo una licencia GPL, usted deberia de haber"\
        + " recibido una copia de esta licencia junto con el programa." )

    def help( self ):
        if sys.platform == "linux2":
            self.process.setWorkingDirectory( "/usr/share/doc/packages/misesquipulas/manual/" )
        elif sys.platform == "win32":
            self.process.setWorkingDirectory( r"C:\Archivos de programa\Esquipulas\manual" )

        self.process.start( "assistant -collectionFile esquipulashelpcollection.qhc" )


    def changePassword( self ):
        dlg = utility.user.dlgPasswordChange( self.user )
        if dlg.exec_() == QDialog.Accepted:
            QMessageBox.information( self, qApp.organizationName(),
                              u"La contraseña se ha cambiado exitorsamente" )


    def showtoolbar( self, new_window ):
        """
        mostrar la toolbar de la ventana que se acaba de mostrar
        """
        for window in self.mdiArea.subWindowList():
            window.widget().toolBar.setVisible( False )

        if not new_window is None:
            new_window.widget().toolBar.setVisible( True )


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
        """
        Intentar desbloquear la sesión
        """
        dlg = utility.user.dlgSmallUserLogin( self )
        if dlg.exec_() == QDialog.Accepted:
            tmpuser = dlg.user
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



