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
'''
Created on 29/05/2010

@author: Andrés Reyes Monge
'''

from PyQt4.QtGui import QTableView, QSortFilterProxyModel, QCompleter, QComboBox, QStyledItemDelegate
from PyQt4.QtCore import Qt

class SingleSelectionSearchPanelDelegate( QStyledItemDelegate ):
    def __init__( self, showTable = False , parent = None ):
        super( SingleSelectionSearchPanelDelegate, self ).__init__( parent )

        self.showTable = showTable
        """
        @ivar: Si se debera o no mostrar la tabla
        @type: bool
        """

        self.proxymodel = QSortFilterProxyModel()
        """
        @ivar:Este es el modelo proxy que utiliza el SearchPanel
        @type: QSortFilterProxyModel
        """



    def createEditor( self, parent, _option, index ):
        """
        Esta función debera reimplementarse en los hijos de esta clase, 
        idealmente mandara a llamar a este metodo base despues de
        haber actualizadao el proxymodel y solamente cuando la columna sea la 
        indicada
        """
        sp = SearchPanel( self.proxymodel, parent, self.showTable )
        sp.setColumn( index.column() )

        return sp


    def filter( self, model, current ):
        """
        Crea la expresión regular que filtrara los elementos ya incluidos en el
        modelo del delegado
        """
        filtro = "|^".join( [str( line.itemId ) for line in model.lines if line.itemId != 0 and line.itemId != current ] )
        if filtro != "":
            filtro = "[^" + filtro + "]"
        return filtro




class SearchPanel( QComboBox ):
    def __init__( self, model, parent = None, showTable = False ):
        super( SearchPanel, self ).__init__( parent )

        self.tabla = None
        self.setFocusPolicy( Qt.StrongFocus )
        self.setEditable( True )
#        self.setModel( model )
        self.setEditable( True )
        self.completer = QCompleter( self )
        # always show all completions
        self.completer.setCompletionMode( QCompleter.UnfilteredPopupCompletion )
        self.pFilterModel = QSortFilterProxyModel( self )
        self.pFilterModel.setFilterCaseSensitivity( Qt.CaseInsensitive )
        self.showTable = showTable

        if model != None:
            self.setModel( model )
#        self.pFilterModel.setSourceModel( model );


        self.completer.setModel( self.pFilterModel )
        self.completerTable = SearchPanelView()
        self.completer.setPopup( self.completerTable )
#Mostrar el Popup en forma de Tabla        
        if self.showTable:
            self.tabla = SearchPanelView()
            self.setView( self.tabla )

        self.setCompleter( self.completer )

        self.setColumn( 1 )

        self.lineEdit().textEdited[unicode].connect( self.pFilterModel.setFilterFixedString if not showTable else self.pFilterModel.setFilterWildcard )

    def setModel( self, model ):
        QComboBox.setModel( self, model )
        self.pFilterModel.setSourceModel( model )

    def setColumn( self, column ):
        self.setModelColumn( 1 )
        self.completer.setCompletionColumn( column )
        self.pFilterModel.setFilterKeyColumn( column )
        self.setModelColumn( column )

    def view( self ):
        return self.completer.popup()

    def data( self ):
        return self.currentIndex()

    def index( self ):
        return self.currentIndex()

    def setColumnHidden( self, col ):
        self.completerTable.hiddenColumns.append( col )
        if self.showTable:
            self.tabla.hiddenColumns.append( col )


    def setMinimumWidth( self, width ):
        self.completerTable.setMinimumWidth( width )
        if self.showTable:
            self.tabla.setMinimumWidth( width )


class SearchPanelView( QTableView ):
    '''
    La tabla que se muestra en un Widget SearchPanel
    '''
    def __init__( self, parent = None ):
        '''
        Constructor
        '''
        super( SearchPanelView, self ).__init__( parent )

        self.setSelectionBehavior( QTableView.SelectRows )
        self.setSelectionMode( QTableView.SingleSelection )
        self.setMinimumHeight( 150 )
        self.setMinimumWidth( 500 )
        self.verticalHeader().setVisible( False )
        self.set = False
        self.hiddenColumns = []



    def paintEvent( self, event ):
        for column in self.hiddenColumns:
            self.setColumnHidden( column, True )

        if not self.set:
            self.resizeColumnsToContents()
            self.set = True
            self.horizontalHeader().setStretchLastSection( True )


        super( SearchPanelView, self ).paintEvent( event )



