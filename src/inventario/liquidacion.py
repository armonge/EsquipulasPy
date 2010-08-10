# -*- coding: utf-8 -*-

"""
Module implementing frmLiquidacion.
"""
from decimal import Decimal
import functools
from PyQt4.QtGui import QMainWindow, QAbstractItemView, QDoubleValidator, QSortFilterProxyModel, QDataWidgetMapper, QTableView, QMessageBox, QPrinter
from PyQt4.QtCore import pyqtSlot, SIGNAL, QDateTime, Qt, QTimer
from PyQt4.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from ui.Ui_liquidacion import Ui_frmLiquidacion

import utility.constantes
from utility.reports import frmReportes
from utility.base import Base
from utility.accountselector import  AccountsSelectorDelegate, AccountsSelectorLine
from document.liquidacion.liquidacionmodel import LiquidacionModel
from document.liquidacion.liquidaciondelegate import LiquidacionDelegate


#navigation model
IDDOCUMENTO, NDOCIMPRESO, FECHA, PROCEDENCIA, AGENCIA, ALMACEN, FLETE, SEGURO, OTROS, TRANSPORTE, PAPELERIA, PESO, PROVEEDOR, BODEGA, ISO, TCAMBIO = range( 16 )

#details model
IDARTICULO, DESCRIPCION, UNIDADES, COSTOCOMPRA, FOB, FLETEP, SEGUROP, OTROSP, CIF, IMPUESTOSP, COMISION, AGENCIAP, ALMACENP, PAPELERIAP, TRANSPORTEP, IDDOCUMENTOT = range( 16 )

#accounts model
IDCUENTA, CODCUENTA, NCUENTA, MONTOCUENTA, IDDOCUMENTOC = range( 5 )
class frmLiquidacion( QMainWindow, Ui_frmLiquidacion, Base ):
    """
    Class documentation goes here.
    """
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
        self.status = True

        self.doubleValidator = QDoubleValidator( 0, 10000, 4, self )
        self.txtAgency.setValidator( self.doubleValidator )
        self.txtStore.setValidator( self.doubleValidator )
        self.txtPaperWork.setValidator( self.doubleValidator )
        self.txtTransportation.setValidator( self.doubleValidator )
        self.txtWeight.setValidator( self.doubleValidator )
        self.txtFreight.setValidator( self.doubleValidator )
        self.txtInsurance.setValidator( self.doubleValidator )
        self.txtOther.setValidator( self.doubleValidator )

        self.xdockWidget.setVisible( False )

#        El modelo principal
        self.navmodel = QSqlQueryModel( self )
