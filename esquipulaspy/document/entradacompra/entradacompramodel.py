# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: Andrés Reyes Monge
'''
from PyQt4.QtCore import QModelIndex, Qt, QDateTime, QAbstractTableModel
from PyQt4.QtSql import QSqlDatabase, QSqlQuery
from decimal import Decimal
from lineaentradacompra import LineaEntradaCompra
from utility import constantes
from utility.decorators import return_decimal
from utility.docbase import DocumentBase
from utility.moneyfmt import moneyfmt
from utility.movimientos import movEntradaCompra
import logging



IDARTICULO, DESCRIPCION, CANTIDAD, PRECIO, PRECIOD, TOTALC, TOTALD = range( 7 )
class EntradaCompraModel( DocumentBase ):
    """
    esta clase es el modelo utilizado en la tabla en la que se editan los documentos
    """
    __documentType = 21
    """
    @cvar: El id del tipo de documento de un Objeto EntradaCompra
    @type: int 
    """
    def __init__( self ):
        super( EntradaCompraModel, self ).__init__()
        self.dirty = False
        self.providerId = 0
        """
        @ivar: El id del tipo de documento
        @type: int 
        """

        self.observations = ""
        """
        @ivar:Las observaciones del documento
        @type:string
        """

        self.rateIVA = Decimal( 0 )
        """
        @ivar:El porcentaje de IVA del documento
        @type:Decimal
        """

        self.idIVA = 0
        """
        @ivar:El id del IVA del documento
        @type: int 
        """

        self.lines = []
        """
         @ivar:Las lineas del documento
         @type: LineaEntradaCompra[] 
        """

        self.printedDocumentNumber = ""
        """
        @ivar:El numero impreso del documento
        @type: string
        """

        self.datetime = QDateTime.currentDateTime()
        """
        @ivar: La fecha del documento
        @type: QDateTime
        """

        self.uid = 0
        """
        @ivar: El id del usuario que guarda el documento
        @type: int 
        """

        self.saveError = ""
        """
        @ivar:Los mensajes de error al salvar
        @type: string
        """

        self.validError = ""
        """
        @ivar:Los errores al validar un documento 
        @type:string
        """

        self.exchangeRate = Decimal( 0 )
        """
        @ivar:El tipo de cambio que se utiliza en el documento
        @type:Decimal
        """

        self.exchangeRateId = 0
        """
        @ivar:El id del tipo de cambio del documento
        @type: int
        """

        self.paytipe = 1
        """
        @ivar: El tipo de pago del documento
        
            0 = Credito
            
            1 = Contado
        @type: int
        """

        self.isCheck = False
        """
        @ivar: Si esta entrada de compra se paga con un cheque o no
        @type: bool
        """




    @property
    def valid( self ):
        """
        Un documento es valido cuando 
        self.printedDocumentNumber != ""
        self.providerId !=0
        self.validLines >0
        self.idIVA !=0
        self.uid != 0
        self.exchangerateid != 0
        Es valido el documento
        @rtype: bool
        """
        if not int( self.exchangeRateId ) > 0:
            self.validError = "No se ha definido un tipo de cambio para el documento"
            return False
        elif not self.printedDocumentNumber != "":
            self.validError = "No ha escrito el numero de documento"
            return False
        elif not int( self.providerId ) != 0:
            self.validError = "No ha definido al proveedor"
            return False
        elif not int( self.validLines ) > 0:
            self.validError = "No hay ninguna linea valida en la entrada de compra"
            return False
        elif not int( self.idIVA ) != 0:
            print self.idIVA
            self.validError = u"No hay un IVA asociado a la entrada de compra"
            return False
        elif not int( self.uid ) != 0:
            self.validError = "No se ha definido el usuario para la entrada compra"
            return False
        return True

    @property
    @return_decimal
    def subtotalC( self ):
        """
        El subtotal del documento, esto es el total antes de aplicarse el IVA
        @rtype: Decimal
        """
        return sum( [x.totalC for x in self.lines if x.valid ] )



    @property
    def totalC( self ):
        """
        El total neto del documento, despues de haber aplicado IVA
        @rtype: Decimal
        """
        return self.subtotalC + self.IVAC

    @property
    @return_decimal
    def subtotalD( self ):
        """
        El subtotal del documento, esto es el total antes de aplicarse el IVA
        @rtype: Decimal
        """
        return sum( [x.totalD for x in self.lines if x.valid ] )

    @property
    def totalD( self ):
        """
        El total en dolares del documento
        @rtype: Decimal
        """
        return  self.subtotalD + self.IVAD

    @property
    def IVAD( self ):
        """
        El IVA total del documento, se calcula en base a subtotal y rateIVA, en dolares
        @rtype: Decimal
        """
        return self.subtotalD * ( self.rateIVA / Decimal( 100 ) )

    @property
    def IVAC( self ):
        """
        El IVA total del documento, se calcula en base a subtotal y rateIVA, en cordobas
        @rtype: Decimal
        """

        return self.subtotalC * ( self.rateIVA / Decimal( 100 ) )




    #Clases especificas del modelo
    def rowCount( self, _index = QModelIndex() ):
        """
        El numero de filas del documento, es igual a la cantidad de lineas en self.lines
        """
        return len( self.lines )

    def columnCount( self, _index = QModelIndex() ):
        """
        El numero de columnas del modelo
        """
        return 7

    def data( self, index, role = Qt.DisplayRole ):
        """
        Los datos que muestran las vistas asignadas a este modelo
        """
        if not index.isValid() or not ( 0 <= index.row() < len( self.lines ) ):
            return ""
        line = self.lines[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == IDARTICULO:
                return line.itemId
            elif column == DESCRIPCION:
                return line.itemDescription
            elif column == CANTIDAD:
                return line.quantity if line.quantity != 0 else ""
            elif column == PRECIO:
                return moneyfmt( Decimal( line.itemPriceC ), 4, "C$" ) if line.itemPriceC != 0 else ""
            elif column == PRECIOD:
                return moneyfmt( Decimal( line.itemPriceD ), 4, "US$" ) if line.itemPriceD != 0 else ""
            elif column == TOTALC:
                return moneyfmt( line.totalC , 4, "C$" ) if line.totalC != 0 else ""
            elif column == TOTALD:
                return moneyfmt( line.totalD, 4, "US$" ) if line.totalD != 0 else ""
        elif role == Qt.EditRole:
            if column == PRECIO:
                return line.itemPriceC
            elif column == PRECIOD:
                return line.itemPriceD

    def flags( self, index ):
        """
        Las flags de las celdas de este modelo, es editable para todas menos para TOTALC y TOTALD
        """
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column()  in ( TOTALC, TOTALD ):
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled
        return Qt.ItemFlags( QAbstractTableModel.flags( self, index ) | Qt.ItemIsEditable )

    def setData( self, index, value, _role = Qt.EditRole ):
        """
        modificar los datos del modelo, este metodo se comunica con el delegate
        """
        if index.isValid() and 0 <= index.row() < len( self.lines ) :
            line = self.lines[index.row()]
            column = index.column()
            if column == DESCRIPCION:
                line.itemId = value[0]
                line.itemDescription = value[1]
            elif column == CANTIDAD:
                line.quantity = value.toInt()[0]
            elif column == PRECIO:
                line.itemPriceC = Decimal( value.toString() )
            elif column == PRECIOD:
                line.itemPriceD = Decimal( value.toString() )

            self.dirty = True



            self.dataChanged.emit( index, index )
            #si la linea es valida y es la ultima entonces aniadir una nueva
            if  index.row() == len( self.lines ) - 1 and line.valid:
                self.insertRows( len( self.lines ) )


            return True
        return False

    def insertRows( self, position, rows = 1, _index = QModelIndex ):
        """
        Insertar filas en el modelo
        """
        self.beginInsertRows( QModelIndex(), position, position + rows - 1 )
        for row in range( rows ):
            self.lines.insert( position + row, LineaEntradaCompra( self ) )
        self.endInsertRows()
        self.dirty = True
        return True

    def removeRows( self, position, rows = 1, _index = QModelIndex() ):
        """
        Borrar filas del modelo
        """
        if len( self.lines ) > 1 and self.lines[position].valid:
            self.beginRemoveRows( QModelIndex(), position, position + rows - 1 )
            for n in range( rows ):
                del self.lines[position + n]
            self.endRemoveRows()
            self.dirty = True
            return True
        else:
            return False

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        """
        Lo que se muestra en los headers del modelo
        """
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignLeft | Qt.AlignVCenter
            return Qt.AlignRight | Qt.AlignVCenter
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if  section == DESCRIPCION:
                return u"Descripción"
            elif section == PRECIO:
                return "Precio C$"
            elif section == PRECIOD:
                return "Precio US$"
            elif section == TOTALC:
                return "Total C$"
            elif section == CANTIDAD:
                return "Cantidad"
            elif section == TOTALD:
                return "Total US$"
        return int( section + 1 )


    def save( self ):
        """
        Este metodo guarda el documento actual en la base de datos
        @return: Si se pudo o no guardar el documento
        @rtype: bool
        """
        if not self.valid:
            raise Exception( "El documento a salvar no es valido" )

        query = QSqlQuery()

        try:

            if not QSqlDatabase.database().transaction():
                raise Exception( u"No se pudo comenzar la transacción" )



            if not query.prepare( """
            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,  observacion,total, idbodega, idtipocambio, escontado) 
            VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:observacion,:total,:idbodega, :idtc, :escontado)
            """ ):
                raise Exception( "No se pudo preparar la consulta para ingresar el documento" )
            query.bindValue( ":ndocimpreso", self.printedDocumentNumber )
            query.bindValue( ":fechacreacion", self.datetime.toString( 'yyyyMMddhhmmss' ) )
            query.bindValue( ":idtipodoc", self.__documentType )
            query.bindValue( ":observacion", self.observations )
            query.bindValue( ":total", self.totalD.to_eng_string() )
            query.bindValue( ":idbodega", 1 )
            query.bindValue( ":idtc", self.exchangeRateId )
            query.bindValue( ":escontado", self.paytipe )


            if not query.exec_():
                raise Exception( "No se pudo insertar el documento" )

            insertedId = query.lastInsertId().toInt()[0]

            #insertar el usuario
            if not query.prepare( """
            INSERT INTO personasxdocumento (idpersona, iddocumento,idaccion) 
            VALUE (:idusuario, :iddocumento,:idaccion)
            """ ):
                raise Exception( "No se pudo preparar la consulta para ingresar el usuario" )
            query.bindValue( ":idusuario", self.uid )
            query.bindValue( ":iddocumento", insertedId )
            query.bindValue( ":idaccion", constantes.AUTOR )

            if not query.exec_():

                raise Exception( "No se pudo insertar  el usuario" )

            #insertar el proveedor
            if not query.prepare( """
            INSERT INTO personasxdocumento (idpersona, iddocumento,idaccion) 
            VALUE (:idproveedor, :iddocumento,:idaccion)
            """ ):
                raise Exception( "No se pudo preparar la consulta para ingresar proveedor" )
            query.bindValue( ":idproveedor", self.providerId )
            query.bindValue( ":iddocumento", insertedId )
            query.bindValue( ":idaccion", constantes.PROVEEDOR )

            if not query.exec_():
                raise Exception( "No se pudo insertar el proveedor" )



            if self.isCheck:
                raise UserWarning( "Todavia no es posible guardar entradas de compras pagadas con cheques" )

            for nline, line in enumerate( self.lines ):
                if line.valid:
                    line.save( insertedId, nline )


            if not query.prepare( """
            INSERT INTO costosxdocumento (iddocumento, idcostoagregado) VALUES( :iddocumento, :idcostoagregado )
            """ ):
                raise Exception( "No se pudo preparar la consulta para insertar el costo del documento" )
            query.bindValue( ":iddocumento", insertedId )
            query.bindValue( ":idcostoagregado", self.idIVA )
            if not query.exec_():
                raise Exception( "No se pudo insertar el costo para el documento" )

            #manejar las cuentas contables
            movEntradaCompra( insertedId, self.totalC, self.IVAC )


            if not QSqlDatabase.database().commit():
                raise Exception( "No se pudo hacer commit" )
        except Exception as inst:
            logging.critical( query.lastError().text() )
            logging.critical( unicode( inst ) )
            QSqlDatabase.database().rollback()
            return False

        return True


