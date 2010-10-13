# -*- coding: utf-8 -*-
'''
Created on 07/10/2010

@author: armonge
'''

from PyQt4.QtGui import QTableView, QItemSelectionModel, QAbstractItemDelegate
class LiquidacionTableDetails( QTableView ):
    '''
    TODO:Deberia de poder hacerla más generica
    
    Esta vista esta diseñada para trabajar con el modelo de liquidación
    su función es manejar el evento closeEditor para que cuando el usuario
    termine de editar el Costo de Compra de un articulo y presione Tab 
    el siguiente elemento sea la descripción de la siguiente linea
    '''
    def closeEditor ( self, editor, hint ):
        if hint == QAbstractItemDelegate.EditNextItem:
            index = self.selectionModel().currentIndex()
            if index.column() == 3:
                model = self.model()
                if model.rowCount() > index.row() + 1:
                    new_index = model.index( index.row() + 1, 1 )
                    self.selectionModel().setCurrentIndex( new_index ,
                                                            QItemSelectionModel.Current )
                    self.edit( new_index )
                elif model.rowCount() == index.row() + 1:
                    new_index = model.index( 0, 1 )
                    self.selectionModel().setCurrentIndex( new_index ,
                                                           QItemSelectionModel.Current )
                    self.edit( new_index )
                else:
                    new_index = model.index( index.row(), 1 )
                    self.selectionModel().setCurrentIndex( new_index ,
                                                           QItemSelectionModel.Current )
                    self.edit( new_index )
            else:
                super( LiquidacionTableDetails, self ).closeEditor( editor, hint )

        super( LiquidacionTableDetails, self ).closeEditor( editor, hint )
