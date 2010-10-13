# -*- coding: utf-8 -*-
"""
Module implementing FrmEntradaCompra.
"""
from decimal import Decimal
import logging

from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QMessageBox, \
QAbstractItemView, QCompleter, qApp
from PyQt4.QtCore import pyqtSlot, Qt, QTimer, QDateTime, QModelIndex
from PyQt4.QtSql import QSqlQueryModel, QSqlQuery

from utility.base import Base
from ui.Ui_entradacompra import Ui_frmEntradaCompra
from document.entradacompra import EntradaCompraModel, EntradaCompraDelegate

from utility.moneyfmt import moneyfmt
from utility.singleselectionmodel import SingleSelectionModel
from utility import constantes


#controles
IDDOCUMENTO, NDOCIMPRESO, FECHA, PROVEEDOR , OBSERVACION, SUBTOTALC, IVAC, \
TOTALC, TOTALD, TIPOPAGO = range( 10 )
#table
IDARTICULO, DESCRIPCION, CANTIDAD, PRECIOC, PRECIOD, TOTALPRODC, \
TOTALPRODD, IDDOCUMENTOT = range( 8 )
class FrmEntradaCompra( QMainWindow, Ui_frmEntradaCompra, Base ):
    """
    Implementacion de la interfaz grafica para entrada compra
    """
    web = "entradaslocales.php?doc="
    def __init__( self, parent = None ):
        """
        Constructor
        """
        super( FrmEntradaCompra, self ).__init__( parent )
        self.setupUi( self )
        self.parentWindow = parent
        Base.__init__( self )





        self.status = True


#        El modelo principal
        self.navmodel = QSqlQueryModel( self )
#        El modelo que filtra a self.navmodel
        self.navproxymodel = RONavigationModel( self )
        self.navproxymodel.setSourceModel( self.navmodel )
#        Este es el modelo con los datos de la con los detalles
        self.detailsmodel = QSqlQueryModel( self )
#        Este es el filtro del modelo anterior
        self.detailsproxymodel = QSortFilterProxyModel( self )
        self.detailsproxymodel.setSourceModel( self.detailsmodel )

        self.providersModel = QSqlQueryModel()

        #inicializando el documento
        self.editmodel = None



        #general events
        self.rbCash.clicked[bool].connect( self.updatePay )
        self.rbCheck.clicked[bool].connect( self.updatePay )
        self.rbCredit.clicked[bool].connect( self.updatePay )

        QTimer.singleShot( 0, self.loadModels )



    def updatePay( self, _checked ):
        if not self.editmodel is None:
            if self.sender() in ( self.rbCash, self.rbCheck ):
                self.editmodel.paytipe = 1
            elif self.sender() == self.rbCredit:
                self.editmodel.paytipe = 0

            self.editmodel.isCheck = self.sender() == self.rbCheck

    def updateModels( self ):
        """
        Recargar todos los modelos
        """
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( "No se pudo conectar con la base de datos para obtener los documentos" )


