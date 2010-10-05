# -*- coding: utf-8 -*-
"""
Module implementing frmDevolucion.
"""
from decimal import Decimal
import logging

from PyQt4.QtCore import pyqtSlot, Qt, QTimer, \
     QDateTime, QModelIndex
from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QDataWidgetMapper, \
    QDialog, QTableView, QDialogButtonBox, QVBoxLayout, QAbstractItemView, QFormLayout, \
     QLineEdit,QMessageBox, qApp
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery

from ui.Ui_devolucion import Ui_frmDevoluciones
from utility.base import Base

from document.devolucion.devoluciondelegate import DevolucionDelegate
from document.devolucion.devolucionmodel import DevolucionModel
from document.devolucion.lineadevolucion import LineaDevolucion

from utility.moneyfmt import moneyfmt
from utility import constantes



#navmodel
IDDOCUMENTO, NDOCIMPRESO, FACTURA, CLIENTE, OBSERVACION, FECHA, SUBTOTAL, IMPUESTOS, COSTO, TOTAL, TASA, CONCEPTO, NOMBREBODEGA = range( 13 )
#detailsmodel
IDARTICULO, DESCRIPCION, CANTIDAD, PRECIO, TOTALPROD, IDDOCUMENTOT = range( 6 )
class FrmDevolucion( QMainWindow, Ui_frmDevoluciones, Base ):
    """
    Formulario para crear nuevas devoluciones
    """
    web = "devoluciones.php?doc="  
    def __init__( self,  parent = None ):
        """
        Constructor
        """
        super( FrmDevolucion, self ).__init__( parent )
        self.setupUi( self )
        self.parentWindow = parent
        Base.__init__( self )



        self.editmodel = None

        self.status = True

#        las acciones deberian de estar ocultas
        

#        El modelo principal
        self.navmodel = RONavigationModel( self )
#        El modelo que filtra a self.navmodel
        self.navproxymodel = QSortFilterProxyModel( self )
        self.navproxymodel.setSourceModel( self.navmodel )
#        Este es el modelo con los datos de la tabla para navegar
        self.detailsmodel = QSqlQueryModel( self )
#        Este es el filtro del modelo anterior
        self.detailsproxymodel = QSortFilterProxyModel( self )
        self.detailsproxymodel.setSourceModel( self.detailsmodel )



#        Cargar los modelos en un hilo aparte
        QTimer.singleShot( 0, self.loadModels )



    def addLine( self ):
        """
        Redefiniendo addLine, se supone que en una liquidacion no se pueden añadir lineas
        """
        raise RuntimeError( "Las devoluciones no deben de añadir lineas nuevas" )

    def updateModels( self ):
#        El modelo principal
        self.navmodel = RONavigationModel( self )
#        El modelo que filtra a self.navmodel
        self.navproxymodel = QSortFilterProxyModel( self )
        self.navproxymodel.setSourceModel( self.navmodel )
        self.navproxymodel.setFilterKeyColumn( -1 )
        self.navproxymodel.setFilterCaseSensitivity ( Qt.CaseInsensitive )

#        Este es el modelo con de la tabla con los detalles
        self.detailsmodel = QSqlQueryModel( self )
