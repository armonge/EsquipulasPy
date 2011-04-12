# -*- coding: utf-8 -*-
'''
Created on 18/05/2010
@author: Luis Carlos Mejia Garcia
'''
from PyQt4.QtCore import QDateTime
from PyQt4.QtSql import QSqlQuery, QSqlDatabase
from decimal import Decimal, DivisionByZero
from utility import constantes
from utility.decorators import return_decimal
from utility.movimientos import redondear
import logging

class PagoModel( object ):
    """
    El modelo que implementa los pagos
    """
    __documentType = constantes.IDPAGO

    def __init__( self , datosSesion ):

        super( PagoModel, self ).__init__()

        self.maxCordoba = Decimal( 0 )
        """
        @ivar: Almacena el maximo de Cordobas que se puede pagar
        @type: Decimal
        """
        self.maxDolar = Decimal( 0 )
        """
        @ivar: Almacena el maximo de Dolares que se puede pagar
        @type: Decimal
        """
        self.docImpreso = ""
        """
        @ivar: Almacena el numero de pago impreso
        @type: string
        """
        self.observaciones = ""
        """
        @ivar: Almacena el las observaciones del pago
        @type: string
        """
        self.totalC = Decimal( 0 )
        """
        @ivar: Almacena el total de cordobas del pago
        @type: Decimal
        """
        self.totalD = Decimal( 0 )
        """
        @ivar: Almacena el total de dolares del pago
        @type: Decimal
        """
        self.datosSesion = datosSesion
        """
        @ivar: Almacena DatosSesion para manejar las documentos en sesion de caja correspondiente
        @type: DatosSesion
        """
        self.conceptoId = 0
        """
        @ivar: Almacena el ID del concepto del documento pago
        @type: Integer
        """
        self.beneficiarioId = 0
        """
        @ivar: Almacena el ID del concepto del documento pago
        @type: Integer
        """
        self.aplicarRet = False
        """
        @ivar: Almacena si se aplicara retencion
        @type: Boolean
        """

        self.retencionId = 0
        """
        @ivar: Almacena el ID del tipo de retencion a aplicar
        @type: Integer
        """

        self.ivaId = 0
        """
        @ivar: Almacena el ID del IVA ACTIVO
        @type: Integer
        """
        self.__retencionTasa = Decimal( 0 )
        """
        @ivar: Almacena la tasa de retencion a aplicar
        @type: Decimal
        """
        self.__ivaTasa = Decimal( 0 )
        """
        @ivar: Almacena tasa del iva a aplicar
        @type: Integer
        """
        self.aplicarIva = True
        """
        @ivar: Almacena si se aplicara IVA
        @type: Boolean
        """
        self.errorMessage = ""
        """
        @ivar: Almacena el mensaje de error
        @type: String
        """


    def __getIvaTasa( self ):
        return self.__ivaTasa if self.aplicarIva else Decimal( 0 )
    def __setIvaTasa( self, value ):
        self.__ivaTasa = value
    ivaTasa = property( __getIvaTasa, __setIvaTasa )


    def __getRetencionTasa( self ):
        return self.__retencionTasa if self.aplicarRet else Decimal( 0 )
    def __setRetencionTasa( self, value ):
        self.__retencionTasa = value
    retencionTasa = property( __getRetencionTasa, __setRetencionTasa )

    def save( self ):
        try:
            if not QSqlDatabase.database().transaction():
                raise Exception( u"No se pudo comenzar la transacción" )

            query = QSqlQuery()

            if not query.prepare( """
            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,observacion,total,idtipocambio,idcaja,idconcepto) 
            VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:observacion,:total,:idtc,:caja,:con)
            """ ):
                raise Exception( "No se pudo guardar el documento" )
            query.bindValue( ":ndocimpreso", self.docImpreso )
            query.bindValue( ":fechacreacion", self.datosSesion.fecha.toString( 'yyyyMMdd' ) + QDateTime.currentDateTime().toString( "hhmmss" ) )
            query.bindValue( ":idtipodoc", self.__documentType )
            query.bindValue( ":observacion", self.observaciones )
            total = self.totalDolar #- ( self.retencionCordoba / self.datosSesion.tipoCambioBanco )
            query.bindValue( ":total", str( total ) )
#            query.bindValue( ":escontado", self.escontado )
            query.bindValue( ":idtc", self.datosSesion.tipoCambioId )
            query.bindValue( ":caja", self.datosSesion.cajaId )
            query.bindValue( ":con", self.conceptoId )
#            query.bindValue( ":estado",  constantes.INCOMPLETO)

            if not query.exec_():
                raise Exception( "No se pudo insertar el PAGO" )


            insertedId = query.lastInsertId().toString()