#        El modelo principal

            self.navmodel.setQuery( """
            SELECT  
                d.iddocumento,
                d.ndocimpreso AS 'Numero de Entrada',
                d.fechacreacion AS 'Fecha',
                p.nombre as Proveedor,
                d.observacion,
                (@subtotalc:=( ( d.total / (1 + (ca.valorcosto / 100)  ) ) )  * tc.tasa  ) AS 'Subtotal C$',
                ( @subtotalc * (  (ca.valorcosto / 100) ) )  AS 'IVA',
                d.total * tc.tasa AS 'Total C$',
                d.total AS 'Total US$',
                escontado as tipopago
            FROM documentos d  
            JOIN personasxdocumento pxd ON pxd.iddocumento = d.iddocumento 
            JOIN personas p ON pxd.idpersona = p.idpersona AND p.tipopersona = %d
            JOIN articulosxdocumento axd ON axd.iddocumento = d.iddocumento
            JOIN costosxdocumento cxd ON cxd.iddocumento = d.iddocumento
            JOIN costosagregados ca ON cxd.idcostoagregado = ca.idcostoagregado
            JOIN tiposcambio tc ON tc.idtc = d.idtipocambio
            WHERE d.idtipodoc = %d
            GROUP BY d.iddocumento
            """ % ( constantes.PROVEEDOR, constantes.IDENTRADALOCAL ) )
    #        El modelo que filtra a self.navmodel
            self.navproxymodel = RONavigationModel( self )
            self.navproxymodel.setSourceModel( self.navmodel )
            self.navproxymodel.setFilterKeyColumn( -1 )
            self.navproxymodel.setFilterCaseSensitivity ( Qt.CaseInsensitive )
    #        Este es el modelo con los datos de la tabla para navegar
            self.detailsmodel = QSqlQueryModel( self )
            self.detailsmodel.setQuery( u"""
                 SELECT 
                    a.idarticulo as id,  
                    CONCAT(m.nombre,' ' , c.nombre, ' ' , subc.nombre) as 'Descripción',  
                    axd.unidades as 'Cantidad',   
                    CONCAT('C$',FORMAT((axd.costounit * tc.tasa),4)) as 'Precio C$',
                    CONCAT('US$', axd.costounit) as 'Precio US$',  
                    CONCAT('C$',FORMAT(((axd.unidades * axd.costounit) * tc.tasa),4)) as 'Total C$',
                    CONCAT('US$',FORMAT((axd.unidades * axd.costounit),4)) as 'Total US$',
                    d.iddocumento
                FROM documentos d  
                JOIN articulosxdocumento axd ON axd.iddocumento=d.iddocumento  
                JOIN articulos a ON a.idarticulo = axd.idarticulo  
                JOIN marcas m ON m.idmarca = a.idmarca  
                JOIN categorias subc ON a.idcategoria = subc.idcategoria  
                JOIN categorias c ON subc.padre = c. idcategoria  
                JOIN tiposcambio tc ON tc.idtc = d.idtipocambio
                WHERE d.idtipodoc = %d
            """ % constantes.IDENTRADALOCAL )
    #        Este es el filtro del modelo anterior
            self.detailsproxymodel = QSortFilterProxyModel( self )
            self.detailsproxymodel.setSourceModel( self.detailsmodel )


    #        Este objeto mapea una fila del modelo self.navproxymodel a los controles

            self.mapper.setModel( self.navproxymodel )
            self.mapper.addMapping( self.txtDocumentNumber, NDOCIMPRESO )
            self.mapper.addMapping( self.txtObservations, OBSERVACION )
            self.mapper.addMapping( self.dtPicker, FECHA )
            self.mapper.addMapping( self.txtProvider, PROVEEDOR, "text" )
            self.mapper.addMapping( self.lblSubtotal, SUBTOTALC, "text" )
            self.mapper.addMapping( self.lblIVA, IVAC, "text" )
            self.mapper.addMapping( self.lblTotal, TOTALC, "text" )
            self.mapper.addMapping( self.lblTotalD, TOTALD, "text" )

    #        asignar los modelos a sus tablas
            self.tablenavigation.setModel( self.navproxymodel )
            self.tabledetails.setModel( self.detailsproxymodel )



        except UserWarning as inst:
            QMessageBox.critical( self, qApp.organizationName(), unicode( inst ) )
            logging.error( unicode( inst ) )
        except Exception as inst:
            QMessageBox.critical( self, qApp.organizationName(), "No se pudo cargar la lista de entradas locales" )
            logging.critical( unicode( inst ) )
        finally:
            if self.database.isOpen():
                self.database.close()

    def updateEditModels( self ):
