# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: Luis Carlos Mejia Garcia
'''
from PyQt4.QtSql import QSqlQuery
from decimal import Decimal



#FIXME: Para que se usa el parametro parent???
class LineaFactura:
    def __init__( self ):
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
    def total( self ):
        """
        el total de esta linea
        """
        return Decimal( self.quantity * self.itemPrice ) if self.valid else Decimal( 0 )

    @property
    def costototal( self ):
        """
        el costo total de esta linea
        """
        return Decimal( self.quantity * self.costo ) if self.valid else Decimal( 0 )


    @property
    def valid( self ):
        """
        es esta linea valida
        """
        if  int( self.itemId ) != 0   and Decimal( self.itemPrice ) > 0 and int( self.quantity ) > 0 :
            return True
        return False

    def save( self, iddocumento, linea ):
        """
        Este metodo guarda la linea en la base de datos
        @param iddocumento: el id del documento al que esta enlazada la linea
        """
        if not self.valid:
            raise Exception( "Se intento guardar una linea no valida" )

        query = QSqlQuery()
        if not query.prepare( 
        """
        INSERT INTO articulosxdocumento (iddocumento, idarticulo, 
        unidades,costounit, precioventa,nlinea ) 
        VALUES( :iddocumento, :idarticulo, :unidades,:costo, :precio,:linea )
        """ ):
            raise Exception( "no esta preparada" )

        query.bindValue( ":iddocumento", iddocumento )
        query.bindValue( ":idarticulo", self.itemId )
        query.bindValue( ":unidades", self.quantity * -1 )
        query.bindValue( ":costo", self.costo.to_eng_string() )
        query.bindValue( ":precio", self.itemPrice.to_eng_string() )
        query.bindValue( ":linea", linea )


        if not query.exec_():
            print( query.lastError().text() )
            raise Exception( "line %s" % self.itemId )



