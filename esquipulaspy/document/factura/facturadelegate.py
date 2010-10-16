# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: armonge
'''
from PyQt4.QtGui import QStyledItemDelegate, QSpinBox, QDoubleSpinBox, QSortFilterProxyModel #, QComboBox, QSortFilterProxyModel, QCompleter
from PyQt4.QtCore import Qt, QSize
from utility.widgets import SingleSelectionSearchPanelDelegate
from utility.moneyfmt import moneyfmt
from decimal import Decimal

IDARTICULO, DESCRIPCION, CANTIDAD, PRECIO, TOTALPROD = range( 5 )
#FIXME: Por que no usar range???
PRECIOSUGERIDO = 2
COSTODOLAR = 3
COSTOARTICULO = 4
EXISTENCIA = 5
BODEGA = 6
class FacturaDelegate( SingleSelectionSearchPanelDelegate ):
    def __init__( self, model, showTable = True , parent = None ):
        super(FacturaDelegate, self).__init__(showTable, parent)
        self.proxymodel.setSourceModel( model )
        self.proxymodel.setFilterKeyColumn( IDARTICULO )
        self.articles = model


    def createEditor( self, parent, option, index ):
        if index.column() == CANTIDAD:
            max_items = index.model().lines[index.row()].existencia
            if max_items < 1 :
                return None
            spinbox = QSpinBox( parent )
            spinbox.setRange( 1, max_items )
            spinbox.setSingleStep( 1 )
            spinbox.setAlignment( Qt.AlignRight | Qt.AlignVCenter )
            return spinbox
        elif index.column() == DESCRIPCION :
            if self.articles.rowCount() > 0:
                self.proxymodel.setSourceModel( self.articles )
                
                current = index.model().data( index.model().index( index.row(), IDARTICULO ) )
                self.proxymodel.setFilterRegExp( self.filter( index.model(), current ) )
                sp = super( FacturaDelegate, self ).createEditor( parent, option, index )
                sp.setColumnHidden( BODEGA )
                sp.setColumnHidden(IDARTICULO)
                return sp
        elif index.column() == TOTALPROD:
            return None
        elif index.column() == PRECIO:
            spinbox = QDoubleSpinBox( parent )
            spinbox.setRange( 0.0001, 10000 )
            spinbox.setDecimals( 4 )
            spinbox.setSingleStep( 1 )
            spinbox.setAlignment( Qt.AlignRight | Qt.AlignVCenter )
            return spinbox
        else:
            super( FacturaDelegate, self ).createEditor( parent, option, index )

    def setEditorData( self, editor, index ):
        """
        En esta funcion se inicializan los datos a mostrarse en el editor
        se ejecuta justo en el momento en el que se muestra el editor
        """
        text = index.data( Qt.DisplayRole ).toString()
        if index.column() == CANTIDAD:
            editor.setValue( index.model().data( index, Qt.DisplayRole ) if index.model().data( index, Qt.DisplayRole ) != "" else 0 )
        elif index.column() == PRECIO:
            editor.setValue( index.model().data( index, Qt.EditRole ) if index.model().data( index, Qt.EditRole ) != "" else 0 )
        elif index.column() == DESCRIPCION:
            current = index.model().data( index.model().index( index.row(), IDARTICULO ) )
            self.proxymodel.setFilterRegExp( self.filter( index.model(), current ) )

            i = editor.findText( text )
            if i == -1:
                i = 0

            editor.setCurrentIndex( i )
            editor.lineEdit().selectAll()
        else:
            super(FacturaDelegate,self).setEditorData( editor, index )

    def setModelData( self, editor, model, index ):
        """
        En este evento se toma el resultado del editor y se introduco en el modelo
        """
        if index.column() in (IDARTICULO, DESCRIPCION):
            if self.proxymodel.rowCount() > 0:
                if editor.currentIndex() != -1:
                    proxyindex = self.proxymodel.index( editor.currentIndex() , 0 )
                    sourceindex = self.proxymodel.mapToSource( proxyindex )

                    fila = sourceindex.row()
                    modelo = self.articles
                    model.setData( index, [
                                           modelo.index( fila , IDARTICULO ).data( Qt.EditRole ).toInt()[0],
                                           modelo.index( fila, DESCRIPCION ).data( Qt.EditRole ).toString(),
                                           modelo.index( fila, PRECIOSUGERIDO ).data( Qt.EditRole ).toString(),
                                           modelo.index( fila , COSTODOLAR ).data( Qt.EditRole ).toString(),
                                           modelo.index( fila, COSTOARTICULO ).data( Qt.EditRole ).toString(),
                                           modelo.index( fila, EXISTENCIA ).data( Qt.EditRole ).toInt()[0],
                                           modelo.index( fila, BODEGA ).data( Qt.EditRole ).toInt()[0]
                            ] )
        else:
            super(FacturaDelegate, self).setModelData(  editor, model, index )

    def sizeHint( self, option, index ):
        u"""
        El tamaño sugerido de los datos en el modelo
        """
        fm = option.fontMetrics
#        if index.column() == :
#            return QSize( 130, fm.height() )
        if index.column() == DESCRIPCION:
            return QSize( 250, fm.height() )

        elif index.column() in ( CANTIDAD, PRECIO ):
            return QSize( 100, fm.height() )
        elif index.column() == TOTALPROD:
            return QSize( 200, fm.height() )

        return super(FacturaDelegate, self).sizeHint( option, index )


class SingleSelectionModel( QSortFilterProxyModel ):
    def data( self, index, role = Qt.DisplayRole ):
        """
        darle formato a los campos de la tabla
        """
        value = super(SingleSelectionModel, self).data(  index, role )
        if role == Qt.DisplayRole:
            if index.column() == PRECIOSUGERIDO :
                return moneyfmt( Decimal( value.toString() ), 4, "US$" )
            elif index.column() == COSTOARTICULO:
                return moneyfmt( Decimal( value.toString() ), 4, "C$" )
            elif index.column() == COSTODOLAR:
                return moneyfmt( Decimal( value.toString() ), 4, "US$" )
            else:
                return value
        return value


    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignLeft | Qt.AlignVCenter

        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if  section == DESCRIPCION:
                return u"Descripción"
            elif section == PRECIOSUGERIDO:
                return "Precio Unit."
            elif section == COSTOARTICULO:
                return "Costo C$"
            elif section == IDARTICULO:
                return "Id"
            elif section == COSTODOLAR:
                return "Costo US$"
            elif section == EXISTENCIA:
                return "Existencia"
            elif section == BODEGA:
                return "Bodega"
        return int( section + 1 )
