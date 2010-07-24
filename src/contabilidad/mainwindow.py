# -*- coding: utf-8 -*-
'''
Created on 28/06/2010

@author: armonge

El formulario principal de contabilidad
'''
from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import pyqtSlot, Qt, SIGNAL
from ui.Ui_mainwindowcontabilidad import Ui_MainWindow
from utility.mainwindowbase import MainWindowBase
from conciliacion import frmConciliacion
from contabilidad.operations import frmOperations
from contabilidad.cuentas import frmAccounts
from estadoresultado import frmEstadoResultado
from movimientosbancarios import frmMovimientosBancarios
from balancegeneral import frmBalanceGeneral

class MainWindow( QMainWindow, Ui_MainWindow, MainWindowBase ):
    def __init__( self, user, parent = None ):
        """
        Constructor
        """
        self.user = user
        QMainWindow.__init__( self, parent )
        self.setupUi( self )
        MainWindowBase.__init__( self )
        self.status = True

    def setControls( self, status ):
        self.btnMovements.setEnabled( status )

        self.actionLockSession.setVisible( status )
        self.actionUnlockSession.setVisible( not status )

    @pyqtSlot(  )
    def on_btnConciliacion_clicked( self ):
        """
        Slot documentation goes here.
        """
        conciliacion = frmConciliacion( self.user, self )
        self.mdiArea.addSubWindow( conciliacion )
        conciliacion.show()
 
    @pyqtSlot(  )
    def on_btnBalance_clicked( self ):
        """
        Slot documentation goes here.
        """
        balance = frmBalanceGeneral( self )
        self.mdiArea.addSubWindow( balance )
        balance.show()

    @pyqtSlot(  )
    def on_btnEstado_clicked( self ):
        """
        Slot documentation goes here.
        """
        estado = frmEstadoResultado( self.user, self )
        self.mdiArea.addSubWindow( estado )
        estado.show()


    @pyqtSlot()
    def on_btnMovements_clicked( self ):
        operations = frmOperations( self.user, self )
        self.mdiArea.addSubWindow( operations )
        operations.show()

    @pyqtSlot()
    def on_btnAccounts_clicked( self ):
    	accounts = frmAccounts( self.user, self )
    	self.mdiArea.addSubWindow( accounts )
    	accounts.show()

    @pyqtSlot()
    def on_btnNotasCD_clicked( self ):
        mov = frmMovimientosBancarios( self.user, self )
        self.mdiArea.addSubWindow( mov )
        mov.show()
        