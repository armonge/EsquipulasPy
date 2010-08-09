# -*- coding: utf-8 -*-
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

    def rowCount( self, index = QModelIndex() ):
        return len( self.items )

    def columnCount( self, index = QModelIndex() ):
        """
        El numero de columnas es el largo del primer indice del arreglo
        """
        try:
            return len( self.items[0] )
        except IndexError:
            return 0

