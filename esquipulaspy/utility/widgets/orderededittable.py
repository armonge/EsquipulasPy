# -*- coding: utf-8 -*-
'''
Created on 07/10/2010

@author: armonge
'''

from PyQt4.QtGui import QTableView, QItemSelectionModel, QAbstractItemDelegate
class OrderedEditTable( QTableView ):
    '''
    Esta vista esta diseñada para trabajar con el modelo de liquidación
    su función es manejar el evento closeEditor para que cuando el usuario
    termine de editar el Costo de Compra de un articulo y presione Tab 
    el siguiente elemento sea la descripción de la siguiente linea
    '''
    def __init__( self, parent = None ):
        super( OrderedEditTable, self ).__init__( parent )
        self.__left = 0
        self.__right = 0

    def setOrder( self, left, right ):
        if 0 <= left < right:
            self.__left = left
            self.__right = right
    @property
    def editOrderDefined( self ):
        return self.__left != 0 or self.__right != 0

    def closeEditor ( self, editor, hint ):
        if self.editOrderDefined:
            if hint == QAbstractItemDelegate.EditNextItem:
                index = self.selectionModel().currentIndex()
                if index.column() == self.__right:
                    model = self.model()
                    if model.rowCount() > index.row() + 1:
                        new_index = model.index( index.row() + 1, self.__left )
                        self.selectionModel().setCurrentIndex( new_index ,
                                                                QItemSelectionModel.Current )
                        self.edit( new_index )
                    elif model.rowCount() == index.row() + 1:
                        new_index = model.index( 0, self.__left )
                        self.selectionModel().setCurrentIndex( new_index ,
                                                               QItemSelectionModel.Current )
                        self.edit( new_index )
                    else:
                        new_index = model.index( index.row(), self.__left )
                        self.selectionModel().setCurrentIndex( new_index ,
                                                               QItemSelectionModel.Current )
                        self.edit( new_index )
                else:
                    super( OrderedEditTable, self ).closeEditor( editor, hint )

        super( OrderedEditTable, self ).closeEditor( editor, hint )
