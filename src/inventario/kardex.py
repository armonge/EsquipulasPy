# -*- coding: utf-8 -*-
'''
Created on 11/07/2010

@author: armonge
'''
from decimal import Decimal

from PyQt4.QtGui import QMainWindow,QSortFilterProxyModel, QVBoxLayout, QDialogButtonBox, QFormLayout, QLineEdit, QDialog, QTableView, QAbstractItemView, QMessageBox
from PyQt4.QtSql import QSqlQueryModel, QSqlQuery, QSqlDatabase
from PyQt4.QtCore import QTimer, Qt, pyqtSlot, SIGNAL, SLOT, QDateTime

from ui.Ui_kardex import Ui_frmKardex

from  utility import constantes
from utility.base import Base
from document.kardex.kardexmodel import KardexModel
from document.kardex.lineakardex import LineaKardex
from document.kardex.kardexdelegate import KardexDelegate


#DETAILS
IDARTICULO, DESCRIPCION, UNIDADES, AJUSTE, IDDOCUMENTOT = range(5)
#NAVIGATION
IDDOCUMENTO, NDOCIMPRESO,NKARDEX, NOMBREBODEGA, FECHA,  OBSERVACIONK ,OBSERVACION, BODEGA = range(8)
class frmKardex(QMainWindow, Ui_frmKardex, Base):
    '''
    classdocs
    '''
    def __init__(self, user, tiposdoc, parent = None, edit = True):
        '''
        Constructor
        '''
        super( frmKardex, self ).__init__( parent )
        self.setupUi( self )
        self.parentWindow = parent
        Base.__init__( self )
        self.user = user
        self.tiposdoc = ",".join([str(item) for item in tiposdoc])
        
        self.edit = edit
        
        
        
        self.navigationmodel = QSqlQueryModel()
        
        self.detailsModel = QSqlQueryModel()
        
        
        self.navproxymodel = QSortFilterProxyModel()
        self.navproxymodel.setSourceModel(self.navigationmodel)
        
        self.detailsproxymodel = QSortFilterProxyModel()
        self.detailsproxymodel.setSourceModel(self.detailsModel)
        
        
        self.tabledetails.setModel(self.detailsproxymodel)
        self.tablenavigation.setModel(self.navproxymodel)
        
        self.editmodel=None
        
        QTimer.singleShot(0, self.loadModels)
        
        
    def updateModels(self):
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning(u"Existen problemas de conexión con la base de datos")
            query = u"""
            SELECT
                d.iddocumento,
                CONCAT_WS(' ',tdc.descripcion, d.ndocimpreso) as 'Documento Referencia',
                kx.ndocimpreso as 'Numero Kardex',
                b.nombrebodega as 'Bodega',
                d.fechacreacion as 'Fecha',
                kx.observacion as 'Observacion Kardex',
                d.observacion as 'Observacion Doc',
                d.idbodega
            FROM documentos d
            JOIN tiposdoc tdc ON tdc.idtipodoc = d.idtipodoc
            JOIN bodegas b ON b.idbodega = d.idbodega
            JOIN docpadrehijos dpd ON dpd.idpadre = d.iddocumento
            JOIN documentos kx ON kx.iddocumento = dpd.idhijo AND kx.idtipodoc = 27
            WHERE d.idtipodoc IN (%s)
            GROUP BY d.iddocumento
            """ % self.tiposdoc
            self.navigationmodel.setQuery(query )

            
            self.detailsModel.setQuery(u"""
            SELECT 
                axd.idarticulo, 
                ad.descripcion as 'Articulo', 
                axd.unidades as 'Unidades',
                IF(akx.unidades > 0, CONCAT('+',akx.unidades), IFNULL(akx.unidades,0)) as 'Ajuste', 
                axd.iddocumento
            FROM articulosxdocumento axd
            JOIN vw_articulosdescritos ad ON ad.idarticulo = axd.idarticulo
            JOIN documentos d ON axd.iddocumento = d.iddocumento AND d.idtipodoc IN (%s)
            JOIN docpadrehijos dph ON axd.iddocumento = dph.idpadre
            LEFT JOIN articulosxdocumento akx ON akx.iddocumento = dph.idhijo
            GROUP BY dph.idpadre, axd.idarticulo
            """ % self.tiposdoc)
            
            self.mapper.setModel( self.navproxymodel )
            self.mapper.addMapping(self.txtParentPrintedDocumentNumber, NDOCIMPRESO)
            self.mapper.addMapping(self.txtPrintedDocumentNumber, NKARDEX)
            self.mapper.addMapping(self.dtPicker, FECHA)
            self.mapper.addMapping(self.txtWarehouse, NOMBREBODEGA)
            self.mapper.addMapping(self.txtKardexObservation, OBSERVACIONK, "plainText")
            self.mapper.addMapping(self.txtDocObservation, OBSERVACION, "plainText")
            
            
            self.tabledetails.horizontalHeader().setStretchLastSection(True)
        except UserWarning as inst:
            QMessageBox.critical(self, "Llantera Esquipulas", str(inst))
        except Exception as inst:
            print inst
    def updateDetailFilter( self, index ):
        self.detailsproxymodel.setFilterKeyColumn( IDDOCUMENTOT )
        self.detailsproxymodel.setFilterRegExp( self.navigationmodel.record( index ).value( "iddocumento" ).toString() )
        self.tablenavigation.selectRow( self.mapper.currentIndex() )

    @pyqtSlot("int")
    def on_ckTransit_stateChanged(self, state):
        if state == Qt.Checked:
            self.stateproxymodel.setFilterRegExp("")
            
    @pyqtSlot()
    def on_actionCancel_activated(self):
        self.editmodel = None
        self.tabledetails.setModel(self.detailsproxymodel)
        self.status = True    
        
    @pyqtSlot()
    def on_txtKardexObservation_textChanged(self):
        if not self.editmodel is None:
            self.editmodel.observations = self.txtKardexObservation.toPlainText()  
         
    def setControls(self, status):
        self.tabnavigation.setEnabled(status)
        
        self.actionGoFirst.setVisible(status)
        self.actionGoPrevious.setVisible(status)
        self.actionGoNext.setVisible(status)
        self.actionGoLast.setVisible(status)
        
        self.actionNew.setVisible(status)
        self.actionPreview.setVisible(status)
        
        self.dtPicker.setReadOnly(status)
        
        self.actionCancel.setVisible(not status)
        self.actionSave.setVisible(not status)
        
        self.tablenavigation.setColumnHidden(IDDOCUMENTO, True)
        self.tablenavigation.setColumnHidden(OBSERVACION, True)
        self.tablenavigation.setColumnHidden(OBSERVACIONK, True)
        self.tablenavigation.setColumnHidden(BODEGA, True)
        
        self.tabledetails.setColumnHidden(AJUSTE, not self.edit)
        
        self.tabledetails.setColumnHidden(IDDOCUMENTOT, True)
        
        self.tabledetails.setEditTriggers(QAbstractItemView.AllEditTriggers if not status else QAbstractItemView.NoEditTriggers)
        self.txtKardexObservation.setReadOnly( status)
        
        self.tabledetails.horizontalHeader().setStretchLastSection(True)
        
        
        
    @pyqtSlot(  )
    def on_actionNew_activated( self ):
        """
        Slot documentation goes here.
        """
        query = QSqlQuery()
        try:
            if not QSqlDatabase.database().open():
                raise Exception( u"No se pudo establecer una conexión con la base de datos" )
    
            dlgdoc = dlgSelectDoc(self.tiposdoc)
            if dlgdoc.exec_() == QDialog.Accepted:
                self.editmodel = KardexModel()
                self.editmodel.parentId = dlgdoc.filtermodel.index( dlgdoc.tblBills.selectionModel().currentIndex().row(), 0 ).data().toInt()[0]
                self.editmodel.uid = self.user.uid
                self.editmodel.parentPrinted = dlgdoc.filtermodel.index( dlgdoc.tblBills.selectionModel().currentIndex().row(), 1 ).data().toString()
                self.editmodel.warehouseId = dlgdoc.filtermodel.index(dlgdoc.tblBills.selectionModel().currentIndex().row(), 4).data().toInt()[0]
                self.editmodel.warehouseName = dlgdoc.filtermodel.index(dlgdoc.tblBills.selectionModel().currentIndex().row(), 2).data().toString()
                
                self.txtDocObservation.setPlainText(dlgdoc.filtermodel.index(dlgdoc.tblBills.selectionModel().currentIndex().row(), 5).data().toString())
                self.txtParentPrintedDocumentNumber.setText(self.editmodel.parentPrinted)
                self.txtWarehouse.setText(self.editmodel.warehouseName)
                
                if not query.prepare("""
                SELECT
                    axd.idarticulo,
                    vw.descripcion,
                    axd.unidades,
                    cxa.valor
                FROM articulosxdocumento axd
                JOIN costosarticulo cxa ON cxa.idarticulo = axd.idarticulo AND cxa.activo = 1
                JOIN vw_articulosdescritos vw ON vw.idarticulo = axd.idarticulo
                WHERE axd.iddocumento = %d
                """ % self.editmodel.parentId):
                    raise Exception("No se pudo preparar la consulta para obtener las lineas del documento")
                
                if not query.exec_():
                    raise Exception("No se pudo ejecutar la consulta para obtener las lineas del documento")
                
                if not query.size()>0:
                    raise Exception("La consulta para las lineas del documento no devolvio nada")
                while query.next():
                    linea = LineaKardex()
                    linea.itemId = query.value(0).toInt()[0]
                    linea.itemDescription = query.value(1).toString()
                    linea.numdoc = query.value(2).toInt()[0]
                    linea.itemCost = Decimal(query.value(3).toString())
                    row = self.editmodel.rowCount()
                    self.editmodel.insertRows(row)
                    self.editmodel.lines[row]=linea

