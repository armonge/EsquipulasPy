# -*- coding: utf-8 -*-
'''
Created on 16/10/2010

@author: armonge
'''
from pyqtconfig import Qt
from utility import constantes

import unittest

from PyQt4.QtTest import QTest
from utility.guitest import GuiTestCase
from utility import  constantes
from utility import user


class TestMainWindow( GuiTestCase ):
    acceso = constantes.ACCESOCAJA
    module = 'caja'

    def test_show(self):
        self.main_window.show()
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
