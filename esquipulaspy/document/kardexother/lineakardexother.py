# -*- coding: utf-8 -*-
'''
Created on 13/08/2010

@author: Andrés Reyes Monge
'''
import logging
from decimal import Decimal

from PyQt4.QtSql import QSqlQuery

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
        self.itemCost = Decimal(0)
        """
        @ivar: El costo en dolares del articulo
        @type: Decimal
        """

    @property
    def valid(self):
        """
        Si una linea es valida o no
        @rtype: bool
        """
        return self.quantity != 0 and self.itemId != 0

    @property
    def totalCost(self):
        """
        El costo total de una linea
        @rtype: Decimal
        """
        return self.quantity * self.itemCost

    def save(self, docid, line):
        """
        Guardar la linea del documento
        """
        query = QSqlQuery()
        if not query.prepare( """
        INSERT INTO articulosxdocumento (iddocumento, idarticulo, unidades, costounit,nlinea)
        VALUES( :iddocumento,:idarticulo,  :unidades, :costounit,:linea)
        """ ):
            raise Exception( "No se pudo preparar la consulta para insertar una de las lineas del documento" )

        query.bindValue(":iddocumento", docid)
        query.bindValue(":idarticulo", self.itemId)
        query.bindValue(":unidades", self.quantity)
        query.bindValue(":costounit", self.itemCost.to_eng_string())
        query.bindValue(":linea", line)

        if not query.exec_():
            logging.error(query.lastError().text())
            raise Exception(u"No se pudo guardar el articulo %s" % self.itemId)
        