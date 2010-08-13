# -*- coding: utf-8 -*-
'''
Created on 02/06/2010

@author: Marcos Moreno
'''
from PyQt4.QtGui import QMessageBox, QDialog, QLineEdit, QIcon
from PyQt4.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt4.QtCore import pyqtSlot, pyqtSignature, QDateTime,Qt
from ui.Ui_frmApertura import Ui_frmApertura
from decimal import Decimal
from utility.user import User

class dlgApertura ( QDialog, Ui_frmApertura ):
    def __init__( self,parent,cerrar=False):
        """
        Constructor para agregar un nuevo articulo
        @param user: El id del usuario que ha creado este documento
        """
        super( dlgApertura, self ).__init__( parent )
        self.setupUi( self )
        
        self.editmodel = AperturaModel(parent.datosSesion)
        self.cerrar = cerrar
        
        
        self.txtUsuario.setText( parent.user.user )
        self.txtUsuario.setReadOnly( True )

        self.txtUser.setFocus()
        self.txtPassword.setEchoMode( QLineEdit.Password )
        self.setWindowIcon( QIcon( ":/icons/res/logo.png" ) )
        
        self.dtFechaTime.setReadOnly( True )
        self.txtMonto.setAlignment(Qt.AlignRight)
        self.supervisor = None
        
        if cerrar:
            self.swcaja.setCurrentIndex(1)
            self.txtcaja.setText(parent.cajaNombre)
            self.txtcaja.setReadOnly(True)
            self.editmodel.cajaId = parent.datosSesion.cajaId
            
        else:
            self.swcaja.setCurrentIndex(0)
            self.cajasmodel = QSqlQueryModel()
            try:
                if not QSqlDatabase.database().isOpen():
                    if not QSqlDatabase.database().open():
                        raise UserWarning(u"No se pudo abrir la conexión con la base de datos")
                    
                self.cajasmodel.setQuery( "SELECT idcaja, descripcion from cajas" )
                if self.cajasmodel.rowCount()==0:
                    QMessageBox.critical(self, "Abrir Caja","No existe ninguna caja en la base de datos")
            except UserWarning as inst:
                QMessageBox.critical(self, "Llantera Esquipulas", unicode(inst))
                self.reject()
            except Exception as e:
                print e
                self.reject()
            finally:
                if QSqlDatabase.database().isOpen():
                    QSqlDatabase.database().close()
                
            self.cbcaja.setModel( self.cajasmodel )
            self.cbcaja.setModelColumn( 1 )
            self.cbcaja.setCurrentIndex(-1)
            self.dtFechaTime.setDateTime( QDateTime.currentDateTime() )
        

#                
#    @pyqtSlot( "int" )
#    def on_cboCaja_currentIndexChanged( self, index ):
#        """
#        @param index: El CurrentIndex del comboBox para la caja seleccionada
#        """
#        self.idCaja = self.model.record( index ).value( "idcaja" ).toInt()[0]

#    @pyqtSlot(  )
#    def on_buttonBox_accepted( self ):
#        """
#        Agrega una apertura de caja        
#        """
#        
    def accept(self):
        if not self.cerrar:
            self.editmodel.datosSesion.cajaId =  self.cajasmodel.record( self.cbcaja.currentIndex() ).value( "idcaja" ).toInt()[0]
            
        if self.editmodel.valid:
            supervisor = User( self.txtUser.text(), self.txtPassword.text())
            if supervisor.valid:
                if not supervisor.hasRole( 'root' ):
                    QMessageBox.critical(self, u"Llantera Esquipulas: Autenticación","El usuario no tiene permisos para autorizar la apertura de caja")
                    self.reject()
                
                
                QDialog.accept(self)
            else:
                QMessageBox.critical(self, u"Llantera Esquipulas: Autenticación",u"El nombre de usuario o contraseña son incorrectos")
                self.txtUser.setFocus()
                self.txtPassword.setText("")
        else:
            if self.editmodel.errorId==1:
                self.cbcaja.setFocus()
                QMessageBox.warning( None, u"La sesión no fue abierta", u"Por favor seleccione la caja en la que se abrirá la sesión")
                self.editmodel.errorId =0
            
                
#        if not self.editmodel.save():
#            QMessageBox.warning( None, u"La sesión no fue abierta", self.editmodel.error[1])
#            if self.editmodel.errorId == 2:
#                QMessageBox.warning( None, u"La sesión no fue abierta", u"La sesión no fue abierta porque no existe un tipo de cambio para la fecha actual")
#        else:
           
            
        

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
        self.errorId=0
    
    @property
    def valid(self):
        
        if self.datosSesion.cajaId == 0:
            self.errorId = 1
        else:
            return True
        return False
    def save(self):
        try:
            if not QSqlDatabase.database().isOpen():
                QSqlDatabase.database().open()

            #extraer el tipo de cambio de acuerdo a la fecha junto con su id
            query = QSqlQuery( "SELECT idtc,tasa,tasabanco FROM tiposcambio t where fecha=DATE('" + self.datosSesion.fecha.toString("yyyyMMdd") + "')")
            if not query.exec_():
                raise Exception("No existe una tasa de cambio para la fecha " + self.datosSesion.fecha.toString("yyyyMMdd"))
            
            if query.size()==0:
                self.errorId = 2
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

        