# -*- coding: utf-8 -*-
'''
Created on 15/10/2010

@author: armonge
Pruebas para el modulo document.factura
'''
from pyqtconfig import Qt

from facturamodel import FacturaModel, DESCRIPCION, CANTIDAD
from caja.mainwindow import DatosSesion

from decimal import Decimal
from lineafactura import LineaFactura
import unittest
from PyQt4.QtCore import QCoreApplication, QVariant, QDate

class TestLineaFactura( unittest.TestCase ):
    """
    Esta clase es un TesCase para LineaFactura reproduce un caso común y
    verifica los resultados del modelo con los esperados
    """
    def setUp( self ):
        _app = QCoreApplication( [] )

        self.line = LineaFactura( self )
        self.line.quantity = 2
        self.line.itemId = 1
        self.line.itemPrice = Decimal( '89' )
        self.line.costo = Decimal( '80' )
        self.line.existencia = 10
        self.line.idbodega = 1

        self.bodegaId = 1

    def test_valid( self ):
        self.assertTrue( self.line.valid, "La linea deberia de ser valida" )

    def test_costototal( self ):
        self.assertEqual( self.line.costototal, Decimal( '160' ) )

    def test_total( self ):
        self.assertEqual( self.line.total, Decimal( '178' ) )

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



class TestFacturaModelValido( unittest.TestCase ):
    def setUp( self ):
        _app = QCoreApplication( [] )

        datosSesion = DatosSesion()
        datosSesion.usuarioId = 1
        datosSesion.sesionId = 1
        datosSesion.tipoCambioId = 1
        datosSesion.tipoCambioOficial = Decimal( 21 )
        datosSesion.tipoCambioBanco = Decimal( 20 )
        datosSesion.fecha = QDate.currentDate()
        datosSesion.cajaId = 1

        self.factura = FacturaModel( datosSesion )
        self.factura.ivaTasa = Decimal( '15' )
        self.factura.bodegaId = 1
        self.factura.insertRow( 0 )
        self.factura.ivaId = 1

        self.factura.setData( 
                             self.factura.index( 0, DESCRIPCION ),
                              [
                                 1,
                                 "Baterias DURUN",
                                 "100",
                                 "80",
                                 "10",
                                 "1"
                               ] )

        self.factura.setData( self.factura.index( 0, CANTIDAD ),
                              QVariant( "1" ) )



    def test_valid_lines( self ):
        self.assertEqual( self.factura.validLines, 1 )

    def test_row_count( self ):
        self.assertEqual( self.factura.rowCount(), 2 )
        self.assertEqual( self.factura.validLines, 1 )

    def test_valid( self ):
        self.assertTrue( self.factura.valid,
                         "La factura deberia de ser valida" )

    def test_iva_total( self ):
        self.assertEqual( self.factura.IVA, Decimal( 15 ) )

    def test_costo_total( self ):
        self.assertEqual( self.factura.costototal, Decimal( 80 ) )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
