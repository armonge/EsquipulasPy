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
Created on 28/06/2010

@author: Andrés Reyes Monge

El formulario principal de contabilidad
'''
from PyQt4.QtCore import pyqtSlot

from operations import FrmOperations
from estadoresultado import FrmEstadoResultado
from cuentas import FrmAccounts
from balancegeneral import FrmBalanceGeneral
from cheques import FrmCheques
from cierrecontable import FrmCierreContable
from conciliacion import FrmConciliacion
from movimientosbancarios import FrmMovimientosBancarios

from ui.Ui_mainwindowcontabilidad import Ui_MainWindow
from utility import constantes
from utility.mainwindowbase import MainWindowBase

class MainWindow( MainWindowBase, Ui_MainWindow ):
    """

    """
    ROL = constantes.ACCESOCONTABILIDAD
    def __init__( self, module, parent = None ):
        """
        Constructor
        """
        super( MainWindow, self ).__init__( module, parent )
        self.startUi()
        self.init()


    def init( self ):
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
        self.btnAccounts.setEnabled( status )
        self.btnBalance.setEnabled( status )
        self.btnNotasCD.setEnabled( status )
        self.btnCheques.setEnabled( status )
        self.btnConciliacion.setEnabled( status )
        self.btnEstado.setEnabled( status )

        self.mdiArea.setEnabled( status )
        self.mdiArea.setVisible( status )

        self.actionLockSession.setVisible( status )
        self.actionUnlockSession.setVisible( not status )


    @pyqtSlot()
    def on_btnCierreMensual_clicked( self ):
        """
        Catalogo de conceptos de modulo de contabilidad
        """
        cierre = FrmCierreContable( self, "Mensual" )
        self.mdiArea.addSubWindow( cierre )
        cierre.show()


    @pyqtSlot()
    def on_btnCierreAnual_clicked( self ):
        """
        Catalogo de conceptos de modulo de contabilidad
        """
        cierre = FrmCierreContable( self, "Anual" )
        self.mdiArea.addSubWindow( cierre )
        cierre.show()

    @pyqtSlot()
    def on_btnCheques_clicked( self ):
        cheques = FrmCheques( self )
        self.mdiArea.addSubWindow( cheques )
        cheques.show()




    @pyqtSlot()
    def on_btnConciliacion_clicked( self ):
        """
        Slot documentation goes here.
        """
        conciliacion = FrmConciliacion( self )
        self.mdiArea.addSubWindow( conciliacion )
        conciliacion.show()

    @pyqtSlot()
    def on_btnBalance_clicked( self ):
        """
        Slot documentation goes here.
        """
        balance = FrmBalanceGeneral( self )
        self.mdiArea.addSubWindow( balance )
        balance.show()

    @pyqtSlot()
    def on_btnEstado_clicked( self ):
        """
        Slot documentation goes here.
        """
        estado = FrmEstadoResultado( self )
        self.mdiArea.addSubWindow( estado )
        estado.show()


    @pyqtSlot()
    def on_btnMovements_clicked( self ):
        operations = FrmOperations( self )
        self.mdiArea.addSubWindow( operations )
        operations.show()

    @pyqtSlot()
    def on_btnAccounts_clicked( self ):
        accounts = FrmAccounts( self )
        self.mdiArea.addSubWindow( accounts )
        accounts.show()

    @pyqtSlot()
    def on_btnNotasCD_clicked( self ):
        mov = FrmMovimientosBancarios( self )
        self.mdiArea.addSubWindow( mov )
        mov.show()
