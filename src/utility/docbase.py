# -*- coding: utf-8 -*-
'''
Created on 16/08/2010

@author: Andrés Reyes Monge
'''
import functools
from decimal import Decimal

def ifValid(fn):
    """
    Decorador que retorna 0 si la linea no es valida, esto es más facil que usar "if valid else Decimal(0)" en todos lados
    """
    @functools.wraps(fn)
    def wrapper(self=None):
        return fn(self) if self.valid else Decimal(0)
    return wrapper
class DocumentBase(object):
    __documentType = NotImplementedError()
    """
    Esta se convertira en un futuro en la clase base para los nuevos documentos
    idealmente aca irian todas las propiedades que de todos modos todos los
    documentos tienen Eg: exchangeRate, exchangeRateId, observaciones

    ademas de algunos metodos como validLines
    """


    @property
    def validLines( self ):
        """
        El total de lineas con la propiedad valid = True
        @rtype: int
        """
        return len( [line for line in self.lines if line.valid] )

    @property
    def valid(self):
        raise NotImplementedError("El metodo valid deberia de ser implementado en todos los documentos")

    def save(self):
        raise NotImplementedError()
class LineaBase(object):
    """
    Esta se convertira en un futuro en la clase base para las nuevas lineas,
    con suerte se podran pasar aca muchos metodos genericos
    """
    @property
    def valid( self ):
        """
        Es esta linea valida
        @rtype: bool
        """
        raise NotImplementedError("No se ha implementado la propiedad Valid")

    def save( self, iddocumento, nlinea ):
        """
        Este metodo guarda la linea en la base de datos
        @param iddocumento: el id del documento al que esta enlazada la linea
        @rtype: bool
        @return: Si se pudo o no guardar el documento
        """
        raise NotImplementedError("No se ha implementado el metodo save")