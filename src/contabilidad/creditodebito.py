# -*- coding: utf-8 -*-
'''
Created on 04/08/2010

@author: marcos
'''
from PyQt4.QtCore import pyqtSlot, SIGNAL, QModelIndex, Qt, QTimer, \
    SLOT, QDateTime

from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QDataWidgetMapper, \
    QDialog, QTableView, QDialogButtonBox, QVBoxLayout, QAbstractItemView, QFormLayout, \
     QLineEdit,QMessageBox

from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery

from ui.Ui_creditodebito import Ui_frmCreditoDebito
from utility.base import Base
from decimal import Decimal
from utility import constantes
from document.creditodebito.creditodebitomodel import creditodebitomodel

class frmCreditoDebito( Ui_frmCreditoDebito, QMainWindow,Base ):
    """
    Implementacion de la interfaz grafica para entrada compra
    """
    def __init__( self, user, parent ):
        super( frmCreditoDebito, self ).__init__( parent )
        self.setupUi( self )
        self.parentWindow = parent
        Base.__init__( self )


        self.user = user

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

    @pyqtSlot(  )
    def on_actionNew_activated( self ):
        """
        Slot documentation goes here.
        """
        query = QSqlQuery( )
        try:
            if not QSqlDatabase.database().open():
                raise Exception( u"No se pudo establecer una conexión con la base de datos" )
            
            dlgbill = dlgSelectBill()
            if dlgbill.exec_() == QDialog.Accepted:
                self.editmodel = creditodebitomodel()
                self.editmodel.invoiceId = dlgbill.filtermodel.index( dlgbill.tblBills.selectionModel().currentIndex().row(), 0 ).data().toInt()[0]
                self.editmodel.clientId = dlgbill.filtermodel.index( dlgbill.tblBills.selectionModel().currentIndex().row(), 5 ).data().toInt()[0]
                self.editmodel.uid = self.user.uid
                self.editmodel.clientName = dlgbill.filtermodel.index( dlgbill.tblBills.selectionModel().currentIndex().row(), 3 ).data().toString()
                self.editmodel.billPrinted = dlgbill.filtermodel.index( dlgbill.tblBills.selectionModel().currentIndex().row(), 1 ).data().toString()
    
                self.editmodel.exchangeRate = Decimal( dlgbill.filtermodel.index( dlgbill.tblBills.selectionModel().currentIndex().row(), 8 ).data().toString() )
                self.editmodel.exchangeRateId = dlgbill.filtermodel.index( dlgbill.tblBills.selectionModel().currentIndex().row(), 9 ).data().toInt()[0]
    
    
                self.txtBill.setText( self.editmodel.billPrinted )
                query = QSqlQuery( """
                CALL spConsecutivo(%d,NULL);
                """ % constantes.IDDEVOLUCION )
                if not query.exec_():
                    raise UserWarning( u"No se pudo calcular el numero de la devolución" )
                query.first()
                self.editmodel.printedDocumentNumber = query.value( 0 ).toString()

                self.txtDocumentNumber.setText( self.editmodel.printedDocumentNumber)
                
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
    
    
                
                self.tabnavigation.setEnabled( False )
                self.tabWidget.setCurrentIndex( 0 )
                self.tabledetails.setModel( self.editmodel )

                delegate = DevolucionDelegate()
                self.tabledetails.setItemDelegate( delegate )

                self.tabledetails.resizeColumnsToContents()
                self.dtPicker.setDateTime( QDateTime.currentDateTime() )
                self.connect( self.editmodel, SIGNAL( "dataChanged(QModelIndex,QModelIndex)" ), self.updateLabels )
                self.status =  False 
        except UserWarning as inst:
            QMessageBox.critical(self, "Llantera Esquipulas", unicode(inst))
            self.status = True
        except Exception as inst:
            print inst
            self.status = True
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()

    def setControls( self, status ):
        """
        @param status false = editando        true = navegando
        """
        self.dtPicker.setReadOnly(  status )            
        self.actionSave.setVisible(  not status )
        self.actionCancel.setVisible( not status )
        self.actionNew.setVisible( status)
        self.actionPreview.setVisible( status)

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
                return "Numero de Devolución"
            elif section == FACTURA:
                return "Numero de Factura"

        return QSqlQueryModel.headerData( self, section , orientation, role )

class dlgSelectBill( QDialog ):
    def __init__( self, parent = None ):
        super( dlgSelectBill, self ).__init__( parent )
        self.billsmodel = QSqlQueryModel()
        self.billsmodel.setQuery( """
        SELECT
                d.ndocimpreso as 'No. Devolucion',
                p.nombre as 'Cliente',
                DATE(d.fechacreacion) as 'Fecha',
                CONCAT('C$ ',d.total) as 'Total'                
            FROM documentos d
            JOIN docpadrehijos dpd ON dpd.idhijo = d.iddocumento
            JOIN documentos padre ON dpd.idpadre = padre.iddocumento
            JOIN tiposcambio tc ON d.idtipocambio = tc.idtc
        JOIN personasxdocumento pd ON d.iddocumento=pd.iddocumento
        LEFT JOIN personas p ON p.idpersona=pd.idpersona
            JOIN articulosxdocumento axd ON axd.iddocumento = d.iddocumento
            LEFT JOIN costosxdocumento cxd ON cxd.iddocumento = padre.iddocumento
            LEFT JOIN costosagregados ca ON ca .idcostoagregado = cxd.idcostoagregado
            WHERE d.idtipoDoc = %d and p.tipopersona=%d
            GROUP BY d.iddocumento    
        """ % (constantes.IDDEVOLUCION,constantes.CLIENTE) )



        self.setWindowTitle( "Seleccione el documento" )
        self.filtermodel = QSortFilterProxyModel()
        self.filtermodel.setSourceModel( self.billsmodel )
        self.filtermodel.setFilterCaseSensitivity( Qt.CaseInsensitive )
        self.filtermodel.setFilterKeyColumn( -1 )
        
        self.tblBills = QTableView()
        self.tblBills.setSelectionMode( QAbstractItemView.SingleSelection )
        self.tblBills.setSelectionBehavior( QAbstractItemView.SelectRows )
        self.tblBills.selectRow( 0 )
        self.tblBills.setModel( self.filtermodel )

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
        self.connect( buttonbox, SIGNAL( "accepted()" ), self, SLOT( "accept()" ) )
        self.connect( buttonbox, SIGNAL( "rejected()" ), self, SLOT( "reject()" ) )
        self.connect( self.txtSearch, SIGNAL( "textChanged(QString)" ), self.updateFilter )

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
