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
        if not ( settings.value( "Database/Name" ).toString() == "" or settings.value( "Database/Server" ).toString() == "" or settings.value( "Database/User" ).toString() == "" or settings.value( "Database/Password" ).toString() == "" )  and not newsettings:                     
                QSqlDatabase.removeDatabase('QMYSQL')
                database = QSqlDatabase.addDatabase( 'QMYSQL' )
                database.setDatabaseName( db )
                database.setHostName( settings.value( "Database/Server" ).toString() )
                database.setUserName( settings.value( "Database/User" ).toString() )
                database.setPassword( settings.value( "Database/Password" ).toString() )
                return database
                
        elif ( settings.value( "Remidb/Name" ).toString() == "" or settings.value( "Remidb/Server" ).toString() == "" or settings.value( "Remidb/User" ).toString() == "" or settings.value( "Remidb/Password" ).toString() == "" )  and not newsettings:
                QSqlDatabase.removeDatabase('QMYSQL')        
                database = QSqlDatabase.addDatabase( 'QMYSQL' )
                database.setDatabaseName( db )
                database.setHostName( settings.value( "Remidb/Server" ).toString() )
                database.setUserName( settings.value( "Remidb/User" ).toString() )
                database.setPassword( settings.value( "Remidb/Password" ).toString() )
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
                    settings.setValue( "Database/Name", dbconfig.txtDatabase.text() )
                    settings.setValue( "Database/Server", dbconfig.txtServer.text() )
                    settings.setValue( "Database/User", dbconfig.txtUser.text() )
                    settings.setValue( "Database/Password", dbconfig.txtPassword.text() )
                    return database
                elif dbconfig.txtDatabase.text()=="remi":
                    #guardar en el archivo de configuracion
                    settings.setValue( "Remidb/Name", dbconfig.txtDatabase.text() )
                    settings.setValue( "Remidb/Server", dbconfig.txtServer.text() )
                    settings.setValue( "Remidb/User", dbconfig.txtUser.text() )
                    settings.setValue( "Remidb/Password", dbconfig.txtPassword.text() )
                    return database

            return False

