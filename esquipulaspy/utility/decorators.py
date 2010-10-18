# -*- coding: utf-8 -*-
'''
Created on 12/10/2010

@author: armonge

Este modulo implementa los decoradores que puedan ser genericos a todo el sistema
'''
import functools
from decimal import Decimal

def ifValid( fn ):
    u"""
    Decorador que retorna Decimal(0) si la linea no es valida, esto es más facil
     que usar "if valid else Decimal(0)" en todos lados
    """
    @functools.wraps( fn )
    def wrapper( self = None ):
        return fn( self ) if self.valid else Decimal( 0 )
    return wrapper

def return_decimal( fn ):
    u"""
    Decorador que retorna Decimal(0) en el caso de que la función este retornando
    int(0)
    """
    @functools.wraps( fn )
    def wrapper( self = None ):
        value = fn( self )
        return   value if type( value ) == Decimal else Decimal( value )
    return wrapper

