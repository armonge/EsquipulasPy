# -*- coding: utf-8 -*-
u"""
Modulo utilizado para manejar la configuración de la base de datos
"""
from PyQt4.QtSql import QSqlDatabase
from PyQt4.QtGui import QDialog, QFormLayout, QVBoxLayout, QLineEdit, QDialogButtonBox
from PyQt4.QtCore import   QObject, QSettings

from utility.reports import Reports

class dlgDatabaseConfig( QDialog ):
    u"""
    Dialogo usado para pedir al usuario nuevos valores de configuración
    """
    def __init__( self, parent = None ):
        """
        Constructor
        """
        super( dlgDatabaseConfig, self ).__init__( parent )

        self.setupUi()

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
    def setupUi(self):
        self.txtServer = QLineEdit()
        self.txtDatabase = QLineEdit()
        self.txtUser = QLineEdit()
        self.txtPassword = QLineEdit()
        self.txtPassword.setEchoMode( QLineEdit.Password )
        self.txtReports = QLineEdit()


        formLayout = QFormLayout()
        formLayout.addRow( "&Servidor", self.txtServer )
        formLayout.addRow( "Base de &Datos", self.txtDatabase )
        formLayout.addRow( "&Usuario", self.txtUser )
        formLayout.addRow( u"&Contraseña", self.txtPassword )
        formLayout.addRow( u"Servidor de &Reportes", self.txtReports )

        self.buttonBox = QDialogButtonBox( QDialogButtonBox.Ok | QDialogButtonBox.Cancel )

        verticalLayout = QVBoxLayout()

        verticalLayout.addLayout( formLayout )
        verticalLayout.addWidget( self.buttonBox )

        self.setLayout( verticalLayout )

        


def newconfiguration(cfg):
    settings = QSettings()

    dbconfig = dlgDatabaseConfig()
    dbconfig.txtDatabase.setText( settings.value("%s/DBName"%cfg).toString())
    dbconfig.txtServer.setText( settings.value("%s/DBServer"%cfg).toString())
    dbconfig.txtReports.setText( settings.value("%s/DBReports"%cfg).toString())
    dbconfig.txtUser.setText( settings.value("%s/DBUser"%cfg).toString())
    
    if dbconfig.exec_() == QDialog.Accepted:
        QSqlDatabase.removeDatabase('QMYSQL')
        database = QSqlDatabase.addDatabase( 'QMYSQL' )
        database.setDatabaseName( dbconfig.txtDatabase.text() )
        database.setHostName( dbconfig.txtServer.text() )
        database.setUserName( dbconfig.txtUser.text() )
        database.setPassword( dbconfig.txtPassword.text() )

        #guardar en el archivo de configuracion
        settings.setValue( "%s/DBName"%cfg, dbconfig.txtDatabase.text() )
        settings.setValue( "%s/DBServer"%cfg, dbconfig.txtServer.text() )
        settings.setValue( "%s/DBUser"%cfg, dbconfig.txtUser.text() )
        settings.setValue( "%s/DBPassword"%cfg, dbconfig.txtPassword.text() )
        settings.setValue( "%s/DBReports"%cfg, dbconfig.txtReports.text() )
        r = Reports()
        r.url = dbconfig.txtReports.text()

def getDatabase(db, newsettings = False ):
    u"""
    @param newsettings: Cuando este parametro es verdadero la configuración de la base de datos se recarga
    @type newsettings: bool
    @rtype: QSqlDatabase
    """
    settings = QSettings()
    if not newsettings and not ( settings.value( "%s/DBName"%db ).toString() == "" or \
                                settings.value( "%s/DBServer"%db ).toString() == "" or \
                                settings.value( "%s/DBUser"%db ).toString() == "" or \
                                settings.value( "%s/DBPassword"%db ).toString() == ""):
        database = QSqlDatabase.addDatabase( 'QMYSQL' )
        database.setDatabaseName( settings.value( "%s/DBName"%db ).toString() )
        database.setHostName( settings.value( "%s/DBServer"%db ).toString() )
        database.setUserName( settings.value( "%s/DBUser"%db ).toString() )
        database.setPassword( settings.value( "%s/DBPassword"%db ).toString() )

        r = Reports()
        r.url  = settings.value( "%s/DBReports"%db ).toString()
    else:
        newconfiguration(db)

