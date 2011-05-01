#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
Created on 13/10/2010

@author: armonge
'''
from pyqtconfig import Qt
from PyQt4.QtCore import QVariant, QCoreApplication
from decimal import Decimal
from document.entradacompra.entradacompramodel import EntradaCompraModel, \
    CANTIDAD, PRECIO, DESCRIPCION
from document.entradacompra.lineaentradacompra import LineaEntradaCompra

import unittest




class TestEntradaCompraSimple( unittest.TestCase ):
    """
    Esta clase es un TesCase para EntradaCompraModel reproduce un caso común y
    verifica los resultados del modelo con los esperados
    """
    def setUp( self ):
        _app = QCoreApplication( [] )

        self.entrada = EntradaCompraModel()


        self.entrada.insertRow( 0 )
        self.entrada.exchangeRate = Decimal( "21.21" )
        self.entrada.rateIVA = Decimal( '15' )
        self.entrada.exchangeRateId = 1
        self.entrada.exchangeRate = Decimal( '21' )

        self.entrada.setData( self.entrada.index( 0, CANTIDAD ), QVariant( "1" ) )
        self.entrada.setData( self.entrada.index( 0, PRECIO ), QVariant( "1" ) )
        self.entrada.setData( self.entrada.index( 0, DESCRIPCION ), [
            1,
            "FRICCIONES* BATERIA  N-150 DURUN"
        ] )


    def valid( self ):
        self.assertTrue( self.entrada.valid, "El documento deberia tener un estado de valido" )

    def test_validLines( self ):
        self.assertEqual( self.entrada.validLines, 1, "El documento deberia tener exactamente una linea valida" )

    def test_iva( self ):
        self.assertEqual( self.entrada.IVAC, Decimal( '0.15' ), "El iva en cordobas deberia ser exactamente 0.15 y es %s" % self.entrada.IVAC.to_eng_string() )
        self.assertEqual( self.entrada.IVAD, Decimal( '0.007142857142857142857142857143' ) )

    def test_total( self ):
        self.assertEqual( self.entrada.totalC, Decimal( '1.15' ) )
        self.assertEqual( self.entrada.totalD, Decimal( '0.05476190476190476190476190476' ) )


    def test_numrows( self ):
        self.assertEqual( self.entrada.rowCount(), 2, "El documento deberia tener 2 lineas" )


class TestLineaLineaEntradCompra( unittest.TestCase ):
    """
    Esta clase es un TesCase para LineaEntradaCompra reproduce un caso común y
    verifica los resultados del modelo con los esperados
    """
    def setUp( self ):
        _app = QCoreApplication( [] )

        self.exchangeRate = Decimal( '21.21' )
        self.exchangeRateId = 1

        self.line = LineaEntradaCompra( self )
        self.line.quantity = 1
        self.line.itemId = 1
        self.line.itemPriceC = Decimal( '1' )

    def test_valid( self ):
        self.assertTrue( self.line.valid, "La linea deberia de ser valida" )

    def test_total( self ):
        self.assertEqual( self.line.totalC, Decimal( '1' ),
                           "El total en cordobas deberia de ser 1 y es %s" % self.line.totalC.to_eng_string() )
        self.assertEqual( self.line.totalD,
                          Decimal( '0.04714757190004714757190004715' ),
                          "El total en dolares deberia de ser y es %s" % self.line.totalD.to_eng_string() )




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
