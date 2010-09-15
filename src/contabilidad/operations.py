# -*- coding: utf-8 -*-
'''
Created on 01/07/2010

@author: Andrés Reyes Monge
'''
import logging

from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QTableView, QItemSelectionModel, \
QItemSelection, QDataWidgetMapper, QMessageBox, qApp
from PyQt4.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt4.QtCore import pyqtSlot, QDateTime, QTimer, QModelIndex, Qt

from ui.Ui_operations import Ui_frmOperations
from utility.accountselector import AccountsSelectorModel, AccountsSelectorDelegate
from utility import constantes
from utility import user

IDDOCUMENTO, NDOCIMPRESO, FECHACREACION, CONCEPTO = range( 4 )

IDCUENTA, CODIGO, DESCRIPCION, MONTO, IDDOCUMENTOC = range( 5 )
class frmOperations( QMainWindow, Ui_frmOperations ):
    def __init__( self,  parent = None ):
        super( frmOperations, self ).__init__( parent )
        self.setupUi( self )
        self.__status = False
        self.database = QSqlDatabase.database()

        self.navmodel = QSqlQueryModel()
        self.navproxymodel = QSortFilterProxyModel()
        self.navproxymodel.setFilterKeyColumn( -1 )
        self.navproxymodel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.navproxymodel.setSourceModel( self.navmodel )

        self.detailsmodel = QSqlQueryModel()
        self.detailsproxymodel = QSortFilterProxyModel()
        self.detailsproxymodel.setSourceModel( self.detailsmodel )

        self.navproxymodel.setDynamicSortFilter( True )
        self.detailsproxymodel.setDynamicSortFilter( True )

        self.mapper = QDataWidgetMapper( self )
        self.mapper.setModel( self.navproxymodel )

        self.user = user.LoggedUser

        self.editModel = None


        self.tableNavigation.setModel( self.navproxymodel )
        self.tableDetails.setModel( self.detailsproxymodel )

        self.tableDetails.setColumnHidden( IDCUENTA, True )
        self.tableDetails.setColumnHidden( IDDOCUMENTOC, True )


        self.buttonBox.accepted.connect( self.save )
        self.tableNavigation.selectionModel().selectionChanged[QItemSelection, QItemSelection].connect(self.updateDetails)

        QTimer.singleShot( 0, self.updateModels )

    def updateModels( self ):
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( "No se pudo conectar con la base de datos" )
            self.navmodel.setQuery( """
            SELECT 
                d.iddocumento, 
                d.ndocimpreso as 'N Doc', 
                d.fechacreacion as 'Fecha', 
                c.descripcion as 'Concepto'
            FROM documentos d
            JOIN conceptos c ON c.idconcepto = d.idconcepto
            WHERE d.idtipodoc = %d
            ORDER BY d.iddocumento DESC
            """ % constantes.IDAJUSTECONTABLE )
            self.detailsmodel.setQuery( """
            SELECT 
                cxd.idcuenta,  
                cc.codigo as 'Codigo Cuenta', 
                cc.descripcion as 'Nombre Cuenta',
                CONCAT('C$',FORMAT(cxd.monto,4)) as Monto,
                cxd.iddocumento  
            FROM cuentasxdocumento cxd 
            JOIN cuentascontables cc ON cxd.idcuenta = cc.idcuenta
            JOIN documentos d ON d.iddocumento = cxd.iddocumento 
            WHERE d.idtipodoc = %d
            ORDER BY nlinea 
            """ % constantes.IDAJUSTECONTABLE )

            self.mapper.addMapping( self.dtPicker, FECHACREACION )
            self.mapper.addMapping( self.txtConcept, CONCEPTO )
            self.tableNavigation.selectionModel().setCurrentIndex( self.navproxymodel.index( 0, 0 ), QItemSelectionModel.Select )

            self.tableNavigation.setColumnHidden( IDDOCUMENTO, True )
            self.tableDetails.setColumnHidden( IDDOCUMENTOC, True )
            self.tableDetails.setColumnHidden( IDCUENTA, True )


            self.tableDetails.setColumnWidth( CODIGO, 240 )
            self.tableDetails.setColumnWidth( DESCRIPCION, 250 )

            self.tableNavigation.setColumnWidth( FECHACREACION, 200 )
            self.tableNavigation.setColumnWidth( CONCEPTO, 250 )
        except UserWarning as inst:
            logging.error(inst)
            QMessageBox.critical(self, qApp.organizationName(), unicode(inst))
        except Exception as inst:
            logging.critical(inst)

    def updateDetails( self, selected, deselected ):
        if len( selected.indexes() ) > 0:
            self.mapper.setCurrentModelIndex( selected.indexes()[0] )
            self.detailsproxymodel.setFilterKeyColumn( IDDOCUMENTOC )
            self.detailsproxymodel.setFilterRegExp( self.navproxymodel.data( selected.indexes()[0] ).toString() )


    def setStatus( self, status ):
        """
        Cambiar el modo del formulario
        
        true = adding
        false = navigating
        
        @param status: El modo del formulario
        @type status:bool
        """
        self.txtSearch.setEnabled( not status )
        self.cbConcepts.setEnabled( status )
        self.tableDetails.setEditTriggers( QTableView.AllEditTriggers if status else QTableView.NoEditTriggers )
        self.tableNavigation.setEnabled( not status )
        self.tableDetails.setEditTriggers( QTableView.AllEditTriggers )
        self.stackedWidget.setCurrentIndex( 0 if status else 1 )
        self.stConcepts.setCurrentIndex( 1 if status else 0 )

    def getStatus( self ):
        return self.__status
    status = property( getStatus, setStatus )


    @pyqtSlot()
    def on_buttonBox_rejected( self ):
        self.status = False
        self.editModel = None

        self.tableDetails.setModel( self.detailsproxymodel )
        self.tableDetails.setColumnHidden( IDDOCUMENTOC, True )
        self.tableDetails.setColumnHidden( IDCUENTA, True )


    @pyqtSlot()
    def on_btnAdd_clicked( self ):
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( "No se pudo abrir la base de datos" )
                
            self.editModel = AccountsSelectorModel()
            self.editModel.insertRow( 1 )
            
            delegate = AccountsSelectorDelegate( QSqlQuery( """
            SELECT 
                c.idcuenta, 
                c.codigo, 
                c.descripcion 
            FROM cuentascontables c 
            JOIN cuentascontables p ON c.padre = p.idcuenta AND p.padre != 1
            """ ) )
    
            self.dtPicker.setDateTime( QDateTime.currentDateTime() )
            self.dtPicker.setMaximumDateTime(QDateTime.currentDateTime())
            
            self.conceptsmodel = QSqlQueryModel()
            self.conceptsmodel.setQuery( """
            SELECT 
                idconcepto, 
                descripcion 
            FROM conceptos 
            WHERE idtipodoc = %d
             """ % constantes.IDAJUSTECONTABLE )
            
            if self.conceptsmodel.rowCount() < 1:
                raise UserWarning("No existen conceptos")
            
            
            self.cbConcepts.setModel( self.conceptsmodel )
            self.cbConcepts.setModelColumn( 1 )
            self.tableDetails.setModel( self.editModel )
            self.tableDetails.setColumnHidden( IDCUENTA, True )
            self.tableDetails.setColumnHidden( IDDOCUMENTOC, True )
            self.tableDetails.setItemDelegate( delegate )
            
            self.status = True
    
            self.tableDetails.resizeColumnsToContents()
        except UserWarning as inst:
            self.status = False
            QMessageBox.critical(self, qApp.organizationName(), unicode(inst))
            logging.error(unicode(inst))
        except Exception as inst:
            QMessageBox.critical(self, qApp.organizationName(), "Hubo un error al tratar de iniciar un nuevo ajuste")
            logging.critical(unicode(inst))
            self.status = False


    @pyqtSlot( "QString" )
    def on_txtSearch_textChanged( self, text ):
        
        self.navproxymodel.setFilterRegExp( text )



    def save( self ):
        query = QSqlQuery()
    
        try:
            if not self.editModel.valid:
                raise UserWarning( "El documento no es valido, no se puede guardar")

            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( "No se pudo conectar con la base de datos" )

            if not self.database.transaction():
                raise Exception( u"No se pudo comenzar la transacción" )
