#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       
#       Copyright 2010 Andrés Reyes Monge <armonge@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
'''
Created on 18/05/2010

@author: Andrés Reyes Monge
'''
from decimal import Decimal

from PyQt4.QtSql import QSqlQuery

from utility.docbase import LineaBase
from utility.decorators import  ifValid


class LineaEntradaCompra( LineaBase ):
    def __init__( self, parent ):
        super( LineaEntradaCompra, self ).__init__()
        self.quantity = 0
        self.itemDescription = ""
        self.__item_price_d = Decimal( 0 )
        self.__item_price_c = Decimal( 0 )
        self.itemId = 0
        self.parent = parent


    def _get_item_price_c( self ):
        """
        El precio en cordobas de esta factura
        @rtype:  Decimal
        """
        return self.__item_price_c
    def _set_item_price_c( self, price ):
        try:
            self.__item_price_d = price / self.parent.exchangeRate
            self.__item_price_c = price
        except ZeroDivisionError:
            self.itemPriceD = Decimal( 0 )
    itemPriceC = property( _get_item_price_c, _set_item_price_c )

    def _get_item_price_d( self ):
        return self.__item_price_d
    def _set_item_price_d( self, price ):
        self.__item_price_c = price * self.parent.exchangeRate
        self.__item_price_d = price
    itemPriceD = property( _get_item_price_d, _set_item_price_d )


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
        if  int( self.itemId ) != 0  \
        and Decimal( self.itemPriceC ) > 0 \
        and int( self.quantity ) > 0  \
        and self.parent.exchangeRateId != 0:
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
            raise Exception( "Hubo un error al guardar una linea" )




