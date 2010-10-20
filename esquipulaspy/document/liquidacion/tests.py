# -*- coding: utf-8 -*-
'''
Created on 12/10/2010

@author: armonge
'''
import sip
import unittest
sip.setapi( 'QString', 2 )

from PyQt4.QtCore import QCoreApplication, QVariant
from decimal import Decimal
from linealiquidacion import LineaLiquidacion
from liquidacionmodel import LiquidacionModel, CANTIDAD, COSTOUNIT, ARTICULO



class TestLiquidacionSimple( unittest.TestCase ):
    """
    Esta clase es un TesCase para LiquidacionModel reproduce un caso común y
    verifica los resultados del modelo con los esperados
    """
    def setUp( self ):
        _app = QCoreApplication( [] )

        self.liquidacion = LiquidacionModel( 1 )

        self.liquidacion.exchangeRate = Decimal( '21.5689' )
        self.liquidacion.exchangeRateId = 1
        self.liquidacion.speTotal = 5
        self.liquidacion.isoRate = Decimal( '35' )
        self.liquidacion.ivaRate = Decimal( '15' )
        self.liquidacion.tsimRate = Decimal( '0.5' )
        self.liquidacion.weightFactor = 1000
        self.liquidacion.warehouseId = 1

        self.liquidacion.insertRow( 0 )

        self.liquidacion.setData( self.liquidacion.index( 0, COSTOUNIT ), QVariant( "1" ) )
        self.liquidacion.setData( self.liquidacion.index( 0, ARTICULO ), [
            1,
            "FRICCIONES* BATERIA  N-150 DURUN",
            Decimal( '5' ),
            Decimal( '76' ),
            0
            ] )
        self.liquidacion.setData( self.liquidacion.index( 0, CANTIDAD ), QVariant( "1" ) )

    def test_valid( self ):
        self.assertFalse( self.liquidacion.valid )

    def test_dai( self ):
        self.assertEqual( self.liquidacion.daiTotal, Decimal( '0.05' ) )

    def test_isc( self ):
        self.assertEqual( self.liquidacion.iscTotal, Decimal( '0.7980' ) )

    def test_cif( self ):
        self.assertEqual( self.liquidacion.cifTotal, Decimal( '1' ) )

    def test_iva( self ):
        self.assertEqual( self.liquidacion.ivaTotal, Decimal( '0.2772' ) )
        self.liquidacion.warehouseId = 2
        self.assertEqual( self.liquidacion.ivaTotal, Decimal( 0 ) )

    def test_taxes( self ):
        self.assertEqual( self.liquidacion.taxesTotal, Decimal( '6.4752' ) )
        self.liquidacion.warehouseId = 2
        self.assertEqual( self.liquidacion.taxesTotal, Decimal( ' 6.1980' ) )

    def test_speTotal( self ):
        self.assertEqual( self.liquidacion.speTotal, Decimal( '5' ) )

    def test_total( self ):
        self.assertEqual( self.liquidacion.totalC, Decimal( '161.23184128' ) )
        self.assertEqual( self.liquidacion.totalD, Decimal( '7.4752' ) )

    def test_fob( self ):
        self.assertEqual( self.liquidacion.fobTotal, 1 )
        self.assertEqual( self.liquidacion.fobTotalC, Decimal( '21.5689' ) )

    def test_numrows( self ):
        self.assertEqual( self.liquidacion.rowCount(), 2 )

    def test_iso( self ):
        self.assertEqual( self.liquidacion.isoTotal, Decimal( '0.35' ) )

class TestLineaLiquidacion( unittest.TestCase ):
    """
    Esta clase es un TesCase para LineaLiquidacion reproduce un caso común y
    verifica los resultados del modelo con los esperados
    """
    def setUp( self ):
        _app = QCoreApplication( [] )

        self.line = LineaLiquidacion( self )
        self.line.quantity = 1
        self.line.itemCost = Decimal( '1' )
        self.line.rateDAI = Decimal( '5' )
        self.line.rateISC = Decimal( '76' )
        self.line.comisionValue = Decimal( '0' )
        self.line.itemId = 1

        self.cifTotal = Decimal( '1' )
        self.fobTotal = Decimal( '1' )
        self.agencyTotal = Decimal( '0' )
        self.storeTotal = Decimal( '0' )
        self.paperworkRate = Decimal( '0' )
        self.transportRate = Decimal( '0' )
        self.applyTaxes = True
        self.tsimTotal = Decimal( '0' )
        self.ivaRate = Decimal( '15' )
        self.speTotal = Decimal( '5' )
        self.isoRate = Decimal( '35' )
        self.exchangeRate = Decimal( '21.5718' )
        self.exchangeRateId = 1

    def test_valid( self ):
        self.assertTrue( self.line.valid )
        self.line.quantity = 0
        self.assertFalse( self.line.valid )

    def test_comision( self ):
        self.assertEqual( self.line.comisionParcial, Decimal( '0' ) )

        self.line.comisionValue = 10
        self.assertEqual( self.line.comisionParcial, 10 )

    def test_isc( self ):
        self.assertEqual( self.line.iscParcial, Decimal( '0.7980' ) )
        self.applyTaxes = False

        self.assertEqual( self.line.iscParcial, 0 )

    def test_dai( self ):
        self.assertEqual( self.line.daiParcial, Decimal( '0.05' ) )
        self.applyTaxes = False
        self.assertEqual( self.line.daiParcial, 0 )

    def test_costo( self ):
        self.assertEqual( self.line.costoDolarT, Decimal( '7.4752' ) )
        self.assertEqual( self.line.costoCordobaT, Decimal( '161.25351936' ) )

    def test_iva( self ):
        self.assertEqual( self.line.ivaParcial, Decimal( '0.2772' ) )

        self.applyTaxes = False
        self.assertEqual( self.line.ivaParcial, Decimal( '0.15' ) )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
