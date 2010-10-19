# -*- coding: utf-8 -*-
'''
Created on 02/06/2010

@author: Marcos Moreno
'''
from decimal import Decimal
import logging

from PyQt4.QtGui import QMessageBox, QDialog, QLineEdit, QIcon, qApp
from PyQt4.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt4.QtCore import pyqtSlot, QDateTime, Qt

from ui.Ui_apertura import Ui_dlgApertura

from utility.user import User
from utility import constantes

class DlgApertura ( QDialog, Ui_dlgApertura ):
    def __init__( self, parent, cerrar = False ):
        """
        Constructor para agregar un nuevo articulo
        """
        super( DlgApertura, self ).__init__( parent )
        self.parentWindow = parent
        self.setupUi( self )

        self.editmodel = AperturaModel( parent.datosSesion )
        self.cerrar = cerrar


        self.txtUsuario.setText( parent.user.user )
        self.txtUsuario.setReadOnly( True )

#        self.txtUser.setFocus()
        self.txtPassword.setEchoMode( QLineEdit.Password )
        self.setWindowIcon( QIcon( ":/icons/res/logo.png" ) )


        self.txtSaldoC.setAlignment( Qt.AlignRight )
        self.txtSaldoD.setAlignment( Qt.AlignRight )
        self.supervisor = None

        if cerrar:
            self.swcaja.setCurrentIndex( 1 )
            self.txtcaja.setText( parent.cajaNombre )
            self.txtcaja.setReadOnly( True )
            self.editmodel.cajaId = parent.datosSesion.cajaId

        else:
            self.swcaja.setCurrentIndex( 0 )
            self.cajasmodel = QSqlQueryModel()
            try:
                if not QSqlDatabase.database().isOpen():
                    if not QSqlDatabase.database().open():
                        raise UserWarning( u"No se pudo abrir la conexión "\
                                           + "con la base de datos" )

                self.cajasmodel.setQuery( "SELECT idcaja, descripcion FROM cajas" )
                if self.cajasmodel.rowCount() == 0:
                    QMessageBox.critical( self, qApp.organizationName(),
                                         "No existe ninguna caja en la base de datos" )

                query = QSqlQuery( """
                SELECT
                    fechacreacion
                    FROM esquipulasdb.documentos d
                    LEFT JOIN personasxdocumento pd on pd.iddocumento = d.iddocumento
                    WHERE pd.idpersona = %d and idtipodoc =%d
                    ;
                    """ % ( self.editmodel.datosSesion.usuarioId,
                            constantes.IDARQUEO ) )
                query.first()

            except UserWarning as inst:
                QMessageBox.critical( self, qApp.organizationName(),
                                      unicode( inst ) )
                logging.error( unicode( inst ) )
                self.reject()
            except Exception as inst:
                logging.error( unicode( inst ) )
                self.reject()
            finally:
                if QSqlDatabase.database().isOpen():
                    QSqlDatabase.database().close()

    #        self.dtFechaTime.setReadOnly( True )
            self.dtFechaTime.setDisplayFormat( 'dd/MM/yyyy' )
            self.dtFechaTime.setMaximumDateTime( QDateTime.currentDateTime() )
            if query.value( 0 ).toDate() is not None:
                self.dtFechaTime.setMinimumDate( query.value( 0 ).toDate() )


            self.cbcaja.setModel( self.cajasmodel )
            self.cbcaja.setModelColumn( 1 )
            self.cbcaja.setCurrentIndex( -1 )
            self.dtFechaTime.setDateTime( QDateTime.currentDateTime() )

            self.buttonBox.rejected.connect( self.reject )

    def accept( self ):
        if not self.cerrar:
            self.editmodel.datosSesion.cajaId = self.cajasmodel.record( self.cbcaja.currentIndex() ).value( "idcaja" ).toInt()[0]

        if self.editmodel.valid:
            supervisor = User( self.txtUser.text(), self.txtPassword.text() )
            if supervisor.valid:
                if not supervisor.hasRole( 'gerencia' ):
                    QMessageBox.critical( self, qApp.organizationName() + u": Autenticación", "El usuario %s no tiene permisos para autorizar la apertura de caja" % supervisor.user )
                    logging.info( u"El usuario %s intento autorizar la apertura de una sesión" % supervisor.user )
                    return


                self.editmodel.supervisorId = supervisor.uid
                self.editmodel.datosSesion.fecha = self.dtFechaTime.date()

                if not self.editmodel.save():
                    QMessageBox.warning( self,
                                         qApp.organizationName(),
                                         self.editmodel.error )
                    logging.error( self.editmodel.error )
                    #else:
                        #QMessageBox.warning( None, u"La sesión no fue abierta", u"La sesión no fue abierta. Por favor Contacte al administrador del sistema")
                else:
                    QMessageBox.information( self,
                                             qApp.organizationName(),
                                              u"La sesión fue abierta exitosamente" )
                    logging.info( u"El usuario %s ha abierto una sesión de caja autorizada por el usuario %s " % ( self.parentWindow.user.user, supervisor.user ) )
                    super( DlgApertura, self ).accept()
            else:
                QMessageBox.critical( self,
                                      qApp.organizationName() + u": Autenticación",
                                      supervisor.error )
                self.txtUser.setFocus()
                self.txtPassword.setText( "" )
        else:
            self.cbcaja.setFocus()
            QMessageBox.warning( self, qApp.organizationName(),
                                  self.editmodel.error )
            #self.editmodel.errorId =0

    @pyqtSlot()
    def on_txtSaldoC_editingFinished( self ):
        if self.editmodel != None:
            self.editmodel.saldoCordoba = Decimal( str( self.txtSaldoC.value() ) )


    @pyqtSlot()
    def on_txtSaldoD_editingFinished( self ):
        if self.editmodel != None:
            self.editmodel.saldoDolar = Decimal( str( self.txtSaldoD.value() ) )

    @property
    def idsesion( self ):
        return self.sesion

    @property
    def fecha( self ):
        return self.dtFechaTime.date()

