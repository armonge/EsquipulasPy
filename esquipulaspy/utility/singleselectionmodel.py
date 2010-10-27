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
@author: Andrés Reyes Monge
'''
from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt
class SingleSelectionModel( QAbstractTableModel ):
    """
    Modelo generico creado para propositos utilitarios, es muy simple y se deberia de implementar
    un modelo nuevo en vez de heredar de este si se quiere mayor flexibilidad
    """
    def __init__( self ):
        super( SingleSelectionModel, self ).__init__()
        self.items = []
        """
        @ivar: Este arreglo contiene los valores del modelo
        @type: array
        """
        self.headers = []
        """
        @ivar: Este arreglo contiene el texto mostrado en los headers del modelo
        @type: string[]
        """

    def data( self, index, role = Qt.DisplayRole ):
        """
        darle formato a los campos de la tabla
        """
        if not index.isValid() or not ( 0 <= index.row() < len( self.items ) ):
            return ""
        line = self.items[index.row()]
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return line[index.column()]

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignLeft | Qt.AlignVCenter

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            try:
                return self.headers[section]
            except IndexError:
                return ""

    def rowCount( self, _index = QModelIndex() ):
        return len( self.items )

    def columnCount( self, _index = QModelIndex() ):
        """
        El numero de columnas es el largo del primer indice del arreglo
        """
        try:
            return len( self.items[0] )
        except IndexError:
            return 0