#INSERTAR LA RELACION CON LA SESION DE CAJA            
            query.prepare( """
                INSERT INTO docpadrehijos (idpadre,idhijo)
                VALUES (:idsesion,:idpago)
                """ )

            query.bindValue( ":idsesion", self.datosSesion.sesionId )
            query.bindValue( ":idpago", insertedId )

            if not query.exec_():
                raise Exception( "No se Inserto la relacion entre la sesion de caja y el pago" )

#INSERTAR LA RELACION CON El USUARIO , EL CLIENTE Y EL PROVEEDOR            
            query.prepare( 
                "INSERT INTO personasxdocumento (iddocumento,idpersona,idaccion) VALUES" +
                "(" + insertedId + ",:iduser,:autor),"
                "(" + insertedId + ",:idbeneficiario,:beneficiario)"
                )

            query.bindValue( ":iduser", self.datosSesion.usuarioId )
            query.bindValue( ":autor", constantes.AUTOR )
            query.bindValue( ":idbeneficiario", self.beneficiarioId )
            query.bindValue( ":beneficiario", constantes.PROVEEDOR )


            if not query.exec_():
                raise Exception( "No se Inserto la relacion entre el documento"

                                 + " y las personas" )
            if self.totalC != 0:
                if not query.prepare( "INSERT INTO movimientoscaja(iddocumento,idtipomovimiento,idtipomoneda,monto) VALUES " +
                "(" + insertedId + ",1,1,-:totalCordoba)" ):
                    raise Exception( query.lastError().text() )
                query.bindValue( ":totalCordoba", str( self.totalC ) )
                if not query.exec_():
                    raise Exception( "No se Inserto el movimiento caja en dolares" )


            if self.totalD != 0:
                if not query.prepare( "INSERT INTO movimientoscaja(iddocumento,idtipomovimiento,idtipomoneda,monto) VALUES " +
                "(" + insertedId + ",1,2,-:totalDolar)" ):
                    raise Exception( query.lastError().text() )
                query.bindValue ( ":totalDolar", str( self.totalD ) )
                if not query.exec_():
                    raise Exception( "No se Inserto el movimiento "\
                                     + "caja en dolares" )



#VERIFICO SI el id del iva es cero. NO SERA CERO CUANDO LA BODEGA=1 PORQUE ESTA NO ES exonerada                                 
            if self.aplicarIva:
                query.prepare( """
                INSERT INTO costosxdocumento (iddocumento, idcostoagregado) 
                VALUES( :iddocumento, :idcostoagregado )
                """ )
                query.bindValue( ":iddocumento", insertedId )
                query.bindValue( ":idcostoagregado", self.ivaId )

                if not query.exec_():
                    raise Exception( "El iva NO SE INSERTO" )

            if self.aplicarRet:
                query.prepare( """
                INSERT INTO costosxdocumento (iddocumento, idcostoagregado) 
                VALUES( :iddocumento, :idcostoagregado )
                """ )
                query.bindValue( ":iddocumento", insertedId )
                query.bindValue( ":idcostoagregado", self.retencionId )

                if not query.exec_():
                    raise Exception( "La retencion NO SE INSERTO" )



            if not QSqlDatabase.database().commit():
                raise Exception( "No se pudo guardar el pago" )

        except Exception as inst:
            logging.error( query.lastError().text() )
            logging.error( unicode( inst ) )
            QSqlDatabase.database().rollback()
            return False

        return True

    @property
    @return_decimal
    def totalDolar( self ):
        try:
            return self.totalD + redondear( self.totalC / self.datosSesion.tipoCambioBanco )
        except DivisionByZero:
            return Decimal( "0" )
    @property
    @return_decimal
    def totalCordoba( self ):
        try:
            return self.totalC + redondear( self.totalD * self.datosSesion.tipoCambioBanco )
        except DivisionByZero:
            return Decimal( "0" )
    @property
    @return_decimal
    def subTotalDolar( self ):
        return redondear( self.totalDolar / ( 1 + ( self.ivaTasa / 100 ) ) )

    @property
    @return_decimal
    def subTotalCordoba( self ):
        return redondear( self.totalCordoba / ( 1 + ( self.ivaTasa / 100 ) ) )

    @property
    def tieneRetencion( self ):
        sub = self.subTotalCordoba
        return sub > 1000

    @property
    def retencionCordoba( self ):
        rt = self.retencionTasa
        if rt > 0 :
            ret = self.subTotalCordoba * ( self.retencionTasa / 100 )
            return ret if ret != 0 else Decimal( 0 )
        else:
            return Decimal( 0 )

