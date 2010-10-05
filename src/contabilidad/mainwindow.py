# -*- coding: utf-8 -*-
'''
Created on 28/06/2010

@author: Andrés Reyes Monge

El formulario principal de contabilidad
'''
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow

from operations import FrmOperations
from estadoresultado import FrmEstadoResultado
from cuentas import FrmAccounts
from balancegeneral import FrmBalanceGeneral
from cheques import FrmCheques
from cierrecontable import FrmCierreContable
from conciliacion import FrmConciliacion
from creditodebito import FrmCreditoDebito
from movimientosbancarios import FrmMovimientosBancarios

from ui.Ui_mainwindowcontabilidad import Ui_MainWindow
from utility import constantes
from utility.mainwindowbase import MainWindowBase

class MainWindow( QMainWindow, Ui_MainWindow, MainWindowBase ):
    """

    """
    ROL = constantes.ACCESOCONTABILIDAD
    def __init__( self,  parent = None ):
        """
        Constructor
        """
        super(MainWindow, self).__init__(  parent )
        self.setupUi( self )
        MainWindowBase.__init__( self)
        self.init()
        
        
    def init(self):
        self.status = True

    def closeEvent( self, event ):
        u"""
        Guardar el tamaño, la posición en la pantalla y la posición de la barra de tareas
        Preguntar si realmente se desea cerrar la pestaña cuando se esta en modo edición
        """
        for hijo in self.mdiArea.subWindowList():
            if not hijo.close():
                event.ignore()
                return
                
    def setControls( self, status ):
        self.btnMovements.setEnabled( status )
        self.btnAccounts.setEnabled(status)
        self.btnBalance.setEnabled(status)
        self.btnNotasCD.setEnabled(status)
        self.btnCheques.setEnabled(status)
        self.btnConciliacion.setEnabled(status)
        self.btnEstado.setEnabled(status)
        
        self.mdiArea.setEnabled(status)
        self.mdiArea.setVisible(status)

        self.actionLockSession.setVisible( status )
        self.actionUnlockSession.setVisible( not status )

    @pyqtSlot(  )
    def on_btnConceptos_clicked( self ):
        """
        Catalogo de conceptos de modulo de contabilidad
        """
        conceptos=FrmCatConceptos(3,self)
        self.mdiArea.addSubWindow(conceptos)
        conceptos.show()
    
    @pyqtSlot(  )
    def on_btnCierreMensual_clicked( self ):
        """
        Catalogo de conceptos de modulo de contabilidad
        """
        cierre=FrmCierreContable(self)
        self.mdiArea.addSubWindow(cierre)
        cierre.show()
        
    @pyqtSlot(  )
    def on_btnCheques_clicked( self ):
        cheques=FrmCheques(self)
        self.mdiArea.addSubWindow(cheques)
        cheques.show()



    
    @pyqtSlot(  )
    def on_btnConciliacion_clicked( self ):
        """
        Slot documentation goes here.
        """
        conciliacion = FrmConciliacion(  self )
        self.mdiArea.addSubWindow( conciliacion )
        conciliacion.show()
 
    @pyqtSlot(  )
    def on_btnBalance_clicked( self ):
        """
        Slot documentation goes here.
        """
        balance = FrmBalanceGeneral( self )
        self.mdiArea.addSubWindow( balance )
        balance.show()

    @pyqtSlot(  )
    def on_btnEstado_clicked( self ):
        """
        Slot documentation goes here.
        """
        estado = FrmEstadoResultado(  self )
        self.mdiArea.addSubWindow( estado )
        estado.show()


    @pyqtSlot()
    def on_btnMovements_clicked( self ):
        operations = FrmOperations(  self )
        self.mdiArea.addSubWindow( operations )
        operations.show()

    @pyqtSlot()
    def on_btnAccounts_clicked( self ):
        accounts = FrmAccounts(  self )
        self.mdiArea.addSubWindow( accounts )
        accounts.show()

    @pyqtSlot()
    def on_btnNotasCD_clicked( self ):
        mov = FrmMovimientosBancarios(  self )
        self.mdiArea.addSubWindow( mov )
        mov.show()
    @pyqtSlot()
    def on_btnCreditoDebito_clicked( self ):
        ncd = FrmCreditoDebito(  self )
        self.mdiArea.addSubWindow( ncd )
        ncd.show()
        