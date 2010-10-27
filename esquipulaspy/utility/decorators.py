#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
Created on 12/10/2010

@author: armonge

Este modulo implementa los decoradores que puedan ser genericos a todo el sistema
'''
import functools
from decimal import Decimal

def ifValid( func ):
    u"""
    Decorador que retorna Decimal(0) si la linea no es valida, esto es más facil
     que usar "if valid else Decimal(0)" en todos lados
    """
    @functools.wraps( func )
    def wrapper( self ):
        return func( self ) if self.valid else Decimal( 0 )
    return wrapper

def return_decimal( func ):
    u"""
    Decorador que retorna Decimal siempre
    """
    @functools.wraps( func )
    def wrapper( self ):
        value = func( self )
        return   value if type( value ) == Decimal else Decimal( value )
    return wrapper

def if_edit_model( func ):
    u""""
    Este decorador ejecuta la función si editmodel is not None
    de otro modo pass
    """
    @functools.wraps( func )
    def wrapper( self, *args ):
        if self.editmodel is not None:
            return func( self, *args )

    return wrapper


