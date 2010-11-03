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
Created on 07/06/2010

@author: Andrés Reyes Monge
'''
import logging

from PyQt4.QtGui import QStyledItemDelegate, QSpinBox
from PyQt4.QtCore import Qt

from utility.widgets.searchpanel import SingleSelectionSearchPanelDelegate

CANTIDAD, DENOMINACION, TOTAL, MONEDA, IDDOCUMMENTOT, IDDENOMINACION = range( 6 )
class ArqueoDelegate( SingleSelectionSearchPanelDelegate ):
    def __init__( self, denominations, parent = None ):
        super( ArqueoDelegate, self ).__init__( parent )
        self.denominationsmodel = denominations

        self.proxymodel.setFilterKeyColumn( 0 )

    def filter( self, model, current ):
        filtro = "|^".join( [str( line.denominationId ) for line in model.sourceModel().lines if line.denominationId != 0 and line.denominationId != current ] )

        if filtro != "":
            filtro = "[^" + filtro + "]"

        return filtro

    def createEditor( self, parent, option, index ):
        if index.column() == CANTIDAD:
            spinbox = QSpinBox( parent )
            spinbox.setRange( 0, 1000 )
            spinbox.setSingleStep( 1 )
            return spinbox
        elif index.column() == DENOMINACION:

            model = index.model()

            self.proxymodel.setSourceModel( self.denominationsmodel )

            current = model.index( index.row(), IDDENOMINACION ).data().toInt()[0]
            self.proxymodel.setFilterRegExp( self.filter( model,
                                                          current ) )


            sp = super( ArqueoDelegate, self ).createEditor( parent, option, index )

            sp.setColumnHidden( 0 )
            sp.setColumnHidden( 2 )
            sp.setColumnHidden( 3 )

            return sp


        else:
            return super( ArqueoDelegate, self ).createEditor( parent,
                                                               option,
                                                               index )

    def setEditorData( self, editor, index ):
        if index.column() == CANTIDAD:
            editor.setValue( index.data( Qt.DisplayRole ).toInt()[0] )
        elif index.column() == DENOMINACION:
            text = index.data( Qt.DisplayRole ).toString()
            i = editor.findText( text )
            if i == -1:
                i = 1
            editor.setCurrentIndex( i )
            editor.lineEdit().selectAll()
        else:
            super( ArqueoDelegate, self ).setEditorData( editor, index )

    def setModelData( self, editor, model, index ):
        if index.column() == DENOMINACION:
            try:
                proxyindex = self.proxymodel.index( editor.currentIndex() , 0 )
                sourceindex = self.proxymodel.mapToSource( proxyindex )
                model.setData( index, self.denominationsmodel.items[sourceindex.row() ] )
            except IndexError as inst:
                logging.error( inst )
        else:
            super( ArqueoDelegate, self ).setModelData( editor, model, index )