#            Rellenar el combobox de los proveedores
        self.providersModel.setQuery( """
            SELECT idpersona , nombre AS proveedor 
            FROM personas
            WHERE tipopersona = 2
        """ )
        if not self.providersModel.rowCount( QModelIndex() ) > 0:
            raise UserWarning( "No existen proveedores en la base de datos" )
        self.cbProvider.setModel( self.providersModel )
        self.cbProvider.setModelColumn( 1 )

        completer = QCompleter()
        completer.setCaseSensitivity( Qt.CaseInsensitive )
        completer.setModel( self.providersModel )
        completer.setCompletionColumn( 1 )

        self.editmodel.providerId = self.providersModel.record( self.cbProvider.currentIndex() ).value( "idpersona" ).toInt()[0]
        query = QSqlQuery( """
        SELECT idarticulo, Descripcion as descripcion FROM vw_articulosdescritos
        """ )
        if not query.size() > 0:
            raise UserWarning( "No existen productos en la base de datos" )
        prods = SingleSelectionModel()
        query.exec_()
        while query.next():
            prods.items.append( [
                query.value( 0 ).toInt()[0],
                query.value( 1 ).toString()
                       ] )

        prods.headers = ["idarticulo", "Articulo"]
        self.delegate.prods = prods


    def updateLabels( self ):
        if not self.editmodel is None:
            self.lblSubtotal.setText( moneyfmt( self.editmodel.subtotalC, 4, "C$" ) )
            self.lblIVA.setText( moneyfmt( self.editmodel.IVAC, 4, "C$" ) )
            self.lblTotal.setText( moneyfmt( self.editmodel.totalC, 4, "C$" ) )
            self.lblTotalD.setText( moneyfmt( self.editmodel.totalD, 4, "US$" ) )
    @property
    def printIdentifier( self ):
        return self.navmodel.record( self.mapper.currentIndex() ).value( "iddocumento" ).toString()



    def newDocument( self ):
        """
        activar todos los controles, llenar los modelos necesarios, crear el modelo EntradaCompraModel, aniadir una linea a la tabla
        """
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( u"No se pudo establecer la conexión con la base de datos" )

            self.editmodel = EntradaCompraModel()
            self.editmodel.uid = self.user.uid
            self.tabledetails.setModel( self.editmodel )
            self.delegate = EntradaCompraDelegate()
            self.tabledetails.setItemDelegate( self.delegate )

            query = QSqlQuery( """
            SELECT idcostoagregado, valorcosto 
            FROM costosagregados c 
            WHERE idtipocosto = %d AND activo = 1 
            LIMIT 1
            """ % constantes.IVA )
            if not query.exec_():
                raise UserWarning( "No se pudo obtener el valor del IVA para iniciar la entrada compra" )
            if not query.size() == 1:
                raise UserWarning( "No se pudo obtener el valor del IVA para iniciar la entrada compra" )
            query.first()
            self.editmodel.idIVA = query.value( 0 ).toInt()[0]
            self.editmodel.rateIVA = Decimal( query.value( 1 ).toString() )


            self.updateEditModels()


            self.rbCash.click()

            self.addLine()
            self.dtPicker.setDateTime( QDateTime.currentDateTime() )
            self.editmodel.providerId = self.providersModel.record( self.cbProvider.currentIndex() ).value( "idpersona" ).toInt()[0]

            self.editmodel.dataChanged[QModelIndex, QModelIndex].connect( self.updateLabels )
            self.tabledetails.setColumnWidth( DESCRIPCION, 250 )
            self.status = False
        except UserWarning as inst:
            QMessageBox.critical( self, qApp.organizationName(), unicode( inst ) )
            logging.error( unicode( inst ) )
#            self.status = True
        except Exception as inst:
            QMessageBox.critical( self, qApp.organizationName(), "No se pudo iniciar una nueva entrada compra" )
            print inst
            logging.error( unicode( inst ) )
