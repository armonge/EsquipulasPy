# -*- coding: utf-8 -*-

"""
Module implementing frmLiquidacion.
"""
from decimal import Decimal
import logging

from PyQt4.QtGui import QMainWindow, QAbstractItemView, \
QSortFilterProxyModel, QDataWidgetMapper, QTableView, QMessageBox, QPrinter
from PyQt4.QtCore import pyqtSlot, QDateTime, Qt, QTimer
from PyQt4.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from ui.Ui_liquidacion import Ui_frmLiquidacion

from utility.moneyfmt import moneyfmt
from utility import constantes
from utility import movimientos
from utility.base import Base
from utility.accountselector import  AccountsSelectorDelegate, AccountsSelectorLine
from document.liquidacion.liquidacionmodel import LiquidacionModel, LiquidacionAccountsModel
from document.liquidacion.liquidaciondelegate import LiquidacionDelegate


#navigation model
IDDOCUMENTO, NDOCIMPRESO, FECHA, PROCEDENCIA, AGENCIA, ALMACEN, FLETE, SEGURO,\
OTROS, TRANSPORTE, PAPELERIA, PESO, PROVEEDOR, BODEGA, ISO, TCAMBIO, ESTADO,FOBTOTAL, CIFTOTAL, IMPUESTOTOTAL, TOTALD, TOTALC = range( 22 )


#details model
IDARTICULO, DESCRIPCION, UNIDADES, COSTOCOMPRA, FOB, FLETEP, SEGUROP, OTROSP, \
CIF, IMPUESTOSP, COMISION, AGENCIAP, ALMACENP, PAPELERIAP, TRANSPORTEP, DTOTALD, DUNITD, DTOTALC, DUNITC, IDDOCUMENTOT = range( 20 )

#accounts model
IDCUENTA, CODCUENTA, NCUENTA, MONTOCUENTA, IDDOCUMENTOC = range( 5 )
class frmLiquidacion( QMainWindow, Ui_frmLiquidacion, Base ):
    """
    Class documentation goes here.
    """
    web = "liquidaciones.php?doc="
    orientation = QPrinter.Landscape
    pageSize = QPrinter.Legal
    def __init__( self, user, parent = None ):
        """
        @param user: EL objeto usuario que esta asociado con esta sesión
        """
        QMainWindow.__init__( self, parent )
        self.setupUi( self )
        self.parentWindow = parent
        Base.__init__( self )


        self.user = user
        #los modelos de edicion
        self.editmodel = None
        self.accountseditmodel = None



        self.xdockWidget.setCollapsed( True )
        self.status = 1


        self.xdockWidget.setVisible( False )

#        El modelo principal
        self.navmodel = LiquidacionNavModel( self )
#        El modelo que filtra a self.navmodel
        self.navproxymodel = QSortFilterProxyModel( self )
        self.navproxymodel.setSourceModel( self.navmodel )
        self.navproxymodel.setFilterKeyColumn( -1 )

        self.navproxyproxymodel = QSortFilterProxyModel( self )
        self.navproxyproxymodel.setSourceModel( self.navproxymodel )
        
#        Este es el modelo con los datos de la con los detalles
        self.detailsmodel = QSqlQueryModel( self )
##        Este es el filtro del modelo anterior
        self.detailsproxymodel = QSortFilterProxyModel( self )
        self.detailsproxymodel.setSourceModel( self.detailsmodel )
        self.detailsproxymodel.setFilterKeyColumn( -1 )

