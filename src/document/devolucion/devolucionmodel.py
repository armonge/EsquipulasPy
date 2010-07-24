# -*- coding: utf-8 -*-
'''
Created on 19/05/2010

@author: armonge
'''
from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt, QDateTime, SIGNAL
from PyQt4.QtSql import QSqlQuery, QSqlDatabase

from decimal import Decimal
from document.devolucion.lineadevolucion import LineaDevolucion
from utility.moneyfmt import moneyfmt
from utility.movimientos import movFacturaCredito
import utility.constantes

DESCRIPCION, PRECIO, CANTIDADMAX, CANTIDAD, TOTALPROD = range( 5 )
class DevolucionModel( QAbstractTableModel ):
    """
    Esta clase es el modelo utilizado en la tabla en la que se editan los documentos
    """
    __documentType = utility.constantes.IDDEVOLUCION
    """
    @cvar: El id del tipo de documento
    @type: int
    """
    def __init__( self ):
        super( DevolucionModel, self ).__init__()
        self.observations = ""
        """
        @ivar:Las observaciones del documento
        @type:string
        """
        self.lines = []
        """
        @ivar:Las lineas en esta devolucion
        @type: LineaDevolucion[]
        """
        self.printedDocumentNumber = ""
        """
        @ivar:El numero de esta devolución
        @type:string
        """
        self.clientId = 0
        """
        @ivar:El id del cliente de esta devolución
        @type: int
        """
        self.invoiceId = 0
        """
        @ivar: El  id de la factura para la cual se realiza esta devolución
        @type:int
        """
        self.billPrinted = ""
        """
        @ivar:El numero impreso de la factura
        @type:string
        """
        self.datetime = QDateTime.currentDateTime()
        """
        @ivar:La hora y fecha del documento
        @type:string
        """
        self.uid = 0
        """
        @ivar: El id del usuario que realiza esta devlución
        @type: int
        """
        self.clientName = ""
        """
        @ivar: El nombre del cliente que realiza esta devolución
        @type: string
        """

        self.ivaRate = Decimal( 0 )
        """
        @ivar: El porcentaje de IVA en esta devolucion, es el de la factura
        @type:Decimal
        """
        self.ivaRateId = 0
        """
        @ivar: El id de este porcentaje IVA
        @type: int
        """
        self.applyIva = True
        """
        @ivar: Si se aplica o no IVA en esta devolución
        type:bool
        """

        self.exchangeRateId = 0
        """
        @ivar: El id del tipo de cambio en esta devolución
        @type:int
        """
        self.exchangeRate = Decimal( 0 )
        """
        @ivar: EL tipo de cambio de esta devolución
        @type:Decimal
        """


    @property
    def valid( self ):
        """
        Un documento es valido cuando 
        @rtype: bool
        """
        if    int( self.clientId ) != 0 and int( self.validLines ) > 0  and int( self.uid ) != 0 and int( self.invoiceId ) != 0 and self.printedDocumentNumber != "" and int( self.exchangeRateId ) != 0 :
            return True
        return False

    @property
    def totalD( self ):
        """
        El total en dolares del documento
        @rtype: Decimal 
        """
        foo = sum( [ line.totalD for line in self.lines if line.valid ] )
        return foo if foo != 0 else Decimal( 0 )
    @property
    def subtotalD( self ):
        """
        El subtotal en dolares del documento
        @rtype: Decimal
        """
        return self.totalD / ( 1 + ( self.ivaRate / 100 ) )

    @property
    def totalC( self ):
        """
        El total en cordobas del documento
        @rtype: decimal
        """
        return self.totalD * self.exchangeRate

    @property
    def subtotalC( self ):
        """
        El subtotal en cordobas del documento
        @rtype: Decimal
        """
        return self.subtotalD * self.exchangeRate
    @property
    def ivaD( self ):
        """
        El iva en dolares
        @rtype: Decimal
        """
        return self.subtotalD * ( self.ivaRate / 100 )

    @property
    def ivaC( self ):
        """
        El iva en cordobas
        @rtype: Decimal
        """
        return self.ivaD * self.exchangeRate

    @property
    def totalCostD( self ):
        """
        El costo total del documento, en dolares
        @rtype: Decimal
        """
        foo = sum( [ line.costoD for line in self.lines if line.valid ] )
        return foo if foo != 0 else Decimal( 0 )

    @property
    def  totalCostC( self ):
        """
        El costo en cordobas del documento
        """
        return self.totalCostD * self.exchangeRate

    @property
    def validLines( self ):
        """
        la cantidad de lineas validas que hay en el documento
        @rtype: int
        """
        return len( [ line for line in self.lines if line.valid ] )

    #Clases especificas del modelo
    def rowCount( self, index = QModelIndex() ):
        return len( self.lines )

    def columnCount( self, index = QModelIndex() ):
        return 5

    def data( self, index, role = Qt.DisplayRole ):
        """
        darle formato a los campos de la tabla
        """
        if not index.isValid() or not ( 0 <= index.row() < len( self.lines ) ):
            return None
        line = self.lines[index.row()]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == DESCRIPCION:
                return line.itemDescription
            elif column == PRECIO:
                return moneyfmt( Decimal( line.itemPrice ), 4, "US$" )
            elif column == CANTIDADMAX:
                return line.maxquantity
            elif column == CANTIDAD:
                return line.quantity
            elif column == TOTALPROD:
                return moneyfmt( line.totalD, 4, "US$" )

    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column() == CANTIDAD:
            return Qt.ItemFlags( QAbstractTableModel.flags( self, index ) | Qt.ItemIsEditable )
        else:
            return Qt.ItemIsEnabled


    def setData( self, index, value, role = Qt.EditRole ):
        """
        modificar los datos del modelo, este metodo se comunica con el delegate
        """
        if index.isValid() and 0 <= index.row() < len( self.lines ):
            line = self.lines[index.row()]
            if index.column() == CANTIDAD:
                line.quantity = value.toInt()[0]

            self.dirty = True

            self.emit( SIGNAL( "dataChanged(QModelIndex, QModelIndex)" ), index, index )

            return True
        return False

    def insertRows( self, position, rows = 1, index = QModelIndex() ):
        self.beginInsertRows( QModelIndex(), position, position + rows - 1 )
        for row in range( rows ):
            self.lines.insert( position + row, LineaDevolucion( self ) )
        self.endInsertRows()
        self.dirty = True
        return True

    def removeRows( self, position, rows = 1, index = QModelIndex ):
        raise NotImplementedError

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignLeft | Qt.AlignVCenter
            return Qt.AlignRight | Qt.AlignVCenter

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == DESCRIPCION:
                return "Articulo"

            elif section == PRECIO:
                return "Precio Unitario"
            elif section == CANTIDADMAX:
                return "Maximo de unidades"
            elif section == CANTIDAD:
                return "Unidades"
            elif section == TOTALPROD:
                return "Total"
        return int( section + 1 )


    def save( self ):
        """
        Este metodo guarda el documento actual en la base de datos
        """
        query = QSqlQuery()
        try:
            if not self.valid:
                raise Exception( "El documento a salvar no es valido" )
            

            if not QSqlDatabase.database().transaction():
                raise Exception( u"No se puedo comenzar la transacción" )

            query.prepare( """
            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,idusuario,anulado, idpersona, observacion,total, idtipocambio)
            VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:idusuario,:anulado,:idpersona,:observacion,:total, :idtipocambio)
            """ )

            query.bindValue( ":ndocimpreso", self.printedDocumentNumber )
            query.bindValue( ":fechacreacion", self.datetime.toString( 'yyyyMMddhhmmss' ) )
            query.bindValue( ":idtipodoc", self.__documentType )
            query.bindValue( ":idusuario", self.uid )
            query.bindValue( ":anulado", 0 )
            query.bindValue( ":idpersona", self.clientId )
            query.bindValue( ":observacion", self.observations )
            query.bindValue( ":total", self.totalD.to_eng_string() )
            query.bindValue( ":idtipocambio", self.exchangeRateId )

            if not query.exec_():
                raise Exception( "No se pudo insertar el documento" )

            insertedId = query.lastInsertId().toInt()[0]

            for linea in self.lines:
                if linea.valid:
                    linea.save( insertedId )

#FIXME:Manejar las cuentas contables de devolucion
            movFacturaCredito( insertedId, self.subtotalC * -1, self.ivaC * -1, self.totalCostC * -1 )







#            Crear la relacion con su padre
            query.prepare( """
            INSERT INTO docpadrehijos (idpadre, idhijo) VALUES (:idpadre, :idhijo)
            """ )
            query.bindValue( ":idpadre", self.invoiceId )
            query.bindValue( ":idhijo", insertedId )

            if not query.exec_():
                raise Exception( "No se crear la relacion de la devolución con la factura" )


            if not QSqlDatabase.database().commit():
                raise Exception( "No se pudo hacer commit" )


        except Exception as inst:
            print QSqlDatabase.database().lastError().text()
            print inst
            QSqlDatabase.database().rollback()

            return False

        return True
