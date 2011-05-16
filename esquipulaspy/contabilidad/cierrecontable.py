# -*- coding: utf-8 -*-
from PyQt4.QtCore import pyqtSlot, Qt, QDate
from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QMessageBox, qApp
from PyQt4.QtSql import QSqlQueryModel, QSqlQuery, QSqlDatabase
from ui.Ui_cierre import Ui_frmCierreContable
from utility import constantes
import logging




IDDOCUMENTO, NDOCUMENTO, TIPODOC, TOTAL, FECHA, OBSERVACIONES, ESTADO = range( 7 )
class FrmCierreContable( Ui_frmCierreContable, QMainWindow ):
    """
    Implementación de la interfaz cierre contable
    """
    def __init__( self, parent,tipocierre ):
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
        self.tipocierre=tipocierre
        self.validomensual=None
        self.validoanual=None
        
        self.dtPicker.setMaximumDate( QDate.currentDate() )
        self.dtPicker.setDate( QDate.currentDate() )
        
        self.lbltitulo.setText(self.lbltitulo.text()+" "+self.tipocierre)
        if self.tipocierre=="Anual":
            self.dtPicker.setDisplayFormat("yyyy")        
    @pyqtSlot( QDate )
    def on_dtPicker_dateChanged( self, date ):
        """
        Asignar la fecha al objeto __document
        """
        self.fecha = date
        self.updateModels()

    def updateModels( self):
        try:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open():
                    raise UserWarning( "No se pudo conectar con la base de datos" )
            query = QSqlQuery()
            if self.tipocierre=="Mensual":         
                'Lista de documentos para cierre mensual'
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
        
                self.navmodel.setQuery( q )  
                   
            else:
                q=u"""
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
                WHERE d.idtipodoc=%d  
                AND YEAR(d.fechacreacion)=%s""" %("%d/%m/%Y",constantes.IDCIERREMENSUAL,self.fecha.toString( "yyyy" ))              
                self.navmodel.setQuery( q )            
            
            'Verifico si hay documentos'
            if self.navmodel.rowCount() == 0:
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
            self.toolBar.removeAction( self.actionSave )
            
        except Exception as inst:
            logging.critical( unicode( inst ) )
            self.toolBar.removeAction( self.actionSave )
            QMessageBox.critical( self, qApp.organizationName(),
                                   u"Hubo un error al actualizar la tabla" )

    def validarCierreAnual(self):
        try:
            query=QSqlQuery()
            q=u"""
            SELECT d.iddocumento 
            FROM documentos d 
            WHERE d.idtipodoc=%d  
            AND YEAR(d.fechacreacion)=%s""" %(constantes.IDCIERREMENSUAL,self.fecha.toString( "yyyy" ))
            query.prepare(q)
            
            if not query.exec_():
                raise Exception( "No se pudo ejecutar la consulta para determinar si se cerraron todos los meses del año" )
            
            if query.size()<12 and query.size()>0:
                raise UserWarning( "No se han cerrado todos los meses del Ejercicio" )
            return True
            
        except UserWarning as inst:
            logging.error( unicode( inst ) )
            QMessageBox.critical( self, qApp.applicationName(), unicode( inst ) )
            self.toolBar.removeAction( self.actionSave )
            return False
            
        except Exception as inst:
            logging.critical( unicode( inst ) )
            self.toolBar.removeAction( self.actionSave )
            QMessageBox.warning( self,
             qApp.organizationName(),unicode(inst))
            return False   

    def validarCierreMensual(self):
        try:
            query=QSqlQuery()
            q=u"""
                SELECT d.iddocumento 
                FROM documentos d 
                WHERE d.idtipodoc=%d  
                AND YEAR(d.fechacreacion)=%s""" %(constantes.IDCIERREMENSUAL,self.fecha.toString( "yyyy" ))
            query.prepare(q)
            
            if not query.exec_():
                raise UserWarning( "No se pudo ejecutar la consulta para determinar si existe algun cierre en el año" )         
            if query.size()>0:
                mes=self.fecha.addMonths(-1)             
                q=u"""
                    SELECT d.iddocumento 
                    FROM documentos d 
                    WHERE d.idtipodoc=%d 
                    AND MONTH(fechacreacion)=%s 
                    AND YEAR(d.fechacreacion)=%s""" %(constantes.IDCIERREMENSUAL,mes.toString( "MM"),self.fecha.toString( "yyyy" ))
                query.prepare(q)
                
                if not query.exec_():
                    raise UserWarning( "No se pudo ejecutar la consulta para determinar si se cerro el mes anterior" )         
                if query.size()==0:
                    raise UserWarning( "No se ha cerrado el mes anterior" )        
            
                  
            #Verifico si existe un cierre para el mes en proceso
            q = """
            SELECT
                d2.iddocumento
            FROM documentos d
            JOIN docpadrehijos dp ON d.iddocumento=dp.idpadre
            JOIN documentos d2 ON d2.iddocumento=dp.idhijo
            WHERE d2.idtipodoc=%d and month(d2.fechacreacion)=%s
            LIMIT 1
            """ % ( constantes.IDCIERREMENSUAL, self.fecha.toString( "MM" ) )
            
            query.prepare( q )
            
            if not query.exec_():
                raise UserWarning( "No se pudo ejecutar la consulta para "\
                                   + "verificar si existe un cierre contable" )
            
            #El mes actual no se puede cerrar
            
            hoy=QDate.currentDate()
            if self.fecha.month()==hoy.month() and self.fecha.year() == hoy.year():
                raise UserWarning( "No se puede cerrar el mes en proceso" )
    
            return True
        
        except Exception as inst:
            logging.critical( unicode( inst ) )
            self.toolBar.removeAction( self.actionSave )
            QMessageBox.warning( self,
             qApp.organizationName(),unicode(inst))
             
        return False
               
    def save( self ):
        if QMessageBox.question( self, qApp.organizationName(),
                                u"¿Esta seguro que desea hacer este cierre "+self.tipocierre+"?\n"\
                                + u"Esta accion no se puede deshacer",  
                                 QMessageBox.Ok | QMessageBox.No ) == QMessageBox.Ok:
            docpendientes = True
            for i in range( self.navproxymodel.rowCount() ):
                if self.navproxymodel.index( i, ESTADO ).data( Qt.EditRole ).toString() != "CONFIRMADO" and self.navproxymodel.index( i, ESTADO ).data( Qt.EditRole ).toString() != "ANULADO":
                    docpendientes = False
            if self.tipocierre=="Mensual":
                if docpendientes == False or self.validarCierreMensual()==False:
                    QMessageBox.warning( self,
                        qApp.organizationName(),
                         u"No se realizó el cierre contable Mensual ")
                else:
                    self.saveMensual()                                     
            else: 
                if docpendientes==False or self.validarCierreAnual()==False:
                    QMessageBox.warning( self,
                     qApp.organizationName(),
                     u"No se realizó el cierre contable Anual ")
                else:
                    self.saveAnual()
    def saveAnual(self):
        pass
                
    def saveMensual(self):
        query = QSqlQuery()
        try:
            query.prepare( """
            CALL `spCierreMensual`(:IDCIERRE,
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
            :OTROSGASTOS,
            :PERDIDASGANANCIAS)
            """ )
            query.bindValue( ":IDCIERRE", constantes.IDCIERREMENSUAL )
            query.bindValue( ":MES", self.fecha.toString( "MM" ) )
            query.bindValue( ":ESTADO", constantes.CONFIRMADO )
            query.bindValue( ":ANO", self.fecha.toString( "yyyy" ) )
            query.bindValue( ":INGRESOSXVENTA",
                             constantes.INGRESOSXVENTA )
            query.bindValue( ":OTROSINGRESOS",
                             constantes.OTROSINGRESOS )
            query.bindValue( ":COSTOSGASTOSOPERACIONES",
                              constantes.COSTOSGASTOSOPERACIONES )
            query.bindValue( ":GASTOSXVENTAS",
                              constantes.GASTOSXVENTAS )
            query.bindValue( ":GASTOS", constantes.GASTOS )
            query.bindValue( ":GASTOSFINANCIEROS",
                             constantes.GASTOSFINANCIEROS )
            query.bindValue( ":PRODUCTOSFINANCIEROS",
                              constantes.PRODUCTOSFINANCIEROS )
            query.bindValue( ":OTROSGASTOS", constantes.OTROSGASTOS )
            query.bindValue( ":PERDIDASGANANCIAS",
                             constantes.PERDIDASGANANCIAS )
            if not query.exec_():
                raise UserWarning( "No se pudo cerrar el mes contable" )

            self.toolBar.removeAction( self.actionSave )
#                self.toolBar.addActions( self.actionPrint )
#                self.actionPrin.triggered.connect( self.printPreview )

        except UserWarning as inst:

            logging.error( inst )
            logging.error( query.lastError().text() )
            QMessageBox.critical( self, qApp.organizationName(),
                                  unicode( inst ) )