#        Este es el modelo para las cuentas
        self.accountsModel = QSqlQueryModel( self )
        self.accountsProxyModel = QSortFilterProxyModel()
        self.accountsProxyModel.setSourceModel( self.accountsModel )


        #inicializando el documento
        self.editmodel = None

        QTimer.singleShot( 0, self.loadModels )



    def updateDetailFilter( self, index ):
        self.detailsproxymodel.setFilterKeyColumn( IDDOCUMENTOT )
        self.detailsproxymodel.setFilterRegExp( "^%d$"%self.navmodel.record( index ).value( IDDOCUMENTO ).toInt()[0] )

        self.accountsProxyModel.setFilterKeyColumn( IDDOCUMENTOC )
        self.accountsProxyModel.setFilterRegExp( "^%d$"%self.navmodel.record( index ).value( IDDOCUMENTO ).toInt()[0] )

        self.navproxyproxymodel.setFilterKeyColumn(IDDOCUMENTO)
        self.navproxyproxymodel.setFilterRegExp( "^%d$"%self.navmodel.record( index ).value( IDDOCUMENTO ).toInt()[0] )
        
        self.tablenavigation.selectRow( self.mapper.currentIndex() )
        
        self.ckISO.setChecked( True if self.navmodel.record( index ).value( "iso" ).toDouble()[0] != 0 else False )

        estado = self.navmodel.record( index ).value( "estado" ).toInt()[0]
        if estado == constantes.INCOMPLETO:
            if self.user.hasRole('contabilidad'):
                self.actionEditAccounts.setVisible(True)
        else:
            self.actionEditAccounts.setVisible(False)
        

    def setControls( self, status ):
        """
        En esta funcion cambio el estado enabled de todos los items en el formulario
        @param status: 1 = navegando 2 = añadiendo productos 3 = añadiendo cuentas contables
        """
        
        self.txtPolicy.setReadOnly( status == 1 or status == 3 )
        self.txtSource.setReadOnly( status == 1 or status == 3)
        
        self.sbAgency.setReadOnly( status == 1 or status == 3)
        self.sbFreight.setReadOnly( status == 1 or status == 3)
        self.sbInsurance.setReadOnly( status == 1 or status == 3)
        self.sbOther.setReadOnly( status == 1 or status == 3)
        
        self.sbWeight.setReadOnly( status == 1 or status == 3)
        self.sbPaperWork.setReadOnly( status == 1 or status == 3)
        self.sbStore.setReadOnly( status == 1 or status == 3)
        self.sbTransportation.setReadOnly( status == 1 or status == 3)
        self.ckISO.setEnabled( not (status == 1 or status == 3 ))
        self.ckTaxes.setEnabled( not (status == 1 or status == 3 ))
        self.tablenavigation.setEnabled(status == 1)


        self.swProvider.setCurrentIndex( 0 if status == 1 or status == 3 else 1 )
        self.swWarehouse.setCurrentIndex( 1 if status == 1 or status == 3 else 0 )


        self.dtPicker.setReadOnly( status != 2 )
        self.cbWarehouse.setEnabled( status == 2 )

        self.actionUpdateArticles.setVisible( status == 2)
        self.actionCancel.setVisible( not status == 1)
        self.actionSave.setVisible( not status == 1)
        self.actionPreview.setVisible( status == 1 )
        self.actionPrint.setVisible( status == 1 )
        self.actionNew.setVisible( status == 1 )


        self.actionGoFirst.setVisible( status == 1 )
        self.actionGoPrevious.setVisible( status == 1)
        self.actionGoNext.setVisible( status == 1)
        self.actionGoLast.setVisible( status == 1)
        
        self.tabledetails.setColumnHidden( IDDOCUMENTOT, True )
        self.tabledetails.setColumnHidden( IDARTICULO, True )

        self.tablenavigation.setColumnHidden( IDDOCUMENTO, True )
        self.tablenavigation.setColumnHidden( AGENCIA, True )
        self.tablenavigation.setColumnHidden( PESO, True )
        self.tablenavigation.setColumnHidden( ALMACEN, True )
        self.tablenavigation.setColumnHidden( FLETE, True )
        self.tablenavigation.setColumnHidden( SEGURO, True )
        self.tablenavigation.setColumnHidden( OTROS, True )
        self.tablenavigation.setColumnHidden( TRANSPORTE, True )
        self.tablenavigation.setColumnHidden( PAPELERIA, True )
        self.tablenavigation.setColumnHidden( BODEGA, True )
        self.tablenavigation.setColumnHidden( ISO, True )
        self.tablenavigation.setColumnHidden( TCAMBIO, True )
        self.tablenavigation.setColumnHidden( FOBTOTAL, True )
        self.tablenavigation.setColumnHidden( CIFTOTAL, True )
        self.tablenavigation.setColumnHidden( IMPUESTOTOTAL, True )

        


        
        self.tableaccounts.setColumnHidden( IDCUENTA, True )
        self.tableaccounts.setColumnHidden( IDDOCUMENTOC, True )
        
        self.tabnavigation.setEnabled( status )
        if status == 1:

            self.tabletotals.setColumnHidden( IDDOCUMENTO, True )
            self.tabletotals.setColumnHidden( AGENCIA, True )
            self.tabletotals.setColumnHidden( PESO, True )
            self.tabletotals.setColumnHidden( ALMACEN, True )
            self.tabletotals.setColumnHidden( FLETE, True )
            self.tabletotals.setColumnHidden( SEGURO, True )
            self.tabletotals.setColumnHidden( OTROS, True )
            self.tabletotals.setColumnHidden( TRANSPORTE, True )
            self.tabletotals.setColumnHidden( PAPELERIA, True )
            self.tabletotals.setColumnHidden( BODEGA, True )
            self.tabletotals.setColumnHidden( ISO, True )
            self.tabletotals.setColumnHidden( TCAMBIO, True )
            self.tabletotals.setColumnHidden(NDOCIMPRESO, True)
            self.tabletotals.setColumnHidden(ESTADO, True)
            self.tabletotals.setColumnHidden(FECHA, True)
            self.tabletotals.setColumnHidden(PROCEDENCIA, True)
            self.tabletotals.setColumnHidden(PESO, True)
            self.tabletotals.setColumnHidden(PROVEEDOR, True)
            self.tabletotals.setColumnHidden(TCAMBIO, True)
        elif status == 2: #editando
            self.tableaccounts.setEditTriggers( QTableView.AllEditTriggers )
            self.tabledetails.addAction( self.actionDeleteRow )

            self.txtPolicy.setText("")
            self.txtSource.setText("")

            self.sbAgency.setValue(0)
            self.sbFreight.setValue(0)
            self.sbInsurance.setValue(0)
            self.sbOther.setValue(0)

            self.sbWeight.setValue(0)
            self.sbPaperWork.setValue(0)
            self.sbStore.setValue(0)
            self.sbTransportation.setValue(0)

            self.tabletotals.resizeColumnsToContents()

            for x in range(self.tabletotals.model().columnCount()):
                self.tabletotals.setColumnHidden(x, False)
            self.actionEditAccounts.setVisible(False)
        elif status == 3:
            self.tabTotalsAccounts.setCurrentIndex(0)
            self.tableaccounts.setEditTriggers( QTableView.AllEditTriggers )
            self.actionEditAccounts.setVisible(False)
        else:
            self.tableaccounts.setEditTriggers( QTableView.NoEditTriggers )
            self.tabledetails.removeAction( self.actionDeleteRow )

    @pyqtSlot( "QDateTime" )
    def on_dtPicker_dateTimeChanged( self, datetime ):
        if not self.editmodel is None:
            super( frmLiquidacion, self ).on_dtPicker_dateTimeChanged( datetime )
            self.txtExchangeRate.setText( self.editmodel.exchangeRate.to_eng_string() )

    def updateLabels(self):
        pass
    
    def updateModels( self ):
        try:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open():
                    raise UserWarning( "No se pudo conectar con la base de datos ")
            query = u"""
            SELECT
                d.iddocumento,
                d.ndocimpreso AS 'Número de Liquidación',
                d.fecha AS 'Fecha',
                d.procedencia AS 'Procedencia',
                d.totalagencia AS 'Agencia',
                d.totalalmacen AS 'Almacen',
                d.fletetotal AS 'Flete',
                d.segurototal as 'Seguro',
                d.otrosgastos AS 'Otros Gastos',
                d.porcentajetransporte AS 'Transporte',
                d.porcentajepapeleria AS 'Papelería',
                d.peso AS 'Peso',
                d.Proveedor AS 'Proveedor',
                d.bodega AS 'Bodega',
                SUM(IFNULL(valorcosto,0)) as  'ISO',
                d.tasa,
                d.estado,
                lt.fobtotal,
                lt.ciftotal,
                lt.impuestototal,
                d.totald AS 'Total US$',
                d.totalc AS 'Total C$'
            FROM esquipulasdb.vw_liquidacionesguardadas d
            JOIN vw_liquidacioncontotales lt ON lt.iddocumento = d.iddocumento
            LEFT JOIN costosxdocumento cxd ON d.iddocumento = cxd.iddocumento
            LEFT JOIN costosagregados ca ON cxd.idcostoagregado = ca.idcostoagregado AND ca.idtipocosto = %d
            GROUP BY d.iddocumento;
            """ % ( constantes.ISO)
            self.navmodel.setQuery( query )
            query = u"""
            SELECT
                a.idarticulo as 'Id',
                descripcion as 'Descripción',
                unidades as 'Cantidad',
                CONCAT('US$', FORMAT(costocompra,4)) as 'Costo Compra US$',
                CONCAT('US$', FORMAT(fob,4)) as 'FOB US$',
                CONCAT('US$', FORMAT(flete,4)) as 'Flete US$',
                CONCAT('US$', FORMAT(seguro,4)) as 'Seguro US$',
                CONCAT('US$', FORMAT(otrosgastos,4)) as 'Otros Gastos US$',
                CONCAT('US$', FORMAT(cif,4)) as 'CIF US$',
                CONCAT('US$', FORMAT(impuestos,4)) as 'Impuestos US$',
                CONCAT('US$', FORMAT(comision,4)) as 'Comisión US$',
                CONCAT('US$', FORMAT(agencia,4)) as 'Agencia US$',
                CONCAT('US$', FORMAT(almacen,4)) as 'Almacen US$',
                CONCAT('US$', FORMAT(papeleria,4)) as 'Papelería US$',
                CONCAT('US$', FORMAT(transporte,4)) as 'Transporte US$',
                CONCAT('US$', FORMAT(costototal,4))  as 'Costo Total US$',
                CONCAT('US$', FORMAT(costounit,4))  as 'Costo Unitario US$',
                CONCAT('C$', FORMAT(costototal * tc.tasa ,4)) as 'Costo Total C$',
                CONCAT('C$', FORMAT(costounit  * tc.tasa ,4)) as 'Costo Unitario C$',
                v.iddocumento
            FROM vw_articulosprorrateados v
            JOIN documentos d on d.iddocumento=v.iddocumento
            JOIN tiposcambio tc ON tc.idtc = d.idtipocambio
            JOIN vw_articulosdescritos a ON a.idarticulo = v.idarticulo
            """
            self.detailsmodel.setQuery( query )
    
            self.accountsModel.setQuery( """
            SELECT
                c.idcuenta, 
                cc.codigo, 
                cc.descripcion,
                CONCAT('C$',FORMAT(c.monto,4)) as 'Monto', 
                d.iddocumento 
            FROM cuentasxdocumento c 
            JOIN documentos d ON c.iddocumento = d.iddocumento
            JOIN cuentascontables cc ON cc.idcuenta = c.idcuenta
            JOIN liquidaciones l ON l.iddocumento = d.iddocumento 
            WHERE l.iddocumento IS NOT NULL
            ORDER BY nlinea
            """ )
    
            self.tableaccounts.setModel( self.accountsProxyModel )

            #query = 
            #self.totalsModel = QSqlQueryModel(query)
            
    
    
    
            #        Este objeto mapea una fila del modelo self.navproxymodel a los controles
    
            self.mapper.setSubmitPolicy( QDataWidgetMapper.ManualSubmit )
            self.mapper.setModel( self.navproxymodel )
            self.mapper.addMapping( self.txtPolicy, NDOCIMPRESO )
            self.mapper.addMapping( self.txtSource, PROCEDENCIA )
            self.mapper.addMapping( self.txtProvider, PROVEEDOR)
            self.mapper.addMapping( self.txtWarehouse, BODEGA )
            self.mapper.addMapping( self.txtExchangeRate, TCAMBIO )
            
            self.mapper.addMapping( self.dtPicker, FECHA )
            
            self.mapper.addMapping( self.sbAgency, AGENCIA )
            self.mapper.addMapping( self.sbFreight, FLETE )
            self.mapper.addMapping( self.sbInsurance, SEGURO )
            self.mapper.addMapping( self.sbOther, OTROS )
            
            self.mapper.addMapping( self.sbTransportation, TRANSPORTE )
            self.mapper.addMapping( self.sbStore, ALMACEN )
            self.mapper.addMapping( self.sbWeight, PESO )
            self.mapper.addMapping( self.sbPaperWork, PAPELERIA )
            
    
            self.tablenavigation.setModel( self.navproxymodel )
            self.tablenavigation.resizeColumnsToContents()
            self.tabledetails.setModel( self.detailsproxymodel )
            self.tabletotals.setModel(self.navproxyproxymodel)
        except UserWarning as inst:
            QMessageBox.critical(self, "Llantera Esquipulas", unicode(inst))
            logging.error(inst)
        except Exception as inst:
            logging.critical(inst)



    def cancel( self ):
        self.editmodel = None

        self.tablenavigation.setModel( self.navproxymodel )
        self.tabledetails.setModel( self.detailsproxymodel )
        self.tabletotals.setModel(self.navproxyproxymodel)

        self.tableaccounts.setModel( self.accountsProxyModel )
        
        self.status = 1
        self.navigate( 'last' )

    @property
    def printIdentifier(self):
        return self.txtPolicy.text()
    #def preview( self ):
        #printer = QPrinter()
        
        #printer.setOrientation(self.orientation)

        #printer.setPageSize(self.pageSize)
        #web = self.web + self.printIdentifier
         ##self.navmodel.record( self.mapper.currentIndex() ).value( 'Número de Liquidación' ).toString()

        #report = frmReportes( web, self.user, printer,self )
        #report.exec_()

    def newDocument( self ):
        """
        Slot documentation goes here.
        """
        try:
            if not QSqlDatabase.database().isOpen:
                if not QSqlDatabase.database().open():
                    raise UserWarning( u"No se pudo establecer una conexión con la base de datos" )
            
            query = QSqlQuery( "SELECT idtc FROM tiposcambio LIMIT 1" )

            query.exec_()
            if not query.first():
                raise UserWarning( u"No existen tipos de cambio en la base de datos" )

            self.editmodel = LiquidacionModel( self.user.uid )
            self.editmodel.applyISO = self.ckISO.isChecked()
            self.addLine()
            query = QSqlQuery( """
            SELECT 
                c.idcostoagregado,
                valorcosto,
                factorpeso,
                idtipocosto 
            FROM costosagregados c 
            LEFT JOIN tsim t on c.idcostoagregado=t.idtsim 
            WHERE activo=1 AND idtipocosto IN (%d,%d,%d,%d)
            """ % (constantes.IVA, constantes.SPE, constantes.TSIM, constantes.ISO))
            if not query.exec_():
                raise UserWarning( "No se pudo ejecutar la consulta para obtener los valores de los impuestos" )
            elif not query.size()==4:
                raise UserWarning( "No se pudieron obtener los valores de los impuestos" )
