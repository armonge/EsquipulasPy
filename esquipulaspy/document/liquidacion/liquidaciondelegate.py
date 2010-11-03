#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ${file}
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
Created on 21/05/2010

@author: Andrés Reyes Monge
'''
from PyQt4.QtCore import Qt, QSize
from PyQt4.QtGui import QSpinBox, QDoubleSpinBox
from utility.widgets.searchpanel import SingleSelectionSearchPanelDelegate


IDARTICULO, ARTICULO, CANTIDAD, COSTOUNIT, FOB, FLETE, SEGURO, OTROS, CIF, IMPUESTOS, COMISION, AGENCIA, ALMACEN, PAPELERIA, TRANSPORTE, TCOSTOD, COSTOD, TCOSTOC, COSTOC = range( 19 )
class LiquidacionDelegate( SingleSelectionSearchPanelDelegate ):
    '''
    classdocs
    '''
    def __init__( self, showTable = True , parent = None ):
        '''
        Constructor
        '''
        super( LiquidacionDelegate, self ).__init__( showTable, parent )

        self.prods = None

        self.proxymodel.setFilterKeyColumn( IDARTICULO )



    def createEditor( self, parent, option, index ):
        if index.column() == CANTIDAD:
            spinbox = QSpinBox( parent )
            spinbox.setRange( 1, 1000 )
            spinbox.setSingleStep( 1 )
            spinbox.setAlignment( Qt.AlignRight | Qt.AlignVCenter )
            return spinbox
        elif index .column() == COSTOUNIT:
            spinbox = QDoubleSpinBox( parent )
            spinbox.setRange( 0.0001, 100000 )
            spinbox.setDecimals( 4 )
            spinbox.setSingleStep( 1 )
            spinbox.setAlignment( Qt.AlignRight | Qt.AlignVCenter )
            return spinbox
        elif index.column() in ( IDARTICULO, ARTICULO ):

            self.proxymodel.setSourceModel( self.prods )
            current = index.model().data( index.model().index( index.row(), IDARTICULO ) )
            self.proxymodel.setFilterRegExp( self.filter( index.model(), current ) )

            sp = super( LiquidacionDelegate, self ).createEditor( parent, option, index )
            sp.setColumnHidden( IDARTICULO )
            sp.setMinimumWidth( 600 )
            return sp

        else:
            super( LiquidacionDelegate, self ).createEditor( parent, option, index )


    def setEditorData( self, editor, index ):
        text = index.data( Qt.DisplayRole ).toString()
        if index.column() == CANTIDAD:
            editor.setValue( index.model().data( index, Qt.DisplayRole ) if index.model().data( index, Qt.DisplayRole ) != "" else 0 )
        elif index.column() == ARTICULO:
            current = index.model().data( index.model().index( index.row(), IDARTICULO ) )
            self.proxymodel.setFilterRegExp( self.filter( index.model(), current ) )

            i = editor.findText( text )
            if i == -1:
                i = 0

            editor.setCurrentIndex( i )
            editor.lineEdit().selectAll()

        elif index.column() == COSTOUNIT:
            editor.setValue( index.data( Qt.EditRole ).toDouble()[0] if index.data( Qt.EditRole ).toDouble()[0] != 0 else 1 )
        else:
            super( LiquidacionDelegate, self ).setEditorData( editor, index )

    def setModelData( self, editor, model, index ):
        if index.column() in ( IDARTICULO, ARTICULO ):
            if editor.currentIndex() != -1:
                proxyindex = self.proxymodel.index( editor.currentIndex() , 0 )
                sourceindex = self.proxymodel.mapToSource( proxyindex )
                model.setData( index, self.prods.items[sourceindex.row() ] )
        else:
            super( LiquidacionDelegate, self ).setModelData( editor, model, index )

    def sizeHint( self, option, index ):
        fm = option.fontMetrics
        if index.column() == ARTICULO:
            return QSize( 250, fm.height() )

        return super( LiquidacionDelegate, self ).sizeHint( option, index )