#               Cargar el numero del asiento actual
            query.prepare( """
            SELECT
                  MAX(CAST(ndocimpreso AS SIGNED))+1
            FROM documentos d
            WHERE idtipodoc=24
            ;
            """ )

            query.exec_()
            query.first()

            n = query.value( 0 ).toString()
            if n == "0" :
                n = "1"

            if not query.prepare( """
            INSERT INTO documentos (ndocimpreso, fechacreacion, idconcepto,   idtipodoc)
            VALUES (:ndocimpreso, :fechacreacion, :idconcepto,  %d)
            """ % constantes.IDAJUSTECONTABLE ):
                raise Exception( "No se pudo preparar la consulta para guardar el documento" )
            query.bindValue( ":ndocimpreso", n )
            query.bindValue( ":fechacreacion", self.dtPicker.dateTime().toString( "yyyyMMddhhmmss" ) )
            query.bindValue( ":idconcepto", self.conceptsmodel.record( self.cbConcepts.currentIndex() ).value( "idconcepto" ).toInt()[0] )

            if not query.exec_():
                raise Exception( "No se pudo ejecutar la consulta para guardar el asiento" )

            insertedId = query.lastInsertId().toInt()[0]

            if not query.prepare( """
            INSERT INTO personasxdocumento (idpersona, iddocumento, idaccion) 
            VALUES (:usuario, :documento, :idaccion)
            """ ):
                raise Exception( "No se pudo preparar la consulta para insertar el usuario" )
            query.bindValue( ":usuario", self.user.uid )
            query.bindValue( ":documento", insertedId )
            query.bindValue( ":idaccion", constantes.ACCCREA)

            if not query.exec_():
                raise Exception( u"No se pudo guardar la relación con el usuario" )

            for lineid, line in enumerate( self.editModel.lines ):
                if line.valid:
                    line.save( insertedId, lineid + 1 )

            if not self.database.commit():
                raise Exception("No se pudo ejecutar la transaccion")
            self.tableDetails.setModel( self.detailsproxymodel )
            self.updateModels()

            self.status = False
        except UserWarning as inst:
            QMessageBox.critical(self, qApp.organizationName(), unicode(inst))
            logging.error(inst)
        except Exception as inst:
            QMessageBox.critical(self, qApp.organizationName(), "Hubo un error al tratar de guardar su ajuste")
            self.database.rollback()
            logging.critical(inst)
            logging.critical(query.lastError().text())
        finally:
            if self.database.isOpen():
                self.database.close()