class AperturaModel( object ):
    def __init__( self, datosSesion ):
        self.datosSesion = datosSesion

        self.supervisorId = 0
        self.errorId = 0
        self.error = ""
        self.saldoCordoba = Decimal( 0 )
        self.saldoDolar = Decimal( 0 )

    @property
    def valid( self ):
        if self.datosSesion.cajaId == 0:
            self.error = u"La sesión no fue abierta por que no se "\
            + "ha seleccionado una caja"
        else:
            return True
        return False
    @property
    def total( self ):

        total = ( self.saldoCordoba / self.datosSesion.tipoCambioBanco ) + self.saldoDolar
        return total

    def save( self ):
        query = QSqlQuery()
        resultado = False
        try:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open():
                    raise UserWarning( u"No se pudo conectar con la base de datos" )

            if not QSqlDatabase.database().transaction():
                raise Exception( u"No se pudo comenzar la transacción" )

            fecha = self.datosSesion.fecha.toString( "yyyyMMdd" )
            #extraer el tipo de cambio de acuerdo a la fecha junto con su id
            query.prepare( "SELECT idtc,tasa,IFNULL(tasabanco,tasa) as tasabanco FROM tiposcambio t where fecha=DATE('" + fecha + "')" )
            if not query.exec_():
                raise Exception( "No existe una tasa de cambio para la fecha " + fecha )


            if query.size() == 0:
                self.error = u"La sesión no fue abierta porque no existe un tipo de cambio para la fecha actual"
                return False


            query.first()

            self.datosSesion.tipoCambioId = query.value( 0 ).toInt()[0]
            self.datosSesion.tipoCambioOficial = Decimal( query.value( 1 ).toString() )
            self.datosSesion.tipoCambioBanco = Decimal( query.value( 2 ).toString() )



            query = QSqlQuery( "CALL spConsecutivo(%d,NULL);" % constantes.IDAPERTURA )

            if not query.exec_():
                raise Exception( "No pudo ser cargado el consecutivo del documento" )

            query.first()

            ndocimpreso = query.value( 0 ).toString()


            query.prepare( """INSERT INTO documentos(ndocimpreso,total,fechacreacion,idtipodoc,idcaja,idtipocambio)
            VALUES (:ndocimpreso,:total,:fecha,:tipodoc,:caja,:tipocambio)""" )

            total = self.total

            query.bindValue( ":ndocimpreso", ndocimpreso )

            query.bindValue( ":total", total.to_eng_string() )
            query.bindValue( ":fecha", fecha + QDateTime.currentDateTime().toString( "hhmmss" ) )
            query.bindValue( ":tipodoc", constantes.IDAPERTURA )
            query.bindValue( ":caja", self.datosSesion.cajaId )
            query.bindValue( ":tipocambio", self.datosSesion.tipoCambioId )

            if not query.exec_():
                raise Exception( query.lastError().text() )

            self.datosSesion.sesionId = query.lastInsertId().toInt()[0]
            insertedId = str( self.datosSesion.sesionId )

            if not query.prepare( "INSERT INTO personasxdocumento (idpersona,iddocumento,idaccion) VALUES" +
            "(:usuario," + insertedId + ", " + str( constantes.ACCCREA ) + " ), "
            "(:supervisor," + insertedId + "," + str( constantes.ACCAUTORIZA ) + " )" ):
                raise Exception( query.lastError().text() )


            query.bindValue( ":usuario", self.datosSesion.usuarioId )
            query.bindValue ( ":supervisor", self.supervisorId )

            if not query.exec_():
                raise Exception( query.lastError().text() )


            if not query.prepare( "INSERT INTO movimientoscaja(iddocumento,idtipomovimiento,idtipomoneda,monto) VALUES " +
            "(" + insertedId + ",1,1,:totalCordoba), "
            "(" + insertedId + ",1,2,:totalDolar)" ):

                raise Exception( query.lastError().text() )

            query.bindValue( ":totalCordoba", str( self.saldoCordoba ) )
            query.bindValue ( ":totalDolar", str( self.saldoDolar ) )

            if not query.exec_():
                raise Exception( query.lastError().text() )


            if not QSqlDatabase.database().commit():
                raise Exception( "No se pudo hacer commit" )

            resultado = True
        except Exception as inst:
            logging.critical( unicode( inst ) )
            logging.critical( query.lastError().text() )
            QSqlDatabase.database().rollback()
            self.error = u"Hubo un error al guardar la sesión de caja en "\
                + "la base de datos"

        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()
        return resultado
#
#
