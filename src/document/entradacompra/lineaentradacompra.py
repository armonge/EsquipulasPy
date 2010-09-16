# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: Andrés Reyes Monge
'''
import unittest
if __name__ == "__main__":
    import sip
    sip.setapi( 'QString', 2 )

from decimal import Decimal

from PyQt4.QtCore import QCoreApplication
from PyQt4.QtSql import QSqlQuery

from utility.docbase import LineaBase, ifValid


class LineaEntradaCompra(LineaBase):
    def __init__( self, parent ):
        super(LineaEntradaCompra, self).__init__()
        self.quantity = 0
        self.itemDescription = ""
        self.__itemPriceD = Decimal( 0 )
        self.__itemPriceC = Decimal(0)
        self.itemId = 0
        self.parent = parent


    def getItemPriceC( self ):
        """
        El precio en cordobas de esta factura
        @rtype:  Decimal
        """
        return self.__itemPriceC
    def setItemPriceC( self, price ):
        try:
            self.__itemPriceD = price / self.parent.exchangeRate
            self.__itemPriceC = price
        except ZeroDivisionError:
            self.itemPriceD = Decimal( 0 )
    itemPriceC = property( getItemPriceC, setItemPriceC )

    def getItemPriceD(self):
        return self.__itemPriceD
    def setItemPriceD(self, price):
        self.__itemPriceC = price * self.parent.exchangeRate
        self.__itemPriceD = price
    itemPriceD = property(getItemPriceD, setItemPriceD)
    

    @property
    @ifValid
    def totalD( self ):
        """
        El total en dolares de esta linea
        @rtype: Decimal
        """
        return self.quantity * self.itemPriceD


    @property
    @ifValid
    def totalC( self ):
        """
        El total en cordobas de esta linea
        @rtype: Decimal
        """
        return self.quantity * self.itemPriceC

    @property
    def valid( self ):
        """
        Es esta linea valida
        @rtype: bool
        """
        if  int( self.itemId ) != 0   and Decimal( self.itemPriceC ) > 0 and int( self.quantity ) > 0  and self.parent.exchangeRateId != 0:
            return True
        return False

    def save( self, iddocumento, nlinea ):
        """
        Este metodo guarda la linea en la base de datos
        @param iddocumento: el id del documento al que esta enlazada la linea
        @rtype: bool
        @return: Si se pudo o no guardar el documento
        """
        if not self.valid:
            raise Exception( "Se intento guardar una linea no valida" )

        query = QSqlQuery()
        if not query.prepare( 
        """
        INSERT INTO articulosxdocumento (iddocumento, idarticulo, unidades, costounit, nlinea) 
        VALUES( :iddocumento, :idarticulo, :unidades, :costounit, :linea )
        """ ):
            raise Exception( "No se pudo preparar la consulta para insertar una de las lineas del documento" )
        query.bindValue( ":iddocumento ", iddocumento )
        query.bindValue( ":idarticulo", self.itemId )
        query.bindValue( ":unidades", self.quantity )
        query.bindValue( ":costounit", self.itemPriceD.to_eng_string() )
        query.bindValue( ":linea", nlinea )


        if not query.exec_():
            print query.lastError().text()
            raise Exception( "Hubo un error al guardar una linea" )

    


class TestLineaLineaEntradCompra(unittest.TestCase):
    """
    Esta clase es un TesCase para LineaEntradaCompra reproduce un caso común y
    verifica los resultados del modelo con los esperados
    """
    def setUp(self):
        app = QCoreApplication([])

        self.exchangeRate = Decimal('21.21')
        self.exchangeRateId = 1
        
        self.line = LineaEntradaCompra(self)
        self.line.quantity = 1
        self.line.itemId = 1
        self.line.itemPriceC = Decimal('1')

    def test_valid(self):
        self.assertTrue(self.line.valid, "La linea deberia de ser valida")

    def test_total(self):
        self.assertEqual(self.line.totalC, Decimal('1'), "El total en cordobas deberia de ser 1 y es %s"% self.line.totalC.to_eng_string())
        self.assertEqual(self.line.totalD, Decimal('0.04714757190004714757190004715'), "El total en dolares deberia de ser y es %s" %self.line.totalD.to_eng_string())


if __name__ == "__main__":
    unittest.main()