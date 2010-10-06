# -*- coding: utf-8 -*-
#TODO: unittest
'''
Created on 19/05/2010

@author: Andrés Reyes Monge
'''
from decimal import Decimal
from PyQt4.QtSql import QSqlQuery

class LineaDevolucion:
    def __init__( self, parent ):
        self.quantity = 0
        """
        @ivar: La cantidad de articulos en esta linea
        @type: int
        """
        self.maxquantity = 0
        """
        @ivar:La cantidad maxima de articulos que esta linea deberia de tener
        @type:int
        """
        self.itemId = 0
        """
        @ivar:El id del articulo en esta linea
        @type: int
        """
        self.itemDescription = ""
        """
        @ivar:La descripción del articulo en esta linea
        @type:string
        """
        self.itemPrice = Decimal( 0 )
        """
        @ivar:El precio de venta por unidad en esta linea
        @type:Decimal
        """
        self.itemCost = Decimal( 0 )
        """
        @ivar: El costo unitario de este articulo
        @type: Decimal
        """
        self.parent = parent
        """
        @ivar: El documento devolución al que esta linea pertenece
        @type: DevolucionModel
        """

    @property
    def totalD( self ):
        """
        Esto es en base al precio de venta, en dolares
        @rtype: Decimal
        """
        return self.quantity * self.itemPrice  if self.valid else Decimal( 0 )

    @property
    def totalC( self ):
        """
        El total en cordobas
        @rtype: Decimal
        """
        return self.totalD * self.parent.exchangeRate

    @property
    def costoD( self ):
        """
        Esto es en base al costo unitario, en dolares
        @rtype: Decimal
        """
        return self.quantity * self.itemCost if self.valid else Decimal( 0 )

    @property
    def costoC( self ):
        """
        El costo en cordobas
        @rtype: Decimal
        """
        return self.costoC * self.parent.exchangeRate

    @property
    def valid( self ):
        """
        Si una linea es valido o no
        @rtype: bool
        """
        if 0 < self.quantity <= self.maxquantity and self.itemId != 0 :
            return True
        return False

    def save( self, iddocumento ):
        if not self.valid:
            raise Exception( "Se intento guardar una linea no valida" )

        query = QSqlQuery()
        if not query.prepare( 
        """
        INSERT INTO articulosxdocumento (iddocumento, idarticulo, unidades, costounit, precioventa ) 
        VALUES( :iddocumento, :idarticulo, :unidades, :costounit, :preciounit )
        """ ):
            raise Exception( u"No se pudo preparar la consulta para añadir una linea" )
        query.bindValue( ":iddocumento", iddocumento )
        query.bindValue( ":idarticulo", self.itemId )
        query.bindValue( ":unidades", self.quantity )
        query.bindValue( ":costounit", self.itemCost.to_eng_string() )
        query.bindValue( ":preciounit", self.itemPrice.to_eng_string() )

        if not query.exec_():
            raise Exception( "No se pudo guardar la linea con el articulo " + str( self.itemId ) )
