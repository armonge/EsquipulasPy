# -*- coding: utf-8 -*-
'''
Created on 07/06/2010

@author: Andrés Reyes Monge
'''
#FIXME: EL arqueo no muestra todavia el total de la sesión
from decimal import  Decimal
from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QTableView, QMessageBox, QDataWidgetMapper, QPrinter
from PyQt4.QtCore import pyqtSlot, SIGNAL, QDateTime, QTimer, QModelIndex
from PyQt4.QtSql import QSqlQueryModel, QSqlQuery
from ui.Ui_arqueo import Ui_frmArqueo
from utility.base import Base
from utility.moneyfmt import moneyfmt
from utility.singleselectionmodel import  SingleSelectionModel
from document.arqueo.arqueomodel import ArqueoModel, ArqueoProxyModel
from document.arqueo.arqueodelegate import ArqueoDelegate

from utility import constantes
from utility.reports import frmReportes
#navmodel
IDDOCUMMENTO, FECHA, NOMBRE, TOTAL, TOTALSESION = range( 5 )
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
                    raise UserWarning( "No se pudo abrir la base de datos" )
            self.navmodel.setQuery( """
            SELECT
                d.iddocumento, 
                d.fechacreacion AS 'Fecha', 
                p.nombre AS 'Arqueador', 
                CONCAT('US$',FORMAT(d.total,4))  as 'Total US$'
            FROM documentos d  
            JOIN tiposcambio tc ON tc.idtc = d.idtipocambio
            JOIN personasxdocumento pxd ON pxd.iddocumento = d.iddocumento
            JOIN personas p ON p.idpersona = pxd.idpersona AND p.tipopersona = %d
            WHERE d.idtipodoc = %d
            """ % ( constantes.USUARIO, constantes.IDARQUEO))
            
            #FIXME: El simbolo de la moneda deberia de venir de la tabla tiposmoneda
            self.detailsModel.setQuery( u"""
            SELECT 
                l.cantidad AS 'Cantidad',
                CONCAT_WS(' ', tm.simbolo, de.valor) as 'Denominación',
                tm.moneda as 'Moneda',
                CONCAT("US$", FORMAT(l.cantidad * IF(de.idtipomoneda = 1, de.valor * tc.tasa, de.valor), 4)) as 'Total US$',
                l.iddocumento
            FROM lineasarqueo l
            JOIN denominaciones de ON de.iddenominacion = l.iddenominacion
            JOIN tiposmoneda tm ON de.idtipomoneda = tm.idtipomoneda
            JOIN documentos d ON d.iddocumento = l.iddocumento
            JOIN tiposcambio tc ON d.idtipocambio = tc.idtc
            """ )

            self.mapper.setSubmitPolicy( QDataWidgetMapper.ManualSubmit )
            self.mapper.setModel( self.navproxymodel )
            self.mapper.addMapping( self.dtPicker, FECHA )
            self.mapper.addMapping( self.lblUserName, NOMBRE, "text" )
            ##self.mapper.addMapping( self.lblTotalArqueo, TOTAL, "text" )

            
        except UserWarning as inst:
            QMessageBox.critical(self, "Llantera Esquipulas", unicode(inst))
        except Exception as inst:
            print inst
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

        self.txtCkD.setReadOnly(status)
        self.txtCkC.setReadOnly(status)
        self.txtCardD.setReadOnly(status)
        self.txtCardC.setReadOnly(status)
        self.txtDepositD.setReadOnly(status)
        self.txtDepositC.setReadOnly(status)
        

        
        if not self.status:
            self.tabledetailsC.setEditTriggers( QTableView.AllEditTriggers )
            self.tabledetailsC.setColumnHidden( IDDOCUMMENTOT, False )
            self.tabledetailsD.setEditTriggers( QTableView.AllEditTriggers )
            self.tabledetailsD.setColumnHidden( IDDOCUMMENTOT, False )
            self.tabWidget.setCurrentIndex( 0 )
            self.tablenavigation.setColumnHidden( IDDOCUMMENTO, False )

            self.tabledetailsC.setColumnHidden( MONEDA, True )
            self.tabledetailsD.setColumnHidden( MONEDA, True )
        else:
            self.tabledetailsC.setModel( self.detailsproxymodel )
            self.tabledetailsC.setColumnHidden( IDDOCUMMENTOT, True )
            
            
            self.tabledetailsD.setModel( self.detailsproxymodel )
            self.tabledetailsD.setColumnHidden( IDDOCUMMENTOT, True )
            
            
            self.tablenavigation.setModel( self.navproxymodel )
            self.tablenavigation.setColumnHidden( IDDOCUMMENTO, True )


        

    def updateLabels( self ):
        self.lblCashC.setText(  moneyfmt( self.editmodel.totalCashC, 4, "C$" ) + " / " + moneyfmt(self.editmodel.expectedCashC, 4, "C$"))
        self.lblCashD.setText( moneyfmt( self.editmodel.totalCashD, 4, "US$" ) + " / " + moneyfmt(self.editmodel.expectedCashD, 4, "US$") )

        self.lblCkC.setText( moneyfmt( self.editmodel.totalCkC, 4, "C$" ) + " / " + moneyfmt(self.editmodel.expectedCkC, 4, "C$") )
        self.lblCkD.setText( moneyfmt( self.editmodel.totalCkD, 4, "US$" ) + " / " + moneyfmt(self.editmodel.expectedCkD, 4, "US$") )

        self.lblCardC.setText( moneyfmt( self.editmodel.totalCardC, 4, "C$" ) + " / " + moneyfmt(self.editmodel.expectedCardC, 4, "C$") )
        self.lblCardD.setText( moneyfmt( self.editmodel.totalCardD, 4, "US$" ) + " / " + moneyfmt(self.editmodel.expectedCardD, 4, "US$") )

        self.lblDepositC.setText( moneyfmt( self.editmodel.totalDepositC, 4, "C$" ) + " / " + moneyfmt(self.editmodel.expectedDepositC, 4, "C$") )
        self.lblDepositD.setText( moneyfmt( self.editmodel.totalDepositD, 4, "US$" ) + " / " + moneyfmt(self.editmodel.expectedDepositD, 4, "US$") )

    @pyqtSlot( )
    def on_actionNew_activated( self ):
        """
        cargar todos los modelos para la edición
        """
        try:
            self.editmodel = ArqueoModel()
            self.editmodel.uid = self.user.uid


            self.dolarproxy = ArqueoProxyModel()
            self.dolarproxy.setSourceModel(self.editmodel)
            self.dolarproxy.setFilterKeyColumn(MONEDA)
            self.dolarproxy.setFilterRegExp(r"^%d$"%constantes.IDDOLARES)
            self.dolarproxy.setDynamicSortFilter(True)
            
            self.cordobaproxy = ArqueoProxyModel()
            self.cordobaproxy.setSourceModel(self.editmodel)
            self.cordobaproxy.setFilterKeyColumn(MONEDA)
            self.cordobaproxy.setFilterRegExp(r"^%d$"%constantes.IDCORDOBAS)
            self.cordobaproxy.setDynamicSortFilter(True)

            self.tabledetailsC.setModel( self.cordobaproxy )
            self.tabledetailsD.setModel( self.dolarproxy)
            
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( "No se pudo conectar con la base de datos" )


            #Obtener los datos de la sesión
            query = QSqlQuery( """
            CALL spConsecutivo( %d, NULL )
            """ % constantes.IDARQUEO)
            if not query.exec_() or not query.size() > 0:
                raise UserWarning( u"Error al obtener el numero del arqueo")
            query.first()
            
            self.editmodel.printedDocumentNumber = query.value(0).toString()
            self.editmodel.exchangeRateId = self.parent.datosSesion.tipoCambioId
            self.editmodel.exchangeRate = self.parent.datosSesion.tipoCambioOficial
            
            self.editmodel.datetime = self.parent.datosSesion.fecha
            
            query = QSqlQuery( """
            CALL spTotalesSesion(%d);
            """ % self.parent.datosSesion.sesionId )
            if not query.exec_():
                raise UserWarning( u"No se pudieron calcular los totales de la sesión" )
            while query.next():
                if query.value(0).toInt()[0]  == constantes.IDPAGOEFECTIVO and query.value(2).toInt()[0] == constantes.IDDOLARES:
                    self.editmodel.expectedCashD = Decimal(query.value(5).toString())
                elif query.value(0).toInt()[0] == constantes.IDPAGOEFECTIVO and query.value(2).toInt()[0] == constantes.IDCORDOBAS:
                    self.editmodel.expectedCashC = Decimal(query.value(5).toString())
                elif query.value(0).toInt()[0] == constantes.IDPAGOCHEQUE and query.value(2).toInt()[0] == constantes.IDDOLARES:
                    self.editmodel.expectedCkD = Decimal(query.value(5).toString())
                elif query.value(0).toInt()[0] == constantes.IDPAGOCHEQUE and query.value(2).toInt()[0] == constantes.IDCORDOBAS:
                    self.editmodel.expectedCkC = Decimal(query.value(5).toString())
                elif query.value(0).toInt()[0] == constantes.IDPAGODEPOSITO and query.value(2).toInt()[0] == constantes.IDDOLARES:
                    self.editmodel.expectedDepositD = Decimal(query.value(5).toString())
                elif query.value(0).toInt()[0] == constantes.IDPAGODEPOSITO  and query.value(2).toInt()[0] == constantes.IDCORDOBAS:
                    self.editmodel.expectedDepositC = Decimal(query.value(5).toString())
                elif query.value(0).toInt()[0] == constantes.IDPAGOTRANSFERENCIA  and query.value(2).toInt()[0] == constantes.IDDOLARES:
                    self.editmodel.expectedTransferD = Decimal(query.value(5).toString())
                elif query.value(0).toInt()[0] == constantes.IDPAGOTRANSFERENCIA  and query.value(2).toInt()[0] == constantes.IDCORDOBAS:
                    self.editmodel.expectedTransferC = Decimal(query.value(5).toString())
                elif query.value(0).toInt()[0] == constantes.IDPAGOTARJETA  and query.value(2).toInt()[0] == constantes.IDDOLARES:
                    self.editmodel.expectedCardD = Decimal(query.value(5).toString())
                elif query.value(0).toInt()[0] == constantes.IDPAGOTARJETA  and query.value(2).toInt()[0] == constantes.IDCORDOBAS:
                    self.editmodel.expectedCardC = Decimal(query.value(5).toString())

                    
            query = QSqlQuery( """
            SELECT 
                d.iddenominacion, 
                CONCAT_WS( ' ',d.valor, m.moneda), 
                d.valor, 
                d.idtipomoneda,
                m.simbolo
            FROM denominaciones d
            JOIN tiposmoneda m ON d.idtipomoneda = m.idtipomoneda
            WHERE d.activo = 1
            ORDER BY d.idtipomoneda, d.valor
            """ )
            if not query.exec_():
                raise UserWarning( "No se pudo recuperar la lista de denominaciones" )
            denominationsmodelC = SingleSelectionModel()
            denominationsmodelC.headers = ["Id", u"Denominación", "Valor", "Id Moneda", "Simbolo"]
            denominationsmodelD = SingleSelectionModel()
            denominationsmodelD.headers = denominationsmodelC.headers

            
            while query.next():
                if query.value(3).toInt()[0] == constantes.IDDOLARES:
                    denominationsmodelD.items.append( [
                                                  query.value( 0 ).toInt()[0], #el id del tipo de denominacion
                                                  query.value( 1 ).toString(), #La descripción de la denominación
                                                  query.value( 2 ).toString(), # el valor de la denominación
                                                  query.value( 3 ).toInt()[0], #El id del tipo de moneda
                                                  query.value( 4 ).toString() #El simbolo de la moneda
                                                  ] )
                else:
                    denominationsmodelC.items.append( [
                                                  query.value( 0 ).toInt()[0], #el id del tipo de denominacion
                                                  query.value( 1 ).toString(), #La descripción de la denominación
                                                  query.value( 2 ).toString() , # el valor de la denominación
                                                  query.value( 3 ).toInt()[0], #El id del tipo de moneda
                                                  query.value( 4 ).toString() #El simbolo de la moneda
                                                  ] )

            delegateC = ArqueoDelegate(denominationsmodelC)
            self.tabledetailsC.setItemDelegate( delegateC )

            delegateD = ArqueoDelegate(denominationsmodelD)
            self.tabledetailsD.setItemDelegate( delegateD )

            self.addLine()
            self.addLine()
            self.editmodel.setData(self.editmodel.index(0, MONEDA), constantes.IDDOLARES)
            self.editmodel.setData(self.editmodel.index(1, MONEDA), constantes.IDCORDOBAS)
            
            self.dtPicker.setDate( self.parentWindow.datosSesion.fecha)

            self.lblUserName.setText( self.user.fullname )
            self.editmodel.dataChanged[QModelIndex,QModelIndex].connect(self.updateLabels)

            self.tabledetailsC.setColumnWidth(DENOMINACION, 200)
            self.tabledetailsD.setColumnWidth(DENOMINACION, 200)
            self.updateLabels()
            self.status = False
            
        except UserWarning as inst:
            QMessageBox.critical(self, "Llantera Esquipulas", unicode(inst))
            self.status = True
        except Exception  as inst:
            print inst
            QMessageBox.critical(self, "Llantera Esquipulas", "El sistema no pudo iniciar un nuevo arqueo")
            self.status = True
        finally:
            if self.database.isOpen():
                self.database.close()

    @pyqtSlot( "QDateTime" )
    def on_dtPicker_dateTimeChanged( self, datetime ):
        if not self.editmodel is None:
            self.editmodel.datetime = datetime

    @pyqtSlot(  )
    def on_actionCancel_activated( self ):
        self.editmodel = None
        
        self.status = True
        self.navigate( 'last' )

    @pyqtSlot(  )
    def on_actionSave_activated( self ):
        """
        Redefiniendo el metodo save de Base para mostrar advertencias si el arqueo no concuerda
        """
        if self.editmodel.total == self.editmodel.expectedTotal or QMessageBox.question( self, "Llantera Esquipulas: Caja", u"El total de la sesión no coincide con el total del arqueo\n ¿Desea continuar?", QMessageBox.Yes | QMessageBox.No ) == QMessageBox.Yes:
            super(frmArqueo, self).on_actionSave_activated()

    @pyqtSlot(  )
    def on_actionPreview_activated( self ):
        """
        Funcion usada para mostrar el reporte de una entrada compra
        """
        printer = QPrinter()
        printer.setPageSize(QPrinter.Letter)
        web = "arqueos.php?doc=%d" % self.navmodel.record( self.mapper.currentIndex() ).value( "iddocumento" ).toInt()[0] 
        report = frmReportes( web , self.parentWindow.user, printer, self )
        report.exec_()

    def navigate( self, to ):
        """
        Esta funcion se encarga de navegar entro los distintos documentos
        @param to: es una string que puede tomar los valores 'next' 'previous' 'first' 'last'
        """
        if self.mapper.currentIndex != -1:
            row = self.mapper.currentIndex()
            if to == "next":
                row += 1
                if row >= self.navproxymodel.rowCount():
                    row = self.navproxymodel.rowCount() - 1
                self.mapper.setCurrentIndex( row )
            elif to == "previous":
                if row <= 1: row = 0
                else: row = row - 1
                self.mapper.setCurrentIndex( row )
            elif to == "first":
                self.mapper.toFirst()
            elif to == "last":
                self.mapper.toLast()
        else:
            self.mapper.toLast()()

        self.tabledetailsC.resizeColumnsToContents()
        self.tabledetailsC.horizontalHeader().setStretchLastSection(True)
        self.tabledetailsD.resizeColumnsToContents()
        self.tabledetailsD.horizontalHeader().setStretchLastSection(True)
        self.tablenavigation.selectRow( self.mapper.currentIndex() )