#               Cargar el numero de kardex 
                query = QSqlQuery( """
                SELECT
                      MAX(CAST(ndocimpreso AS SIGNED))+1
                FROM documentos d
                WHERE idtipodoc=%d
                """ % constantes.IDKARDEX )
    
                query.exec_()
                query.first()
    
                n = query.value( 0 ).toString()
                if n == "0" or n=="" :
                    n = "1"
    
                self.txtPrintedDocumentNumber.setText( n )
                self.editmodel.printedDocumentNumber = n
                
                
                self.status = False 
                self.tabnavigation.setEnabled( False )
                self.tabWidget.setCurrentIndex( 0 )
                self.tabledetails.setModel( self.editmodel )

                delegate = KardexDelegate()
                self.tabledetails.setItemDelegate( delegate )

                self.tabledetails.resizeColumnsToContents()
                self.tabledetails.horizontalHeader().setStretchLastSection  (True)
#                self.dtPicker.emit( SIGNAL( "dateTimeChanged( QDateTime )" ), QDateTime.currentDateTime() )
                self.dtPicker.setDateTime( QDateTime.currentDateTime() )
                self.connect( self.editmodel, SIGNAL( "dataChanged(QModelIndex,QModelIndex)" ), self.updateLabels )
                
        except Exception as inst:
            QMessageBox.critical(self, "Llantera Esquipulas", "No se pudo iniciar el documento kardex")
            print inst
            self.on_actionCancel_activated()
        finally:
            if self.database.isOpen():
                self.database.close()
            
        
        
    def updateLabels(self):
        pass
        
