# -*- coding: utf-8 -*-
'''
Created on 17/10/2010

@author: armonge
'''
#TODO: Esta prueba TIENE que ser más extensiva
import sip
sip.setapi( "QString", 2 )

from lineaconciliacion import LineaConciliacion
from conciliacionmodel import ConciliacionModel
import unittest

from PyQt4.QtCore import QCoreApplication


class TestLineConciliacion( unittest.TestCase ):

    def setUp( self ):
        _app = QCoreApplication( [] )
        self.linea_conciliacion = LineaConciliacion( self )

    def test_valid( self ):
        """
        Esta prueba verifica si las reglas para que la linea sea valida se 
        cumplen 
        """
        self.assertFalse( self.linea_conciliacion.valid )

        self.linea_conciliacion.idDoc = 1

        self.assertTrue( self.linea_conciliacion.valid )

class TestConciliacionModel( unittest.TestCase ):
    def setUp( self ):
        _app = QCoreApplication( [] )
        self.conciliacion = ConciliacionModel()
        self.conciliacion.idCuentaContable = 1
        self.conciliacion.uid = 1

        self.conciliacion.insertRow( 0 )

    def test_valid( self ):
        self.assertTrue( self.conciliacion.valid )
        self.conciliacion.uid = 0
        self.assertFalse( self.conciliacion.valid )
        self.conciliacion.uid = 1
        self.conciliacion.idCuentaContable = 0
        self.assertFalse( self.conciliacion.valid )

    def test_rows( self ):
        self.assertEqual( self.conciliacion.rowCount(), 1 )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