#        Este es el filtro del modelo anterior
        self.detailsproxymodel = QSortFilterProxyModel( self )
        self.detailsproxymodel.setSourceModel( self.detailsmodel )


        try:

            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open():
                    raise UserWarning(u"No se pudo abrir la conexión con la base de datos")
            query = u"""
             SELECT
                d.iddocumento,
                d.ndocimpreso AS 'Numero de Entrada',
                padre.ndocimpreso AS padre,
                p.nombre as 'Cliente',
                d.observacion,
                d.fechacreacion AS 'Fecha',
                (@subtotald:=(d.total / ( 1 + ( IF( ca.valorcosto IS NOT NULL , ca.valorcosto / 100, 0 ) )) ) ) AS subtotald,
                @subtotald * (IF( ca.valorcosto IS NOT NULL , ca.valorcosto / 100, 0 )  ) AS ivad,
                SUM( axd.costounit ) as costod,
                d.total AS totald,
                tc.tasa,
                c.descripcion AS 'Concepto',
                b.nombrebodega AS 'Bodega'
            FROM documentos d
            JOIN bodegas b ON d.idbodega = b.idbodega
            JOIN conceptos c ON c.idconcepto = d.idconcepto
            JOIN docpadrehijos dpd ON dpd.idhijo = d.iddocumento
            JOIN documentos padre ON dpd.idpadre = padre.iddocumento
            JOIN tiposcambio tc ON d.idtipocambio = tc.idtc
            JOIN personasxdocumento pd ON d.iddocumento=pd.iddocumento
            LEFT JOIN personas p ON p.idpersona=pd.idpersona
            JOIN articulosxdocumento axd ON axd.iddocumento = d.iddocumento
            LEFT JOIN costosxdocumento cxd ON cxd.iddocumento = padre.iddocumento
            LEFT JOIN costosagregados ca ON ca .idcostoagregado = cxd.idcostoagregado
            WHERE d.idtipodoc = %d AND p.tipopersona=%d
            GROUP BY d.iddocumento""" %(constantes.IDNC,constantes.CLIENTE) 
            
            self.navmodel.setQuery(query )

            self.detailsmodel.setQuery( u"""
            SELECT 
                ad.idarticulo, 
                ad.descripcion as 'Descripción', 
                axd.unidades as 'Cantidad', 
                axd.precioventa as 'Precio de venta',
                axd.unidades * axd.precioventa as Total,
                axd.iddocumento
            FROM articulosxdocumento axd
            JOIN vw_articulosdescritos ad ON axd.idarticulo = ad.idarticulo
            JOIN documentos d ON d.iddocumento = axd.iddocumento 
            WHERE d.idtipodoc = %d
            """ % constantes.IDNC)




            #        Este objeto mapea una fila del modelo self.navproxymodel a los controles

            self.mapper.setSubmitPolicy( QDataWidgetMapper.ManualSubmit )
            self.mapper.setModel( self.navproxymodel )
            self.mapper.addMapping( self.txtDocumentNumber, NDOCIMPRESO )
            self.mapper.addMapping( self.txtObservations, OBSERVACION )
            self.mapper.addMapping( self.dtPicker, FECHA )
            self.mapper.addMapping( self.txtClient, CLIENTE, "text" )
            self.mapper.addMapping( self.txtBill, FACTURA, "text" )
            self.mapper.addMapping( self.lblTotal, TOTAL, "text" )
            self.mapper.addMapping( self.lblSubtotal, SUBTOTAL, "text" )
            #self.mapper.addMapping( self.lblCost, COSTO, "text" )
            self.mapper.addMapping( self.lblTaxes, IMPUESTOS, "text" )
            self.mapper.addMapping( self.txtConcept, CONCEPTO, "text" )
            self.mapper.addMapping( self.txtWarehouse, NOMBREBODEGA, "text" )

    #        asignar los modelos a sus tablas
            self.tablenavigation.setModel( self.navproxymodel )
            self.tabledetails.setModel( self.detailsproxymodel )

            self.tablenavigation.setColumnHidden( IDDOCUMENTO, True )
            self.tablenavigation.setColumnHidden( OBSERVACION, True )
            self.tablenavigation.setColumnHidden( SUBTOTAL, True )
            self.tablenavigation.setColumnHidden( IMPUESTOS, True )
            self.tablenavigation.setColumnHidden( TASA, True )
            self.tablenavigation.setColumnHidden( COSTO, True )
            

            self.tablenavigation.resizeColumnsToContents()
            self.tablenavigation.horizontalHeader().setStretchLastSection(True)

        except UserWarning as inst:
            QMessageBox.critical(self, qApp.organizationName(), unicode(inst))
            logging.error(unicode(inst))
        except Exception as inst:
            logging.critical(unicode(inst))
            QMessageBox.critical(self, qApp.organizationName(), u"Hubo un error al cargar la lista de devoluciones")
            print inst
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()

    def updateDetailFilter( self, index ):
        self.detailsproxymodel.setFilterRegExp( self.navmodel.record( index ).value( "iddocumento" ).toString() )
        self.detailsproxymodel.setFilterKeyColumn( IDDOCUMENTOT )
        self.tablenavigation.selectRow( self.mapper.currentIndex() )

    def updateLabels( self ):
        self.lblTotal.setText( moneyfmt( self.editmodel.totalD, 4, "US$" ) + " / " + moneyfmt( self.editmodel.totalC, 4, "C$" ) )
        self.lblSubtotal.setText( moneyfmt( self.editmodel.subtotalD, 4, "US$" ) + " / " + moneyfmt( self.editmodel.subtotalC, 4, "C$" ) )
        self.lblTaxes.setText( moneyfmt( self.editmodel.ivaD, 4, "US$" ) + " / " + moneyfmt( self.editmodel.ivaC, 4, "C$" ) )
        #self.lblCost.setText( moneyfmt( self.editmodel.totalCostD, 4, "US$" ) + " / " + moneyfmt( self.editmodel.totalCostC, 4, "C$" ) )

    def setControls( self, status ):
        """
        En esta funcion cambio el estado enabled de todos los items en el formulario
        @param status: false = editando        true = navegando
        """
        self.actionPrint.setVisible(status)
        self.actionSave.setVisible( not status )
        self.actionCancel.setVisible( not status )
        self.tabnavigation.setEnabled( status )
        self.actionNew.setVisible( status )
        self.actionGoFirst.setVisible( status )
        self.actionGoPrevious.setVisible( status )
        self.actionGoNext.setVisible( status )
        self.actionGoLast.setVisible( status )
        self.actionPreview.setVisible( status )
        #self.txtDocumentNumber.setReadOnly( status )
        self.txtObservations.setReadOnly( status )
        self.dtPicker.setReadOnly( status )
        
        self.actionSave.setVisible( not status )
        self.actionCancel.setVisible( not status )
        
        self.swConcept.setCurrentIndex(1 if status else 0)
        if status:
            
            self.navigate( 'last' )
            self.tabledetails.setEditTriggers( QAbstractItemView.NoEditTriggers )
        else:
            self.txtClient.setText( self.editmodel.clientName )
            self.txtObservations.setPlainText( "" )
            self.lblTotal.setText( "US$0.0000 / C$0.0000" )
            #self.lblCost.setText( "US$0.0000 / C$0.0000" )
            self.lblTaxes.setText( "US$0.0000 / C$0.0000" )
            self.lblSubtotal.setText( "US$0.0000 / C$0.0000" )
            self.tabledetails.setEditTriggers( QAbstractItemView.AllEditTriggers )
            self.tabWidget.setCurrentIndex( 0 )
            
