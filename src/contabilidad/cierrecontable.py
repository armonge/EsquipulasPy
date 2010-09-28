from PyQt4.QtCore import pyqtSlot, SIGNAL, QModelIndex, Qt, QTimer, \
    SLOT, QDate
import logging
from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QDataWidgetMapper, \
    QDialog, QTableView, QDialogButtonBox, QVBoxLayout, QAbstractItemView, QFormLayout, \
     QLineEdit,QMessageBox,qApp

from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from ui.Ui_cierre import Ui_frmCierreContable
from utility.base import Base

from utility import constantes
IDDOCUMENTO,NDOCUMENTO,TIPODOC,TOTAL,FECHA,OBSERVACIONES,ESTADO=range(7)
class frmCierreContable( Ui_frmCierreContable, QMainWindow ):
    def __init__( self,  parent ):
        super( frmCierreContable, self ).__init__( parent )
        self.setupUi( self )
        self.parentWindow = parent
                
        self.navmodel = QSqlQueryModel( self )
        self.navproxymodel = QSortFilterProxyModel( self )
        self.navproxymodel.setSourceModel( self.navmodel )
        
        self.navproxymodel.setFilterKeyColumn( -1 )
        self.navproxymodel.setFilterCaseSensitivity ( Qt.CaseInsensitive )
        self.editmodel = None  
        self.fecha=None
        self.status = True

        self.dtPicker.setMaximumDate(QDate.currentDate())
        self.dtPicker.setDate(QDate.currentDate())
        
    @pyqtSlot( "QDateTime" )
    def on_dtPicker_dateTimeChanged( self, datetime ):
        """
        Asignar la fecha al objeto __document
        """
        self.fecha=datetime
        self.updateModels()
                
    def updateModels(self):
        
        self.navmodel.setQuery(u"select iddocumento,ndocimpreso as 'No. Documento',td.descripcion as TipoDocumento,format(total ,4)as Total,date_format(fechacreacion,'%d/%m/%Y') as Fecha,observacion as Observaciones, estados.descripcion as Estado from documentos d join estadosdocumento estados on estados.idestado=d.idestado join tiposdoc td on d.idtipodoc=td.idtipodoc where MONTH(fechacreacion)="+self.fecha.toString("MM")+" and d.idtipodoc!="+ str(constantes.IDAPERTURA))
        query=QSqlQuery()
        query.prepare( "SELECT iddocumento FROM documentos where MONTH(fechacreacion)="+self.fecha.toString("MM")+" and idtipodoc="+str(constantes.IDCIERREMENSUAL))
        if not query.exec_():
            raise UserWarning("No se pudo ejecutar la consulta para verificar si existe un cierre contable")
        
        if self.navmodel.rowCount()==0 or query.size()>0: 
            self.toolBar.removeAction(self.actionSave)
        else:
            self.toolBar.addActions([
            self.actionSave])
            self.actionSave.triggered.connect(self.save)

        self.tabledetails.setModel(self.navproxymodel)
        self.tabledetails.setColumnHidden( 0, True )
        self.tabledetails.resizeColumnsToContents()
        
#    def setControls( self, status ):
#        """
#        @param status: false = editando        true = navegando
#        """
#        self.actionPrint.setVisible(status)
#        self.actionSave.setVisible(   status )
#        self.actionPreview.setVisible( status)
#        self.actionSave.setVisible(status)
    def save(self):
        validado=False
        for i in range(self.navproxymodel.rowCount()):
            if self.navproxymodel.index(i,ESTADO).data(Qt.EditRole).toString()!="CONFIRMADO":
                validado=True
        if validado==True:
            QMessageBox.warning(None, "Documentos Pendientes", "Existen documentos que aun no han sido confirmados")
        else:
            try:
                query=QSqlQuery()
                query.prepare( "CALL `esquipulasdb`.`spCierreMensual`(:IDCIERRE,:MES,:ESTADO:ANO)" )
                query.bindValue( ":IDCIERRE", constantes.IDCIERREMENSUAL)
                query.bindValue( ":MES",self.fecha.toString("MM") )
                query.bindValue( ":ESTADO", constantes.CONFIRMADO)
                query.bindValue( ":ANO", self.fecha.toString("yyyy"))
                
                if not query.exec_():
                    raise UserWarning("No se pudo Cerrar el mes Contable")
                
                QMessageBox.information( None, "Cierre Mensual", "Cierre mensual exitoso" )
                self.toolBar.removeAction(self.actionSave)
                self.toolBar.addActions(self.actionPrint)
                self.actionPrin.triggered.connect(self.printPreview)
                                
            except UserWarning as inst:             
        
                logging.error(inst)
                QMessageBox.critical(self, qApp.organizationName(), unicode(inst))
                