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
Created on 07/06/2010

@author: Andrés Reyes Monge
'''
import logging
from decimal import Decimal

from PyQt4.QtSql import QSqlQuery


class LineaArqueo( object ):
    def __init__( self , parent ):
        self.quantity = 0
        """
        @ivar: La cantidad de unidades de esta denominación en el arqueo
        @type: int
        """
        self.parent = parent
        """
        @ivar: El objeto arqueo al que pertenece esta linea
        @type: ArqueoModel
        """
        self.value = Decimal( 0 )
        """
        @ivar: El valor de esta denominación
        @type: Decimal
        """
        self.denominationId = 0
        """
        @ivar: El id de la denominación
        @type: int
        """
        self.denomination = ""
        """
        @ivar: La descripción de la denominación
        @type:string
        """
        self.currencyId = 0
        """
        @ivar: El id de la moneda
        @type: int
        """
        self.symbol = ""
        """
        @ivar: El simbolo de la moneda
        @type: string
        """


    @property
    def total( self ):
        return self.value * self.quantity

    @property
    def valid( self ):
        return self.total > 0 and self.currencyId != 0

    def save( self, iddocumento ):
        if not self.valid:
            raise Exception( "Se intento guardar una linea no valida" )

        query = QSqlQuery()
        if not query.prepare( """
        INSERT INTO lineasarqueo (cantidad, iddocumento, iddenominacion)
        VALUES (:cantidad,  :iddocumento, :denominacion)
        """ ):
            raise  Exception( "No se pudo preparar la consulta para insertar una linea" )
        query.bindValue( ":cantidad", self.quantity )
        query.bindValue( ":iddocumento", iddocumento )
        query.bindValue( ":denominacion", self.denominationId )

        if not query.exec_():
            logging.critical( query.lastError().text() )
            raise Exception( "No se pudo insertar una linea" )
