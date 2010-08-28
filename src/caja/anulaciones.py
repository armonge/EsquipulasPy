'''
Created on 20/07/2010

@author: marcos
'''
# -*- coding: UTF-8 -*-
'''
Created on 06/06/2010

@author: armonge
'''
from PyQt4.QtGui import QMainWindow, QDialog, QSortFilterProxyModel, QTableView, QAbstractItemView, QDialogButtonBox, QLineEdit, QFormLayout, QVBoxLayout
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase
from PyQt4.QtCore import SIGNAL, Qt, SLOT,QDate
#from ui.Ui_anulaciones import Ui_frmAnulacionesFactura

class frmAnulaciones( QMainWindow):#, Ui_frmAnulacionesFactura ):
    '''
    classdocs
    '''

    def __init__( self, user, parent ):
        '''
        Constructor
        '''
        super( frmAnulaciones, self ).__init__()

        self.setupUi( self )
        
        self.user = user
        #self.sesion = parent.sesion
        self.dtPicker=QDate.currentDate()
        
        try:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open():
                    raise Exception( "No se pudo abrir la base de datos" )
            self.model = QSqlQueryModel()
            self.model.setQuery( """
            SELECT d.ndocimpreso as 'Numero de Factura',  d.fechacreacion as 'Fecha', p.nombre as 'Cliente', CONCAT('US$', FORMAT(d.total, 2)) as 'Total'
            FROM documentos d 
            JOIN personasxdocumento per ON per.iddocumento=d.iddocumento
            JOIN personas p ON p.idpersona=per.idpersona
            WHERE d.idtipodoc = 5 and p.tipopersona=1
            AND anulado = 1
            """ )
            self.tablenavigation.setModel( self.model )
        except Exception as inst:
            print inst

    def on_actionNew_activated( self ):
        dlg = dlgSelectInvoice()
        if dlg.exec_() == QDialog.Accepted:
            print "accepted"

class dlgSelectInvoice( QDialog ):
    def __init__( self, parent = None ):
        super(dlgSelectInvoice, self).__init__( parent )

        self.annullmentsmodel = QSqlQueryModel()
        self.annullmentsmodel.setQuery( """
        SELECT 
            d.ndocimpreso as 'Numero de Factura',  
            d.fechacreacion as 'Fecha', 
            p.nombre as 'Cliente', 
            CONCAT('US$', FORMAT(d.total, 2)) as 'Total'
        FROM documentos d 
        JOIN personas p ON d.idpersona = p.idpersona
        LEFT JOIN docpadrehijos dpd ON dpd.idpadre =  d.iddocumento
        WHERE d.idtipodoc = 5 AND dpd.idpadre IS NULL
        AND anulado = 0 and d.fechacreacion=CURDATE()
        """ )

        self.setWindowTitle( "Seleccione la factura a anular" )
        self.filtermodel = QSortFilterProxyModel()
        self.filtermodel.setSourceModel( self.annullmentsmodel )
        self.filtermodel.setFilterCaseSensitivity( Qt.CaseInsensitive )
        self.filtermodel.setFilterKeyColumn( -1 )

        self.tbl = QTableView()
        self.tbl.setSelectionMode( QAbstractItemView.SingleSelection )
        self.tbl.setSelectionBehavior( QAbstractItemView.SelectRows )
        self.tbl.selectRow( 0 )
        self.tbl.setModel( self.filtermodel )
        self.tbl.horizontalHeader().setStretchLastSection( True )
        self.tbl.resizeColumnsToContents()

        buttonbox = QDialogButtonBox( QDialogButtonBox.Ok | QDialogButtonBox.Cancel )
        txtSearch = QLineEdit()

        formlayout = QFormLayout()

        formlayout.addRow( "&Buscar", txtSearch )

        layout = QVBoxLayout()

        layout.addWidget( self.tbl )
        layout.addLayout( formlayout )
        layout.addWidget( buttonbox )

        self.setLayout( layout )

        self.setMinimumWidth( 400 )
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)
        self.txtSearch.textChanged[unicode].connect(self.updateFilter)

    def updateFilter( self, string ):
        self.filtermodel.setFilterWildcard( string )
