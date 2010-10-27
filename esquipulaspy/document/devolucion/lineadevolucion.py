#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ${file}
#       
#       Copyright 2010 Andrés Reyes Monge <armonge@armonge-laptop.site>
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
Created on 19/05/2010

@author: Andrés Reyes Monge
'''
from decimal import Decimal
from PyQt4.QtSql import QSqlQuery
from utility.docbase import LineaBase
from utility.decorators import ifValid

class LineaDevolucion( LineaBase ):
    """
    Este es un articulo de la DevolucionModel
    """
    def __init__( self, parent ):
        super( LineaDevolucion, self ).__init__()
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
        @ivar:El precio de venta por unidad en esta linea, en dolares
        @type:Decimal
        """
        self.itemCost = Decimal( 0 )
        """
        @ivar: El costo unitario de este articulo en dolares
        @type: Decimal
        """
        self.parent = parent
        """
        @ivar: El documento devolución al que esta linea pertenece
        @type: DevolucionModel
        """

    @property
    @ifValid
    def totalD( self ):
        """
        Esto es en base al precio de venta, en dolares
        @rtype: Decimal
        """
        return self.quantity * self.itemPrice

    @property
    def totalC( self ):
        """
        El total en cordobas
        @rtype: Decimal
        """
        return self.totalD * self.parent.exchangeRate

    @property
    @ifValid
    def costoD( self ):
        """
        Esto es en base al costo unitario, en dolares
        @rtype: Decimal
        """
        return self.quantity * self.itemCost

    @property
    def costoC( self ):
        """
        El costo en cordobas
        @rtype: Decimal
        """
        return self.costoD * self.parent.exchangeRate

    @property
    def valid( self ):
        """
        Si una linea es valido o no
        @rtype: bool
        """
        if 0 < self.quantity <= self.maxquantity \
        and self.itemId != 0 :
            return True
        return False

    def save( self, iddocumento, nlinea ):
        if not self.valid:
            raise Exception( "Se intento guardar una linea no valida" )

        query = QSqlQuery()
        if not query.prepare( 
        """
        INSERT INTO articulosxdocumento (iddocumento, idarticulo,
         unidades, costounit, precioventa, nlinea ) 
        VALUES( :iddocumento, :idarticulo, 
        :unidades, :costounit, :preciounit, :nlinea )
        """ ):
            raise Exception( u"No se pudo preparar la consulta para añadir"\
                             + " una linea" )
        query.bindValue( ":iddocumento", iddocumento )
        query.bindValue( ":idarticulo", self.itemId )
        query.bindValue( ":unidades", self.quantity )
        query.bindValue( ":costounit", str( self.itemCost ) )
        query.bindValue( ":preciounit", str( self.itemPrice ) )
        query.bindValue( ":nlinea", nlinea )

        if not query.exec_():
            raise Exception( "No se pudo guardar la linea con el articulo %d" %
                              self.itemId )