#            self.status = True

        if self.database.isOpen():
            self.database.close()


    def cancel( self ):
        """
        Aca se cancela la edicion del documento
        """
        if QMessageBox.question( self, qApp.organizationName(), u"¿Desea realmente cancelar?", QMessageBox.Yes | QMessageBox.No ) == QMessageBox.Yes:
            self.editmodel = None

            self.tablenavigation.setModel( self.navproxymodel )
            self.tabledetails.setModel( self.detailsproxymodel )
            self.tabledetails.removeAction( self.actionDeleteRow )

            self.status = True


    def updateDetailFilter( self, index ):
        self.detailsproxymodel.setFilterKeyColumn( IDDOCUMENTOT )
        self.detailsproxymodel.setFilterRegExp( "^" + self.navmodel.record( index ).value( "iddocumento" ).toString() + "$" )
        self.tablenavigation.selectRow( self.mapper.currentIndex() )

        paytype = self.navmodel.record( index ).value( "tipopago" ).toInt()[0]
        if paytype == 0:
            self.rbCredit.setChecked( True )
        elif paytype == 1:
            self.rbCash.setChecked( True )




    def setControls( self, status ):
        """
        @param status: false = editando        true = navegando
        """
        self.txtDocumentNumber.setReadOnly( status )
        self.actionPrint.setVisible( status )
        self.dtPicker.setReadOnly( status )
        self.txtObservations.setReadOnly( status )

        self.actionSave.setVisible( not status )
        self.actionCancel.setVisible( not status )
        self.rbCash.setEnabled( not status )
        self.rbCheck.setEnabled( not status )
        self.rbCredit.setEnabled( not status )

        self.tabnavigation.setEnabled( status )
        self.actionNew.setVisible( status )
        self.actionGoFirst.setVisible( status )
        self.actionGoPrevious.setVisible( status )
        self.actionGoNext.setVisible( status )
        self.actionGoLast.setVisible( status )
        self.actionPreview.setVisible( status )


        if status:
            self.navigate( 'last' )
            self.swProvider.setCurrentIndex( 1 )
            self.tabledetails.removeAction( self.actionDeleteRow )
            self.tabledetails.setEditTriggers( QAbstractItemView.NoEditTriggers )

            #ocultar columnas en tabledetails
            self.tabledetails.setColumnHidden( IDARTICULO, True )
            self.tabledetails.setColumnHidden( IDDOCUMENTOT, True )
            #ocultar columnas en tablenavigation
            self.tablenavigation.setColumnHidden( TIPOPAGO, True )
            self.tablenavigation.setColumnHidden( IDDOCUMENTO, True )
            self.tablenavigation.setColumnHidden( OBSERVACION, True )
            self.tablenavigation.setColumnHidden( SUBTOTALC, True )
            self.tablenavigation.setColumnHidden( IVAC, True )
        else:
            self.tabledetails.addAction( self.actionDeleteRow )
            self.tabWidget.setCurrentIndex( 0 )
            self.txtDocumentNumber.setText( "" )
            self.txtObservations.setPlainText( "" )
            self.swProvider.setCurrentIndex( 0 )

            self.lblSubtotal.setText( "C$0.00" )
            self.lblIVA.setText( "C$0.00" )
            self.lblTotal.setText( "C$0.00" )
            self.tabledetails.setEditTriggers( QAbstractItemView.AllEditTriggers )
            self.tabledetails.setColumnHidden( IDARTICULO, True )


    @pyqtSlot( "QString" )
    def on_txtDocumentNumber_textChanged( self, text ):
        """
        Asignar el contenido al objeto documeto
        """
        if not self.editmodel is None:
            self.editmodel.printedDocumentNumber = text



    @pyqtSlot( "int" )
    def on_cbProvider_currentIndexChanged( self, index ):
        """
        asignar proveedor al objeto self.editmodel
        """
        if not self.editmodel is None:
            self.editmodel.providerId = self.providersModel.record( index ).value( "idpersona" ).toInt()[0]



class RONavigationModel( QSortFilterProxyModel ):
    """
    basicamente le da formato a la salida de mapper
    """
    def data( self, index, role = Qt.DisplayRole ):
        """
        Esta funcion redefine data en la clase base, es el metodo que se utiliza para mostrar los datos del modelo
        """
        value = QSortFilterProxyModel.data( self, index, role )
        if value.isValid() and role in ( Qt.EditRole, Qt.DisplayRole ):
            if index.column() in ( SUBTOTALC, IVAC, TOTALC ):
                return moneyfmt( Decimal( value.toString() ), 4, "C$" )
            elif index.column() == TOTALD:
                return moneyfmt( Decimal( value.toString() ), 4, "US$" )
        return value


