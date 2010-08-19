# -*- coding: utf-8 -*-
'''
Created on 03/06/2010

@author: Administrator
'''
import logging

from PyQt4.QtGui import  QStyledItemDelegate, QSortFilterProxyModel, QLineEdit, QRegExpValidator, QIntValidator, QTextDocument, QMessageBox
from PyQt4.QtCore import  Qt, QRegExp, QSize, QVariant
from PyQt4.QtSql import QSqlTableModel
from utility.catgeneric import frmCatGeneric, PeopleDelegate


IDPERSONA, NOMBRE, FECHACREACION, TELEFONO, EMAIL, RUC, ESTADO, TIPOPERSONA, CUENTA = range( 9 )
class frmCatClientes( frmCatGeneric ):
    """
    Catalogo de Clientes
    """
    def __init__( self, parent = None ):
        super( frmCatClientes, self ).__init__( "personas", parent )
        clientsdelegate = PeopleDelegate()
        self.tableview.setItemDelegate( clientsdelegate )
        self.setWindowTitle( "Catalogo de clientes" )


    def updateModels( self ):
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning(u"No se pudo conectar con la base de datos")
            self.backmodel.setTable( self.table )
            self.backmodel.setFilter( "tipopersona=1" )
            self.backmodel.select()
            self.filtermodel = QSortFilterProxyModel()
            self.filtermodel.setSourceModel( self.backmodel )
            self.filtermodel.setFilterKeyColumn( 0 )
            self.filtermodel.setFilterCaseSensitivity( Qt.CaseInsensitive )
            self.tableview.setModel( self.filtermodel )
            self.database.close()

            self.tableview.setColumnHidden( IDPERSONA, True )
            self.tableview.setColumnHidden( FECHACREACION, True )
            self.tableview.setColumnHidden( TIPOPERSONA, True )
            self.tableview.setColumnHidden( ESTADO, True )
            self.tableview.setColumnHidden( RUC, True )
            self.tableview.setColumnHidden( CUENTA, True )

            self.backmodel.setHeaderData( NOMBRE, Qt.Horizontal, "Nombre", Qt.DisplayRole );
            self.backmodel.setHeaderData( TELEFONO, Qt.Horizontal, u"Telefóno", Qt.DisplayRole );
            self.backmodel.setHeaderData( EMAIL, Qt.Horizontal, "e-mail", Qt.DisplayRole );
        except UserWarning as inst:
            logging.error(inst)
            QMessageBox.critical(self, "Llantera Esquipulas", unicode(inst))
            return False
        except Exception as inst:
            logging.critical(inst)
            return False
        finally:
            if self.database.isOpen():
                self.database.close()
        return True
            

    def new( self ):
        super( frmCatClientes, self ).new()
        self.backmodel.setData( self.backmodel.index( self.backmodel.rowCount() - 1, TIPOPERSONA ), 1 )



