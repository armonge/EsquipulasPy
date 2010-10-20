# -*- coding: utf-8 -*-

"""
Module implementing frmLiquidacion.
"""
from PyQt4.QtCore import pyqtSlot, QDateTime, Qt, QTimer, QSettings, \
    QAbstractTableModel, QModelIndex
from PyQt4.QtGui import QAbstractItemView, QSortFilterProxyModel, \
    QDataWidgetMapper, QTableView, QMessageBox, QPrinter, qApp, QIcon
from PyQt4.QtSql import QSqlQuery, QSqlQueryModel
from decimal import Decimal
from document.liquidacion import LiquidacionModel, LiquidacionAccountsModel, \
    LiquidacionDelegate
from ui.Ui_liquidacion import Ui_FrmLiquidacion
from utility import constantes, movimientos
from utility.accountselector import AccountsSelectorDelegate, \
    AccountsSelectorLine
from utility.base import Base
from utility.decorators import if_edit_model
from utility.moneyfmt import moneyfmt
import logging



#from document.liquidacion.liquidaciondelegate import LiquidacionDelegate


#navigation model
IDDOCUMENTO, NDOCIMPRESO, FECHA, PROCEDENCIA, AGENCIA, ALMACEN, FLETE, SEGURO, \
OTROS, TRANSPORTE, PAPELERIA, PESO, PROVEEDOR, BODEGA, ISO, TCAMBIO, \
ESTADO, FOBTOTAL, CIFTOTAL, IMPUESTOTOTAL, TOTALD, TOTALC, EXONERADO = range( 23 )


#details model
IDARTICULO, DESCRIPCION, UNIDADES, COSTOCOMPRA, FOB, FLETEP, SEGUROP, OTROSP, \
CIF, IMPUESTOSP, COMISION, AGENCIAP, ALMACENP, PAPELERIAP, TRANSPORTEP, \
DTOTALD, DUNITD, DTOTALC, DUNITC, IDDOCUMENTOT = range( 20 )

