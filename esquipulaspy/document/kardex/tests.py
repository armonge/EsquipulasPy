# -*- coding: utf-8 -*-
'''
Created on 18/10/2010

@author: armonge
'''
from pyqtconfig import Qt
from lineakardex import LineaKardex

from PyQt4.QtCore import QCoreApplication
import unittest


class TestLineaKardex( unittest.TestCase ):


    def setUp( self ):
        _app = QCoreApplication( [] )

        self.line = LineaKardex()
        self.line.numdoc = 10
        self.line.numajuste = -3




    def test_num( self ):
        self.assertEqual( self.line.numfinal, 7 )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
