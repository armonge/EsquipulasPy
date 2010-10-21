# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: Luis Carlos Mejia Garcia
'''
from PyQt4.QtSql import QSqlQuery
from decimal import Decimal
from utility.decorators import ifValid


class LineaFactura:
    def __init__( self, parent ):
        """
        @type parent: FacturaModel
        @param parent: El FacturaModel al que pertenece esta factura
        """

        self.__parent = parent
        """
        @ivar: El FacturaModel al que pertenece esta factura
        @type: FacturaModel
        """
        self.quantity = 0
        """
        @ivar: La cantidad de articulos en esta linea
        @type: int
        """
        self.itemDescription = ""
        """
        @ivar: La descripción del articulo
        @type: string
        """
        self.itemPrice = Decimal( 0 )
        """
        @ivar: El precio en el que se vende el articulo en esta transacción
        @type: Decimal
        """
        self.itemId = 0
        """
        @ivar: El id de este item en la base de datos
        @type: Decimal
        """


        self.costo = Decimal( 0 )
        """
        @ivar: El costo unitario en cordobas para cada linea de la factura
        @type: Decimal
        """

        self.sugerido = Decimal( 0 )
        """
        @ivar: El precio sugerido para este producto, se calcula multiplicando el costo del producto por su porcentaje de ganancia
        @type: Decimal
        """

        self.existencia = 0
        """
        @ivar: La existencia de este producto en la bodega
        @type: int
        """
        self.idbodega = 0
        """
        @ivar: El id de la bodega
        @type: int
        """





    @property
    @ifValid
    def total( self ):
        """
        el total de esta linea
        """
        return Decimal( self.quantity * self.itemPrice )

    @property
    @ifValid
    def costototal( self ):
        """
        el costo total de esta linea
        """
        return Decimal( self.quantity * self.costo )


    @property
    def valid( self ):
        """
        es esta linea valida
        """


        if  self.itemId != 0 \
            and  self.itemPrice > 0 \
            and  0 < self.quantity <= self.existencia \
            and self.idbodega == self.__parent.bodegaId \
            and self.idbodega > 0:
            return True
        return False

    def save( self, iddocumento, linea, tipoCambio ):
        """
        Este metodo guarda la linea en la base de datos
        @param iddocumento: el id del documento al que esta enlazada la linea
        """
        if not self.valid:
            raise Exception( "Se intento guardar una linea no valida" )

        query = QSqlQuery()
        if not query.prepare( 
        """
        INSERT INTO articulosxdocumento (iddocumento, idarticulo,unidades,costounit, precioventa,nlinea, tccosto ) 
        VALUES( :iddocumento, :idarticulo, :unidades,:costo, :precio,:linea ,:tc)
        """ ):
            raise Exception( "no esta preparada" )

        query.bindValue( ":iddocumento", iddocumento )
        query.bindValue( ":idarticulo", self.itemId )
        query.bindValue( ":unidades", self.quantity * -1 )
        query.bindValue( ":costo", str( self.costo ) )
        query.bindValue( ":precio", str( self.itemPrice ) )
        query.bindValue( ":linea", linea )
        query.bindValue( ":tc", tipoCambio )


        if not query.exec_():
            print( query.lastError().text() )
            raise Exception( "line %d" % self.itemId )