class dlgSelectDoc( QDialog ):
    def __init__( self, tiposdoc, parent = None ):
        super( dlgSelectDoc, self ).__init__( parent )
        self.setupUi()
        
        self.model = QSqlQueryModel()
        query = u"""
        SELECT 
            d.iddocumento, 
            CONCAT_WS(' ', tdc.descripcion, d.ndocimpreso) as 'Documento',
            b.nombrebodega as 'Bodega',        
            d.fechacreacion as 'Fecha',
            b.idbodega,
            d.observacion
        FROM documentos d
        JOIN tiposdoc tdc ON tdc.idtipodoc = d.idtipodoc
        JOIN bodegas b ON b.idbodega = d.idbodega
        LEFT JOIN docpadrehijos dpd ON dpd.idpadre = d.iddocumento
        LEFT JOIN documentos h ON h.iddocumento = dpd.idhijo AND h.idtipodoc = %d
        WHERE d.idtipodoc IN (%s) 
        GROUP BY d.iddocumento
        HAVING SUM(h.idtipodoc) IS NULL
        """ % ( constantes.IDKARDEX , tiposdoc)
        print query
        self.model.setQuery( query)




        self.setWindowTitle( "Seleccione el documento para bodega" )
        self.filtermodel = QSortFilterProxyModel()
        self.filtermodel.setSourceModel( self.model )
        self.filtermodel.setFilterCaseSensitivity( Qt.CaseInsensitive )
        self.filtermodel.setFilterKeyColumn( -1 )

        self.tblBills.setModel( self.filtermodel )
        
        self.tblBills.horizontalHeader().setStretchLastSection(True)
        
        iddoc, ndocimpreso, bodega, fecha, idbodega, observacion = range(6)
        self.tblBills.setColumnHidden( iddoc, True )
        self.tblBills.setColumnHidden( idbodega, True )
        self.tblBills.setColumnHidden(observacion, True)
        self.tblBills.resizeColumnsToContents()
        
        self.connect( self.buttonbox, SIGNAL( "accepted()" ), self, SLOT( "accept()" ) )
        self.connect( self.buttonbox, SIGNAL( "rejected()" ), self, SLOT( "reject()" ) )
        self.connect( self.txtSearch, SIGNAL( "textChanged(QString)" ), self.updateFilter )

    def setupUi(self):
        
        self.tblBills = QTableView()
        self.tblBills.setSelectionMode( QAbstractItemView.SingleSelection )
        self.tblBills.setSelectionBehavior( QAbstractItemView.SelectRows )
        self.tblBills.selectRow( 0 )
        


        
        self.buttonbox = QDialogButtonBox( QDialogButtonBox.Ok | QDialogButtonBox.Cancel )

        self.txtSearch = QLineEdit()
        formlayout = QFormLayout()

        formlayout.addRow( "&Buscar", self.txtSearch )

        layout = QVBoxLayout()

        layout.addWidget( self.tblBills )
        layout.addLayout( formlayout )
        layout.addWidget( self.buttonbox )
        self.setLayout( layout )

        self.setMinimumWidth( 450 )
        
    def updateFilter( self, str ):
        self.filtermodel.setFilterWildcard( str )
        
