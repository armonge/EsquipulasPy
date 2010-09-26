# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: Luis Carlos Mejia Garcia
'''
import unittest
if __name__ == "__main__":
    import sip
    sip.setapi( 'QString', 2 )

from decimal import Decimal

from PyQt4.QtCore import QCoreApplication
from PyQt4.QtSql import QSqlQuery

#FIXME: Para que se usa el parametro parent???
class LineaFactura:
    def __init__( self, parent ):
        self.quantity = 0
        """
        @ivar: La cantidad de articulos en esta linea
        @type: int
        """
        self.itemDescription = ""
        """
        @ivar: La descripción del articulo
        @type: string
        """
        #FIXME: por que hay un setter y un getter aca? la propiedad no es ni siquiera privada.... si es por lo de decimal entonces
        #de principio se deberia de pasar como Decimal y no como string, eso es algo que el modelo le deberia de dar
        self.price = Decimal( 0 )
        """
        @ivar: El precio en el que se vende el articulo en esta transacción
        @type: Decimal
        """

#FIXME: Donde se ocupa esta propiedad???
        self.costodolar =  Decimal( 0 )
        """
        @ivar: El costo en dolares de este articulo
        @type: Decimal
        """

        self.itemId = 0
        """
        @ivar: El id de este item en la base de datos
        @type: Decimal
        """
        
        self.parent = parent
        """
        @ivar: FIXME: que es este parent???
        @type: ???
        """
        
        self.costo = 0
        """
        @ivar: El costo unitario en cordobas para cada linea de la factura
        @type: int
        """
        
        self.sugerido = Decimal( 0 )
        """
        @ivar: El precio sugerido para este producto, se calcula multiplicando el costo del producto por su porcentaje de ganancia
        @type: Decimal
        """
        
        self.existencia = 0
        """
        @ivar: La existencia de este producto en la bodega
        @type: int
        """
        self.idbodega = 0
        """
        @ivar: El id de la bodega
        @type: int
        """
        



    def getPrice( self ):
        """
        el precio unitario del producto en esta linea
        """
        return self.price
    def setPrice( self, price ):
        self.price = Decimal( price )

    itemPrice = property( getPrice, setPrice )

    @property
    def total( self ):
        """
        el total de esta linea
        """
        return Decimal( self.quantity * self.itemPrice ) if self.valid else Decimal( 0 )

    @property
    def costototal( self ):
        """
        el costo total de esta linea
        """
        return Decimal( self.quantity * self.costo ) if self.valid else Decimal( 0 )


    @property
    def valid( self ):
        """
        es esta linea valida
        """
        if  int( self.itemId ) != 0   and Decimal( self.itemPrice ) > 0 and int( self.quantity ) > 0 :
            return True
        return False

    def save( self, iddocumento, linea ):
        """
        Este metodo guarda la linea en la base de datos
        @param iddocumento: el id del documento al que esta enlazada la linea
        """
        if not self.valid:
            raise Exception( "Se intento guardar una linea no valida" )

        query = QSqlQuery()
        if not query.prepare( 
        """
        INSERT INTO articulosxdocumento (iddocumento, idarticulo, unidades,costounit, precioventa,nlinea ) 
        VALUES( :iddocumento, :idarticulo, :unidades,:costo, :precio,:linea )
        """ ):
            raise Exception( "no esta preparada" )

        query.bindValue( ":iddocumento", iddocumento )
        query.bindValue( ":idarticulo", self.itemId )
        query.bindValue( ":unidades", self.quantity * -1 )
        query.bindValue( ":costo", self.costo.to_eng_string() )
        query.bindValue( ":precio", self.itemPrice.to_eng_string() )
        query.bindValue( ":linea", linea )


        if not query.exec_():
            print( query.lastError().text() )
            raise Exception( "line" + str( self.itemId ) )



class TestLineaFactura(unittest.TestCase):
    """
    Esta clase es un TesCase para LineaLiquidacion reproduce un caso común y
    verifica los resultados del modelo con los esperados
    """
    def setUp(self):
        app = QCoreApplication([])

        self.line = LineaFactura(self)
        self.line.quantity = 1
        self.line.itemId = 1
        self.line.itemPrice = Decimal( '89')
        self.line.costo = Decimal('80')

    def test_valid(self):
        self.assertTrue(self.line.valid, "La linea deberia de ser valida")

    def test_costototal(self):
        self.assertEqual(self.line.costototal, Decimal('80'))

    def test_total(self):
        self.assertEqual(self.line.total, Decimal('89'))

class TestLineaFacturaInvalida(unittest.TestCase):
    def setUp(self):
        app = QCoreApplication([])

        self.line = LineaFactura(self)
        self.line.quantity = 1
        self.line.itemPrice = Decimal( '89')
        self.line.costo = Decimal('80')

    def test_valid(self):
        self.assertFalse(self.line.valid, "La linea deberia de ser invalida")

    def test_costototal(self):
        self.assertEqual(self.line.costototal, Decimal('0'))

    def test_total(self):
        self.assertEqual(self.line.total, Decimal('0'))

if __name__ == "__main__":
    unittest.main()