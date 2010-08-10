# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

"""
    Module implementing MainWindow.
"""

from PyQt4.QtGui import QMainWindow, QDialog, QMessageBox
from PyQt4.QtCore import pyqtSlot, Qt,QDate
from PyQt4.QtSql import QSqlDatabase,QSqlQuery
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
        
        
        self.datosSesion = None
        self.status = False
    
#    def closeEvent( self, event ):
#        u"""
#        Guardar el tamaño, la posición en la pantalla y la posición de la barra de tareas
#        Preguntar si realmente se desea cerrar la pestaña cuando se esta en modo edición
#        """
#        for hijo in self.mdiArea.subWindowList():
#            if not hijo.close():
#                event.ignore()
#                return
                
            
#        if not QMessageBox.question(self, "Llantera Esquipulas", u"¿Está seguro que desea salir?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
#            event.ignore()        
        
    def setControls( self, state ):
        """
        En esta funcion cambio el estado enabled de todos los items en el formulario
        @param state: false = bloqueado        true = desbloqueado
        """
        if state:
            self.btnApertura.setText("Cierre de Caja")
        else:
            self.btnApertura.setText("Abrir Caja")
        
        if self.datosSesion!= None:
            self.actionUnlockSession.setVisible( not state )

        self.btnArqueo.setEnabled( state )
        self.btnClients.setEnabled( state )
        self.btnrecibo.setEnabled( state )
        self.btnfactura.setEnabled( state )

        self.mdiArea.setEnabled( state )
        self.mdiArea.setVisible( state )
        self.actionLockSession.setVisible( state )


    @pyqtSlot(  )
    def on_btnConceptos_clicked( self ):
        conceptos=frmCatConceptos(2,self)
        self.mdiArea.addSubWindow(conceptos)
        conceptos.show()
        

    @pyqtSlot(  )
    def on_btnArqueo_clicked( self ):
        arqueo = frmArqueo( self.user, self )
        self.mdiArea.addSubWindow( arqueo )
        arqueo.show()

  
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
        if self.status:
        
            
            db = QSqlDatabase.database()
    #        try:
            if not db.isOpen():
                db.open()
            query = QSqlQuery( """
            SELECT 
                apertura.iddocumento,
                apertura.idtipocambio,
                tc.fecha, 
                tc.tasa,
                tc.tasabanco
                FROM `esquipulasdb`.`documentos` apertura
                JOIN tiposcambio tc ON tc.idtc = apertura.idtipocambio
                JOIN personasxdocumento pd ON pd.iddocumento = apertura.iddocumento AND pd.autoriza=0
                LEFT JOIN docpadrehijos ph ON apertura.iddocumento=ph.idpadre
                LEFT JOIN documentos cierre ON cierre.iddocumento = ph.idhijo AND cierre.idtipodoc=17
                WHERE apertura.idtipodoc=22 AND pd.idpersona=1 
                AND cierre.iddocumento IS NULL;
               """)
            if not query.exec_():
                raise Exception("No se pudo preparar la Query")                                   
    # Si existe al menos una sesion abierta no muestra el dialogo de iniciar caja    
            if query.size()>0:
                reply=QMessageBox.question(None, 'Abrir Caja',u"Usted tiene una sesión de caja abierta. Desea continuar?", QMessageBox.Yes, QMessageBox.No)                        
                if reply == QMessageBox.Yes:
                    
                    query.first()
                    
                    DatosSesion = namedtuple('DatosSesion','usuarioId sesionId tipoCambioId tipoCambioOficial tipoCambioBanco fecha')
                        
                    sesionId = query.value(0).toInt()[0]
                    tipoCambioId = query.value(1).toInt()[0]
                    fecha = query.value(2).toDate()
                    
                    tipoCambio = Decimal (query.value(3).toString())
                    tipoBanco =  Decimal (query.value(4).toString())  
                    
                    self.datosSesion = DatosSesion(self.user.uid,sesionId,tipoCambioId,tipoCambio,tipoBanco,fecha)
                         
                    self.setControls(True)
    #        except Exception, e:
    #            print e
    #        finally:
            if db.isOpen():
                db.close()                    
                                       
            return None                                      
        #Si query.size no es mayor que cero Ejecutara esto                     
                            
            apertura = frmApertura( self )
            if apertura.exec_() == QDialog.Accepted:
                self.setControls( True )
                
        else:
            

    
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


    
        