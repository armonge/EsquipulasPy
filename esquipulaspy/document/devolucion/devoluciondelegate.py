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
Created on 19/05/2010

@author: Andrés Reyes Monge
'''
from PyQt4.QtGui import QStyledItemDelegate, QSpinBox
from PyQt4.QtCore import Qt
DESCRIPCION, PRECIO, CANTIDADMAX, CANTIDAD, TOTALPROD = range( 5 )
class DevolucionDelegate( QStyledItemDelegate ):

    def createEditor( self, parent, option, index ):
        if index.column() == CANTIDAD:
            spinbox = QSpinBox( parent )
            spinbox.setRange( 0, index.model().lines[index.row()].maxquantity )
            spinbox.setSingleStep( 1 )
            return spinbox
        else:
            QStyledItemDelegate.createEditor( self, parent, option, index )

    def setEditorData( self, editor, index ):
        if index.column() == CANTIDAD:
            editor.setValue( index.data( Qt.DisplayRole ).toInt()[0] )
        else:
            QStyledItemDelegate.setEditorData( self, editor, index )


