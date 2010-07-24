# -*- coding: utf-8 -*-
'''
Created on 02/06/2010

@author: Marcos Moreno
'''
from PyQt4.QtGui import QMessageBox, QDialog, QLineEdit, QIcon
from PyQt4.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt4.QtCore import pyqtSlot, pyqtSignature, QDateTime
from ui.Ui_frmApertura import Ui_frmApertura

from utility.user import User

class frmApertura ( QDialog, Ui_frmApertura ):
    def __init__( self, user,  parent = None ):
        """
        Constructor para agregar un nuevo articulo
        @param user: El id del usuario que ha creado este documento
        """
        super( frmApertura, self ).__init__( parent )
        self.setupUi( self )
        self.user = user
        
        
        self.txtUsuario.setText( self.user.user )
        self.txtUsuario.setReadOnly( True )

        self.txtUser.setFocus()
        self.txtPassword.setEchoMode( QLineEdit.Password )
        self.setWindowIcon( QIcon( ":/icons/res/logo.png" ) )
        
        self.model = QSqlQueryModel()
        try:

            if not QSqlDatabase.database().isOpen():
                QSqlDatabase.database().open()
            self.model.setQuery( "SELECT idcaja, descripcion from cajas" )
        except Exception, e:
            print e
            self.reject()

        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()
                
        self.cboCaja.setModel( self.model )
        self.cboCaja.setModelColumn( 1 )
        
        self.dtFechaTime.setDateTime( QDateTime.currentDateTime() )
        self.dtFechaTime.setReadOnly( True )
        self.sesion=0

        self.idCaja = 1
        
        self.usuario = User( self.txtUser.text(), self.txtPassword.text())
        print self.usuario.uid
        if self.usuario.valid:
            if not self.usuario.hasRole( 'root' ):               
                QMessageBox.Critical("Autenticacion","Usuario Invalido")
                self.reject()

        self.exchangeRateId = 0
        self.exchangeRate = 0
        self.bankExchangeRate = 0

                
    @pyqtSlot( "int" )
    def on_cboCaja_currentIndexChanged( self, index ):
        """
        @param index: El CurrentIndex del comboBox para la caja seleccionada
        """
        self.idCaja = self.model.record( index ).value( "idcaja" ).toInt()[0]

    @pyqtSlot(  )
    def on_buttonBox_accepted( self ):
        """
        Agrega una apertura de caja        
        """

        try:

            if not QSqlDatabase.database().isOpen():
                QSqlDatabase.database().open()

            #extraer el tipo de cambio de acuerdo a la fecha junto con su id
            query = QSqlQuery( "SELECT idtc,tasa,tasabanco FROM tiposcambio t where fecha=DATE('" + self.fecha.toString("yyyyMMdd") + "')")
            if not query.exec_():
                raise Exception("No existe una tasa de cambio para la fecha " + self.fecha.toString("yyyyMMdd"))
            
            if query.size()==0:
                QMessageBox.warning( None, u"La sesión no fue abierta", u"La sesión no fue abierta porque no existe un tipo de cambio para la fecha actual")
                self.reject()
                return ""
                
            
            query.first()
            self.exchangeRateId = query.value(0).toInt()[0]
            self.exchangeRate = query.value(1).toString()
            self.bankExchangeRate = query.value(2).toString()
        

            query.prepare("""
            SELECT
            MAX(CAST(ndocimpreso AS SIGNED))+1
            FROM documentos d
            WHERE idtipodoc=22
            ;
            """ )
            query.exec_()
            query.first()
            ndocimpreso = query.value( 0 ).toString()
            
            if ndocimpreso == "0":
                ndocimpreso = "1" 
            
            if not query.prepare( """INSERT INTO documentos(ndocimpreso,total,fechacreacion,idtipodoc,idcaja,observacion,idtipocambio)
            VALUES(:ndocimpreso,:total,:fecha,:tipodoc,:caja,:observacion,:tipocambio)""" ):
                raise Exception( query.lastError().text() )
            query.bindValue( ":ndocimpreso", ndocimpreso )
            query.bindValue( ":total", self.txtMonto.text() )
            query.bindValue( ":fecha", self.dtFechaTime.dateTime().toString( "yyyyMMddhhmmss" ) )
            query.bindValue( ":tipodoc", 22 )
            query.bindValue( ":usuario", self.user.uid )
            query.bindValue( ":caja", self.idCaja )
            query.bindValue( ":observacion", self.usuario.user )
            query.bindValue( ":tipocambio", self.exchangeRateId )

            if not query.exec_():
                raise Exception( query.lastError().text() )
            
            self.sesion=query.lastInsertId().toInt()[0]
                        
            if not query.prepare( """INSERT INTO personasxdocumento (idpersona,iddocumento)
            VALUES(:usuario,:documento)""" ):
                raise Exception( query.lastError().text() )
            query.bindValue( ":usuario", self.user.uid )
            query.bindValue( ":documento", self.sesion )

            if not query.exec_():
                raise Exception( query.lastError().text() )
            
            self.accept() 
                       
        except Exception, e:
            print e
            self.reject()

        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()

    def on_buttonBox_cancelled( self ):
        """
        Cancela la apertura de caja        
        """
        self.reject()

    @property
    def idsesion(self):
        return self.sesion
    
    @property
    def fecha(self):
        return self.dtFechaTime.date()