#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       
#       Copyright 2010 Andrés Reyes Monge <armonge@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
"""
Module implementing frmCatProveedores.
"""
import logging

from PyQt4.QtGui import QStyledItemDelegate, QAbstractItemView, \
 QSortFilterProxyModel, QLineEdit, QRegExpValidator, QIntValidator, \
 QTextDocument, qApp, QMessageBox
from PyQt4.QtCore import  Qt, QRegExp, QSize, QVariant
from utility.catgeneric import FrmCatGeneric


class FrmCatMarcas( FrmCatGeneric ):
    """
    Catalogo de Marcas
    """
    def __init__( self, parent = None ):
        super( FrmCatMarcas, self ).__init__( "marcas", parent )
        self.setWindowTitle( "Catalogo de Marcas" )
    def updateModels( self ):
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( u"No se pudo conectar con la base de datos" )
            self.backmodel.setTable( self.table )
            self.backmodel.select()
            self.filtermodel = QSortFilterProxyModel()
            self.filtermodel.setSourceModel( self.backmodel )
            self.filtermodel.setFilterKeyColumn( -1 )
            self.filtermodel.setFilterCaseSensitivity( Qt.CaseInsensitive )
            self.tableview.setModel( self.filtermodel )
            self.database.close()

            self.tableview.setColumnHidden( 0, True )
            return True
        except UserWarning as inst:
            logging.error( inst )
            QMessageBox.critical( self, qApp.organizationName(), unicode( inst ) )
        except Exception as inst:
            logging.critical( inst )
        finally:
            if self.database.isOpen():
                self.database.close()

            return False


IDCONCEPTO, DESCRIPCION, MODULO = range( 3 )
class FrmCatConceptos( FrmCatGeneric ):
    """
    Catalogo de conceptos
    """
    def __init__( self, modulo, parent = None ):
        self.modulo = modulo
        super( FrmCatConceptos, self ).__init__( "conceptos", parent )
        self.setWindowTitle( "Catalogo de Conceptos" )


    def updateModels( self ):
        try:
            self.database.open()
            self.backmodel.setTable( self.table )
            self.backmodel.setFilter( "modulo=" + str( self.modulo ) )
            self.backmodel.select()
            self.filtermodel = QSortFilterProxyModel()
            self.filtermodel.setSourceModel( self.backmodel )
            self.filtermodel.setFilterKeyColumn( -1 )
            self.filtermodel.setFilterCaseSensitivity( Qt.CaseInsensitive )
            self.tableview.setModel( self.filtermodel )
            self.tableview.resizeColumnsToContents()
            self.database.close()
            self.tableview.setColumnHidden( IDCONCEPTO, True )
            self.tableview.setColumnHidden( MODULO, True )
            self.backmodel.setHeaderData( DESCRIPCION, Qt.Horizontal,
                                           "Descripcion", Qt.DisplayRole );
            return True
        except Exception as inst:

            if self.database.isOpen():
                self.database.close()

            return False

    def new( self ):
        super( FrmCatConceptos, self ).new()
        self.backmodel.setData( self.backmodel.index( self.backmodel.rowCount()
                                                   - 1, MODULO ), self.modulo )







