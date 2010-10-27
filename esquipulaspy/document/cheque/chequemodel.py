# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: Marcos Moreno
'''
import logging
from decimal import Decimal, DivisionByZero

from PyQt4.QtSql import QSqlDatabase, QSqlQuery
from PyQt4.QtCore import Qt, QDateTime, QModelIndex

from utility.accountselector import AccountsSelectorModel
from utility import constantes

IDARTICULO, DESCRIPCION, REFERENCIA, MONTO, TOTALPROD, MONEDA = range( 6 )
IDCUENTA, CODCUENTA, NCUENTA, MONTO = range( 4 )
class ChequeModel( AccountsSelectorModel ):
    """
    esta clase es el modelo utilizado en la tabla en la que se editan los documentos
    """

    __documentType = constantes.IDCHEQUE
    """
    @cvar:El tipo de documento
    @type: int
    """
    def __init__( self ):
        super( ChequeModel, self ).__init__()

        self.proveedorId = 0
        """
        @ivar: El id del proveedor en este documento
        @type: int
        """
        self.observations = ""
        """
        @ivar: Las observaciones que podria tener el documento
        @type: string
        """
        self.printedDocumentNumber = ""
        """
        @ivar: El numero de documento impreso
        @type:string
        """
        self.datetime = QDateTime.currentDateTime()
        """
        @ivar: La fecha en la que se hizo el documento
        @type: QDateTime
        """
        self.uid = 0
        """
        @ivar: El id del usuario que esta haciendo este documento
        @type: int
        """
        self.conceptoId = 0
        """
        @ivar: El id del concepto de este documento
        @type: int
        """

        self.simbolo = ""
        """
        @ivar: El simbolo de la moneda del documento
        @type: String
        """


        self.retencionId = 0
        """
        @ivar: El id de la retención de este documento
        @type: int
        """
        self.retencionPorcentaje = Decimal(0)
        """
        @ivar: El porcentaje de retención de este documento
        @type: Decimal
        """

        self.ivaRate = Decimal( 0 )
        """
        @ivar: El porcentaje del iva a aplicar en este documento
        @type: Decimal
        """

        self.moneda = ""
        """
        @ivar: El simbolo de la moneda a aplicar en este documento
        @type: String
        """

        self.exchangeRateId = 0
        """
        @ivar: El id del tipo de cambio de este documento
        @type: int
        """
        self.exchangeRate = Decimal( 0 )
        """
        @ivar: El tipo de cambio usado en este documento
        @type: Decimal
        """

        self.validError = ""
        """
        @ivar: Si existe o no un error de validación en este documento entonces se muestra aca
        @type: string
        """
        self.hasretencion = False
        """
        @ivar: Para verificar si tiene retencion o no
        @type: Boolean
        """
        self.subtotal = Decimal( 0 )
        """
        @ivar: El subtotal del documento
        @type: Decimal
        """
        self.hasiva = False
        """
        @ivar: Para determinar si el cheque lleva IVA o no
        @type: Boolean
        """
        self.ivaId = 0
        """
        @ivar: El ID del costo agregado IVA
        @type: Int
        """

    def setData( self, index, value, _role = Qt.EditRole ):
        if index.isValid() and 0 <= index.row() < len( self.lines ):
            line = self.lines[index.row()]
            column = index.column()
            if column in ( NCUENTA, CODCUENTA ):
                line.itemId = value[0]
                line.code = value[1]
                line.name = value[2]
            if column == MONTO:
                line.amount = Decimal( value.toString() ).quantize( Decimal( '0.0001' ) ) if type( value ) != Decimal else value.quantize( Decimal( '0.0001' ) )


            if not super( ChequeModel, self ).valid and self.lines[-1].valid and self.currentSum != 0:
                self.insertRow( len( self.lines ) )
            elif not self.valid and not self.lines[-1].valid:
                self.lines[-1].amount = self.currentSum * -1

            if super( ChequeModel, self ).valid and not self.lines[-1].valid:
                if len( self.lines ) > 1:
                    self.removeRows( len( self.lines ) - 1, 1 )
            self.dataChanged.emit( index, index )

            self.dataChanged.emit( self.index( MONTO, len( self.lines ) ) , self.index( MONTO, len( self.lines ) ) )

            return True
        return False
        
    def removeRows( self, position, rows = 1, _parent = QModelIndex() ):
        """
        En el modelo del cheque no se puede borrar la primera fila
        """
        if position > 0:
            return super(ChequeModel, self).removeRows(position, rows, _parent)

        return False

        
    @property
    def valid( self ):
        """
        Un documento es valido cuando 
        self.printedDocumentNumber != ""
        self.providerId !=0
        self.validLines >0
        self.__idIVA !=0
        self.uid != 0
        self.total>0 
        """
        try:
            if  self.printedDocumentNumber == "":
                raise UserWarning("No existe numero de doc impreso")
            elif int( self.proveedorId ) < 1:
                raise UserWarning("No ha seleccionado ningun beneficiario")
            elif Decimal( self.subtotal ) <= 0:
                raise UserWarning("Escriba una cantidad para el documento")
            elif int( self.uid ) == 0:
                raise UserWarning("Existe un error con el Usario que esta "\
                                    + "creando el documento")
            elif int( self.conceptoId ) == 0:
                raise UserWarning("No hay un concepto seleccionado")
            elif self.exchangeRateId == 0:
                raise UserWarning("No se ha seleccionado un tipo de cambio")
            elif self.hasretencion == True and self.retencionPorcentaje == 0:
                raise UserWarning( u"No se ha seleccionado un porcentaje de Retención")
            elif not super( ChequeModel, self ).valid :
                raise UserWarning("Hay un error en sus cuentas contables")
        except UserWarning as inst:
            self.validError = unicode(inst)
            return False
        return True



    def save( self ):
        """
        Este metodo guarda el documento actual en la base de datos
        """

        if not self.valid:
            raise UserWarning( "El documento a guardar no es valido" )

        query = QSqlQuery()

        try:

            if not QSqlDatabase.database().transaction():
                raise UserWarning( u"No se pudo iniciar la transacción" )
#           
            #INSERTAR CHEQUE
            query.prepare( """
            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,idestado, observacion,total,idtipocambio,idconcepto) 
            VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:estado,:observacion,:total,:idtc,:concepto)
            """ )

            query.bindValue( ":ndocimpreso", self.printedDocumentNumber )
            query.bindValue( ":fechacreacion", self.datetime.toString( 'yyyyMMddhhmmss' ) )
            query.bindValue( ":idtipodoc", self.__documentType )
            query.bindValue( ":estado", constantes.CONFIRMADO )
            query.bindValue( ":observacion", self.observations )
            query.bindValue( ":total", self.totalDolares.to_eng_string() )
            query.bindValue( ":idtc", self.exchangeRateId )
            query.bindValue( ":concepto", self.conceptoId )

            if not query.exec_():
                raise UserWarning( "No se pudo crear el Cheque" )
            insertedId = query.lastInsertId().toString()
            #INSERTAR LA RELACION CON El USUARIO , EL CLIENTE Y EL PROVEEDOR            
            if not query.prepare( 
                "INSERT INTO personasxdocumento (iddocumento,idpersona,idaccion) VALUES" +
                "(" + insertedId + ",:iduser,:autor),"
                "(" + insertedId + ",:idproveedor,:proveedor)"
                ):
                raise Exception( "No se puedo preparar la consulta para insertar las personas" )

            query.bindValue( ":iduser", self.uid )
            query.bindValue( ":idproveedor", self.proveedorId )
            query.bindValue( ":autor", constantes.AUTOR )
            query.bindValue( ":proveedor", constantes.PROVEEDOR )

            if not query.exec_():
                raise Exception( "No se Inserto la relacion entre el documento y las personas" )

            if self.hasiva == True:
                # INSERTAR EL ID DEL COSTO IVA                
                query.prepare( """
                INSERT INTO costosxdocumento (iddocumento, idcostoagregado) VALUES( :iddocumento, :idcostoagregado )
                """ )
                query.bindValue( ":iddocumento", insertedId )
                query.bindValue( ":idcostoagregado", self.ivaId )
                if not query.exec_():
                    raise UserWarning( "el costo IVA no se inserto" )

            if self.retencion >= 0 and self.retencionId >= 0 and self.hasretencion == True:
                #INSERTAR EL DOCUMENTO RETENCION            
                query.prepare( """
                INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,idestado, observacion,total,escontado,idtipocambio,idconcepto) 
                VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:idestado,:observacion,:total,:escontado,:idtc,:concepto)
                """ )
                query.bindValue( ":ndocimpreso", self.printedDocumentNumber )
                query.bindValue( ":fechacreacion", self.datetime )
                query.bindValue( ":idtipodoc", constantes.IDRETENCION )
                query.bindValue( ":idestado", constantes.CONFIRMADO )
                query.bindValue( ":observacion", self.observations )
                query.bindValue( ":total", self.retencion.to_eng_string() )
                query.bindValue( ":escontado", 1 )
                query.bindValue( ":idtc", self.exchangeRateId )
                query.bindValue( ":concepto", self.conceptoId )
                if not query.exec_():
                    raise UserWarning( "No se Inserto la retencion" )

                idret = query.lastInsertId().toInt()[0]

                #INSERTAR EL BENEFICIARIO Y USUARIO DE LA RETENCION
                query.prepare( "INSERT INTO personasxdocumento(iddocumento,idpersona,idaccion) VALUES(:iddocumento,:idusuario,:autor)" )
                query.bindValue( ":iddocumento", idret )
                query.bindValue( ":idusuario", self.uid )
                query.bindValue( ":autor", constantes.AUTOR )
                if not query.exec_():
                    raise UserWarning( "No se pudo regitrar el usuario que creo la retencion" )


                query.prepare( "INSERT INTO personasxdocumento(iddocumento,idpersona,idaccion) VALUES(:iddocumento,:idproveedor,:proveedor)" )
                query.bindValue( ":iddocumento", idret )
                query.bindValue( ":idproveedor", self.proveedorId )
                query.bindValue( ":proveedor", constantes.PROVEEDOR )
                if not query.exec_():
                    raise UserWarning( "No se pudo insertar el beneficiario de la retencion" )

                #DOCUMENTO PADRE CHEQUE, DOCUMENTO HIJO RETENCION
                query.prepare( """
                INSERT INTO docpadrehijos (idpadre,idhijo)
                VALUES (:idcheque,:idretencion)
                """ )

                query.bindValue( ":idcheque", insertedId )
                query.bindValue( ":idretencion", idret )

                if not query.exec_():
                    raise UserWarning( "No se Inserto la relacion entre la retencion y el Cheque" )


                # INSERTAR EL ID DEL COSTO RETENCION                
                query.prepare( """
                INSERT INTO costosxdocumento (iddocumento, idcostoagregado) VALUES( :iddocumento, :idcostoagregado )
                """ )
                query.bindValue( ":iddocumento", idret )
                query.bindValue( ":idcostoagregado", self.retencionId )
                if not query.exec_():
                    raise UserWarning( "el costo Retencion  NO SE INSERTO" )

            #INSERTAR LAS CUENTAS CONTABLES
            for lineid, line in enumerate( self.lines ):
                if line.valid:
                    line.save( insertedId, lineid + 1 )

            if not QSqlDatabase.database().commit():
                raise UserWarning( "No se pudo realizar la Transaccion" )

            return True

        except UserWarning as inst:
            logging.error( unicode( inst ) )
            logging.error( query.lastError().text() )
            QSqlDatabase.database().rollback()
            return False
        except Exception as inst:
            logging.critical( unicode( inst ) )
            logging.critical( query.lastError().text() )
            QSqlDatabase.database().rollback()
            return False
    @property
    def totalCordobas( self ):
        """
        El total neto del documento, despues de haber aplicado IVA y Retencion en Cordobas
        @rtype: Decimal
        """
        subtotalcordobas = self.subtotal if self.moneda == constantes.IDCORDOBAS else self.subtotal * self.exchangeRate
        retencion = self.retencion
        if self.hasiva == True:
            return subtotalcordobas + ( subtotalcordobas * self.ivaRate / 100 ) - ( retencion if self.moneda == constantes.IDCORDOBAS else retencion * self.exchangeRate )
        else:
            return subtotalcordobas - ( retencion if self.moneda == constantes.IDCORDOBAS else retencion * self.exchangeRate )


    @property
    def totalDolares( self ):
        """
        El total neto del documento, despues de haber aplicado IVA y Retencion en Dolares
        @rtype: Decimal
        """
        try:
            return self.totalCordobas / self.exchangeRate
        except DivisionByZero as _inst:
            return Decimal( 0 )


    @property
    def iva( self ):
        """
        El valor del IVA en Cordobas
        @rtype: Decimal
        """
        if self.hasiva == True:
            return self.subtotal * ( self.ivaRate / 100 )
        else:
            return Decimal( 0 )

    @property
    def retencion( self ):
        """
        El valor de la retencion en cordobas
        @rtype: Decimal
        """
        subtotalcordobas = self.subtotal if self.moneda == constantes.IDCORDOBAS else self.subtotal * self.exchangeRate
        if subtotalcordobas > 1000:
            return self.subtotal * ( self.retencionPorcentaje / 100 )
        else:
            return Decimal( 0 )

    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled
        elif index.row() != 0:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable
        else:
            return Qt.ItemIsEnabled
