# -*- coding: utf-8 -*-
'''
Created on 15/10/2010

@author: armonge
Pruebas para el modulo document.factura
'''
import sip
sip.setapi( 'QString', 2 )
from document.factura.facturamodel import FacturaModel
from caja.mainwindow import DatosSesion

from decimal import Decimal
from lineafactura import LineaFactura
import unittest
from PyQt4.QtCore import QCoreApplication

class TestLineaFactura( unittest.TestCase ):
    """
    Esta clase es un TesCase para LineaFactura reproduce un caso común y
    verifica los resultados del modelo con los esperados
    """
    def setUp( self ):
        _app = QCoreApplication( [] )

        self.line = LineaFactura( self )
        self.line.quantity = 1
        self.line.itemId = 1
        self.line.itemPrice = Decimal( '89' )
        self.line.costo = Decimal( '80' )

    def test_valid( self ):
        self.assertTrue( self.line.valid, "La linea deberia de ser valida" )

    def test_costototal( self ):
        self.assertEqual( self.line.costototal, Decimal( '80' ) )

    def test_total( self ):
        self.assertEqual( self.line.total, Decimal( '89' ) )

class TestLineaFacturaInvalida( unittest.TestCase ):
    def setUp( self ):
        _app = QCoreApplication( [] )

        self.line = LineaFactura( self )
        self.line.quantity = 1
        self.line.itemPrice = Decimal( '89' )
        self.line.costo = Decimal( '80' )

    def test_valid( self ):
        self.assertFalse( self.line.valid, "La linea deberia de ser invalida" )

    def test_costototal( self ):
        self.assertEqual( self.line.costototal, Decimal( '0' ) )

    def test_total( self ):
        self.assertEqual( self.line.total, Decimal( '0' ) )



class TestFacturaModel( unittest.TestCase ):
    def setUp( self ):
        _app = QCoreApplication( [] )
        datosSesion = DatosSesion()
        self.factura = FacturaModel( datosSesion )

    def test_valid( self ):
        self.assertFalse( self.factura.valid, "La factura deberia de ser invalida" )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
