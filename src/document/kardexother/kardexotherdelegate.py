# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: Andrés Reyes Monge
'''
from decimal import Decimal

from PyQt4.QtGui import QStyledItemDelegate, QSpinBox, QDoubleSpinBox,QSortFilterProxyModel 
from PyQt4.QtCore import Qt,QSize 
from PyQt4.QtSql import QSqlQueryModel

from utility.widgets.searchpanel import SingleSelectionSearchPanelDelegate
from utility.moneyfmt import moneyfmt



IDARTICULO, DESCRIPCION, CANTIDAD = range(3)
class KardexOtherDelegate( SingleSelectionSearchPanelDelegate ):
    def __init__( self, model, showTable=True , parent = None  ):
        super(KardexOtherDelegate, self).__init__( )
        self.articles = model
        self.proxymodel = SingleSelectionModel()
        self.proxymodel.setFilterKeyColumn(0)
        self.proxymodel.setSourceModel(self.articles)
        self.showTable = showTable

        self.proxymodel.setFilterKeyColumn(IDARTICULO)
        self.proxymodel.setSourceModel(self.articles)

    def createEditor(self,  parent,  option,  index):
        if index.column() == CANTIDAD:
            spinbox = QSpinBox(parent)
            spinbox.setRange(-500,500)
            spinbox.setSingleStep(1)
            spinbox.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
            return spinbox
        elif index.column() in (DESCRIPCION, IDARTICULO):
            current = index.model().data(index.model().index( index.row(), IDARTICULO) )
            self.proxymodel.setFilterRegExp( self.filter(index.model(),current ))

            return super(KardexOtherDelegate, self).createEditor(parent, option, index)
        else:
            super(KardexOtherDelegate, self).createEditor(parent,  option,  index)

    def setEditorData(self, editor, index):
        """
        En esta funcion se inicializan los datos a mostrarse en el editor
        se ejecuta justo en el momento en el que se muestra el editor
        """
        if index.column() == CANTIDAD:
            editor.setValue( index.model().data(index, Qt.DisplayRole) if index.model().data(index, Qt.DisplayRole) != "" else 0 )
        elif index.column() in (IDARTICULO,  DESCRIPCION):

            current = index.model().data(index.model().index(index.row() , IDARTICULO))
            self.proxymodel.setFilterRegExp( self.filter(index.model(),current ))
            
            super(KardexOtherDelegate, self).setEditorData(editor, index)
            editor.lineEdit().selectAll()
        else:
            super(KardexOtherDelegate, self).setEditorData(editor, index)

    def setModelData(self,  editor,  model,  index):
        """
        En este evento se toma el resultado del editor y se introduco en el modelo
        """
        if index.column() in (DESCRIPCION, IDARTICULO):
            if self.proxymodel.rowCount()>0:

                fila = editor.currentIndex()
                modelo = self.proxymodel
                model.setData( index, [
                                       modelo.index(fila , IDARTICULO ).data(Qt.EditRole).toInt()[0],
                                       modelo.index(fila, DESCRIPCION ).data(Qt.EditRole).toString(),
                        ])
        else:
            super(KardexOtherDelegate, self).setModelData(editor,  model,  index)

    def sizeHint( self, option, index ):
        fm = option.fontMetrics
        if index.column() == IDARTICULO:
            return QSize( fm.width( "99" ), fm.height() )
        if index.column() == DESCRIPCION:
            return QSize( 250, fm.height() )

        return super(KardexOtherDelegate, self).sizeHint(  option, index )

class SingleSelectionModel( QSortFilterProxyModel ):
    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignLeft | Qt.AlignVCenter

        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if  section == DESCRIPCION:
                return u"Descripción"
            elif section == IDARTICULO:
                return "Id"
        return int( section + 1 )