IDPERSONA, NOMBRE, FECHACREACION, TELEFONO, EMAIL, RUC, ACTIVO, \
TIPOPERSONA, CUENTA = range( 9 )
class FrmCatProveedores( FrmCatGeneric ):
    """
    Catalogo de Proveedores
    """
    def __init__( self, parent = None ):
        super( FrmCatProveedores, self ).__init__( "personas", parent )
        providersdelegate = PeopleDelegate()
        self.tableview.setItemDelegate( providersdelegate )
        self.setWindowTitle( "Catalogo de Proveedores" )

    def updateModels( self ):
        try:
            self.database.open()
            self.backmodel.setTable( self.table )
            self.backmodel.setFilter( "tipopersona=2" )
            self.backmodel.select()
            self.filtermodel = ProvidersModel( self )
            self.filtermodel.setSourceModel( self.backmodel )
            self.filtermodel.setFilterKeyColumn( -1 )
            self.filtermodel.setFilterCaseSensitivity( Qt.CaseInsensitive )
            self.tableview.setModel( self.filtermodel )
            self.database.close()

            self.tableview.setColumnHidden( IDPERSONA, True )
            self.tableview.setColumnHidden( FECHACREACION, True )
            self.tableview.setColumnHidden( TIPOPERSONA, True )
            self.tableview.setColumnHidden( CUENTA, True )

            self.backmodel.setHeaderData( NOMBRE, Qt.Horizontal,
                                           "Nombre", Qt.DisplayRole )
            self.backmodel.setHeaderData( TELEFONO, Qt.Horizontal,
                                           u"Telefóno", Qt.DisplayRole )
            self.backmodel.setHeaderData( EMAIL, Qt.Horizontal,
                                          "e-mail", Qt.DisplayRole )
            self.backmodel.setHeaderData( RUC, Qt.Horizontal,
                                           "RUC", Qt.DisplayRole )
            self.backmodel.setHeaderData( ACTIVO, Qt.Horizontal,
                                          "Activo", Qt.DisplayRole )

            return True

        except Exception as inst:

            if self.database.isOpen():
                self.database.close()

            return False

    def edit( self ):
        self.tableview.setEditTriggers( QAbstractItemView.AllEditTriggers )
        self.tableview.edit( self.tableview.selectionModel().currentIndex() )

    def new( self ):
        super( FrmCatProveedores, self ).new()
        self.backmodel.setData( self.backmodel.index( 
                                                     self.backmodel.rowCount()
                                                     - 1, TIPOPERSONA ), 2 )
        self.backmodel.setData( self.backmodel.index( 
                                                      self.backmodel.rowCount()
                                                      - 1, ACTIVO ), 1 )


class ProvidersModel( QSortFilterProxyModel ):
    def __init__( self, parent = None ):
        super( ProvidersModel, self ).__init__( parent )

    def data( self, index, role ):
        if not index.isValid():
            return None

        if index.column() == ACTIVO and role in ( Qt.CheckStateRole,
                                                  Qt.DisplayRole ):
            if role == Qt.CheckStateRole:
                value = QVariant( Qt.Checked ) if index.data( Qt.EditRole ).toBool() else QVariant( Qt.Unchecked )
                return value
        else:
            return QSortFilterProxyModel.data( self, index, role )


    def setData( self, index, data, role = Qt.DisplayRole ):
        if not index.isValid():
            return False
        if index.column() == ACTIVO and role == Qt.CheckStateRole:
            return QSortFilterProxyModel.setData( self, index, 1 if data == Qt.Checked else 0, Qt.EditRole )
        else:
            return QSortFilterProxyModel.setData( self, index, data, role )



    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        elif index.column() == ACTIVO:
            return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

class PeopleDelegate( QStyledItemDelegate ):
    def __init__( self, parent = None ):
        super( PeopleDelegate, self ).__init__( parent )

    def createEditor( self, parent, option, index ):
        """
        Aca se inicializa el control que se usara para editar
        """
        if index.column() == EMAIL:
            lineedit = QLineEdit( parent )
            #accepts only mail
            validator = QRegExpValidator( QRegExp( r"^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$" ), self )
            lineedit.setValidator( validator )
            return lineedit
        elif index.column() == TELEFONO:
            lineedit = QLineEdit( parent )
            validator = QIntValidator( self )
            lineedit.setValidator( validator )
            return lineedit
        else:
            return QStyledItemDelegate.createEditor( self, parent, option, index )

    def sizeHint( self, option, index ):
        fm = option.fontMetrics
        if index.column() in ( NOMBRE, TELEFONO, RUC, EMAIL ):
            text = index.model().data( index ).toString()
            document = QTextDocument()
            document.setDefaultFont( option.font )
            document.setHtml( text )
            return QSize( document.idealWidth() + 5, fm.height() )
        elif index.column() == ACTIVO:
                return QSize( fm.width( "9" ), fm.height() )
        else:
            return QStyledItemDelegate.sizeHint( self, option, index )


    def setEditorData( self, editor, index ):
        """
        Aca se definen los datos iniciales que tendra el control, 
        justo antes de mostrarlo
        """
        if index.column() in ( NOMBRE, TELEFONO, RUC, EMAIL ):
            text = index.model().data( index, Qt.DisplayRole )
            editor.setText( text.toString() )
        else:
            QStyledItemDelegate.setEditorData( self, editor, index )