#accounts model
IDCUENTA, CODCUENTA, NCUENTA, MONTOCUENTA, IDDOCUMENTOC = range( 5 )
class FrmLiquidacion( Ui_FrmLiquidacion, Base ):
    """
    Class documentation goes here.
    """
    web = "liquidaciones.php?doc="
    orientation = QPrinter.Landscape
    pageSize = QPrinter.Legal
    def __init__( self, parent = None ):
        """
        @param parent: El formulario padre de este documento
        """
        super( FrmLiquidacion, self ).__init__( parent )



        #los modelos de edicion
        self.editmodel = None
        self.accountseditmodel = None



        self.status = 1

        if self.tabWidget.currentIndex() == 1:
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
        """
        @ivar: El modelo de edición
        @type: LiquidacionModel
        """

        self.editdelegate = None
        """
        @ivar: El delegado usado en la tabla de detalles
        @type: LiquidacionDelegate
        """

        self.accountseditdelegate = None
        """
        @ivar: El delegado para la edición de las cuentas contables
        @type: AccountsSelectorDelegate
        """


        self.tabledetails.setOrder( 1, 3 )

        QTimer.singleShot( 0, self.loadModels )

    def updateDetailFilter( self, index ):

        self.detailsproxymodel.setFilterKeyColumn( IDDOCUMENTOT )
        self.detailsproxymodel.setFilterRegExp( "^%d$" % self.navmodel.record( 
                                        index ).value( IDDOCUMENTO ).toInt()[0] )

        self.accountsProxyModel.setFilterKeyColumn( IDDOCUMENTOC )
        self.accountsProxyModel.setFilterRegExp( "^%d$" % self.navmodel.record( 
                                        index ).value( IDDOCUMENTO ).toInt()[0] )

        self.navproxyproxymodel.setFilterKeyColumn( IDDOCUMENTO )
        self.navproxyproxymodel.setFilterRegExp( "^%d$" % self.navmodel.record( 
                                         index ).value( IDDOCUMENTO ).toInt()[0] )

        self.tablenavigation.selectRow( self.mapper.currentIndex() )

        self.ckISO.setChecked( True if self.navmodel.record( 
                                        index ).value( ISO ).toDouble()[0] != 0 else False )

        self.ckTaxes.setChecked( True if self.navmodel.record( 
                                         index ).value( EXONERADO ).toDouble()[0] != 0 else False )




        if self.user.hasRole( 'contabilidad' ):
            estado = self.navmodel.record( index ).value( ESTADO ).toInt()[0]
            if estado == constantes.INCOMPLETO:
                self.actionEditAccounts.setVisible( True )
            else:
                self.actionEditAccounts.setVisible( False )


    def setControls( self, status ):
        """
        En esta funcion cambio el estado enabled de todos los items en el formulario
        @param status: 1 = navegando 2 = añadiendo productos 3 = añadiendo cuentas contables
        """

        self.txtPolicy.setReadOnly( status == 1 or status == 3 )
        self.txtSource.setReadOnly( status == 1 or status == 3 )

        self.sbAgency.setReadOnly( status == 1 or status == 3 )
        self.sbFreight.setReadOnly( status == 1 or status == 3 )
        self.sbInsurance.setReadOnly( status == 1 or status == 3 )
        self.sbOther.setReadOnly( status == 1 or status == 3 )

        self.sbWeight.setReadOnly( status == 1 or status == 3 )
        self.sbPaperWork.setReadOnly( status == 1 or status == 3 )
        self.sbStore.setReadOnly( status == 1 or status == 3 )
        self.sbTransportation.setReadOnly( status == 1 or status == 3 )
        self.ckISO.setEnabled( not ( status == 1 or status == 3 ) )
        self.ckTaxes.setEnabled( not ( status == 1 or status == 3 ) )
        self.tablenavigation.setEnabled( status == 1 )


        self.swProvider.setCurrentIndex( 0 if status in ( 1, 3 ) else 1 )
        self.swWarehouse.setCurrentIndex( 1 if status in ( 1, 3 ) else 0 )


        self.dtPicker.setReadOnly( status != 2 )
        self.cbWarehouse.setEnabled( status == 2 )

        self.actionUpdateArticles.setVisible( status == 2 )
        self.actionCancel.setVisible( not status == 1 )
        self.actionSave.setVisible( not status == 1 )
        self.actionPreview.setVisible( status == 1 )
        self.actionPrint.setVisible( status == 1 )
        self.actionNew.setVisible( status == 1 )


        self.actionGoFirst.setVisible( status == 1 )
        self.actionGoPrevious.setVisible( status == 1 )
        self.actionGoNext.setVisible( status == 1 )
        self.actionGoLast.setVisible( status == 1 )

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
        self.tablenavigation.setColumnHidden( ESTADO, True )
        self.tablenavigation.setColumnHidden( EXONERADO, True )





        self.tableaccounts.setColumnHidden( IDCUENTA, True )
        self.tableaccounts.setColumnHidden( IDDOCUMENTOC, True )


        self.tabnavigation.setEnabled( status )
        if status == 1:

