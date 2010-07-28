# -*- coding: utf-8 -*-
'''
Created on 07/06/2010

@author: armonge
'''
from PyQt4.QtSql import QSqlQuery
from decimal import Decimal, DivisionByZero, InvalidOperation

class LineaArqueo( object ):
    def __init__( self , parent ):
        self.quantity = 0
        self.parent = parent
        self.value = Decimal( 0 )
        self.denominationId = 0
        self.denomination = ""
        self.currencyId = 0


    @property
    def total( self ):
        try:
            return self.value * self.quantity / self.parent.exchangeRate if self.currencyId == 1 else self.value * self.quantity
        except DivisionByZero:
            return Decimal(0)
        except InvalidOperation:
            return Decimal(0)

    @property
    def valid( self ):
        return self.value > 0 and self.quantity > 0

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
            print query.lastError().text()
            raise Exception( "No se pudo insertar una linea" )
