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
#TODO: Unittest
'''
Created on 16/07/2010

@author: Andrés Reyes Monge
'''
import logging
from decimal import Decimal
from PyQt4.QtSql import QSqlQuery
class LineaKardex( object ):
    def __init__( self ):

        self.itemId = 0
        """
        @ivar: El ide del item en esta linea
        @type: int
        """
        self.itemDescription = ""
        """
        @ivar: La descripción de esta linea
        @type: string
        """
        self.numdoc = 0
        """
        @ivar: El numero de articulos en esta linea de kardex
        @type: int
        """
        self.numajuste = 0
        """
        @ivar: El numero de ajuste si es que hay en esta linea de kardex
        @type: int
        """
        self.itemCost = Decimal( 0 )
        """
        @ivar: El costo de este articulo
        @type: Decimal
        """

        self.cost = Decimal( 0 )

    @property
    def dirty( self ):
        """
        Si la linea se ha modificado o no
        @rtype: bool
        """
        return self.numajuste != 0

    @property
    def numfinal( self ):
        """
        El total de articulos despues del ajuste
        @rtype: int
        """
        return self.numdoc + self.numajuste

    @property
    def ajusteMonetario( self ):
        """
        El valor del ajuste monetario
        @rtype: Decimal
        """
        return self.itemCost * self.numajuste

    @property
    def diry( self ):
        """
        Si la linea contiene algún cambio o no
        @rtype: bool
        """
        return self.numajuste != 0

    def save( self, iddocumento ):
        if not self.diry:
            raise Exception( "Se intento guardar una linea del kardex "\
                             + "sin ninguna información" )

        query = QSqlQuery()
        if not query.prepare( """
        INSERT INTO articulosxdocumento (iddocumento, idarticulo, unidades) 
        VALUES (:iddocumento, :idarticulo, :unidades)
        """ ):
            raise Exception( "No se pudo preparar la consulta para "\
                             + "añadir una de las lineas" )
        query.bindValue( ":iddocumento", iddocumento )
        query.bindValue( ":idarticulo", self.itemId )
        query.bindValue( ":unidades", self.numajuste )

        if not query.exec_():
            logging.error( query.lastError().text() )
            raise Exception( "No se pudo insertar una linea" )
