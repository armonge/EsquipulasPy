from PyQt4.QtCore import pyqtSlot, SIGNAL, QModelIndex, Qt, QTimer, \
    SLOT, QDate

from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QDataWidgetMapper, \
    QDialog, QTableView, QDialogButtonBox, QVBoxLayout, QAbstractItemView, QFormLayout, \
     QLineEdit,QMessageBox

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

        self.status = True

        self.addActionsToToolBar()
        self.dtPicker.setMaximumDate(QDate.currentDate())
        self.dtPicker.setDate(QDate.currentDate())

    @pyqtSlot( "QDateTime" )
    def on_dtPicker_dateTimeChanged( self, datetime ):
        """
        Asignar la fecha al objeto __document
        """
        self.updateModels(datetime)
        
    def updateModels(self,fecha):
        
        self.navmodel.setQuery(u"select iddocumento,ndocimpreso as 'No. Documento',td.descripcion as TipoDocumento,format(total ,4)as Total,date_format(fechacreacion,'%d/%m/%Y') as Fecha,observacion as Observaciones, estados.descripcion as Estado from documentos d join estadosdocumento estados on estados.idestado=d.idestado join tiposdoc td on d.idtipodoc=td.idtipodoc where MONTH(fechacreacion)="+fecha.toString("MM")+" and d.idtipodoc!="+ str(constantes.IDAPERTURA))
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
#    
    def addActionsToToolBar(self):
        self.toolBar.addActions([
#            self.actionPreview,
#            self.actionPrint,
            self.actionSave,
#            self.actionCancel,
        ])
        self.actionSave.triggered.connect(self.save)
        
    def save(self):
        validado=False
        for i in range(self.navproxymodel.rowCount()):
            if self.navproxymodel.index(i,ESTADO).data(Qt.EditRole).toString()!="CONFIRMADO":
                validado=True
        if validado==True:
            QMessageBox.warning(None, "Documentos Pendientes", "Existen documentos que aun no han sido confirmados")
        else:
            query=QSqlQuery()
            query.prepare( "CALL `esquipulasdb`.`spCierreMensual`(:IDCIERRE,:MES,:ESTADO)" )
            query.bindValue( ":IDCIERRE", constantes.IDCIERREMENSUAL)
            query.bindValue( ":MES",fecha.toString("MM") )
            query.bindValue( ":ESTADO", constantes.CONFIRMADO)
            
            if not query.exec_():
                raise Exception("No se pudo CERRAR el MES CONTABLE")
            
            QMessageBox.information( None, "Cierre Mensual", "Cierre mensual exitoso" )
            
            