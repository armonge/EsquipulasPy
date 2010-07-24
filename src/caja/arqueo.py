# -*- coding: UTF-8 -*-
'''
Created on 07/06/2010

@author: armonge
'''
if __name__ == "__main__":
    import sip
    sip.setapi( "QString", 2 )

from decimal import  Decimal
from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QTableView, QMessageBox, QDataWidgetMapper
from PyQt4.QtCore import pyqtSlot, SIGNAL, QDateTime, QTimer
from PyQt4.QtSql import QSqlQueryModel, QSqlQuery
from ui.Ui_arqueo import Ui_frmArqueo
from utility.base import Base
from utility.moneyfmt import moneyfmt

from document.arqueo.arqueomodel import ArqueoModel
from document.arqueo.arqueodelegate import ArqueoDelegate

#navmodel
IDDOCUMMENTO, NDOCIMPRESO, FECHA, NOMBRE, TOTAL = range( 5 )
#detailsmodel
CANTIDAD, DENOMINACION, MONEDA, TOTALP, IDDOCUMMENTOT = range( 5 )
class frmArqueo( QMainWindow, Ui_frmArqueo, Base ):
    '''
    Esta clase implementa el formulario arqueo
    '''
    def __init__( self, user, parent = None ):
        '''
        Constructor
        '''
        super( frmArqueo, self ).__init__( parent )
        self.setupUi( self )
        self.parentWindow = parent
        Base.__init__( self )



        self.editmodel = None
        self.user = user
        self.parent = parent

#        El modelo principal
        self.navmodel = QSqlQueryModel( self )
#        El modelo que filtra a self.navmodel
        self.navproxymodel = QSortFilterProxyModel( self )
        self.navproxymodel.setSourceModel( self.navmodel )
#        Este es el modelo con los datos de la tabla con los detalles
        self.detailsModel = QSqlQueryModel( self )
#        Este es el filtro del modelo anterior
        self.detailsproxymodel = QSortFilterProxyModel( self )
        self.detailsproxymodel.setSourceModel( self.detailsModel )

        self.status = True
        QTimer.singleShot( 0, self.loadModels )

    def updateModels( self ):
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise Exception( "No se pudo abrir la base de datos" )
            self.navmodel.setQuery( """
            SELECT
                d.iddocumento, 
                d.ndocimpreso, 
                d.fechacreacion, 
                u.nombre, 
                CONCAT('US$',FORMAT(d.total,4))  as 'Total US$'
            FROM documentos d  
            JOIN tiposcambio tc ON tc.idtc = d.idtipocambio
            JOIN usuarios u ON u.idusuario = d.idusuario
            WHERE d.idtipodoc = 23
            """ )
            self.detailsModel.setQuery( """
            SELECT 
                l.cantidad as 'Cantidad', 
                CONCAT(IF(l.idtipomoneda = 1, "C$", "US$") ,l.denominacion) as 'Denominacion',
                CASE l.idtipomoneda WHEN 1 THEN 'Cordoba' WHEN 2 THEN 'Dolar' END as 'Moneda',
                CONCAT("US$", FORMAT(l.cantidad * IF(l.idtipomoneda = 1, l.denominacion * tc.tasa, l.denominacion), 4)) as 'Total US$',
                l.iddocumento
            FROM lineasarqueo l
            JOIN documentos d ON d.iddocumento = l.iddocumento
            JOIN tiposcambio tc ON d.idtipocambio = tc.idtc
            """ )

            self.mapper.setSubmitPolicy( QDataWidgetMapper.ManualSubmit )
            self.mapper.setModel( self.navproxymodel )
            self.mapper.addMapping( self.lblPrintedDocumentNumber, NDOCIMPRESO, "text" )
            self.mapper.addMapping( self.dtPicker, FECHA )
            self.mapper.addMapping( self.lblUserName, NOMBRE, "text" )
            self.mapper.addMapping( self.lblTotalArqueo, TOTAL, "text" )


        except Exception, e:
            print e
        finally:
            if self.database.isOpen():
                self.database.close()

    def updateDetailFilter( self, index ):
        self.detailsproxymodel.setFilterKeyColumn( IDDOCUMMENTOT )
        self.detailsproxymodel.setFilterRegExp( self.navmodel.record( index ).value( "iddocumento" ).toString() )
        self.tablenavigation.selectRow( self.mapper.currentIndex() )

    def setControls( self, status ):
        """
        @param status: false = editando true = navegando 
        """
        self.tablenavigation.setEnabled( status )
        self.tabnavigation.setEnabled( status )

        self.actionNew.setVisible( status )
        self.actionPreview.setVisible( status )

        self.actionCancel.setVisible( not status )
        self.actionSave.setVisible( not status )
        if not self.status:
            self.tabledetails.setEditTriggers( QTableView.AllEditTriggers )
            self.tabledetails.addAction( self.actionDeleteRow )
            self.tabWidget.setCurrentIndex( 0 )
            self.tabledetails.setColumnHidden( IDDOCUMMENTOT, False )
            self.tablenavigation.setColumnHidden( IDDOCUMMENTO, False )
            self.lblTotalArqueo.setText( "US$0.0000" )
        else:
            self.tabledetails.removeAction( self.actionDeleteRow )
            self.tabledetails.setModel( self.detailsproxymodel )
            self.tablenavigation.setModel( self.navproxymodel )
            self.tablenavigation.setColumnHidden( IDDOCUMMENTO, True )
            self.tabledetails.setColumnHidden( IDDOCUMMENTOT, True )

    def updateLabels( self ):
        self.lblTotalArqueo.setText( moneyfmt( self.editmodel.total, 4, "US$" ) )

    @pyqtSlot( )
    def on_actionNew_activated( self ):
        """
        cargar todos los modelos para la edición
        """
        try:
            self.editmodel = ArqueoModel()
            self.editmodel.uid = self.user.uid
            self.tabledetails.setModel( self.editmodel )

            if not self.database.isOpen():
                if not self.database.open():
                    raise Exception( "No se pudo conectar con la base de datos" )

            query = QSqlQuery( """
            SELECT 
                IF(SUM(d.total) IS NOT NULL, SUM(d.total), 0) + p.total as 'totalsesion', 
                DATE(p.fechacreacion), 
                tc.tasa,
                tc.idtc
            FROM documentos p
            LEFT JOIN docpadrehijos dpd ON dpd.idpadre = p.iddocumento
            LEFT JOIN documentos d ON dpd.idhijo = d.iddocumento
            JOIN tiposcambio tc ON tc.idtc = p.idtipocambio
            WHERE d.escontado = 1 AND p.iddocumento = %d
            """ % self.parent.sesion )


            if not query.exec_():
                raise Exception( u"No se pudo ejecutar la consulta para obtener el total de la sesion" )
            if not query.size() > 0:
                raise Exception( "Error al obtener el total de la consulta" )
            query.first()
            self.editmodel.expectedTotal = Decimal( query.value( 0 ).toString() )

