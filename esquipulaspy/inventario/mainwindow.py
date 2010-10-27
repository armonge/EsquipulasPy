#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       
#       Copyright 2010 Andrés Reyes Monge <armonge@armonge-laptop.site>
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

"""
Module implementing MainWindow.
"""
from PyQt4.QtCore import pyqtSlot
from articulos import FrmArticulos
from catalogos import FrmCatMarcas, FrmCatConceptos
from categorias import FrmCategorias
from entradacompra import FrmEntradaCompra
from kardex import FrmKardex
from kardexother import FrmKardexOther
from liquidacion import FrmLiquidacion
from ui.Ui_mainwindowinventario import Ui_MainWindow
from utility import constantes
from utility.mainwindowbase import MainWindowBase
from utility.persona import FrmPersona

class MainWindow( MainWindowBase, Ui_MainWindow ):
    """
    Class documentation goes here.
    """
    ROL = constantes.ACCESOINVENTARIO
    def __init__( self, module, parent = None ):
        """
        Constructor
        """
        super( MainWindow, self ).__init__( module, parent )
        self.startUi()
        self.init()

    def init( self ):
        if self.user.hasRole( 'root' ):
            return

        if not ( self.user.hasAnyRole( [ 'inventario', 'contabilidad'] ) ) :
            self.page.setVisible( False )
            self.toolBox.removeItem( 2 )
            self.page_2.setVisible( False )
            self.toolBox.removeItem( 0 )

        if self.user.hasRole( 'contabilidad' ) and not self.user.hasRole( 'kardex' ):
            self.btnKExits.setVisible( False )
            self.btnKEntries.setVisible( False )

        if not ( self.user.hasAnyRole( [ 'kardex', 'contabilidad' ] ) ):
            #Quitar la pestaña de kardex
            self.widget.setVisible( False )
            self.toolBox.removeItem( 1 )




    def closeEvent( self, event ):
        u"""
        Guardar el tamaño, la posición en la pantalla y la posición de la barra
        de tareas
        Preguntar si realmente se desea cerrar la pestaña cuando
        se esta en modo edición
        """
        for hijo in self.mdiArea.subWindowList():
            if not hijo.close():
                event.ignore()
                return
    def setControls( self, state ):
        """
        En esta funcion cambio el estado enabled de todos los items en el formulario
        @param state: false = bloqueado        true = activado
        """
        self.btnArticles.setEnabled( state )
        self.btnBrands.setEnabled( state )
        self.btnCategories.setEnabled( state )
        self.btnEntries.setEnabled( state )
        self.btnLiquidations.setEnabled( state )
        self.btnProviders.setEnabled( state )

        self.mdiArea.setEnabled( state )
        self.mdiArea.setVisible( state )

        self.btnKEntries.setEnabled( state )
        self.btnKExits.setEnabled( state )
        self.btnKOther.setEnabled( state )

        self.actionLockSession.setVisible( state )
        self.actionUnlockSession.setVisible( not state )

    @pyqtSlot()
    def on_btnConceptos_clicked( self ):
        """
        Slot documentation goes here.
        """
        conceptos = FrmCatConceptos( 4, self )
        self.mdiArea.addSubWindow( conceptos )
        conceptos.show()

    @pyqtSlot()
    def on_btnEntries_clicked( self ):
        """
        Slot documentation goes here.
        """
        entradacompra = FrmEntradaCompra( self )
        self.mdiArea.addSubWindow( entradacompra )
        entradacompra.show()

    @pyqtSlot()
    def on_btnArticles_clicked( self ):
        """
        Slot documentation goes here.
        """
        catproducts = FrmArticulos( self )
        self.mdiArea.addSubWindow( catproducts )
        catproducts.show()


    @pyqtSlot()
    def on_btnCategories_clicked( self ):
        """
        Slot documentation goes here.
        """

        catcategorias = FrmCategorias( self )
        self.mdiArea.addSubWindow( catcategorias )
        catcategorias.show()

    @pyqtSlot()
    def on_btnBrands_clicked( self ):
        """
        Slot documentation goes here.
        """

        catmarcas = FrmCatMarcas( self )
        self.mdiArea.addSubWindow( catmarcas )
        catmarcas.show()

    @pyqtSlot()
    def on_btnProviders_clicked( self ):
        """
        Slot documentation goes here.
        """
        dialog = FrmPersona( constantes.PROVEEDOR, "Proveedor" )
        dialog.show()
#        catproveedores = FrmCatProveedores( self )
#        self.mdiArea.addSubWindow( catproveedores )
#        catproveedores.show()

    @pyqtSlot()
    def on_btnLiquidations_clicked( self ):
        """
        Slot documentation goes here.
        """
        liquidacion = FrmLiquidacion( self )
        self.mdiArea.addSubWindow( liquidacion )
        liquidacion.show()

    @pyqtSlot()
    def on_btnKEntries_clicked( self ):
        """
        Slot documentation goes here.
        """
        kardex = FrmKardex( [constantes.IDLIQUIDACION,
                             constantes.IDNC,
                             constantes.IDANULACION,
                              constantes.IDENTRADALOCAL], self )
        self.mdiArea.addSubWindow( kardex )
        kardex.show()

    @pyqtSlot()
    def on_btnKOther_clicked( self ):
        """
        Slot documentation goes here
        """
        kardex = FrmKardexOther( self )
        self.mdiArea.addSubWindow( kardex )
        kardex.show()

    @pyqtSlot()
    def on_btnKExits_clicked( self ):
        """
        Slot documentation goes here.
        """
        kardex = FrmKardex( [5], self, False )
        self.mdiArea.addSubWindow( kardex )
        kardex.show()
