# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: Andrés Reyes Monge
'''
from decimal import Decimal
from PyQt4.QtSql import QSqlQuery
class LineaEntradaCompra( object ):
    def __init__( self, parent ):
        self.quantity = 0
        self.itemDescription = ""
        self.itemPriceD = Decimal( 0 )
        self.itemId = 0
        self.parent = parent

    def getItemPriceC( self ):
        """
        El precio en cordobas de esta factura
        @rtype:  Decimal
        """
        return self.itemPriceD * self.parent.exchangeRate if self.parent.exchangeRate != 0 else Decimal( 0 )
    def setItemPriceC( self, price ):
        try:
            self.itemPriceD = price / self.parent.exchangeRate
        except ZeroDivisionError:
            self.itemPriceD = Decimal( 0 )
    itemPriceC = property( getItemPriceC, setItemPriceC )

    @property
    def totalD( self ):
        """
        El total en dolares de esta linea
        @rtype: Decimal
        """
        return self.quantity * self.itemPriceD if self.valid else Decimal( 0 )


    @property
    def totalC( self ):
        """
        El total en cordobas de esta linea
        @rtype: Decimal
        """
        return self.quantity * self.itemPriceC  if self.valid else Decimal( 0 )

    @property
    def valid( self ):
        """
        Es esta linea valida
        @rtype: bool
        """
        if  int( self.itemId ) != 0   and Decimal( self.itemPriceC ) > 0 and int( self.quantity ) > 0  and self.parent.exchangeRateId != 0:
            return True
        return False

    def save( self, iddocumento, nlinea ):
        """
        Este metodo guarda la linea en la base de datos
        @param iddocumento: el id del documento al que esta enlazada la linea
        @rtype: bool
        @return: Si se pudo o no guardar el documento
        """
        if not self.valid:
            raise Exception( "Se intento guardar una linea no valida" )

        query = QSqlQuery()
        if not query.prepare( 
        """
        INSERT INTO articulosxdocumento (iddocumento, idarticulo, unidades, costounit, nlinea) 
        VALUES( :iddocumento, :idarticulo, :unidades, :costounit, :linea )
        """ ):
            raise Exception( "No se pudo preparar la consulta para insertar una de las lineas del documento" )
        query.bindValue( ":iddocumento ", iddocumento )
        query.bindValue( ":idarticulo", self.itemId )
        query.bindValue( ":unidades", self.quantity )
        query.bindValue( ":costounit", self.itemPriceD.to_eng_string() )
        query.bindValue( ":linea", nlinea )


        if not query.exec_():
            print query.lastError().text()
            raise Exception( "Hubo un error al guardar una linea" )



