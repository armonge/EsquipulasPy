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
Created on 18/05/2010

@author: Andrés Reyes Monge
'''
from decimal import Decimal

from PyQt4.QtGui import  QSpinBox, QSortFilterProxyModel
from PyQt4.QtCore import Qt, QSize

from utility.widgets.searchpanel import SingleSelectionSearchPanelDelegate



IDARTICULO, DESCRIPCION, COSTO, CANTIDAD = range( 4 )
class KardexOtherDelegate( SingleSelectionSearchPanelDelegate ):
    def __init__( self, model, showTable = True ):
        super( KardexOtherDelegate, self ).__init__()
        self.articles = model
        self.proxymodel = SingleSelectionModel()
        self.proxymodel.setFilterKeyColumn( 0 )
        self.proxymodel.setSourceModel( self.articles )
        self.showTable = showTable

        self.proxymodel.setFilterKeyColumn( IDARTICULO )
        self.proxymodel.setSourceModel( self.articles )

    def createEditor( self, parent, option, index ):
        if index.column() == CANTIDAD:
            spinbox = QSpinBox( parent )
            spinbox.setRange( -500, 500 )
            spinbox.setSingleStep( 1 )
            spinbox.setAlignment( Qt.AlignLeft | Qt.AlignVCenter )
            return spinbox
        elif index.column() in ( DESCRIPCION, IDARTICULO ):
            current = index.model().data( index.model().index( index.row(), IDARTICULO ) )
            self.proxymodel.setFilterRegExp( self.filter( index.model(), current ) )

            sp = super( KardexOtherDelegate, self ).createEditor( parent, option, index )
            sp.setColumnHidden( IDARTICULO )
            sp.setColumnHidden( COSTO )
            return sp
        else:
            super( KardexOtherDelegate, self ).createEditor( parent, option, index )

    def setEditorData( self, editor, index ):
        """
        En esta funcion se inicializan los datos a mostrarse en el editor
        se ejecuta justo en el momento en el que se muestra el editor
        """
        if index.column() == CANTIDAD:
            editor.setValue( index.model().data( index, Qt.DisplayRole ) if index.model().data( index, Qt.DisplayRole ) != "" else 0 )
        elif index.column() in ( IDARTICULO, DESCRIPCION ):

            current = index.model().data( index.model().index( index.row() , IDARTICULO ) )
            self.proxymodel.setFilterRegExp( self.filter( index.model(), current ) )

            super( KardexOtherDelegate, self ).setEditorData( editor, index )
            editor.lineEdit().selectAll()
        else:
            super( KardexOtherDelegate, self ).setEditorData( editor, index )

    def setModelData( self, editor, model, index ):
        """
        En este evento se toma el resultado del editor y se introduce en el modelo
        """
        if index.column() in ( DESCRIPCION, COSTO ):
            if self.proxymodel.rowCount() > 0:

                fila = editor.currentIndex()
                modelo = self.proxymodel
                model.setData( index, [
                                       modelo.index( fila , 0 ).data( Qt.EditRole ).toInt()[0],
                                       modelo.index( fila, DESCRIPCION ).data( Qt.EditRole ).toString(),
                                       Decimal( modelo.index( fila, COSTO ).data( Qt.EditRole ).toString() )
                        ] )
        else:
            super( KardexOtherDelegate, self ).setModelData( editor, model, index )

    def sizeHint( self, option, index ):
        fm = option.fontMetrics
        if index.column() == DESCRIPCION:
            return QSize( 250, fm.height() )

        return super( KardexOtherDelegate, self ).sizeHint( option, index )

class SingleSelectionModel( QSortFilterProxyModel ):
    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignLeft | Qt.AlignVCenter

        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if  section == DESCRIPCION:
                return u"Descripción"
            elif section == IDARTICULO:
                return "Id"
            elif section == COSTO:
                return "Costo"
        return int( section + 1 )
