# -*- coding: utf-8 -*-
from PyQt4.QtCore import pyqtSlot, Qt, QDate
from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QMessageBox, qApp
from PyQt4.QtSql import QSqlQueryModel, QSqlQuery, QSqlDatabase
from ui.Ui_cierre import Ui_frmCierreContable
from utility import constantes
import logging




IDDOCUMENTO, NDOCUMENTO, TIPODOC, TOTAL, FECHA, OBSERVACIONES, ESTADO = range( 7 )
class FrmCierreContable( Ui_frmCierreContable, QMainWindow ):
    def __init__( self, parent ):
        super( FrmCierreContable, self ).__init__( parent )
        self.setupUi( self )
        self.parentWindow = parent

        self.navmodel = QSqlQueryModel( self )
        self.navproxymodel = QSortFilterProxyModel( self )
        self.navproxymodel.setSourceModel( self.navmodel )

        self.navproxymodel.setFilterKeyColumn( -1 )
        self.navproxymodel.setFilterCaseSensitivity ( Qt.CaseInsensitive )
        self.editmodel = None
        self.fecha = None
        self.status = True

        self.dtPicker.setMaximumDate( QDate.currentDate() )
        self.dtPicker.setDate( QDate.currentDate() )

    @pyqtSlot( "QDateTime" )
    def on_dtPicker_dateTimeChanged( self, datetime ):
        """
        Asignar la fecha al objeto __document
        """
        self.fecha = datetime
        self.updateModels()

    def updateModels( self ):
        try:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open():
                    raise UserWarning( "No se pudo conectar con la base de datos" )
            q = u"""
            SELECT
                iddocumento,
                ndocimpreso as 'No. Documento',
                td.descripcion as TipoDocumento,
                format(total ,4)as Total,
                date_format(fechacreacion,'%s') as Fecha,
                observacion as Observaciones,
                estados.descripcion as Estado
            FROM documentos d
            JOIN estadosdocumento estados ON estados.idestado=d.idestado
            JOIN tiposdoc td ON d.idtipodoc=td.idtipodoc
            WHERE MONTH(d.fechacreacion)= %s  AND d.idtipodoc!=%d and d.idtipodoc!= %d
            """ % ( "%d/%m/%Y", self.fecha.toString( "MM" ), +constantes.IDAPERTURA , constantes.IDCIERREMENSUAL )
            print q
            self.navmodel.setQuery( q )

            query = QSqlQuery()
            q = """
            SELECT
                d2.iddocumento
            FROM documentos d
            JOIN docpadrehijos dp ON d.iddocumento=dp.idpadre
            JOIN documentos d2 ON d2.iddocumento=dp.idhijo
            WHERE d.idtipodoc= %d and month(d2.fechacreacion)= %s
            LIMIT 1
            """ % ( constantes.IDCIERREMENSUAL, self.fecha.toString( "MM" ) )
            print q
            query.prepare( q )

            if not query.exec_():
                print query.executedQuery()
                raise UserWarning( "No se pudo ejecutar la consulta para verificar si existe un cierre contable" )

            if self.navmodel.rowCount() == 0 or query.size() > 0:
                self.toolBar.removeAction( self.actionSave )
            else:
                self.toolBar.addActions( [
                self.actionSave] )
                self.actionSave.triggered.connect( self.save )

            self.tabledetails.setModel( self.navproxymodel )
            self.tabledetails.setColumnHidden( 0, True )
            self.tabledetails.resizeColumnsToContents()
        except UserWarning as inst:
            logging.error( unicode( inst ) )
            QMessageBox.critical( self, qApp.applicationName(), unicode( inst ) )
        except Exception as inst:
            logging.critical( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(), u"Hubo un error al actualizar la tabla" )

#    def setControls( self, status ):
#        """
#        @param status: false = editando        true = navegando
#        """
#        self.actionPrint.setVisible(status)
#        self.actionSave.setVisible(   status )
#        self.actionPreview.setVisible( status)
#        self.actionSave.setVisible(status)
    def save( self ):
        validado = False
        for i in range( self.navproxymodel.rowCount() ):
            if self.navproxymodel.index( i, ESTADO ).data( Qt.EditRole ).toString() != "CONFIRMADO":
                validado = True
        if validado == True:
            QMessageBox.warning( None, "Documentos Pendientes", "Existen documentos que aun no han sido confirmados" )
        else:
            try:
                query = QSqlQuery()
                query.prepare( """CALL `esquipulasdb`.`spCierreMensual`(:IDCIERRE,
                :MES,
                :ESTADO,
                :ANO,
                :INGRESOSXVENTA,
                :OTROSINGRESOS,
                :COSTOSGASTOSOPERACIONES,
                :GASTOSXVENTAS,
                :GASTOS,
                :GASTOSFINANCIEROS,
                :PRODUCTOSFINANCIEROS,
                :OTROSGASTOS)""" )
                query.bindValue( ":IDCIERRE", constantes.IDCIERREMENSUAL )
                query.bindValue( ":MES", self.fecha.toString( "MM" ) )
                query.bindValue( ":ESTADO", constantes.CONFIRMADO )
                query.bindValue( ":ANO", self.fecha.toString( "yyyy" ) )
                query.bindValue( ":INGRESOSXVENTA", constantes.INGRESOSXVENTA )
                query.bindValue( ":OTROSINGRESOS", constantes.OTROSINGRESOS )
                query.bindValue( ":COSTOSGASTOSOPERACIONES", constantes.COSTOSGASTOSOPERACIONES )
                query.bindValue( ":GASTOSXVENTAS", constantes.GASTOSXVENTAS )
                query.bindValue( ":GASTOS", constantes.GASTOS )
                query.bindValue( ":GASTOSFINANCIEROS", constantes.GASTOSFINANCIEROS )
                query.bindValue( ":PRODUCTOSFINANCIEROS", constantes.PRODUCTOSFINANCIEROS )
                query.bindValue( ":OTROSGASTOS", constantes.OTROSGASTOS )

                if not query.exec_():
                    raise UserWarning( "No se pudo Cerrar el mes Contable" )

                QMessageBox.information( None, "Cierre Mensual", "Cierre mensual exitoso" )
                self.toolBar.removeAction( self.actionSave )
                self.toolBar.addActions( self.actionPrint )
                self.actionPrin.triggered.connect( self.printPreview )

            except UserWarning as inst:

                logging.error( inst )
                QMessageBox.critical( self, qApp.organizationName(), unicode( inst ) )