#            self.sbAgency.setPrefix("US$ ")
#            self.sbStore.setPrefix("US$ ")

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
            self.tabletotals.setColumnHidden( NDOCIMPRESO, True )
            self.tabletotals.setColumnHidden( ESTADO, True )
            self.tabletotals.setColumnHidden( FECHA, True )
            self.tabletotals.setColumnHidden( PROCEDENCIA, True )
            self.tabletotals.setColumnHidden( PESO, True )
            self.tabletotals.setColumnHidden( PROVEEDOR, True )
            self.tabletotals.setColumnHidden( TCAMBIO, True )
            self.tabletotals.setColumnHidden( EXONERADO, True )

            self.tabledetails.removeAction( self.actionDeleteRow )

            self.tableaccounts.setEditTriggers( QTableView.NoEditTriggers )

        elif status == 2: #editando
            self.sbAgency.setPrefix( "C$ " )
            self.sbStore.setPrefix( "C$ " )
            self.tableaccounts.setEditTriggers( QTableView.AllEditTriggers )
            self.tabledetails.addAction( self.actionDeleteRow )

            self.txtPolicy.setText( "" )
            self.txtSource.setText( "" )

            self.sbAgency.setValue( 0 )
            self.sbFreight.setValue( 0 )
            self.sbInsurance.setValue( 0 )
            self.sbOther.setValue( 0 )

            self.sbWeight.setValue( 0 )
            self.sbPaperWork.setValue( 0 )
            self.sbStore.setValue( 0 )
            self.sbTransportation.setValue( 0 )

            for column in range( self.tabletotals.model().columnCount() ):
                self.tabletotals.setColumnWidth( column, 170 )

            for x in range( self.tabletotals.model().columnCount() ):
                self.tabletotals.setColumnHidden( x, False )

            if self.user.hasRole( "contabilidad" ):
                self.actionEditAccounts.setVisible( False )

        elif status == 3:
            self.tabTotalsAccounts.setCurrentIndex( 0 )
            self.tableaccounts.setEditTriggers( QTableView.AllEditTriggers )
            self.actionEditAccounts.setVisible( False )




    def updateLabels( self ):
        pass

    def updateModels( self ):
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( "No se pudo conectar con la base de datos " )
            query = u"""
                SELECT
                    d.iddocumento,
                    d.ndocimpreso AS 'Número de Liquidación',
                    d.fecha AS 'Fecha',
                    d.procedencia AS 'Procedencia',
                    ROUND(d.totalagencia * d.tasa,4) AS 'Agencia',
                    ROUND(d.totalalmacen * d.tasa,4) AS 'Almacen',
                    d.fletetotal AS 'Flete',
                    d.segurototal as 'Seguro',
                    d.otrosgastos AS 'Otros Gastos',
                    d.porcentajetransporte AS 'Transporte',
                    d.porcentajepapeleria AS 'Papelería',
                    d.peso AS 'Peso',
                    d.Proveedor AS 'Proveedor',
                    d.bodega AS 'Bodega',
                    IF(SUM(IF(ca.idtipocosto = %d AND ca.valorcosto IS NOT NULL,ca.valorcosto,0)) != 0, 1,0) as  'APLICA ISO',
                    d.tasa,
                    d.estado,
                    lt.fobtotal,
                    lt.ciftotal,
                    lt.impuestototal,
                    d.totald AS 'Total US$',
                    d.totalc AS 'Total C$',
                    IF(SUM(IFNULL(ca.valorcosto,0)) + SUM(caxl.dai +caxl.isc) != 0, 0,1) as  'EXONERADO'
                FROM vw_liquidacionesguardadas d
                JOIN vw_liquidacioncontotales lt ON lt.iddocumento = d.iddocumento
                LEFT JOIN costosxdocumento cxd ON d.iddocumento = cxd.iddocumento
                LEFT JOIN costosagregados ca ON cxd.idcostoagregado = ca.idcostoagregado AND ca.idtipocosto IN ( %d,%d)
                JOIN articulosxdocumento axd ON d.iddocumento = axd.iddocumento
                JOIN costosxarticuloliquidacion caxl ON caxl.idarticuloxdocumento = axd.idarticuloxdocumento
                GROUP BY d.iddocumento;
            """ % ( constantes.ISO, constantes.ISO, constantes.IVA )
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
            ORDER BY v.nlinea
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


            #Este objeto mapea una fila del modelo self.navproxymodel a los controles

            self.mapper.setSubmitPolicy( QDataWidgetMapper.ManualSubmit )
            self.mapper.setModel( self.navproxymodel )
            self.mapper.addMapping( self.txtPolicy, NDOCIMPRESO )
            self.mapper.addMapping( self.txtSource, PROCEDENCIA )
            self.mapper.addMapping( self.txtProvider, PROVEEDOR )
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
            self.tabletotals.setModel( self.navproxyproxymodel )
        except UserWarning as inst:
            QMessageBox.critical( self, qApp.organizationName(),
                                   unicode( inst ) )
            logging.error( inst )
        except Exception as inst:
            logging.critical( inst )



    def cancel( self ):
        self.editmodel = None

        self.tablenavigation.setModel( self.navproxymodel )
        self.tabledetails.setModel( self.detailsproxymodel )
        self.tabletotals.setModel( self.navproxyproxymodel )

        self.tableaccounts.setModel( self.accountsProxyModel )

        self.status = 1
        self.navigate( 'last' )

    @property
    def printIdentifier( self ):
        return self.navmodel.record( self.mapper.currentIndex() ).value( IDDOCUMENTO ).toString()


    def newDocument( self ):
        """
        Slot documentation goes here.
        """
        query = QSqlQuery()
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( u"No se pudo establecer una conexión "\
                                       + "con la base de datos" )

            query.prepare( "SELECT idtc FROM tiposcambio LIMIT 1" )
            query.exec_()
            if not query.first():
                raise UserWarning( u"No existen tipos de cambio en "\
                                   + "la base de datos" )

            self.editmodel = LiquidacionModel( self.user.uid )
            self.editmodel.applyISO = self.ckISO.isChecked()
            self.addLine()
            query.prepare( """
            SELECT 
                c.idcostoagregado,
                valorcosto,
                factorpeso,
                idtipocosto 
            FROM costosagregados c 
            LEFT JOIN tsim t on c.idcostoagregado=t.idtsim 
            WHERE activo=1 AND idtipocosto IN (%d,%d,%d,%d)
            LIMIT 4
            """ % ( constantes.IVA,
                    constantes.SPE,
                    constantes.TSIM,
                    constantes.ISO ) )
            if not query.exec_():
                raise UserWarning( "No se pudo ejecutar la consulta para "\
                                   + "obtener los valores de los impuestos" )
            elif not query.size() == 4:
                raise UserWarning( "No se pudieron obtener los valores "\
                                   + "de los impuestos" )
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
            SELECT idpersona, nombre
            FROM personas p
            WHERE tipopersona = %d AND activo = 1
            """ % constantes.PROVEEDOR )
            if not providersModel.rowCount() > 0:
                raise UserWarning( "No existen proveedores en el sistema" )
            self.cbProvider.setModel( providersModel )
            self.cbProvider.setModelColumn( 1 )

            warehouseModel = QSqlQueryModel()
            warehouseModel.setQuery( """
            SELECT idbodega, nombrebodega 
            FROM bodegas b
            ORDER BY idbodega  
            """ )
            if not warehouseModel.rowCount() > 0:
                raise UserWarning( "No existen bodegas en el sistema" )
            self.cbWarehouse.setModel( warehouseModel )
            self.cbWarehouse.setModelColumn( 1 )

            self.editdelegate = LiquidacionDelegate()
            self.updateArticleList( query )
            if self.editdelegate.prods.rowCount() == 0:
                raise UserWarning( u"El sistema no tiene registrado ningún "\
                                   + u"tipo de articulo, por favor añada "\
                                   + "articulos antes de hacer una "\
                                   + u"liquidación" )




            self.tabnavigation.setEnabled( False )
            self.tabWidget.setCurrentIndex( 0 )
            self.tabledetails.setModel( self.editmodel )

            self.tabledetails.setItemDelegate( self.editdelegate )
            self.tabledetails.setEditTriggers( QAbstractItemView.EditKeyPressed
                                            | QAbstractItemView.AnyKeyPressed
                                             | QAbstractItemView.DoubleClicked )




            self.accountseditdelegate = AccountsSelectorDelegate( 
            QSqlQuery( """
                SELECT c.idcuenta, c.codigo, c.descripcion 
                FROM cuentascontables c 
                JOIN cuentascontables p ON c.padre = p.idcuenta AND p.padre != 1
                WHERE c.padre != 1 AND c.idcuenta != %s
            """ % movimientos.INVENTARIO ), True )

            self.dtPicker.setDateTime( QDateTime.currentDateTime() )
            self.dtPicker.setMaximumDateTime( QDateTime.currentDateTime() )



            self.tabletotals.setModel( self.editmodel.totalsModel )
            self.tabledetails.setColumnHidden( IDDOCUMENTOT, False )

            self.tableaccounts.setModel( None )
            self.tabledetails.setColumnWidth( DESCRIPCION, 250 )



            self.status = 2

        except UserWarning as inst:
            self.status = 1
            QMessageBox.critical( self,
                                  qApp.organizationName(), unicode( inst ) )
            logging.error( inst )
        except Exception as inst:
            QMessageBox.critical( self, qApp.organizationName(),
                                  u"Hubo un error al intentar iniciar "\
                                  + u"una nueva liquidación" )
            self.status = 1
            logging.critical( inst )
        finally:
            if self.database.isOpen():
                self.database.close()

    def updateArticleList( self, query ):
        """
        Actualizar los valores de los articulos para el delegado
        @param query: El objeto consulta en el que se van a tratar de
        obtener los nuevos valores de los articulos
        @type query: QSqlQuery
        """

        query.prepare( """
        SELECT
            idarticulo,
            Descripcion AS 'Articulo',
            dai,
            isc,
            Comision as comision
        FROM vw_articulosconcostosactuales
        WHERE activo=1
        """ )

        query.exec_()
        self.editdelegate.prods = ArticlesModel()
        while query.next():
            self.editdelegate.prods.items.append( [
                query.value( 0 ).toInt()[0],
                query.value( 1 ).toString(),
                Decimal( query.value( 2 ).toString() ),
                Decimal( query.value( 3 ).toString() ),
                Decimal( query.value( 4 ).toString() ),
                                    ] )

    @pyqtSlot( QDateTime )
    @if_edit_model
    def on_dtPicker_dateTimeChanged( self, datetime ):
        super( FrmLiquidacion, self ).on_dtPicker_dateTimeChanged( datetime )
        self.txtExchangeRate.setText( 
                             str( self.editmodel.exchangeRate ) )


    @pyqtSlot( int )
    def on_tabWidget_currentChanged( self, _id ):
        self.xdockWidget.setVisible( True if  not _id else False )



    @pyqtSlot( unicode )
    @if_edit_model
    def on_txtPolicy_textChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        self.editmodel.printedDocumentNumber = p0

    @pyqtSlot( unicode )
    @if_edit_model
    def on_txtSource_textChanged( self, p0 ):
        self.editmodel.origin = p0

    @pyqtSlot( float )
    @if_edit_model
    def on_sbStore_valueChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        self.editmodel.storeTotalC = Decimal( str( p0 ) )
        self.editmodel.reset()

    @pyqtSlot( float )
    @if_edit_model
    def on_sbAgency_valueChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        self.editmodel.agencyTotalC = Decimal( str( p0 ) )
        self.editmodel.reset()


    @pyqtSlot( float )
    @if_edit_model
    def on_sbPaperWork_valueChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        self.editmodel.paperworkRate = Decimal( str( p0 ) )
        self.editmodel.reset()


    @pyqtSlot( float )
    @if_edit_model
    def on_sbTransportation_valueChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        self.editmodel.transportRate = Decimal( str( p0 ) )
        self.editmodel.reset()

    @pyqtSlot( float )
    @if_edit_model
    def on_sbWeight_valueChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        self.editmodel.weight = Decimal( str( p0 ) )
        self.editmodel.reset()

    @pyqtSlot( float )
    @if_edit_model
    def on_sbFreight_valueChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        self.editmodel.freightTotal = Decimal( str( p0 ) )
        self.editmodel.reset()

    @pyqtSlot( float )
    @if_edit_model
    def on_sbInsurance_valueChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        self.editmodel.insuranceTotal = Decimal( str( p0 ) )
        self.editmodel.reset()

    @pyqtSlot( float )
    @if_edit_model
    def on_sbOther_valueChanged( self, p0 ):
        """
        Slot documentation goes here.
        """
        self.editmodel.otherTotal = Decimal( str( p0 ) )
        self.editmodel.reset()

    @pyqtSlot( int )
    @if_edit_model
    def on_cbWarehouse_currentIndexChanged( self, index ):
        self.editmodel.warehouseId = self.cbWarehouse.model().index( index, 0 ).data().toInt()[0]
        self.editmodel.reset()

    @pyqtSlot( int )
    @if_edit_model
    def on_cbProvider_currentIndexChanged( self, index ):
        self.editmodel.providerId = self.cbProvider.model().index( index, 0 ).data().toInt()[0]


    @pyqtSlot( int )
    @if_edit_model
    def on_ckISO_stateChanged( self, status ):
        self.editmodel.applyISO = True if status == Qt.Checked else False
        self.editmodel.setData( self.editmodel.index( 0, 0 ),
                                self.editmodel.lines[0].itemId )

        if status == Qt.Checked:
            self.ckTaxes.setChecked( False )

    @pyqtSlot( int )
    @if_edit_model
    def on_ckTaxes_stateChanged( self, status ):
        self.editmodel.applyTaxes = True if status == Qt.Unchecked else False
        self.editmodel.reset()

        if status == Qt.Checked:
            self.ckISO.setChecked( False )


    def loadModels( self ):
        """
        Esta función se ejecuta en el constructor del formulario mediante
        un QTimer, carga los formularios por primera vez
        """
        self.updateModels()
        self.navigate( 'last' )
        self.status = 1


    def closeEvent( self, event ):
        u"""
        reimplementando por que self.status no sigue el formato True,. False
        """
        if self.status != 1:
            if not QMessageBox.question( self,
            qApp.organizationName(),
            u"¿Está seguro que desea salir?",
            QMessageBox.Yes | QMessageBox.No ) == QMessageBox.Yes:
                event.ignore()

        #Guardar el tamaño y la posición
        settings = QSettings()
        settings.setValue( self.windowTitle() + "/Geometry", self.saveGeometry() )
        settings.setValue( self.windowTitle() + "/State", self.saveState() )

        #quitar la toolbar
        self.parentWindow.removeToolBar( self.toolBar )


    def save( self ):
        """
        Guardar el documento actual
        """
        if QMessageBox.question( self, qApp.organizationName(),
                      u"¿Esta seguro que desea guardar?",
                      QMessageBox.Yes | QMessageBox.No ) == QMessageBox.Yes:
            if self.status == 2:
                if self.editmodel.valid:
                    if self.editmodel.save():
                        QMessageBox.information( self,
                             qApp.organizationName(),
                             u"El documento se ha guardado con éxito" )
                        self.editmodel = None
                        self.updateModels()
                        self.status = 1
                        self.navigate( 'last' )

                    else:
                        QMessageBox.critical( self,
                            qApp.organizationName(),
                             "Ha ocurrido un error al guardar el documento" )


                else:
                    try:
                        QMessageBox.warning( self, qApp.organizationName(),
                                             self.editmodel.validError )
                    except AttributeError:
                        QMessageBox.warning( self, qApp.organizationName(),
                            u"El documento no puede guardarse ya que la información no esta completa" )
            elif self.status == 3:
                if self.accountsEditModel.valid:
                    if self.accountsEditModel.save():
                        QMessageBox.information( self, qApp.organizationName(),
                            "Las cuentas contables se han guardado correctamente" )
                        self.updateModels()
                        self.status = 1
                        self.navigate( 'last' )
                    else:
                        QMessageBox.critical( self, qApp.organizationName(),
                            "Hubo un error al guardar las cuentas contables" )
                else:
                    QMessageBox.critical( self, qApp.organizationName(),
                        "Existe un error con sus cuentas contables," \
                            + u" reviselo antes de guardar" )


    def updateArticles( self ):
        """
        Actualizar la lista de articulos
        """
        query = QSqlQuery()
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( u"No se pudo conectar con la base de datos" )



            self.updateArticleList( query )
            self.editmodel.updateLines( query )


            providersModel = QSqlQueryModel()
            providersModel.setQuery( """
            SELECT idpersona, nombre 
            FROM personas p 
            WHERE tipopersona = 2 AND activo = 1
            """ )
            if not providersModel.rowCount() > 0:
                raise UserWarning( "No existen proveedores en el sistema" )
            self.cbProvider.setModel( providersModel )
            self.cbProvider.setModelColumn( 1 )

            warehouseModel = QSqlQueryModel()
            warehouseModel.setQuery( """
            SELECT idbodega, nombrebodega
            FROM bodegas b
            ORDER BY idbodega
            """ )
            if not warehouseModel.rowCount() > 0:
                raise UserWarning( "No existen bodegas en el sistema" )
            self.cbWarehouse.setModel( warehouseModel )
            self.cbWarehouse.setModelColumn( 1 )

            self.cbWarehouse.setCurrentIndex( -1 )
            self.cbProvider.setCurrentIndex( -1 )



        except UserWarning as inst:
            QMessageBox.warning( self, qApp.organizationName(), unicode( inst ) )
            logging.error( query.lastError().text() )
            logging.error( unicode( inst ) )
            self.cancel()
        except Exception as inst:
            QMessageBox.critical( self, qApp.organizationName(),
                "Hubo un error fatal al tratar de actualizar la lista " \
                + "de articulos, el sistema no puede recuperarse" \
                + " y sus cambios se han perdido" )
            logging.error( query.lastError().text() )
            logging.critical( unicode( inst ) )
            self.cancel()

    def editAccounts( self ):
        """
        Editar las cuentas contables
        """
        try:
            if not self.user.hasRole( "contabilidad" ):
                raise UserWarning( "Usted no tiene permisos para editar "\
                                  + "cuentas contables" )
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( u"No se pudo abrir la conexión con la base de datos" )
            docid = self.navmodel.record( self.mapper.currentIndex() ).value( 
                                                        IDDOCUMENTO ).toInt()[0]
            self.xdockWidget.setCollapsed( False )
            self.accountsEditModel = LiquidacionAccountsModel( docid, self.user )
            accountsdelegate = AccountsSelectorDelegate( QSqlQuery( """
             SELECT c.idcuenta, c.codigo, c.descripcion
             FROM cuentascontables c
             JOIN cuentascontables p ON c.padre = p.idcuenta AND p.padre != 1
             WHERE c.padre != 1 AND c.idcuenta != 22
             """ ), True )
            self.tableaccounts.setItemDelegate( accountsdelegate )

            self.tableaccounts.setModel( self.accountsEditModel )

            self.accountsEditModel.insertRows( 0, 2 )

            line = AccountsSelectorLine()
            line.itemId = int( movimientos.INVENTARIO )
            line.code = "110 003 001 000 000"
            line.name = "INV Inventario de Bodega"

            line.amount = Decimal( self.navmodel.record( 
                                        self.mapper.currentIndex()
                                        ).value( TOTALC ).toString()
                                         ).quantize( Decimal( '0.0001' ) )
            self.accountsEditModel.lines[0] = line
            self.tabWidget.setCurrentIndex( 0 )

            self.tableaccounts.resizeColumnsToContents()
            self.status = 3

        except UserWarning as inst:
            QMessageBox.critical( self, qApp.organizationName(),
                                  unicode( inst ) )
            self.tableaccounts.setModel( self.accountsProxyModel )
            logging.error( unicode( inst ) )
            self.status = 1

        except Exception as inst:
            QMessageBox.critical( self, qApp.organizationName(),
                                  u"El sistema no pudo iniciar la edición " \
                                  + " de las cuentas contables" )

            logging.critical( unicode( inst ) )
            self.tableaccounts.setModel( self.accountsProxyModel )
            self.status = 1

    def addActionsToToolBar( self ):
        self.actionUpdateArticles = self.createAction( 
                text = "Actualizar lista de articulos",
                icon = ":/icons/res/view-refresh.png",
                 slot = self.updateArticles )

        self.toolBar.addActions( [
            self.actionNew,
            self.actionPreview,
            self.actionPrint,
            self.actionSave,
            self.actionCancel,
            self.actionUpdateArticles
        ] )
        self.toolBar.addSeparator()
        self.toolBar.addActions( [
            self.actionGoFirst,
            self.actionGoPrevious,
            self.actionGoLast,
            self.actionGoNext,
            self.actionGoLast
        ] )
        self.toolBar.addSeparator()

        if self.user.hasRole( "contabilidad" ):
            self.action_edit_accounts = self.createAction( 
                 text = "Editar cuentas contables",
                 icon = ":/icons/res/view-bank-account.png",
                 slot = self.editAccounts )


            self.toolBar.addActions( [
                self.action_edit_accounts
                                     ] )
        action_toggle_details = self.xdockWidget.toggleViewAction()
        action_toggle_details.setIcon( QIcon( ":/icons/res/view-list-details.png" ) )
        self.toolBar.addAction( action_toggle_details )


class LiquidacionNavModel( QSqlQueryModel ):
    def data( self, index, role = Qt.DisplayRole ):
        if role == Qt.DisplayRole:
            if index.column() in  ( TOTALD, IMPUESTOTOTAL, CIFTOTAL, FOBTOTAL ):
                return moneyfmt( 
                     Decimal( super( LiquidacionNavModel, self ).data( index,
                                                         role ).toString() ),
                      4, "US$" )
            elif index.column() == TOTALC:
                return moneyfmt( 
                     Decimal( super( LiquidacionNavModel, self ).data( index,
                                                         role ).toString() ),
                     4, "C$" )
        return super( LiquidacionNavModel, self ).data( index, role )


class ArticlesModel( QAbstractTableModel ):
    def __init__( self ):
        super( ArticlesModel, self ).__init__()
        self.items = []

    def data( self, index, role = Qt.DisplayRole ):
        """
        darle formato a los campos de la tabla
        """
        if not index.isValid() or not ( 0 <= index.row() < len( self.items ) ):
            return ""
        line = self.items[index.row()]
        if role == Qt.DisplayRole:
            if index.column() in ( 2, 3 ):
                return str( line[index.column()] ) + "%"
            elif index.column() == 4:
                return moneyfmt( line[index.column()], 4, "US$" )
            return line[index.column()]
# 0 = id articulo, 1 = descripcion articulo, 2 = dai, 3 = isc, 4 = comision
        elif role == Qt.EditRole:
            return line[index.column()]



    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignLeft | Qt.AlignVCenter
            return Qt.AlignRight | Qt.AlignVCenter

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == 0:
                return "id"
            elif section == 1:
                return "Articulo"
            elif section == 2:
                return "DAI"
            elif section == 3:
                return "ISC"
            elif section == 4:
                return u"Comisión"
        return int( section + 1 )

    def rowCount( self, _index = QModelIndex() ):
        return len( self.items )

    def columnCount( self, _index = QModelIndex() ):
        return 5

