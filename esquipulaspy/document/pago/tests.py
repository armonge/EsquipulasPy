'''
Created on 21/10/2010

@author: Administrador
'''
import sip
sip.setapi( "QString", 2 )

import unittest
from decimal import Decimal
from PyQt4.QtCore import QCoreApplication
from pagomodel import PagoModel
from caja.mainwindow import DatosSesion
class TestPagoModel( unittest.TestCase ):


    def setUp( self ):
        _app = QCoreApplication( [] )
        self.sesion = DatosSesion()
        self.sesion.tipoCambioBanco = Decimal( "21.6" )
        self.model = PagoModel( self.sesion )
        self.model.maxCordoba = Decimal( 100 )
        self.model.maxDolar = Decimal( 100 )
        self.model.docImpreso = "1212"
        self.model.observaciones = "dkjshndkjhsdkjh"
        self.model.totalC = Decimal( "216" )
        self.model.totalD = Decimal( "10" )
        self.model.conceptoId = 1
        self.model.beneficiarioId = 1

        self.model.aplicarRet = True
        self.model.retencionId = 0
        self.model.ivaId = 0
        self.model.aplicarIva = True
        self.model.ivaTasa = Decimal( 15 )
        self.retencionTasa = Decimal( "2" )

    def test_total( self ):
        self.assertEqual( self.model.totalDolar, Decimal( "20.00" ) )
        self.assertEqual( self.model.totalCordoba, Decimal( "432.00" ) )

    def test_subtotal( self ):
        self.assertEqual( self.model.subTotalDolar, Decimal( "17.3913" ) )

    def test_iva( self ):
        self.assertEqual( self.model.ivaTasa, Decimal( 15 ) )





if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
