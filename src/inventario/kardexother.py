# -*- coding: utf-8 -*-
'''
Created on 23/07/2010

@author: Andrés Reyes Monge
'''
import logging
from decimal import Decimal

from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QMessageBox, QAbstractItemView, qApp
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt4.QtCore import QTimer,pyqtSlot, QDateTime

from ui.Ui_kardexother import Ui_frmKardexOther

from document.kardexother import KardexOtherModel, KardexOtherDelegate

from utility.base import Base
from utility import constantes, movimientos
from utility.accountselector import AccountsSelectorDelegate, AccountsSelectorLine

                
IDDOCUMENTO, NDOCIMPRESO, FECHA, OBSERVACIONES,BODEGA, TOTAL, ESTADO, CONCEPT, PENDIENTE=range(9)
IDARTICULO, DESCRIPCION,COSTO, CANTIDAD, IDDOCUMENTOD = range(5)
IDCUENTA, CODIGO, NOMBRECUENTA, MONTOCUENTA, IDDOCUMENTOC = range(5) 

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
        
        self.navmodel = QSqlQueryModel()
        
        self.detailsModel = QSqlQueryModel()
        
        
        self.navproxymodel = QSortFilterProxyModel()
        self.navproxymodel.setSourceModel(self.navmodel)
        
        self.detailsproxymodel = QSortFilterProxyModel()
        self.detailsproxymodel.setSourceModel(self.detailsModel)

        self.accountsnavmodel = QSqlQueryModel()
        self.accountsproxymodel = QSortFilterProxyModel()
        self.accountsproxymodel.setSourceModel(self.accountsnavmodel)
        

        
        self.editmodel=None

        if not self.user.hasRole("contabilidad"):
            self.tableaccounts.setVisible(False)
            self.lblaccounts.setVisible(False)

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
        self.swWarehouse.setCurrentIndex(0 if status else 1)
        self.tabnavigation.setEnabled(status)

        self.txtObservations.setReadOnly(status)

        self.tabledetails.setEditTriggers(QAbstractItemView.NoEditTriggers if status else QAbstractItemView.AllEditTriggers)
        
        
        if not status:
            self.tabWidget.setCurrentIndex(0)
            self.tabledetails.addAction(self.actionDeleteRow)
        else:
            self.tabledetails.removeAction(self.actionDeleteRow)

            self.tabledetails.setModel(self.detailsproxymodel)
            self.tablenavigation.setModel(self.navproxymodel)
            self.tableaccounts.setModel(self.accountsproxymodel)


        self.tabledetails.setColumnHidden(IDARTICULO, True)
        self.tabledetails.setColumnHidden(IDDOCUMENTOD, True)

        self.tableaccounts.setColumnHidden(IDDOCUMENTOC, True)
        self.tableaccounts.setColumnHidden(IDCUENTA, True)

        if not self.user.hasRole("contabilidad"):
            self.actionNew.setVisible(False)

        self.tabledetails.setColumnWidth(DESCRIPCION, 300)

        self.tablenavigation.setColumnHidden(IDDOCUMENTO, True)
        self.tablenavigation.setColumnHidden(ESTADO, True)
        self.tablenavigation.setColumnHidden(OBSERVACIONES, True)
        
        
    def addActionsToToolBar(self):
        if self.user.hasRole("contabilidad"):
            self.toolBar.addActions([
                self.actionNew,
                self.actionPreview,
                self.actionPrint,
                self.actionSave,
                self.actionCancel
            ])
        else:
            self.toolBar.addActions([
                self.actionPreview,
                self.actionPrint,
            ])
        self.toolBar.addSeparator()
        self.toolBar.addActions([
            self.actionGoFirst,
            self.actionGoPrevious,
            self.actionGoLast,
            self.actionGoNext,
            self.actionGoLast
        ])
        if self.user.hasRole("kardex"): #si el usuario no es de kardex no deberia de poder dar entrada a bodega
            self.actionGiveEntry = self.createAction(text="Dar entrada al documento", icon=":/icons/res/dialog-ok-apply.png", slot=self.giveEntry)
            self.toolBar.addActions([
                self.actionGiveEntry
            ])
    def giveEntry(self):
        """
        Dar entrada a un kardex
        """
        if QMessageBox.question(self, qApp.organizationName(), u"¿Realmente desea dar entrada a este documento?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            iddoc = self.navmodel.record( self.mapper.currentIndex() ).value( IDDOCUMENTO ).toInt()[0]


            query = QSqlQuery()
            try:
                if not self.database.isOpen():
                    if not self.database.open():
                        raise UserWarning(u"No se pudo conectar con la base de datos")

                if not self.database.transaction():
                    raise Exception(u"No se pudo iniciar la transacción para confirmar el kardex")

                q = """
                UPDATE documentos d SET idestado = %d  WHERE d.iddocumento = %d LIMIT 1
                """ % (constantes.CONFIRMADO, iddoc)
                if not query.exec_(q):
                    raise Exception(u"No se pudo actualizar el estado del documento")

                if not query.exec_("""
                    INSERT INTO documentos (ndocimpreso, fechacreacion, idtipodoc, total, idtipocambio, idbodega)
                    SELECT fnConsecutivo(%d,NULL), NOW(), %d, total, idtipocambio, idbodega FROM documentos
                    WHERE iddocumento = %d;
                """ % (constantes.IDKARDEX, constantes.IDKARDEX, iddoc)):
                    raise Exception(u"No se pudo insertar el documento kardex")

                insertedId = query.lastInsertId().toInt()[0]
                
                if not query.exec_("""
                    INSERT INTO docpadrehijos (idpadre, idhijo) VALUES (%d, %d)
                """ % (iddoc, insertedId)):
                    raise Exception(u"No se pudo crear la relación entre el documento ajuste de bodega y su kardex")

                if not self.database.commit():
                    raise Exception(u"No se pudo hacer commit")
                QMessageBox.information(self, qApp.organizationName(),"El documento se ha guardado con exito")
                self.updateModels()
            except UserWarning as inst:
                logging.error(unicode(inst))
                self.database.rollback()
                QMessageBox.critical(self, qApp.organizationName(), unicode(inst))
            except Exception as inst:
                logging.critical(unicode(inst))
                self.database.rollback()
                QMessageBox.critical(self, qApp.organizationName(), u"No se pudo confirmar la entrada de este documento")

                
                

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
                d.ndocimpreso AS 'Ndoc',
                d.fechacreacion,
                d.observacion,
                b.nombrebodega AS 'Bodega',
                d.total AS 'Total',
                d.idestado,
                c.descripcion AS 'Concepto',
                IF( dph.idhijo IS NULL, 1, 0) AS 'Pendiente'
            FROM documentos d
            JOIN bodegas b ON b.idbodega = d.idbodega
            JOIN conceptos c ON c.idconcepto = d.idconcepto
            LEFT JOIN docpadrehijos dph ON dph.idpadre = d.iddocumento
            LEFT JOIN documentos kardex ON dph.idhijo = kardex.iddocumento AND kardex.idtipodoc = %d
            WHERE d.idtipodoc = %d
            """ % ( constantes.IDKARDEX, constantes.IDAJUSTEBODEGA)
            self.navmodel.setQuery(query)
            query = """
            SELECT
                a.idarticulo,
                a.descripcion,
                axd.costounit,
                axd.unidades,
                axd.iddocumento
            FROM vw_articulosdescritos a
            JOIN articulosxdocumento axd ON axd.idarticulo = a.idarticulo
            JOIN documentos d ON d.iddocumento = axd.iddocumento AND d.idtipodoc = %d
            LEFT JOIN docpadrehijos dph ON dph.idhijo = d.iddocumento
            WHERE dph.idhijo IS NULL
            """ % constantes.IDAJUSTEBODEGA
            self.detailsModel.setQuery(query)


            if self.user.hasAnyRole(["inventario", "contabilidad"]):
                query = """
                SELECT
                    cc.idcuenta,
                    cc.codigo,
                    cc.descripcion,
                    cxd.monto,
                    cxd.iddocumento
                FROM cuentasxdocumento cxd
                JOIN documentos d ON d.iddocumento = cxd.iddocumento AND d.idtipodoc = %d
                JOIN cuentascontables cc ON cxd.idcuenta = cc.idcuenta
                """ % constantes.IDAJUSTEBODEGA
                self.accountsnavmodel.setQuery(query)
            
            self.mapper.setModel( self.navproxymodel )
            self.mapper.addMapping( self.txtPrintedDocumentNumber, NDOCIMPRESO )
            self.mapper.addMapping( self.txtConcept, CONCEPT )
            self.mapper.addMapping( self.txtWarehouse, BODEGA )
            self.mapper.addMapping( self.txtObservations, OBSERVACIONES )
            self.mapper.addMapping(self.dtPicker, FECHA )


            
        except UserWarning as inst:
            QMessageBox.critical(self, qApp.organizationName(), unicode(inst))
            logging.error(unicode(inst))
        except Exception as inst:
            QMessageBox.critical(self, qApp.organizationName(), u"No se pudo iniciar un nuevo ajuste de kardex")
            logging.critical(unicode( inst))


    def updateDetailFilter(self, index):
        self.detailsproxymodel.setFilterKeyColumn( IDDOCUMENTOD )
        self.detailsproxymodel.setFilterRegExp( "^%d$"%self.navmodel.record( index ).value( IDDOCUMENTO ).toInt()[0] )

        self.accountsproxymodel.setFilterKeyColumn( IDDOCUMENTOC )
        self.accountsproxymodel.setFilterRegExp( "^%d$"%self.navmodel.record( index ).value( IDDOCUMENTO ).toInt()[0] )

        if self.user.hasRole('kardex'):
            estado = self.navmodel.record( index ).value( PENDIENTE ).toInt()[0]
            self.actionGiveEntry.setVisible( estado == 1 )

    def newDocument(self):
        try:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open:
                    raise UserWarning("No se pudo conectar con la base de datos")
            
            self.editmodel = KardexOtherModel()

            self.editmodel.uid = self.user.uid
            
            conceptosmodel = QSqlQueryModel()
            conceptosmodel.setQuery("""
            SELECT
            	c.idconcepto,
            	c.descripcion
            FROM conceptos c
            WHERE c.idtipodoc = %d
            """ % constantes.IDAJUSTEBODEGA)

            if conceptosmodel.rowCount() == 0:
                raise UserWarning(u"No existen conceptos para los ajustes de bodega")
            
            self.cbConcept.setModel(conceptosmodel)
            self.cbConcept.setModelColumn(1)

            warehouseModel = QSqlQueryModel()
            warehouseModel.setQuery("""
            SELECT idbodega, nombrebodega
            FROM bodegas b
            ORDER BY idbodega
            """)

            self.cbWarehouse.setModel(warehouseModel)
            self.cbWarehouse.setModelColumn(1)

            #Calcular el numero de kardex
            query = QSqlQuery( """
            CALL spConsecutivo(%d,NULL);
            """ % constantes.IDAJUSTEBODEGA )
            if not query.exec_():
                raise UserWarning( "No se pudo calcular el numero del kardex" )
            
            query.first()
            self.editmodel.printedDocumentNumber = query.value( 0 ).toString()
            self.txtPrintedDocumentNumber.setText(self.editmodel.printedDocumentNumber)

            
            
            
            articlesmodel = QSqlQueryModel()
            articlesmodel.setQuery("""
            SELECT
                a.idarticulo,
                a.descripcion,
                ca.valor as costo
            FROM vw_articulosdescritos a
            JOIN costosarticulo ca ON a.idarticulo = ca.idarticulo AND ca.activo = 1
            """)
            
            delegate = KardexOtherDelegate(articlesmodel)
            self.tabledetails.setItemDelegate(delegate)
            self.tabledetails.setModel(self.editmodel)

            accountsdelegate = AccountsSelectorDelegate(QSqlQuery( """
             SELECT c.idcuenta, c.codigo, c.descripcion
             FROM cuentascontables c
             JOIN cuentascontables p ON c.padre = p.idcuenta AND p.padre != 1
             WHERE c.padre != 1 AND c.idcuenta != 22
             """ ),True )
            self.tableaccounts.setItemDelegate( accountsdelegate )

            self.tableaccounts.setModel(self.editmodel.accountsmodel)

            self.editmodel.accountsmodel.insertRows( 0,2 )

            line = AccountsSelectorLine()
            line.itemId = int(movimientos.INVENTARIO)
            line.code = "110 003 001 000 000"
            line.name = "INV Inventario de Bodega"

            self.editmodel.accountsmodel.lines[0] = line
            
            self.addLine()
            self.dtPicker.setDateTime(QDateTime.currentDateTime())
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

    @pyqtSlot( "int" )
    def on_cbWarehouse_currentIndexChanged( self, index ):
        if not self.editmodel is None:
            self.editmodel.warehouseId = self.cbWarehouse.model().index( index, 0 ).data().toInt()[0]
            
    @pyqtSlot( "int" )
    def on_cbConcept_currentIndexChanged( self, index ):
        if not self.editmodel is None:
            self.editmodel.conceptId= self.cbConcept.model().index( index, 0 ).data().toInt()[0]