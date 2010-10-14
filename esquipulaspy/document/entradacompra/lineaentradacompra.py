# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: Andrés Reyes Monge
'''
from decimal import Decimal

from PyQt4.QtCore import QCoreApplication
from PyQt4.QtSql import QSqlQuery

from utility.docbase import LineaBase
from utility.decorators import  ifValid


class LineaEntradaCompra( LineaBase ):
    def __init__( self, parent ):
        super( LineaEntradaCompra, self ).__init__()
        self.quantity = 0
        self.itemDescription = ""
        self.__itemPriceD = Decimal( 0 )
        self.__itemPriceC = Decimal( 0 )
        self.itemId = 0
        self.parent = parent


    def getItemPriceC( self ):
        """
        El precio en cordobas de esta factura
        @rtype:  Decimal
        """
        return self.__itemPriceC
    def setItemPriceC( self, price ):
        try:
            self.__itemPriceD = price / self.parent.exchangeRate
            self.__itemPriceC = price
        except ZeroDivisionError:
            self.itemPriceD = Decimal( 0 )
    itemPriceC = property( getItemPriceC, setItemPriceC )

    def getItemPriceD( self ):
        return self.__itemPriceD
    def setItemPriceD( self, price ):
        self.__itemPriceC = price * self.parent.exchangeRate
        self.__itemPriceD = price
    itemPriceD = property( getItemPriceD, setItemPriceD )


    @property
    @ifValid
    def totalD( self ):
        """
        El total en dolares de esta linea
        @rtype: Decimal
        """
        return self.quantity * self.itemPriceD


    @property
    @ifValid
    def totalC( self ):
        """
        El total en cordobas de esta linea
        @rtype: Decimal
        """
        return self.quantity * self.itemPriceC

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