#            mostrar las columnas para el modeo edicion u ocultar para navegación
        self.tabledetails.setColumnHidden( IDARTICULO, status )
        self.tabledetails.setColumnHidden( IDDOCUMENTOT, status )

    @pyqtSlot( "QString" )
    def on_txtDocumentNumber_textEdited( self, string ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.printedDocumentNumber = string

    @pyqtSlot( "QString" )
    def on_txtnotacredito_textEdited( self, string ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.numnotacredito = string


    @pyqtSlot(  )
    def on_txtObservations_textChanged( self ):
        """
        Slot documentation goes here.
        """
        if not self.editmodel is None:
            self.editmodel.observations = self.txtObservations.toPlainText()

    def newDocument( self ):
        """
        Slot documentation goes here.
        """
        query = QSqlQuery( )
        try:
            if not QSqlDatabase.database().open():
                raise Exception( u"No se pudo establecer una conexión con la base de datos" )
            
            self.conceptsmodel = QSqlQueryModel()
            self.conceptsmodel.setQuery("""
            SELECT idconcepto, descripcion 
            FROM conceptos 
            WHERE idtipodoc = %d
            """ % constantes.IDNC)
            
            if self.conceptsmodel.rowCount()==0:
                raise UserWarning( u"No existen conceptos para devolución")
                
            
            dlgbill = DlgSelectBill()
            if dlgbill.exec_() == QDialog.Accepted:
                self.editmodel = DevolucionModel()
                self.editmodel.invoiceId = dlgbill.filtermodel.index( dlgbill.tblBills.selectionModel().currentIndex().row(), 0 ).data().toInt()[0]
                self.editmodel.billPrinted = dlgbill.filtermodel.index( dlgbill.tblBills.selectionModel().currentIndex().row(), 1 ).data().toString()
                self.editmodel.clientName = dlgbill.filtermodel.index( dlgbill.tblBills.selectionModel().currentIndex().row(), 3 ).data().toString()
                
                self.editmodel.clientId = dlgbill.filtermodel.index( dlgbill.tblBills.selectionModel().currentIndex().row(), 5 ).data().toInt()[0]
                
                self.editmodel.ivaRate = Decimal( dlgbill.filtermodel.index( dlgbill.tblBills.selectionModel().currentIndex().row(), 6 ).data().toString() )
                self.editmodel.ivaRateId = dlgbill.filtermodel.index( dlgbill.tblBills.selectionModel().currentIndex().row(), 7 ).data().toInt()[0]
    
                self.editmodel.exchangeRate = Decimal( dlgbill.filtermodel.index( dlgbill.tblBills.selectionModel().currentIndex().row(), 8 ).data().toString() )
                self.editmodel.exchangeRateId = dlgbill.filtermodel.index( dlgbill.tblBills.selectionModel().currentIndex().row(), 9 ).data().toInt()[0]
                
                self.editmodel.warehouseName = dlgbill.filtermodel.index( dlgbill.tblBills.selectionModel().currentIndex().row(), 10 ).data().toString()
                self.editmodel.warehouseId = dlgbill.filtermodel.index( dlgbill.tblBills.selectionModel().currentIndex().row(), 11 ).data().toInt()[0]
                
    
                self.editmodel.uid = self.user.uid
                
                
                query = QSqlQuery( """
                CALL spConsecutivo(%d,NULL);
                """ % constantes.IDNC )
                if not query.exec_():
                    raise UserWarning( u"No se pudo calcular el numero de la devolución" )
                query.first()
                self.editmodel.printedDocumentNumber = query.value( 0 ).toString()

                
                
                query.prepare( """
                SELECT 
                    v.idarticulo, 
                    v.descripcion,
                    facs.costounit,
                    facs.precioventa, 
                    -1*SUM(unidades) as existencia
                FROM articulosxdocumento facs
                JOIN vw_articulosdescritos v ON facs.idarticulo = v.idarticulo
                LEFT JOIN docpadrehijos devs ON devs.idhijo = facs.iddocumento
                WHERE facs.iddocumento = %d OR devs.idpadre = %d
                GROUP BY v.idarticulo
                """ % ( self.editmodel.invoiceId, self.editmodel.invoiceId ) )
                if not query.exec_():
                    raise Exception( "Ocurrio un error en la consulta" )
    
                while query.next():
                    linea = LineaDevolucion( self.editmodel )
                    linea.itemId = query.value( 0 ).toInt()[0]
                    linea.itemDescription = query.value( 1 ).toString()
                    linea.itemCost = Decimal( query.value( 2 ).toString() )
                    linea.itemPrice = Decimal( query.value( 3 ).toString() )
                    linea.maxquantity = query.value( 4 ).toInt()[0]
    
    
                    row = self.editmodel.rowCount()
                    self.editmodel.insertRows( row )
    
                    self.editmodel.lines[row] = linea
                
                
                self.cbConcept.setModel(self.conceptsmodel)
                self.cbConcept.setModelColumn(1)
                self.cbConcept.setCurrentIndex(-1)
    
                
                self.tabnavigation.setEnabled( False )
                self.tabWidget.setCurrentIndex( 0 )
                self.tabledetails.setModel( self.editmodel )

                delegate = DevolucionDelegate()
                self.tabledetails.setItemDelegate( delegate )

                self.tabledetails.resizeColumnsToContents()
                self.dtPicker.setDateTime( QDateTime.currentDateTime() )
                self.editmodel.dataChanged[QModelIndex, QModelIndex].connect(self.updateLabels)
                
                
                self.txtDocumentNumber.setText( self.editmodel.printedDocumentNumber)
                self.txtBill.setText( self.editmodel.billPrinted )
                self.txtWarehouse.setText(self.editmodel.warehouseName)
                
                self.status =  False 
        except UserWarning as inst:
            QMessageBox.critical(self, qApp.organizationName(), unicode(inst))
            self.status = True
        except Exception as inst:
            print inst
            self.status = True
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()

    @pyqtSlot( "int" )
    def on_cbConcept_currentIndexChanged( self, index ):
        """
        asignar proveedor al objeto self.editmodel
        """
        if not self.editmodel is None:
            self.editmodel.conceptId = self.conceptsmodel.record( index ).value( "idconcepto" ).toInt()[0]

    @property
    def printIdentifier(self):
        return self.navmodel.record( self.mapper.currentIndex() ).value( "iddocumento" ).toString()

    def cancel( self ):
        self.editmodel = None

        self.tablenavigation.setModel( self.navproxymodel )
        self.tabledetails.setModel( self.detailsproxymodel )


        self.status = True
#
#    def save( self ):
#        """
#        Slot documentation goes here.
#        """
##        self.datosRecibo.lineasAbonos =self.abonoeditmodel.lines
##        self.datosRecibo.lineas = self.editmodel.lines
#        self.datosRecibo.observaciones = self.txtObservations.toPlainText()
#        if self.datosRecibo.valid(self):
#            if QMessageBox.question(self, qApp.organizationName(), u"¿Esta seguro que desea guardar el recibo?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
#                if not QSqlDatabase.database().isOpen():
#                    QSqlDatabase.database().open()
#    
#          
#                if self.datosRecibo.save():
#                    QMessageBox.information( None,
#                        self.trUtf8( qApp.organizationName() ),
#                        self.trUtf8( u"""El documento se ha guardado con éxito""" ) )
#                    self.editmodel = None
#                    self.updateModels()
#                    self.navigate( 'last' )
#                    self.status = True
#                else:
#                    QMessageBox.critical( None,
#                        self.trUtf8( qApp.organizationName() ),
#                        self.trUtf8( """Ha ocurrido un error al guardar el documento""" ) )
#    
#                if QSqlDatabase.database().isOpen():
#                    QSqlDatabase.database().close()


class DlgSelectBill( QDialog ):
    def __init__( self, parent = None ):
        super( DlgSelectBill, self ).__init__( parent )
        self.billsmodel = QSqlQueryModel()
        query = """
        SELECT * FROM (
            SELECT
                factura.iddocumento,
                CONCAT_WS(' ', tdc.descripcion, factura.ndocimpreso) AS 'Numero de Factura',
                factura.fechacreacion AS 'Fecha',
                p.nombre AS 'Cliente',
                -SUM(axd.unidades) -
            IFNULL((
                SELECT
                SUM(axddev.unidades)
                FROM documentos devoluciones
                JOIN docpadrehijos dpddev ON devoluciones.iddocumento = dpddev.idhijo
                JOIN articulosxdocumento axddev ON axddev.iddocumento = devoluciones.iddocumento
                WHERE devoluciones.idtipodoc = %d AND dpddev.idpadre = factura.iddocumento
                GROUP BY dpddev.idpadre
            ),0) as unittotal,
                p.idpersona,
                ca.valorcosto,
                ca.idcostoagregado,
                tc.tasa,
                tc.idtc,
                b.nombrebodega AS 'Bodega',
                b.idbodega
            FROM documentos factura
            JOIN bodegas b ON factura.idbodega = b.idbodega
            JOIN tiposdoc tdc ON tdc.idtipodoc = factura.idtipodoc
            JOIN articulosxdocumento axd ON axd.iddocumento = factura.iddocumento AND factura.idtipodoc = %d
            JOIN tiposcambio tc ON tc.idtc = factura.idtipocambio
            JOIN personasxdocumento pxd ON pxd.iddocumento = factura.iddocumento
            JOIN personas p ON pxd.idpersona = p.idpersona AND p.tipopersona=%d
            LEFT JOIN costosxdocumento cxd ON cxd.iddocumento = factura.iddocumento
            LEFT JOIN costosagregados ca ON cxd.idcostoagregado = ca.idcostoagregado
            JOIN (
                SELECT
                dpdk.idpadre
                FROM documentos kardex
                JOIN docpadrehijos dpdk ON kardex.iddocumento = dpdk.idhijo
                WHERE kardex.idtipodoc = %d
            ) as kardex ON kardex.idpadre = factura.iddocumento
            GROUP BY factura.iddocumento
            ) as tbl
            WHERE unittotal > 0
        """ % (constantes.IDNC, constantes.IDFACTURA, constantes.CLIENTE, constantes.IDKARDEX)
        
        self.billsmodel.setQuery( query)



        self.setWindowTitle( "Seleccione la factura para la devolucion" )
        self.filtermodel = QSortFilterProxyModel()
        self.filtermodel.setSourceModel( self.billsmodel )
        self.filtermodel.setFilterCaseSensitivity( Qt.CaseInsensitive )
        self.filtermodel.setFilterKeyColumn( -1 )

        iddoc, ndocimpreso, fechacreacion, nombre, total, idpersona, valorcosto, idcosto, tasacambio, idcambio, nombrebodega, idbodega = range( 12 )
        self.tblBills = QTableView()
        self.tblBills.setSelectionMode( QAbstractItemView.SingleSelection )
        self.tblBills.setSelectionBehavior( QAbstractItemView.SelectRows )
        self.tblBills.selectRow( 0 )
        self.tblBills.setModel( self.filtermodel )

        self.tblBills.setColumnHidden( iddoc, True )
        self.tblBills.setColumnHidden( idpersona, True )
        self.tblBills.setColumnHidden( total, True )
        self.tblBills.setColumnHidden( valorcosto, True )
        self.tblBills.setColumnHidden( idcosto, True )
        self.tblBills.setColumnHidden( idcambio, True )
        self.tblBills.setColumnHidden( tasacambio, True )
        self.tblBills.setColumnHidden( idbodega, True )

        self.tblBills.horizontalHeader().setStretchLastSection( True )

        self.tblBills.resizeColumnsToContents()
        buttonbox = QDialogButtonBox( QDialogButtonBox.Ok | QDialogButtonBox.Cancel )

        self.txtSearch = QLineEdit()
        formlayout = QFormLayout()

        formlayout.addRow( "&Buscar", self.txtSearch )

        layout = QVBoxLayout()

        layout.addWidget( self.tblBills )
        layout.addLayout( formlayout )
        layout.addWidget( buttonbox )
        self.setLayout( layout )

        self.setMinimumWidth( 400 )
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)
        self.txtSearch.textChanged[unicode].connect(self.updateDetailFilter)
#FIXME: Que pasa cuando no hay facturas?
#    def exec_( self ):
#        if self.billsmodel.rowCount() == 0:
#            QMessageBox.critical( None,
#            self.trUtf8( "Llantera Esquipulas: Inventario" ),
#            self.trUtf8( """No hay facturas a las cuales hacer devoluciones""" ),
#            QMessageBox.StandardButtons( \
#                QMessageBox.Ok ) )
#            self.reject()
#        else:
#            QDialog.exec_( self )




    def updateFilter( self, str ):

        self.filtermodel.setFilterWildcard( str )

class RONavigationModel( QSqlQueryModel ):
    """
    basicamente le da formato a la salida de mapper
    """
    def data( self, index, role = Qt.DisplayRole ):
        """
        Esta funcion redefine data en la clase base, es el metodo que se utiliza para mostrar los datos del modelo
        """
        value = QSqlQueryModel.data( self, index, role )
        exchangeRate = Decimal( QSqlQueryModel.data( self, index.model().index( index.row(), TASA ) ).toString() )
        if value.isValid() and role in ( Qt.DisplayRole, Qt.EditRole ):
            if index.column() in ( TOTAL, SUBTOTAL, COSTO, IMPUESTOS ):
                return moneyfmt( Decimal( value.toString() ), 2, "US$" ) + " / " + moneyfmt( Decimal( value.toString() ) * exchangeRate, 2 , "C$" )
        return value

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int( Qt.AlignLeft | Qt.AlignVCenter )
            return int( Qt.AlignRight | Qt.AlignVCenter )
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if  section == TOTAL:
                return "Total"
            elif section == SUBTOTAL:
                return "Subtotal"
            elif section == IMPUESTOS:
                return "Impuestos"
            elif section == COSTO:
                return "Costo"
            elif section == IDDOCUMENTO:
                return "Id"
            elif section == NDOCIMPRESO:
                return u"Numero de Devolución"
            elif section == FACTURA:
                return "Numero de Factura"

        return QSqlQueryModel.headerData( self, section , orientation, role )
