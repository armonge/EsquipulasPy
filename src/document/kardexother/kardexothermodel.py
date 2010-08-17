# -*- coding: utf-8 -*-
'''
Created on 09/08/2010

@author: armonge
'''
from decimal import Decimal
from PyQt4.QtCore import QAbstractTableModel, Qt, QModelIndex, QDateTime

from utility import constantes
from document.kardexother.lineakardexother import LineaKardexOther

IDARTICULO, DESCRIPCION, CANTIDAD = range(3)
class KardexOtherModel(QAbstractTableModel):
    '''
    Esta clase es el modelo utilizado en la tabla en la que se editan documentos
    de tipo kardex generados por entradas o salidas extraordinarias
    '''
    __documentType = constantes.IDKARDEX    
    def __init__(self):
        '''
        Constructor
        '''
        super(KardexOtherModel, self).__init__()

        self.datetime = QDateTime.currentDateTime()
        """
        @ivar:La hora y fecha del documento
        @type:string
        """

        self.uid = 0
        """
        @ivar: El id del usuario que realiza este kardex
        @type: int
        """
        
        self.observations = ""
        """
        @ivar: Las  observaciones del documento kardex
        @type:string
        """
        
        self.lines = []
        """
        @ivar: Las lineas del documento kardex
        @type: OtherKardexLine
        """

        self.warehouseId = 0
        """
        @ivar: El id de la bodega en que se hace el movimiento
        @tyoe: int
        """

        self.exchangeRateId = 0
        """
        @ivar: El id del tipo  de cambio
        @type: int
        """
        self.exchangeRate = Decimal(0)
        """
        @ivar: El tipo de cambio
        @type: Decimal
        """

        
        
    def data( self, index, role = Qt.DisplayRole ):
        if not index.isValid() or not ( 0 <= index.row() < len( self.lines ) ):
            return None
        line = self.lines[index.row()]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == IDARTICULO:
                return line.itemId
            elif column == DESCRIPCION:
                return line.description
            elif column == CANTIDAD:
                return line.quantity

    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column() != IDARTICULO:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable 
        else:
            return Qt.ItemIsEnabled
            
    def insertRows( self, position, rows = 1, index = QModelIndex() ):
        self.beginInsertRows( QModelIndex(), position, position + rows - 1 )
        for row in range( rows ):
            self.lines.insert( position + row, LineaKardexOther( ) )
        self.endInsertRows()
        return True

    def setData( self, index, value, role = Qt.EditRole ):
        """
        modificar los datos del modelo, este metodo se comunica con el delegate
        """
        if index.isValid() and 0 <= index.row() < len( self.lines ):
            line = self.lines[index.row()]
            if index.column() in (DESCRIPCION, IDARTICULO):
                print value.toString()
                line.itemId = value[0]
                line.description = value[1]
            elif index.column() == CANTIDAD:
                line.quantity == value.toInt()[0]
            self.dirty = True
            self.dataChanged.emit(index, index)
            return True
        return False

        
    def rowCount( self, index = QModelIndex() ):
        return len( self.lines )

    def columnCount( self, index = QModelIndex() ):
        return 3

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        """
        El contenido que aparece en las cabeceras del modelo
        """
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignLeft | Qt.AlignVCenter
            return Qt.AlignRight | Qt.AlignVCenter

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == IDARTICULO:
                return "Id"
            elif section == DESCRIPCION:
                return u"Descripción"
            elif section == CANTIDAD:
                return "Cantidad"