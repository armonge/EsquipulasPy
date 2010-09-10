# -*- coding: utf-8 -*-
'''
Created on 13/08/2010

@author: Andrés Reyes Monge
'''

class LineaKardexOther(object):
    def __init__(self):
        self.itemId = 0
        """
        @ivar: El id del articulo
        @type: int
        """
        self.description = ""
        """
        @ivar: El id del articulo
        @type: string
        """
        self.quantity = 0
        """
        @ivar: La cantidad de articulos en la linea
        @type: int
        """

    @property
    def valid(self):
        return self.quantity != 0 and self.itemId != 0