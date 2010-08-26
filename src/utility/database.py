# -*- coding: utf-8 -*-
u"""
Modulo utilizado para manejar la configuración de la base de datos
"""
from PyQt4.QtSql import QSqlDatabase
from PyQt4.QtGui import QDialog, QFormLayout, QVBoxLayout, QLineEdit, QDialogButtonBox
from PyQt4.QtCore import   SLOT, SIGNAL, QObject, QSettings


class dlgDatabaseConfig( QDialog ):
    u"""
    Dialogo usado para pedir al usuario nuevos valores de configuración
    """
    def __init__( self, parent = None ):
        """
        Constructor
        """
        super( dlgDatabaseConfig, self ).__init__( parent )

        self.txtServer = QLineEdit()
        self.txtDatabase = QLineEdit()
        self.txtUser = QLineEdit()
        self.txtPassword = QLineEdit()
        self.txtPassword.setEchoMode( QLineEdit.Password )


        formLayout = QFormLayout()
        formLayout.addRow( "&Servidor", self.txtServer )
        formLayout.addRow( "Base de &Datos", self.txtDatabase )
        formLayout.addRow( "&Usuario", self.txtUser )
        formLayout.addRow( u"&Contraseña", self.txtPassword )

        self.buttonBox = QDialogButtonBox( QDialogButtonBox.Ok | QDialogButtonBox.Cancel )



        verticalLayout = QVBoxLayout()

        verticalLayout.addLayout( formLayout )
        verticalLayout.addWidget( self.buttonBox )

        self.setLayout( verticalLayout )

        QObject.connect( self.buttonBox, SIGNAL( "accepted()" ), self, SLOT( "accept()" ) );
        QObject.connect( self.buttonBox, SIGNAL( "rejected()" ), self, SLOT( "reject()" ) );


class Database:
    @staticmethod
    def getDatabase(db, newsettings = False ):
        u"""
        @param newsettings: Cuando este parametro es verdadero la configuración de la base de datos se recarga
        @type newsettings: bool
        @rtype: QSqlDatabase
        """
        settings = QSettings()
        if not ( settings.value( "Esquipulas/Name" ).toString() == "" or settings.value( "Esquipulas/Server" ).toString() == "" or settings.value( "Esquipulas/User" ).toString() == "" or settings.value( "Esquipulas/Password" ).toString() == "" )  and not newsettings:                     
                QSqlDatabase.removeDatabase('QMYSQL')
                database = QSqlDatabase.addDatabase( 'QMYSQL' )
                database.setDatabaseName( db )
                database.setHostName( settings.value( "Esquipulas/Server" ).toString() )
                database.setUserName( settings.value( "Esquipulas/User" ).toString() )
                database.setPassword( settings.value( "Esquipulas/Password" ).toString() )
                return database
                
        elif ( settings.value( "Remi/Name" ).toString() == "" or settings.value( "Remi/Server" ).toString() == "" or settings.value( "Remi/User" ).toString() == "" or settings.value( "Remi/Password" ).toString() == "" )  and not newsettings:
                QSqlDatabase.removeDatabase('QMYSQL')        
                database = QSqlDatabase.addDatabase( 'QMYSQL' )
                database.setDatabaseName( db )
                database.setHostName( settings.value( "Remi/Server" ).toString() )
                database.setUserName( settings.value( "Remi/User" ).toString() )
                database.setPassword( settings.value( "Remi/Password" ).toString() )
                return database
        else:
            dbconfig = dlgDatabaseConfig()
            if dbconfig.exec_() == QDialog.Accepted:
                QSqlDatabase.removeDatabase('QMYSQL')
                database = QSqlDatabase.addDatabase( 'QMYSQL' )
                database.setDatabaseName( dbconfig.txtDatabase.text() )
                database.setHostName( dbconfig.txtServer.text() )
                database.setUserName( dbconfig.txtUser.text() )
                database.setPassword( dbconfig.txtPassword.text() )
                
                if dbconfig.txtDatabase.text()=="esquipulasdb":
                    #guardar en el archivo de configuracion
                    settings.setValue( "Esquipulas/Name", dbconfig.txtDatabase.text() )
                    settings.setValue( "Esquipulas/Server", dbconfig.txtServer.text() )
                    settings.setValue( "Esquipulas/User", dbconfig.txtUser.text() )
                    settings.setValue( "Esquipulas/Password", dbconfig.txtPassword.text() )
                    return database
                elif dbconfig.txtDatabase.text()=="remi":
                    #guardar en el archivo de configuracion
                    settings.setValue( "Remi/Name", dbconfig.txtDatabase.text() )
                    settings.setValue( "Remi/Server", dbconfig.txtServer.text() )
                    settings.setValue( "Remi/User", dbconfig.txtUser.text() )
                    settings.setValue( "Remi/Password", dbconfig.txtPassword.text() )
                    return database

        return False

