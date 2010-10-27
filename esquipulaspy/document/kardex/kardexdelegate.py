#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ${file}
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
Created on 16/07/2010

@author: Andrés Reyes Monge
'''
from PyQt4.QtGui import QStyledItemDelegate, QSpinBox
from PyQt4.QtCore import Qt
IDARTICULO, DESCRIPCION, NUMDOC, NUMAJUSTE, NUMTOTAL = range( 5 )
class KardexDelegate( QStyledItemDelegate ):

    def createEditor( self, parent, option, index ):
        if index.column() == NUMAJUSTE:
            spinbox = QSpinBox( parent )
            spinbox.setRange( -1000, 1000 )
            spinbox.setSingleStep( 1 )
            return spinbox
        else:
            QStyledItemDelegate.createEditor( self, parent, option, index )

    def setEditorData( self, editor, index ):
        if index.column() == NUMAJUSTE:
            editor.setValue( index.data( Qt.EditRole ).toInt()[0] )
        else:
            QStyledItemDelegate.setEditorData( self, editor, index )


