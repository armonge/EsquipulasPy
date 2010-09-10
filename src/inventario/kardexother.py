# -*- coding: utf-8 -*-
'''
Created on 23/07/2010

@author: Andrés Reyes Monge
'''
import logging

from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QMessageBox, QAbstractItemView, qApp
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt4.QtCore import QTimer,pyqtSlot, QDateTime

from ui.Ui_kardexother import Ui_frmKardexOther

from document.kardexother.kardexothermodel import KardexOtherModel
from document.kardexother.kardexotherdelegate import KardexOtherDelegate
from utility.base import Base
from utility import constantes

IDARTICULO, DESCRIPCION, CANTIDAD = range(3)
class frmKardexOther(QMainWindow, Ui_frmKardexOther, Base):
    '''
    classdocs
    '''

    def __init__(self,  parent=None):
        '''
        Constructor
        '''
        super( frmKardexOther, self ).__init__( parent )
        self.setupUi( self )
        self.parentWindow = parent
        Base.__init__( self )
        
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
        
    def setControls(self,status):
        self.actionPrint.setVisible(status)
        self.actionGoFirst.setVisible(status)
        self.actionGoPrevious.setVisible(status)
        self.actionGoNext.setVisible(status)
        self.actionGoLast.setVisible(status)
        
        self.actionNew.setVisible(status)
        self.actionPreview.setVisible(status)
        
        self.actionCancel.setVisible(not status)
        self.actionSave.setVisible(not status)
        
        self.swConcept.setCurrentIndex(0 if status else 1)
        self.tabnavigation.setEnabled(status)

        self.tabledetails.setEditTriggers(QAbstractItemView.NoEditTriggers if status else QAbstractItemView.AllEditTriggers)
        if not status:
            self.tabWidget.setCurrentIndex(0)

            self.tabledetails.setColumnHidden(IDARTICULO, True)

            self.tabledetails.setColumnWidth(DESCRIPCION, 250)

            self.tabledetails.addAction(self.actionDeleteRow)
    def deleteRow(self):
        """
        Funcion usada para borrar lineas de la tabla
        """
        index = self.tabledetails.currentIndex()

        if not index.isValid():
            return
        row = index.row()

        self.editmodel.removeRows( row, 1 )

    def updateModels(self):
        try:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open:
                    raise UserWarning("No se pudo conectar con la base datos")
            
            query = """
            SELECT 
                d.iddocumento, 
                d.ndocimpreso, 
                d.fechacreacion, 
                d.observacion,
                b.nombrebodega, 
                d.total,
                d.idestado
            FROM documentos d 
            JOIN bodegas b ON b.idbodega = d.idbodega
            LEFT JOIN docpadrehijos dph ON dph.idhijo = d.iddocumento
            WHERE d.idtipodoc = %d AND dph.idhijo IS NULL
            """ % constantes.IDKARDEX
            self.navigationmodel.setQuery(query)
            
            query = """
            SELECT * 
            FROM articulosxdocumento axd
            JOIN documentos d ON d.iddocumento = axd.iddocumento AND d.idtipodoc = %d
            LEFT JOIN docpadrehijos dph ON dph.idhijo = d.iddocumento
            WHERE dph.idhijo IS NULL
            """ % constantes.IDKARDEX
            self.detailsModel.setQuery(query)
            
            
        except UserWarning as inst:
            QMessageBox.critical(self, qApp.organizationName(), unicode(inst))
            logging.error(unicode(inst))
        except Exception as inst:
            QMessageBox.critical(self, qApp.organizationName(), u"No se pudo iniciar un nuevo ajuste de kardex")
            logging.critical(unicode( inst))
    def newDocument(self):
        try:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open:
                    raise UserWarning("No se pudo conectar con la base de datos")
            
            self.editmodel = KardexOtherModel()
            
            
            conceptosmodel = QSqlQueryModel()
            conceptosmodel.setQuery("""
            SELECT
            	c.idconcepto,
            	c.descripcion
            FROM conceptos c
            WHERE c.idtipodoc = %d
            """ % constantes.IDKARDEX)

            if conceptosmodel.rowCount() == 0:
                raise UserWarning(u"No existen conceptos para los ajustes de bodega")
            
            self.cbConcept.setModel(conceptosmodel)
            self.cbConcept.setModelColumn(1)


            #Calcular el numero de kardex
            query = QSqlQuery( """
            CALL spConsecutivo(%d,NULL);
            """ % constantes.IDKARDEX )
            if not query.exec_():
                raise UserWarning( "No se pudo calcular el numero del kardex" )
            
            query.first()
            self.editmodel.printedDocumentNumber = query.value( 0 ).toString()
            self.txtPrintedDocumentNumber.setText(self.editmodel.printedDocumentNumber)

            
            self.dtPicker.setDateTime(QDateTime.currentDateTime())
            articlesmodel = QSqlQueryModel()
            articlesmodel.setQuery("""
            SELECT
                a.idarticulo,
                a.descripcion,
                ca.idcostoarticulo,
                ca.valor
            FROM vw_articulosdescritos a
            JOIN costosarticulo ca ON a.idarticulo = ca.idarticulo AND ca.activo = 1
            """)
            
            delegate = KardexOtherDelegate(articlesmodel)
            self.tabledetails.setItemDelegate(delegate)
            self.tabledetails.setModel(self.editmodel)

            self.addLine()
            self.status = False
        except UserWarning as inst:
            QMessageBox.critical(self,qApp.organizationName(), unicode(inst))
            self.status = True
        except Exception as inst:
            QMessageBox.critical(self,qApp.organizationName(), "El sistema no pudo iniciar una nueva entrada de kardex")
            self.status = True
            print inst
        
        
    def cancel( self ):
        u"""
        Borrar todos los modelos que se hallan creado para el modo edición, asignar los modelos de navegación a las 
        vistas
        """
        self.editmodel = None
        self.tabledetails.setModel(self.detailsproxymodel)
        self.status = True    