#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ${file}
#       
#       Copyright 2010 Andrés Reyes Monge <armonge@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
'''
Created on 18/10/2010

@author: armonge
'''
import sip
sip.setapi( "QString", 2 )
from PyQt4.QtCore import QCoreApplication
from decimal import Decimal
from devolucionmodel import DevolucionModel
from lineadevolucion import LineaDevolucion

import unittest



class TestLineaDevolucion( unittest.TestCase ):


    def setUp( self ):
        _app = QCoreApplication( [] )
        self.linea = LineaDevolucion( self )

        self.linea.quantity = 10
        self.linea.maxquantity = 10
        self.linea.itemId = 1
        self.linea.itemPrice = Decimal( 50 )
        self.linea.itemCost = Decimal( 30 )

        self.exchangeRate = Decimal( '21' )


    def test_valid( self ):
        self.assertTrue( self.linea.valid )

        self.linea.itemId = 0
        self.assertFalse( self.linea.valid )

    def test_total( self ):
        self.assertEqual( self.linea.totalD, Decimal( 500 ) )
        self.assertEqual( self.linea.totalC, Decimal( 10500 ) )

    def test_costo( self ):
        self.assertEqual( self.linea.costoD, Decimal( 300 ) )
        self.assertEqual( self.linea.costoC, Decimal( 6300 ) )

class TestDevolucionModel( unittest.TestCase ):
    #TODO: Este test deberia de ser MAS EXTENSIVO
    def setUp( self ):
        _app = QCoreApplication( [] )

        self.devolucion = DevolucionModel()
        self.devolucion.insertRow( 0 )

    def test_total( self ):
        self.assertEqual( self.devolucion.totalC, Decimal( '0' ) )
        self.assertEqual( self.devolucion.totalD, Decimal( '0' ) )

    def test_cost( self ):
        self.assertEqual( self.devolucion.totalCostC, Decimal( '0' ) )
        self.assertEqual( self.devolucion.totalCostD, Decimal( '0' ) )

    def test_numrows( self ):
        self.assertEqual( self.devolucion.rowCount(), 1 )

    def test_validLines( self ):
        self.assertEqual( self.devolucion.validLines, 0 )

    def test_valid( self ):
        self.assertFalse( self.devolucion.valid )

    def test_subtotal( self ):
        self.assertEqual( self.devolucion.subtotalD, Decimal( '0' ) )
        self.assertEqual( self.devolucion.subtotalC, Decimal( '0' ) )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
