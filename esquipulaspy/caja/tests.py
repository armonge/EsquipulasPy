# -*- coding: utf-8 -*-
'''
Created on 16/10/2010

@author: armonge
'''
import sip
from utility import constantes
sip.setapi( "QString", 2 )

import unittest

from PyQt4.QtTest import QTest
from PyQt4.QtGui import QApplication

from caja.mainwindow import MainWindow


class TestMainWindow( unittest.TestCase ):
    def setUp( self ):
        _app = QApplication( [] )
        self.mainwindow = MainWindow( constantes.ACCESOCAJA )

    def test_clients( self ):
        QTest.mouseClick( self.mainwindow.actionClients )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
