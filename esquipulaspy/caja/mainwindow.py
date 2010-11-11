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

"""
    Module implementing MainWindow.
"""
from PyQt4.QtCore import pyqtSlot, Qt
from PyQt4.QtGui import  QDialog, QMessageBox, qApp
from PyQt4.QtSql import  QSqlQuery
from apertura import DlgApertura
from arqueo import FrmArqueo
from decimal import Decimal
from devolucion import FrmDevolucion
from factura import FrmFactura
from pago import FrmPago
from recibo import FrmRecibo
from ui.Ui_mainwindowcaja import Ui_MainWindow
from utility import constantes
from utility.mainwindowbase import MainWindowBase
from utility.persona import FrmPersona
import logging


class MainWindow( MainWindowBase, Ui_MainWindow, ):
    """
    Esta clase implementa el MainWindow de Caja
    """
    ROL = constantes.ACCESOCAJA
    def __init__( self, module, parent = None ):
        """
        Constructor
        """
        super( MainWindow, self ).__init__( module, parent )
        self.startUi()
#        MainWindowBase.__init__( self )
        self.init()

    def init( self ):
        self.datosSesion = DatosSesion()
        self.datosSesion.usuarioId = self.user.uid
        self.cajaNombre = ""
        self.abierto = False
        self.setControls( True )


    def setControls( self, state ):
        """
        En esta funcion cambio el estado enabled de todos los items en el formulario
        @param state: false = bloqueado        true = desbloqueado
        """
        self.actionUnlockSession.setVisible( not state )


        self.abierto = ( state and self.datosSesion.sesionId != 0 )
        if self.datosSesion.sesionId != 0:
            self.btnApertura.setText( "Cierre de Caja" )
        else:
            self.btnApertura.setText( "Aperturar Caja" )

        self.btnApertura.setEnabled( state )
        self.actionClients.setEnabled( state )

        self.btnArqueo.setEnabled( self.abierto )

#        self.btnClients.setEnabled( state )

        self.btnrecibo.setEnabled( self.abierto )
        self.btnfactura.setEnabled( self.abierto )
        self.btnDevolutions.setEnabled( self.abierto )
        self.mdiArea.setEnabled( self.abierto )
        self.mdiArea.setVisible( self.abierto )
        self.btnpago.setEnabled( self.abierto )


        self.actionLockSession.setVisible( state )



    @pyqtSlot()
    def on_actionClients_triggered( self ):
        """
        Activar el formulario de personas
        """
        clientes = FrmPersona( constantes.CLIENTE, "Cliente" , self )
        clientes.show()



    @pyqtSlot()
    def on_btnArqueo_clicked( self ):
        """
        Activar el formulario de arqueo
        """
        arqueo = FrmArqueo( self.datosSesion, self )
        arqueo.show()


    @pyqtSlot()
    def on_btnrecibo_clicked( self ):
        """
        Activar el formulario de recibos
        """
        recibo = FrmRecibo( self )
        self.mdiArea.addSubWindow( recibo )
        recibo.show()

    @pyqtSlot()
    def on_btnApertura_clicked( self ):
        """
        Llamar a el formulario apertura para intentar crear una nueva sesión
        de caja ó continuar con una sesión anterior
        """
        self.datosSesion.usuarioId = self.user.uid
        estado = not self.abierto
        query = QSqlQuery()
        if estado:
