
# -*- coding: utf-8 -*-

"""
    Module implementing MainWindow.
"""

from PyQt4.QtGui import QMainWindow, QDialog, QMessageBox
from PyQt4.QtCore import pyqtSlot, Qt,QDate
from PyQt4.QtSql import QSqlDatabase
from factura import frmFactura
from recibo import frmRecibo
from ui.Ui_mainwindowcaja import Ui_MainWindow
from apertura import frmApertura
from utility.user import dlgUserLogin, User
from utility.mainwindowbase import MainWindowBase
from inventario.catalogos import frmCatConceptos
from banks import frmBanks
from cajas import frmCajas
from catalogos import frmCatClientes
from anulaciones import frmAnulaciones 
from arqueo import frmArqueo
from cheques import frmCheques
from cierrecaja import frmCierreCaja
from decimal import Decimal
from collections import namedtuple

class MainWindow( QMainWindow, Ui_MainWindow, MainWindowBase ):
    """
    Esta clase implementa el MainWindow de Caja
    """

    def __init__( self, user, parent = None ):
        """
        Constructor
        """
        super( MainWindow, self ).__init__( parent )
        self.setupUi( self )
        MainWindowBase.__init__( self )
        self.user = user
        
        DatosSesion = namedtuple('DatosSesion','sesionId tiposCambioId tiposCambioOficial tiposCambioBanco fecha')
        
        self.datosSesion = DatosSesion(1,12,'21.4138','21.50',QDate.currentDate()) 
        
        self.status = True
        
        
    def setControls( self, state ):
        """
        En esta funcion cambio el estado enabled de todos los items en el formulario
        @param state: false = bloqueado        true = desbloqueado
        """
        if self.datosSesion.sesionId != 0:
            self.btnApertura.setEnabled( state )
            self.actionUnlockSession.setVisible( not state )


        self.btnCheques.setVisible(state)
        self.btnArqueo.setEnabled( state )
        self.btnBanks.setEnabled( state )
        self.btnpos.setEnabled( state )
        self.btnClients.setEnabled( state )
        self.btnrecibo.setEnabled( state )
        self.btnfactura.setEnabled( state )
        self.btnAnnulments.setEnabled( state )
        self.btnConceptos.setEnabled( state )
        self.mdiArea.setEnabled( state )
        self.mdiArea.setVisible( state )
        self.actionLockSession.setVisible( state )

    @pyqtSlot(  )
    def on_btnAnnulments_clicked( self ):
        """
        Slot documentation goes here.
        """
        dlguser = dlgUserLogin()
        if dlguser.exec_() == QDialog.Accepted:
            user = User( dlguser.txtUser.text(), dlguser.txtPassword.text() )
    
            if user.valid:
                if user.hasRole( 'root' ):            
                    anulacion=frmAnulaciones( self.user, user)
                    self.mdiArea.addSubWindow(anulacion)
                    anulacion.show()
            
            else:
                QMessageBox.critical( None,
                    "Llantera Esquipulas",
                    str( user.error ),
                    QMessageBox.StandardButtons( QMessageBox.Ok ) )

    @pyqtSlot(  )
    def on_btnConceptos_clicked( self ):
        conceptos=frmCatConceptos(2,self)
        self.mdiArea.addSubWindow(conceptos)
        conceptos.show()
        

    @pyqtSlot(  )
    def on_btnCheques_clicked( self ):
        cheques=frmCheques(self.user,self)
        self.mdiArea.addSubWindow(cheques)
        cheques.show()


    @pyqtSlot(  )
    def on_btnArqueo_clicked( self ):
        arqueo = frmArqueo( self.user, self )
        self.mdiArea.addSubWindow( arqueo )
        arqueo.show()

    @pyqtSlot(  )
    def on_btnBanks_clicked( self ):
        """
        Slot documentation goes here.
        """
        bancos = frmBanks( self )
        self.mdiArea.addSubWindow( bancos )
        bancos.show()

    @pyqtSlot(  )
    def on_btnpos_clicked( self ):
        """
        Slot documentation goes here.
        """
        cajas = frmCajas( self )
        self.mdiArea.addSubWindow( cajas )
        cajas.show()


    @pyqtSlot(  )
    def on_btnrecibo_clicked( self ):
        """
        Slot documentation goes here.
        """
        recibo = frmRecibo( self.user, self )
        recibo.setAttribute( Qt.WA_DeleteOnClose )
        self.mdiArea.addSubWindow( recibo )
        recibo.show()

    @pyqtSlot(  )
    def on_btnApertura_clicked( self ):
        """
        Slot documentation goes here.
        """
        db = QSqlDatabase.database()
        try:
#            if not db.isOpen():
#                db.open()
#            query = QSqlQuery( """
#               SELECT d.iddocumento FROM documentos d
#               LEFT JOIN docpadrehijos dp ON dp.idpadre=d.iddocumento
#               LEFT JOIN documentos hijo ON dp.idhijo=hijo.iddocumento and hijo.idtipodoc=17
#               where d.idtipodoc=22 and d.idusuario=""" +str(self.user.uid)+ """ AND hijo.iddocumento IS  NULL""")
#            if not query.exec_():
#                raise Exception("No se pudo preparar la Query")                                   
#    # Si existe al menos una sesion abierta no muestra el dialogo de iniciar caja    
#            if query.size()>0:
#                reply=QMessageBox.question(None, 'Message',"Tiene sesion de caja abierta continuar?", QMessageBox.Yes, QMessageBox.No)                        
#                if reply == QMessageBox.Yes:
#                    self.btnApertura.setEnabled(False)
#                    query.first()
#                    self.sesion= query.value(0).toInt()[0]
#                    self.setControls(True)                            
#                return None                                      
#    #Si query.size no es mayor que cero Ejecutara esto                     
#                        
                AperturaCaja = frmApertura( self.user )
                if AperturaCaja.exec_() == QDialog.Accepted:
                    self.setControls( True )
                    self.sesion=AperturaCaja.sesion
                    self.exchangeRate=AperturaCaja.exchangeRate
                    self.exchangeRateId= AperturaCaja.exchangeRateId
                    self.bankExchangeRate= AperturaCaja.bankExchangeRate
                    self.date=AperturaCaja.fecha
        except Exception, e:
            print e
        finally:
            if db.isOpen():
                db.close()
    
    @pyqtSlot(  )
    def on_btnfactura_clicked( self ):
        """
        Slot documentation goes here.
        """
        factura = frmFactura( self.user , self )
        self.mdiArea.addSubWindow( factura )
        factura.show()

    @pyqtSlot(  )
    def on_btnClients_clicked( self ):
        """
        Slot documentation goes here.
        """
        clientes = frmCatClientes( self )
        self.mdiArea.addSubWindow( clientes )
        clientes.show()


    
        