# -*- coding: utf-8 -*-
'''
Created on 23/07/2010

@author: armonge
'''
from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QMessageBox
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase
from PyQt4.QtCore import QTimer,pyqtSlot, QDateTime
from utility.base import Base
from ui.Ui_kardexother import Ui_frmKardexOther

import utility.constantes
class frmKardexOther(QMainWindow, Ui_frmKardexOther, Base):
    '''
    classdocs
    '''


    def __init__(self, user, parent=None):
        '''
        Constructor
        '''
        super( frmKardexOther, self ).__init__( parent )
        self.setupUi( self )
        self.parentWindow = parent
        Base.__init__( self )
        self.user = user
        
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
        self.actionGoFirst.setVisible(status)
        self.actionGoPrevious.setVisible(status)
        self.actionGoNext.setVisible(status)
        self.actionGoLast.setVisible(status)
        
        self.actionNew.setVisible(status)
        self.actionPreview.setVisible(status)
        
        self.actionCancel.setVisible(not status)
        self.actionSave.setVisible(not status)
        
        self.swConcept.setCurrentIndex(0 if status else 1)
        if not status:
            self.tabWidget.setCurrentIndex(0)
        
    def updateModels(self):
        try:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open:
                    raise UserWarning("No se pudo conectar con la base datos")
            self.navigationmodel.setQuery("""
            SELECT 
                d.iddocumento, 
                d.ndocimpreso, 
                d.fechacreacion, 
                d.observacion,
                b.nombrebodega, 
                d.total
            FROM documentos d 
            JOIN bodegas b ON b.idbodega = d.idbodega
            LEFT JOIN docpadrehijos dph ON dph.idhijo = d.iddocumento
            WHERE d.idtipodoc = %d AND dph.idhijo IS NULL
            """ % utility.constantes.IDKARDEX)
        except UserWarning as inst:
            QMessageBox.critical(self, "Llantera Esquipulas", str(inst))
        except Exception as inst:
            print inst
    @pyqtSlot()
    def on_actionNew_activated(self):
        try:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open:
                    raise UserWarning("No se pudo conectar con la base de datos")

            conceptosmodel = QSqlQueryModel()
            conceptosmodel.setQuery("""
            SELECT
            	c.idconcepto,
            	c.descripcion
            FROM conceptos c
            WHERE c.modulo = %d
            """ % utility.constantes.IDINVENTARIO)

            self.cbConcept.setModel(conceptosmodel)
            self.cbConcept.setModelColumn(1)

            self.dtPicker.setDateTime(QDateTime.currentDateTime())

            self.status = False
        except UserWarning as inst:
            QMessageBox.critical(self,"Llantera Esquipulas", str(inst))
            self.status = True
        except Exception as inst:
            self.status = True
            print inst
        
        