#        El modelo que filtra a self.navmodel
        self.navproxymodel = QSortFilterProxyModel( self )
        self.navproxymodel.setSourceModel( self.navmodel )
        self.navproxymodel.setFilterKeyColumn( -1 )
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
        self.detailsproxymodel.setFilterRegExp( "^"+self.navmodel.record( index ).value( "iddocumento" ).toString()+"$" )

        self.accountsProxyModel.setFilterKeyColumn( IDDOCUMENTOC )
        self.accountsProxyModel.setFilterRegExp( "^"+self.navmodel.record( index ).value( "iddocumento" ).toString()+"$" )

        self.tablenavigation.selectRow( self.mapper.currentIndex() )
        
        self.ckISO.setChecked( True if self.navmodel.record( index ).value( "iso" ).toDouble()[0] != 0 else False )

    def setControls( self, status ):
        """
        En esta funcion cambio el estado enabled de todos los items en el formulario
        @param status: false = editando        true = navegando
        """
        self.txtPolicy.setReadOnly( status )
        self.txtAgency.setReadOnly( status )
        self.txtFreight.setReadOnly( status )
        self.txtInsurance.setReadOnly( status )
        self.txtOther.setReadOnly( status )
        self.txtSource.setReadOnly( status )
        self.txtWeight.setReadOnly( status )
        self.txtPaperWork.setReadOnly( status )
        self.txtStore.setReadOnly( status )
        self.txtTransportation.setReadOnly( status )
        self.ckISO.setEnabled( not status )
        self.tablenavigation.setEnabled(status)


        self.swProvider.setCurrentIndex( 0 if status else 1 )
        self.swWarehouse.setCurrentIndex( 1 if status else 0 )


        self.dtPicker.setReadOnly( status )
        self.cbWarehouse.setEnabled( not status )

        self.actionCancel.setVisible( not status )
        self.actionSave.setVisible( not status )
        self.actionPreview.setVisible( status )
        self.actionNew.setVisible( status )


        self.actionGoFirst.setVisible( status )
        self.actionGoPrevious.setVisible( status )
        self.actionGoNext.setVisible( status )
        self.actionGoLast.setVisible( status )
        
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
        
        self.tableaccounts.setColumnHidden( IDCUENTA, True )
        self.tableaccounts.setColumnHidden( IDDOCUMENTOC, True )
        
        self.tabnavigation.setEnabled( status )
        
        if not status: #editando
            self.tableaccounts.setEditTriggers( QTableView.AllEditTriggers )
            self.tabledetails.addAction( self.actionDeleteRow )
            
            self.txtAgency.setText("0")
            self.txtFreight.setText("0")
            self.txtInsurance.setText("0")
            self.txtTransportation.setText("15")
            self.txtOther.setText("0")
            self.txtPaperWork.setText("15")
            self.txtStore.setText("0")
            self.txtWeight.setText("0")
            self.txtPolicy.setText('')
            self.txtSource.setText('')
            
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
                    raise UserWarning( "No se pudo conectar con la base de datos para recuperar los documentos" )

            self.navmodel.setQuery( u"""
                SELECT 
                    d.iddocumento as iddocumento, 
                    d.ndocimpreso as 'Número de Liquidación', 
                    DATE(d.fechacreacion) as 'Fecha', 
                    l.procedencia as 'Procedencia',
                    l.totalagencia as 'Agencia',
                    l.totalalmacen as 'Almacén',
                    l.fletetotal as 'Flete',
                    l.segurototal as 'Seguro',
                    l.otrosgastos as 'Otros Gastos',
                    l.porcentajetransporte as 'Transporte',
                    l.porcentajepapeleria as 'Papelería',
                    l.peso as 'Peso',
                    p.nombre as 'Proveedor', 
                    b.nombrebodega as 'Bodega',
                    SUM(IFNULL(valorcosto,0)) as  'ISO',
                    tc.tasa as 'Tasa de Cambio'
                FROM documentos d 
                JOIN liquidaciones l ON d.iddocumento = l.iddocumento
                JOIN personasxdocumento pxd ON pxd.iddocumento = d.iddocumento
                JOIN personas p ON p.idpersona = pxd.idpersona AND p.tipopersona = %d
                JOIN bodegas b ON b.idbodega = d.idbodega
                LEFT JOIN costosxdocumento cxd ON d.iddocumento = cxd.iddocumento
                LEFT JOIN costosagregados ca ON cxd.idcostoagregado = ca.idcostoagregado AND ca.idtipocosto = 6 
                JOIN tiposcambio tc ON d.idtipocambio = tc.idtc
                GROUP BY d.iddocumento
            """ % utility.constantes.PROVEEDOR )
    
            self.detailsmodel.setQuery( u"""
            SELECT 
                a.idarticulo as 'Id',
                descripcion as 'Descripción', 
                unidades as 'Cantidad', 
                CONCAT('U$', FORMAT(costocompra,4)) as 'Costo Compra US$', 
                CONCAT('U$', FORMAT(fob,4)) as 'FOB US$', 
                CONCAT('U$', FORMAT(flete,4)) as 'Flete US$', 
                CONCAT('U$', FORMAT(seguro,4)) as 'Seguro US$', 
                CONCAT('U$', FORMAT(otrosgastos,4)) as 'Otros Gastos US$', 
                CONCAT('U$', FORMAT(cif,4)) as 'CIF US$', 
                CONCAT('U$', FORMAT(impuestos,4)) as 'Impuestos US$', 
                CONCAT('U$', FORMAT(comision,4)) as 'Comisión US$', 
                CONCAT('U$', FORMAT(agencia,4)) as 'Agencia US$', 
                CONCAT('U$', FORMAT(almacen,4)) as 'Almacen US$', 
                CONCAT('U$', FORMAT(papeleria,4)) as 'Papelería US$', 
                CONCAT('U$', FORMAT(transporte,4)) as 'Transporte US$', 
                iddocumento
            FROM vw_articulosprorrateados v
            JOIN vw_articulosdescritos a ON a.idarticulo = v.idarticulo
            """ )
    
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
            
    
    
    
            #        Este objeto mapea una fila del modelo self.navproxymodel a los controles
    
            self.mapper.setSubmitPolicy( QDataWidgetMapper.ManualSubmit )
            self.mapper.setModel( self.navproxymodel )
            self.mapper.addMapping( self.txtPolicy, NDOCIMPRESO )
            self.mapper.addMapping( self.dtPicker, FECHA )
            self.mapper.addMapping( self.txtProvider, PROVEEDOR, "text" )
            self.mapper.addMapping( self.txtAgency, AGENCIA )
            self.mapper.addMapping( self.txtFreight, FLETE )
            self.mapper.addMapping( self.txtInsurance, SEGURO )
            self.mapper.addMapping( self.txtOther, OTROS )
            self.mapper.addMapping( self.txtSource, PROCEDENCIA )
            self.mapper.addMapping( self.txtTransportation, TRANSPORTE )
            self.mapper.addMapping( self.txtStore, ALMACEN )
            self.mapper.addMapping( self.txtWeight, PESO )
            self.mapper.addMapping( self.txtPaperWork, PAPELERIA )
            self.mapper.addMapping( self.txtWarehouse, BODEGA )
            self.mapper.addMapping( self.txtExchangeRate, TCAMBIO )
    
            self.tablenavigation.setModel( self.navproxymodel )
            self.tablenavigation.resizeColumnsToContents()
            self.tabledetails.setModel( self.detailsproxymodel )
        except UserWarning as inst:
            QMessageBox.critical(self, "Llantera Esquipulas", str(inst))
        except Exception as inst:
            print inst



    @pyqtSlot(  )
    def on_actionCancel_activated( self ):
        self.editmodel = None

        self.tablenavigation.setModel( self.navproxymodel )
        self.tabledetails.setModel( self.detailsproxymodel )


        self.tableaccounts.setModel( self.accountsProxyModel )

        
        
        self.status = True
        self.navigate( 'last' )
        

    @pyqtSlot(  )
    def on_actionPreview_activated( self ):
        printer = QPrinter()
        printer.setOrientation(QPrinter.Landscape)
        printer.setPageSize(QPrinter.Letter)
        web = "liquidaciones.php?doc=%d" % self.navmodel.record( self.mapper.currentIndex() ).value( "iddocumento" ).toInt()[0] 
        report = frmReportes( web, self.user, printer,self )
        report.exec_()

    @pyqtSlot(  )
    def on_actionNew_activated( self ):
        """
        Slot documentation goes here.
        """
        try:
            if not QSqlDatabase.database().isOpen:
                if not QSqlDatabase.database().open():
                    raise UserWarning( u"No se pudo establecer una conexión con la base de datos" )
            
            query = QSqlQuery( "SELECT idtc FROM tiposcambio LIMIT 1" )
            
            if not query.first():
                raise UserWarning( u"No existen tipos de cambio en la base de datos" )

            self.editmodel = LiquidacionModel( self.user.uid )
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
            """ % (utility.constantes.IVA, utility.constantes.SPE, utility.constantes.TSIM, utility.constantes.ISO))
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
                


            self.status = False
            self.tabnavigation.setEnabled( False )
            self.tabWidget.setCurrentIndex( 0 )
            self.tabledetails.setModel( self.editmodel )
            
            self.tabledetails.setItemDelegate( delegate )
            self.tabledetails.setEditTriggers( QAbstractItemView.EditKeyPressed | QAbstractItemView.AnyKeyPressed | QAbstractItemView.DoubleClicked )




            self.accountseditdelegate = AccountsSelectorDelegate( QSqlQuery( """
            SELECT c.idcuenta, c.codigo, c.descripcion 
            FROM cuentascontables c 
            JOIN cuentascontables p ON c.padre = p.idcuenta AND p.padre != 1
            WHERE c.padre != 1 AND c.idcuenta != 22
            """ ),True )
            self.tableaccounts.setItemDelegate( self.accountseditdelegate )
            self.tableaccounts.setModel( self.editmodel.accountsModel )
            
            self.editmodel.accountsModel.insertRows( 0 )

            line = AccountsSelectorLine()
            line.itemId = 22
            line.code = "110 003 001 000 000"
            line.name = "INV Inventario de Bodega"
            
            self.editmodel.accountsModel.lines[0] = line
            self.dtPicker.setMaximumDateTime(QDateTime.currentDateTime())
            self.dtPicker.setDateTime(QDateTime.currentDateTime() )

            self.tabletotals.setModel( self.editmodel.totalsModel )
            self.tabledetails.setColumnHidden( IDDOCUMENTOT, False )
        except UserWarning as inst:
            self.status = True
            QMessageBox.warning(self, "Llantera Esquipulas", str(inst))
        except Exception as inst:
            self.status = True
            print inst
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()



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


    @pyqtSlot( "int" )
    def on_tabWidget_currentChanged( self, id ):
            self.xdockWidget.setVisible( True if  not id else False )

    @pyqtSlot( "QString" )
    def on_txtAgency_textChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.agencyTotal = Decimal( p0 ) if not p0 == "" else Decimal( 0 )
            self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.lines[0].itemId )
            

    @pyqtSlot( "QString" )
    def on_txtStore_textChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.storeTotal = Decimal( p0 ) if not p0 == "" else Decimal( 0 )
            self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.lines[0].itemId )



    @pyqtSlot( "QString" )
    def on_txtPaperWork_textChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.paperworkRate = Decimal( p0 ) if not p0 == "" else Decimal( 0 )
            self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.lines[0].itemId )


    @pyqtSlot( "QString" )
    def on_txtTransportation_textChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.transportRate = Decimal( p0 ) if not p0 == "" else Decimal( 0 )
            self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.lines[0].itemId )

    @pyqtSlot( "QString" )
    def on_txtWeight_textChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.weight = Decimal( p0 ) if not p0 == "" else Decimal( 0 )
            self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.lines[0].itemId )

    @pyqtSlot( "QString" )
    def on_txtFreight_textChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.freightTotal = Decimal( p0 ) if not p0 == "" else Decimal( 0 )
            self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.lines[0].itemId )

    @pyqtSlot( "QString" )
    def on_txtInsurance_textChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.insuranceTotal = Decimal( p0 ) if not p0 == "" else Decimal( 0 )
            self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.lines[0].itemId )

    @pyqtSlot( "QString" )
    def on_txtOther_textChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.otherTotal = Decimal( p0 ) if not p0 == "" else Decimal( 0 )
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




