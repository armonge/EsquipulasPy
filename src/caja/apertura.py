# -*- coding: utf-8 -*-
'''
Created on 02/06/2010

@author: Marcos Moreno
'''
from PyQt4.QtGui import QMessageBox, QDialog, QLineEdit, QIcon
from PyQt4.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt4.QtCore import pyqtSlot, pyqtSignature, QDateTime,Qt
from ui.Ui_apertura import Ui_dlgApertura
from decimal import Decimal
from utility.user import User
from utility import constantes

class dlgApertura ( QDialog, Ui_dlgApertura ):
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
        self.txtSaldoC.setAlignment(Qt.AlignRight)
        self.txtSaldoD.setAlignment(Qt.AlignRight)
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
                          
                self.editmodel.supervisorId = supervisor.uid
                self.editmodel.datosSesion.fecha = self.dtFechaTime.date()
                
                if not self.editmodel.save():
                    if self.editmodel.errorId == 1:
                        QMessageBox.warning( None, u"La sesión no fue abierta","")
                    elif self.editmodel.errorId == 2:
                        QMessageBox.warning( None, u"La sesión no fue abierta", u"La sesión no fue abierta porque no existe un tipo de cambio para la fecha actual")
                    else:
                        QMessageBox.warning( None, u"La sesión no fue abierta", u"La sesión no fue abierta. Por favor Contacte al administrador del sistema")
                else:
                    QMessageBox.information(None,u"Sesión Abierta", u"La sesión fue abierta exitosamente")
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
            
    @pyqtSlot()
    def on_txtSaldoC_editingFinished(self):
        if self.editmodel != None:
            self.editmodel.saldoCordoba = Decimal(str(self.txtSaldoC.value()))
            print self.editmodel.saldoCordoba
               
    @pyqtSlot( )
    def on_txtSaldoD_editingFinished(self):
        if self.editmodel != None:
            self.editmodel.saldoDolar = Decimal(str(self.txtSaldoD.value()))
            print self.editmodel.saldoDolar                
           
            
        

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
    
        self.supervisorId = 0
        self.errorId=0
        self.saldoCordoba = Decimal(0)
        self.saldoDolar = Decimal(0)
    
    @property
    def valid(self):
        
        if self.datosSesion.cajaId == 0:
            self.errorId = 1
        else:
            return True
        return False
    @property
    def total(self):
        print self.datosSesion.tipoCambioBanco
        total = (self.saldoCordoba / self.datosSesion.tipoCambioBanco) + self.saldoDolar
        return total
    
    def save(self):
        try:
            if not QSqlDatabase.database().isOpen():
                QSqlDatabase.database().open()

            if not QSqlDatabase.database().transaction():
                raise Exception( u"No se pudo comenzar la transacción" )
            
            fecha = self.datosSesion.fecha.toString("yyyyMMdd") 
            #extraer el tipo de cambio de acuerdo a la fecha junto con su id
            query = QSqlQuery( "SELECT idtc,tasa,IFNULL(tasabanco,tasa) as tasabanco FROM tiposcambio t where fecha=DATE('" + fecha + "')")
            if not query.exec_():
                raise Exception("No existe una tasa de cambio para la fecha " + fecha)
            
            
            if query.size()==0:
                self.errorId = 2
#                self.reject()
                return False
                
            
            query.first()
        
            self.datosSesion.tipoCambioId = query.value(0).toInt()[0]
            self.datosSesion.tipoCambioOficial = Decimal(query.value(1).toString())
            self.datosSesion.tipoCambioBanco = Decimal(query.value(2).toString())
            
            

            query = QSqlQuery("CALL spConsecutivo(22,NULL);")
            
            if not query.exec_():
                raise Exception("No pudo ser cargado el consecutivo del documento")
            
            query.first()
            
            ndocimpreso = query.value( 0 ).toString()
           
            
            query.prepare( """INSERT INTO documentos(ndocimpreso,total,fechacreacion,idtipodoc,idcaja,idtipocambio)
            VALUES (:ndocimpreso,:total,:fecha,:tipodoc,:caja,:tipocambio)""" )
            
            total = self.total
            
            query.bindValue( ":ndocimpreso", ndocimpreso )
            
            query.bindValue( ":total", total.to_eng_string() )
            query.bindValue( ":fecha", fecha + QDateTime.currentDateTime().toString("hhmmss"))
            query.bindValue( ":tipodoc", constantes.IDAPERTURA )
            query.bindValue( ":caja", self.datosSesion.cajaId )
            query.bindValue( ":tipocambio", self.datosSesion.tipoCambioId)

            if not query.exec_():
                raise Exception( query.lastError().text() )
            
            self.datosSesion.sesionId=query.lastInsertId().toInt()[0]
            insertedId = str(self.datosSesion.sesionId)             
            
            if not query.prepare( "INSERT INTO personasxdocumento (idpersona,iddocumento,autoriza) VALUES" + 
            "(:usuario," + insertedId + ",0), "
            "(:supervisor," + insertedId + ",1)"):
                raise Exception( query.lastError().text() )
            

            query.bindValue( ":usuario", self.datosSesion.usuarioId )
            query.bindValue (":supervisor", self.supervisorId)

            if not query.exec_():
                raise Exception( query.lastError().text() )
            
            
            if not query.prepare( "INSERT INTO movimientoscaja(iddocumento,idtipomovimiento,idtipomoneda,monto) VALUES " +
            "(" + insertedId + ",1,1,:totalCordoba), "
            "(" + insertedId + ",1,2,:totalDolar)"):
                
                raise Exception( query.lastError().text() )
            
            query.bindValue( ":totalCordoba", self.saldoCordoba.to_eng_string() )
            query.bindValue (":totalDolar", self.saldoDolar.to_eng_string())

            if not query.exec_():
                raise Exception( query.lastError().text() )
            
            
            if not QSqlDatabase.database().commit():
                raise Exception( "No se pudo hacer commit" )
            
            resultado = True
        except Exception as inst:
            print  query.lastError().databaseText()
            print query.lastError().driverText()
            print inst.args
            QSqlDatabase.database().rollback()
            resultado = False
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()
        return resultado
#
#        