#            self.editmodel.datetime = QDateTime( query.value( 1 ).toDateTime() )

            self.editmodel.exchangeRate = Decimal( query.value( 2 ).toString() )
            self.editmodel.exchangeRateId = query.value( 3 ).toInt()[0]
            query = QSqlQuery( """
            SELECT
            MAX(CAST(ndocimpreso AS SIGNED))+1
            FROM documentos d
            WHERE idtipodoc=23
            ;
            """ )
            if not query.exec_():
                raise Exception( "No se pudo calcular el numero del arqueo" )
            query.first()
            self.editmodel.printedDocumentNumber = query.value( 0 ).toString()

            self.lblTotalSesion.setText( moneyfmt( self.editmodel.expectedTotal, 4, "US$" ) )
            self.lblPrintedDocumentNumber.setText( self.editmodel.printedDocumentNumber )


            delegate = ArqueoDelegate()
            self.tabledetails.setItemDelegate( delegate )

            self.addLine()
            self.dtPicker.setDateTime( QDateTime.currentDateTime() )

            self.lblUserName.setText( self.user.fullname )
            self.connect( self.editmodel, SIGNAL( "dataChanged(QModelIndex, QModelIndex)" ), self.updateLabels )
            self.status = False
        except Exception, e:
            print e
            self.status = True
        finally:
            if self.database.isOpen():
                self.database.close()



    @pyqtSlot(  )
    def on_actionCancel_activated( self ):
        self.editmodel = None
        self.tablenavigation.setModel( self.navproxymodel )
        self.tabledetails.setModel( self.detailsproxymodel )
        self.status = True
        self.navigate( 'last' )

    @pyqtSlot(  )
    def on_actionSave_activated( self ):
        """
        Redefiniendo el metodo save de Base para mostrar advertencias si el arqueo no concuerda
        """
        if self.editmodel.valid:
            if self.editmodel.total == self.editmodel.expectedTotal or QMessageBox.question( self, "Llantera Esquipulas: Caja", u"El total de la sesión no coincide con el total del arqueo\n ¿Desea continuar?", QMessageBox.Yes | QMessageBox.No ) == QMessageBox.Yes:
                if not self.database.isOpen():
                    if not self.database.open():
                        raise Exception( "No se pudo conectar con la base de datos" )

                if self.editmodel.save():
                    QMessageBox.information( self,
                         "Llantera Esquipulas" ,
                         """El documento se ha guardado con exito""" )
                    self.editmodel = None
                    self.updateModels()
                    self.navigate( 'last' )
                    self.status = True
                else:
                    QMessageBox.critical( self,
                         "Llantera Esquipulas" ,
                         """Ha ocurrido un error al guardar el documento""" )

                if self.database.isOpen():
                    self.database.close()

        else:
            QMessageBox.warning( self,
                 "Llantera Esquipulas" ,
                u"""El documento no puede guardarse ya que la información no esta completa""" ,
                QMessageBox.StandardButtons( \
                    QMessageBox.Ok ),
                QMessageBox.Ok )



