#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       
#       Copyright 2010 Andrés Reyes Monge <armonge@armonge-laptop.site>
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
from PyQt4.QtCore import Qt, QSize
from PyQt4.QtGui import QSpinBox, QDoubleSpinBox
from utility.widgets.searchpanel import SingleSelectionSearchPanelDelegate

IDARTICULO, DESCRIPCION, CANTIDAD, PRECIO, PRECIOD, TOTALPROD, TOTALD = range( 7 )
class EntradaCompraDelegate( SingleSelectionSearchPanelDelegate ):
    def __init__( self, parent = None ):
        super( EntradaCompraDelegate, self ).__init__( parent )

        self.prods = None
        """
        @ivar:El modelo en el que se almacenan los articulos
        @type:SingleSelectionModel
        """
    def createEditor( self, parent, option, index ):
        """
        Aca se crean los widgets para edición
        """
        if index.column() == CANTIDAD:
            spinbox = QSpinBox( parent )
            spinbox.setRange( 1, 1000 )
            spinbox.setSingleStep( 1 )
            spinbox.setAlignment( Qt.AlignRight | Qt.AlignVCenter )
            return spinbox
        elif index.column() == DESCRIPCION :
#            if index.data() != "":
#                self.prods.items.append( [ index.model().data( index.model().index( index.row(), 0 ) ) , index.data().toString()] )
            self.proxymodel.setSourceModel( self.prods )
            model = index.model()

            current = model.index( index.row(), IDARTICULO ).data()

            self.proxymodel.setFilterRegExp( self.filter( model, current ) )

            sp = super( EntradaCompraDelegate, self ).createEditor( parent, option, index )
            return sp

        elif index.column() == TOTALPROD:
            return None

        elif index.column() in ( PRECIO, PRECIOD ):
            spinbox = QDoubleSpinBox( parent )
            spinbox.setRange( 0, 10000 )
            spinbox.setDecimals( 4 )
            spinbox.setSingleStep( 1 )
            spinbox.setAlignment( Qt.AlignRight | Qt.AlignVCenter )
            return spinbox
        else:
            return super( EntradaCompraDelegate, self ).createEditor( parent, option, index )

    def setEditorData( self, editor, index ):
        """
        En esta funcion se inicializan los datos a mostrarse en el editor
        se ejecuta justo en el momento en el que se muestra el editor
        """
        text = index.model().data( index, Qt.DisplayRole )
        if index.column() == CANTIDAD:
            editor.setValue( index.model().data( index, Qt.DisplayRole ) if index.model().data( index, Qt.DisplayRole ) != "" else 0 )
        elif index.column() in ( PRECIO, PRECIOD ):
            editor.setValue( index.model().data( index, Qt.EditRole ) if index.model().data( index, Qt.EditRole ) != 0 else 1 )
        elif index.column() == DESCRIPCION:
            i = editor.findText( text )
            if i == -1:
                i = 0
            editor.setCurrentIndex( i )
            editor.lineEdit().selectAll()
        else:
            super( EntradaCompraDelegate, self ).setEditorData( editor, index )

    def setModelData( self, editor, model, index ):
        """
        En este evento se toma el resultado del editor y se introduco 
        en el modelo
        """
        if index.column() == DESCRIPCION:
            proxy_index = self.proxymodel.index( editor.currentIndex(), 0 )
            source_index = self.proxymodel.mapToSource( proxy_index )

            fila = source_index.row()
            modelo = self.prods

            model.setData( index, [
                                   modelo.items[fila][0],
                                   modelo.items[fila][1]
            ] )
        else:
            super( EntradaCompraDelegate, self ).setModelData( editor,
                                                               model,
                                                               index )

    def sizeHint( self, option, index ):
        u"""
        El tamaño sugerido de los datos en el modelo
        """
        fm = option.fontMetrics
        if index.column() == IDARTICULO:
            return QSize( fm.width( "99" ), fm.height() )
        if index.column() == DESCRIPCION:
            return QSize( 250, fm.height() )

        return super( EntradaCompraDelegate, self ).sizeHint( option, index )
