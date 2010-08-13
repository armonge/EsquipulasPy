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

class dlgApertura ( QDialog, Ui_frmApertura ):
    def __init__( self,parent,cerrar=False):
        """
        Constructor para agregar un nuevo articulo
        @param user: El id del usuario que ha creado este documento
        """
        super( dlgApertura, self ).__init__( parent )
        self.setupUi( self )
        
        self.datosSesion = parent.datosSesion
        
        self.txtUsuario.setText( parent.user.user )
        self.txtUsuario.setReadOnly( True )

        self.txtUser.setFocus()
        self.txtPassword.setEchoMode( QLineEdit.Password )
        self.setWindowIcon( QIcon( ":/icons/res/logo.png" ) )
        
        self.dtFechaTime.setReadOnly( True )
        self.supervisor = None
        
        if cerrar:
            self.swcaja.setCurrentIndex(1)
            self.txtcaja.setText("Caja 1")
            self.txtcaja.setReadOnly(True)

            
        else:
            self.swcaja.setCurrentIndex(0)
            self.cajamodel = QSqlQueryModel()
            try:
                if not QSqlDatabase.database().isOpen():
                    if not QSqlDatabase.database().open():
                        raise UserWarning(u"No se pudo abrir la conexión con la base de datos")
                    self.cajamodel.setQuery( "SELECT idcaja, descripcion from cajas" )
            except UserWarning as inst:
                QMessageBox.critical(self, "Llantera Esquipulas", unicode(inst))
                self.reject()
            except Exception as e:
                print e
                self.reject()

            finally:
                if QSqlDatabase.database().isOpen():
                    QSqlDatabase.database().close()
                
            self.cbcaja.setModel( self.cajamodel )
            self.cbcaja.setModelColumn( 1 )
            self.dtFechaTime.setDateTime( QDateTime.currentDateTime() )
        

                
    @pyqtSlot( "int" )
    def on_cboCaja_currentIndexChanged( self, index ):
        """
        @param index: El CurrentIndex del comboBox para la caja seleccionada
        """
        self.idCaja = self.model.record( index ).value( "idcaja" ).toInt()[0]

#    @pyqtSlot(  )
#    def on_buttonBox_accepted( self ):
#        """
#        Agrega una apertura de caja        
#        """
#        
    def accept(self):
        self.supervisor = User( self.txtUser.text(), self.txtPassword.text())
        if self.supervisor.valid:
            if not self.supervisor.hasRole( 'root' ):
                QMessageBox.critical(self, u"Llantera Esquipulas: Autenticación","Usuario Invalido")
                self.reject()
#        if not self.editmodel.save():
#            QMessageBox.warning( None, u"La sesión no fue abierta", self.editmodel.mensajeError())
#        else:
            QDialog.accept(self)
            
        

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
    
class AperturaModel(object):
    def __init__(self,datosSesion):
        self.datosSesion = datosSesion        
        self.monto = Decimal(0)
        self.cajaId = 0
        self.supervisorId = 0
        self.mensajeError = None

    def save(self):
        try:
            if not QSqlDatabase.database().isOpen():
                QSqlDatabase.database().open()

            #extraer el tipo de cambio de acuerdo a la fecha junto con su id
            query = QSqlQuery( "SELECT idtc,tasa,tasabanco FROM tiposcambio t where fecha=DATE('" + self.datosSesion.fecha.toString("yyyyMMdd") + "')")
            if not query.exec_():
                raise Exception("No existe una tasa de cambio para la fecha " + self.datosSesion.fecha.toString("yyyyMMdd"))
            
            if query.size()==0:
                self.mensajeError=u"La sesión no fue abierta porque no existe un tipo de cambio para la fecha actual"
#                self.reject()
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

        