#TODO: Deberian acaso los valores de iva, spe, tsim, iso cambiar cuando cambie la fecha???            
            while query.next():
                if query.value( 3 ).toInt()[0] == 1: #IVA
                    self.editmodel.ivaId = query.value( 0 ).toInt()[0]
                    self.editmodel.ivaRate = Decimal( query.value( 1 ).toString() )
                elif query.value( 3 ).toInt()[0] == 4: #SPE
                    self.editmodel.speId = query.value( 0 ).toInt()[0]
                    self.editmodel.speTotal = Decimal( query.value( 1 ).toString() )
                elif query.value( 3 ).toInt()[0] == 5: #TSIM
                    self.editmodel.tsimId = query.value( 0 ).toInt()[0]
                    self.editmodel.tsimRate = Decimal( query.value( 1 ).toString() )
                    self.editmodel.weightFactor = Decimal( query.value( 2 ).toString() )
                elif query.value( 3 ).toInt()[0] == 6: #ISO
                    self.editmodel.isoId = query.value( 0 ).toInt()[0]
                    self.editmodel.isoRate = Decimal( query.value( 1 ).toString() )
        
            providersModel = QSqlQueryModel()
            providersModel.setQuery( """
            SELECT idpersona, nombre FROM personas p WHERE tipopersona = 2 AND activo = 1
            """ )
            if not providersModel.rowCount() > 0:
                raise UserWarning("No existen proveedores en el sistema")
            self.cbProvider.setModel( providersModel )
            self.cbProvider.setModelColumn( 1 )

            warehouseModel = QSqlQueryModel()
            warehouseModel.setQuery( """
            SELECT idbodega, nombrebodega 
            FROM bodegas b
            ORDER BY idbodega  
            """ )
            if not warehouseModel.rowCount() > 0:
                raise UserWarning("No existen bodegas en el sistema")
            self.cbWarehouse.setModel( warehouseModel )
            self.cbWarehouse.setModelColumn( 1 )

            delegate = LiquidacionDelegate()
            if delegate.prods.rowCount()==0:
                raise UserWarning("No hay articulos en existencia")
                



            self.tabnavigation.setEnabled( False )
            self.tabWidget.setCurrentIndex( 0 )
            self.tabledetails.setModel( self.editmodel )
            
            self.tabledetails.setItemDelegate( delegate )
            self.tabledetails.setEditTriggers( QAbstractItemView.EditKeyPressed | QAbstractItemView.AnyKeyPressed | QAbstractItemView.DoubleClicked )




            self.accountseditdelegate = AccountsSelectorDelegate( QSqlQuery( """
            SELECT c.idcuenta, c.codigo, c.descripcion 
            FROM cuentascontables c 
            JOIN cuentascontables p ON c.padre = p.idcuenta AND p.padre != 1
            WHERE c.padre != 1 AND c.idcuenta != %s
            """ % movimientos.INVENTARIO ),True )
            

            self.dtPicker.setMaximumDateTime(QDateTime.currentDateTime())
            self.dtPicker.setDateTime(QDateTime.currentDateTime() )

            
            self.tabletotals.setModel( self.editmodel.totalsModel )
            self.tabledetails.setColumnHidden( IDDOCUMENTOT, False )

            self.tableaccounts.setModel(None)
            self.status = 2

        except UserWarning as inst:
            self.status = 1
            QMessageBox.critical(self, "Llantera Esquipulas", unicode(inst))
            logging.error(inst)
        except Exception as inst:
            QMessageBox.critical(self, "Llantera Esquipulas", u"Hubo un error al intentar iniciar una nueva liquidación")
            self.status = 1
            logging.critical(inst)
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()





    @pyqtSlot( "int" )
    def on_tabWidget_currentChanged( self, id ):
            self.xdockWidget.setVisible( True if  not id else False )



    @pyqtSlot( "QString" )
    def on_txtPolicy_textChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.printedDocumentNumber = p0

    @pyqtSlot( "QString" )
    def on_txtSource_textChanged( self, p0 ):
        if not self.editmodel is None:
            self.editmodel.origin = p0            

    @pyqtSlot( "double" )
    def on_sbStore_valueChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.storeTotal = Decimal(str(p0)) if not p0 == "" else Decimal( 0 )
            self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.lines[0].itemId )

    @pyqtSlot( "double" )
    def on_sbAgency_valueChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.agencyTotal = Decimal( str(p0) ) if not p0 == "" else Decimal( 0 )
            self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.lines[0].itemId )


    @pyqtSlot( "double" )
    def on_sbPaperWork_valueChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.paperworkRate = Decimal(str(p0)) if not p0 == "" else Decimal( 0 )
            self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.lines[0].itemId )


    @pyqtSlot( "double" )
    def on_sbTransportation_valueChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.transportRate = Decimal(str(p0)) if not p0 == "" else Decimal( 0 )
            self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.lines[0].itemId )

    @pyqtSlot( "double" )
    def on_sbWeight_valueChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.weight = Decimal(str(p0)) if not p0 == "" else Decimal( 0 )
            self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.lines[0].itemId )

    @pyqtSlot( "double" )
    def on_sbFreight_valueChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.freightTotal = Decimal(str(p0)) if not p0 == "" else Decimal( 0 )
            self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.lines[0].itemId )

    @pyqtSlot( "double" )
    def on_sbInsurance_valueChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.insuranceTotal = Decimal(str(p0)) if not p0 == "" else Decimal( 0 )
            self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.lines[0].itemId )

    @pyqtSlot( "double" )
    def on_sbOther_valueChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.otherTotal = Decimal(str(p0)) if not p0 == "" else Decimal( 0 )
            self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.lines[0].itemId )

    @pyqtSlot( "int" )
    def on_cbWarehouse_currentIndexChanged( self, index ):
        if not self.editmodel is None:
            self.editmodel.warehouseId = self.cbWarehouse.model().index( index, 0 ).data().toInt()[0]
            #el iva solo se aplica cuando la bodega es 1
            self.editmodel.applyIVA = True if self.editmodel.warehouseId == 1 else False
            self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.lines[0].itemId )

    @pyqtSlot( "int" )
    def on_cbProvider_currentIndexChanged( self, index ):
        if not self.editmodel is None:
            self.editmodel.providerId = self.cbProvider.model().index( index, 0 ).data().toInt()[0]


    @pyqtSlot( "int" )
    def on_ckISO_stateChanged( self, status ):
        if not self.editmodel is None:
            self.editmodel.applyISO = True if status == Qt.Checked else False
            self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.lines[0].itemId )

            if status == Qt.Checked:
                self.ckTaxes.setChecked(False)

    @pyqtSlot( "int" )
    def on_ckTaxes_stateChanged( self, status ):
        if not self.editmodel is None:
            self.editmodel.applyTaxes = True if status == Qt.Unchecked else False
            self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.lines[0].itemId )

            if status == Qt.Checked:
                self.ckISO.setChecked(False)


    def loadModels( self ):
        """
        Esta función se ejecuta en el constructor del formulario mediante un QTimer,
        carga los formularios por primera vez
        """
        self.updateModels()
        self.navigate( 'last' )
        self.status = 1

    def save( self ):
        """
        Guardar el documento actual
        """
        if QMessageBox.question(self, "Llantera Esquipulas", u"¿Esta seguro que desea guardar?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            if self.status ==2:
                if self.editmodel.valid:
                    if self.editmodel.save():
                        QMessageBox.information( self,
                             "Llantera Esquipulas" ,
                             u"El documento se ha guardado con éxito")
                        self.editmodel = None
                        self.updateModels()
                        self.status = 1
                        self.navigate( 'last' )
                        
                    else:
                        QMessageBox.critical( self,
                            "Llantera Esquipulas" ,
                             "Ha ocurrido un error al guardar el documento")


                else:
                    try:
                        QMessageBox.warning( self,"Llantera Esquipulas" ,self.editmodel.validError)
                    except AttributeError:
                        QMessageBox.warning( self,"Llantera Esquipulas" ,u"El documento no puede guardarse ya que la información no esta completa")
            elif self.status == 3:
                if self.accountsEditModel.valid:
                    if self.accountsEditModel.save():
                        QMessageBox.information(self, "Llantera Esquipulas", "Las cuentas contables se han guardado correctamente")
                        self.updateModels()
                        self.status = 1
                        self.navigate('last')
                    else:
                        QMessageBox.critical(self, "Llantera Esquipulas", "Hubo un error al guardar las cuentas contables")
                else:
                    QMessageBox.critical("Existe un error con sus cuentas contables, reviselo antes de guardar")
                
                    
    def updateArticles(self):
        """
        Actualizar la lista de articulos
        """
        query = QSqlQuery()
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning(u"No se pudo conectar con la base de datos")



            self.tabledetails.itemDelegate().update(query)
            for line in [line for line in self.editmodel.lines if line.itemId != 0]:
                line.update(query)
                
        except UserWarning as inst:
            QMessageBox.warning(self, "Llantera Esquipulas", unicode(inst))
            logging.error(query.lastError().text())
            logging.error(unicode(inst))
            self.cancel()
        except Exception as inst:
            QMessageBox.critical(self, "Llantera Esquipulas", "Hubo un error fatal al tratar de actualizar la lista de articulos, el sistema no puede recuperarse" + \
                                                             " y sus cambios se han perdido")
            logging.error(query.lastError().text())
            logging.critical(unicode(inst))
            self.cancel()

    def editAccounts(self):
        """
        Editar las cuentas contables
        """
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning(u"No se pudo abrir la conexión con la base de datos")
            docid = self.navmodel.record( self.mapper.currentIndex() ).value( IDDOCUMENTO ).toInt()[0]
            self.xdockWidget.setCollapsed(False)
            self.accountsEditModel = LiquidacionAccountsModel(docid, self.user)
            accountsdelegate = AccountsSelectorDelegate(QSqlQuery( """
             SELECT c.idcuenta, c.codigo, c.descripcion
             FROM cuentascontables c
             JOIN cuentascontables p ON c.padre = p.idcuenta AND p.padre != 1
             WHERE c.padre != 1 AND c.idcuenta != 22
             """ ),True )
            self.tableaccounts.setItemDelegate( accountsdelegate )
            
            self.tableaccounts.setModel(self.accountsEditModel)

            self.accountsEditModel.insertRows( 0,2 )
            
            line = AccountsSelectorLine()
            line.itemId = int(movimientos.INVENTARIO)
            line.code = "110 003 001 000 000"
            line.name = "INV Inventario de Bodega"

            line.amount = Decimal(self.navmodel.record( self.mapper.currentIndex() ).value( TOTALC ).toString())
            self.accountsEditModel.lines[0] = line
            self.tabWidget.setCurrentIndex( 0 )
            
            self.tableaccounts.resizeColumnsToContents()
            self.status = 3
        except UserWarning as inst:
            QMessageBox.critical(self, "Llantera Esquipulas", unicode(inst))
            self.tableaccounts.setModel( self.accountsProxyModel )
            logging.error(unicode(inst))
            self.status = 1
        except Exception as inst:
            QMessageBox.critical(self, "Llantera Esquipulas", u"El sistema no pudo iniciar la edición de las cuentas contables")
            logging.critical(unicode(inst))
            self.tableaccounts.setModel( self.accountsProxyModel )
            self.status = 1

    def addActionsToToolBar(self):
        self.actionEditAccounts = self.createAction(text="Editar cuentas contables", icon=":/icons/res/view-bank-account.png", slot=self.editAccounts)
        self.actionUpdateArticles = self.createAction(text="Actualizar lista de articulos", icon=":/icons/res/view-refresh.png", slot=self.updateArticles)

        self.toolBar.addActions([
            self.actionNew,
            self.actionEditAccounts,
            self.actionPreview,
            self.actionPrint,
            self.actionSave,
            self.actionCancel,
            self.actionUpdateArticles
        ])
        self.toolBar.addSeparator()
        self.toolBar.addActions([
            self.actionGoFirst,
            self.actionGoPrevious,
            self.actionGoLast,
            self.actionGoNext,
            self.actionGoLast
        ])


class LiquidacionNavModel(QSqlQueryModel):
    def data(self, index, role = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if index.column() in  (TOTALD, IMPUESTOTOTAL, CIFTOTAL, FOBTOTAL):
                return moneyfmt(Decimal(super(LiquidacionNavModel, self).data(index, role).toString()),4,"US$")
            elif index.column() == TOTALC:
                return moneyfmt(Decimal(super(LiquidacionNavModel, self).data(index, role).toString()),4,"C$")
        return super(LiquidacionNavModel, self).data(index, role)