#            try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( u"No se pudo abrir la conexión con la"\
                                       + " base de datos" )

            q = """
                SELECT
                    apertura.iddocumento,
                    apertura.idtipocambio,
                    tc.fecha,
                    tc.tasa,
                    IFNULL(tc.tasabanco,tc.tasa) as tasabanco,
                    apertura.idcaja
                FROM `esquipulasdb`.`documentos` apertura
                JOIN tiposcambio tc ON tc.idtc = apertura.idtipocambio
                JOIN personasxdocumento pd ON pd.iddocumento = apertura.iddocumento AND pd.idaccion=%d
                LEFT JOIN docpadrehijos ph ON apertura.iddocumento=ph.idpadre
                LEFT JOIN documentos cierre ON cierre.iddocumento = ph.idhijo AND cierre.idtipodoc=%d
                WHERE apertura.idtipodoc=%d AND pd.idpersona=%d
                GROUP BY apertura.iddocumento
                HAVING SUM(IFNULL(cierre.idtipodoc,0)) = 0;
               """ % ( constantes.AUTOR,
                       constantes.IDARQUEO,
                       constantes.IDAPERTURA,
                       self.datosSesion.usuarioId )
            if not query.prepare( q ):
                raise Exception( u"No se pudo preparar la consulta para "\
                                 + "recuperar la información de la sesión" )
            if not query.exec_():
                raise Exception( u"No se pudo ejecutar la consulta para"\
                                 + " recuperar la información de la sesión" )

            # Si existe al menos una sesion abierta no muestra el dialogo
            # de iniciar caja
            if query.size() > 0:
                reply = QMessageBox.question( self,
                                              qApp.organizationName(),
                                              u"Usted tiene una sesión de caja"\
                                              + " abierta. Desea continuar?",
                                              QMessageBox.Yes, QMessageBox.No )
                if reply == QMessageBox.Yes:

                    query.first()

                    self.datosSesion.usuarioId = self.user.uid
                    self.datosSesion.sesionId = query.value( 0 ).toInt()[0]
                    self.datosSesion.tipoCambioId = query.value( 1 ).toInt()[0]
                    self.datosSesion.fecha = query.value( 2 ).toDate()
                    self.datosSesion.tipoCambioOficial = Decimal ( query.value( 3 ).toString() )
                    self.datosSesion.tipoCambioBanco = Decimal ( query.value( 4 ).toString() )
                    self.datosSesion.cajaId = query.value( 5 ).toInt()[0]

                    if self.datosSesion.valid:
                        self.status = estado
                        logging.info( u"El usuario %s ha continuado una sesión de caja" % self.user.user )
                    else:
                        QMessageBox.critical( self,
                                               qApp.organizationName(),
                                                u"No fue posible abrir la "\
                                                + "sesión anterior. Por favor"\
                                                + " contacte al administrador"\
                                                + " del sistema" )
                        logging.error( u"No se pudo continuar con la sesión"\
                                       + " de caja del usuario" )
            else:
                apertura = DlgApertura( self )
                if apertura.exec_() == QDialog.Accepted:
                    self.status = estado

            if self.database.isOpen():
                self.database.close()
        else:
            arqueo = FrmArqueo( self.datosSesion, self )
            arqueo.show()




    @pyqtSlot()
    def on_btnfactura_clicked( self ):
        """
        Activar el formulario de facturas
        """
        factura = FrmFactura( self )
        self.mdiArea.addSubWindow( factura )
        factura.show()


    @pyqtSlot()
    def on_btnpago_clicked( self ):
        """
        Activar el formulario de pagos
        """
        pago = FrmPago( self.datosSesion , self )
        pago.show()

    @pyqtSlot()
    def on_btnDevolutions_clicked( self ):
        """
        Activar el formulario de devoluciones
        """
        devolucion = FrmDevolucion( self )
        devolucion.setAttribute( Qt.WA_DeleteOnClose )
        self.mdiArea.addSubWindow( devolucion )
        devolucion.show()



class DatosSesion():
    """
    Esta clase almacena la información de una sesión de caja
    """
    def __init__( self ):
        self.usuarioId = 0
        """
        @ivar: El id del usuario en esta sesión
        @type: int
        """

        self.sesionId = 0
        """
        @ivar: El id de la sesión
        @type:int
        """

        self.tipoCambioId = 0
        """
        @ivar: El id del tipo de cambio
        @type: int
        """

        self.tipoCambioOficial = Decimal( 0 )
        """
        @ivar: El tipo de cambio oficial
        @type: Decimal
        """

        self.tipoCambioBanco = Decimal( 0 )
        """
        @ivar: El tipo de cambio del banco
        @type: Decimal
        """

        self.fecha = None
        """
        @ivar: La fecha de la sesión
        @type: QDate
        """

        self.cajaId = 0
        """
        @ivar: El id de la caja
        @type: int
        """


#FIXME: Para que es mensaje????
    @property
    def valid( self ):
        mensaje = u"La sesión no fue abierta porque no se cargo "
        if self.usuarioId == 0:
            mensaje += "el id de usuario"
        elif self.sesionId == 0:
            mensaje += "el id de sesion"
        elif self.tipoCambioId == 0:
            mensaje += "el id del tipo de cambio"
        elif self.tipoCambioOficial == 0:
            mensaje += "la tasa de cambio oficial"
        elif self.tipoCambioBanco == 0:
            mensaje += "la tasa de cambio del banco"
        elif self.fecha == None:
            mensaje += "la fecha"
        elif self.cajaId == 0:
            mensaje += "el id de la caja"
        else:
            return True

        return False

