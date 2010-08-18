# -*- coding: utf-8 -*-
'''
Created on 07/06/2010

@author: Andrés Reyes Monge
'''
from PyQt4.QtSql import QSqlQuery
from decimal import Decimal, DivisionByZero, InvalidOperation

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
            print query.lastError().text()
            raise Exception( "No se pudo insertar una linea" )
