# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: armonge
'''
from PyQt4.QtCore import Qt, QSize
from PyQt4.QtGui import  QSpinBox, QDoubleSpinBox, \
    QSortFilterProxyModel
from decimal import Decimal
from utility.moneyfmt import moneyfmt
from utility.widgets import SingleSelectionSearchPanelDelegate
IDARTICULOEX, DESCRIPCIONEX, PRECIOEX, COSTOEX, EXISTENCIAEX, IDBODEGAEX = range( 6 )


IDARTICULO, DESCRIPCION, CANTIDAD, PRECIO, TOTALPROD = range( 5 )
class FacturaDelegate( SingleSelectionSearchPanelDelegate ):
    """
    El delegado para la tabla factura
    """
    def __init__( self, model, showTable = True , parent = None ):
        super( FacturaDelegate, self ).__init__( showTable, parent )
        self.proxymodel.setSourceModel( model )
        self.proxymodel.setFilterKeyColumn( IDARTICULOEX )
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
                model = index.model()

                current = model.index( index.row(), IDARTICULOEX ).data()
                self.proxymodel.setFilterRegExp( self.filter( model , current ) )
                sp = super( FacturaDelegate, self ).createEditor( parent, option, index )
                #sp.setColumnHidden( IDBODEGAEX )
                #sp.setColumnHidden( IDARTICULOEX )
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
            data = index.data( Qt.DisplayRole ).toInt()[0]
            editor.setValue( data  if data != "" else 0 )
        elif index.column() == PRECIO:
            data = index.data( Qt.EditRole ).toDouble()[0]
            editor.setValue( data )
        elif index.column() == DESCRIPCION:
            model = index.model()
            current = model.data( model.index( index.row(), IDARTICULOEX ) )
            self.proxymodel.setFilterRegExp( self.filter( model, current ) )

            i = editor.findText( text )
            if i == -1:
                i = 0

            editor.setCurrentIndex( i )
            editor.lineEdit().selectAll()
        else:
            super( FacturaDelegate, self ).setEditorData( editor, index )

    def setModelData( self, editor, model, index ):
        """
        En este evento se toma el resultado del editor y se introduco en el modelo
        """
        if index.column() in ( IDARTICULO, DESCRIPCION ):
            if self.proxymodel.rowCount() > 0:
                if editor.currentIndex() != -1:
                    proxyindex = self.proxymodel.index( editor.currentIndex() , 0 )
                    sourceindex = self.proxymodel.mapToSource( proxyindex )

                    fila = sourceindex.row()
                    modelo = self.articles
                    model.setData( index, [
                                           modelo.index( fila , IDARTICULOEX ).data( Qt.EditRole ).toInt()[0],
                                           modelo.index( fila, DESCRIPCION ).data( Qt.EditRole ).toString(),
                                           modelo.index( fila, PRECIOEX ).data( Qt.EditRole ).toString(),
                                           modelo.index( fila, COSTOEX ).data( Qt.EditRole ).toString(),
                                           modelo.index( fila, EXISTENCIAEX ).data( Qt.EditRole ).toInt()[0],
                                           modelo.index( fila, IDBODEGAEX ).data( Qt.EditRole ).toInt()[0]
                            ] )
        else:
            super( FacturaDelegate, self ).setModelData( editor, model, index )

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

        return super( FacturaDelegate, self ).sizeHint( option, index )


class SingleSelectionModel( QSortFilterProxyModel ):
    def data( self, index, role = Qt.DisplayRole ):
        """
        darle formato a los campos de la tabla
        """
        value = super( SingleSelectionModel, self ).data( index, role )
        if role == Qt.DisplayRole:
            if index.column() == PRECIOEX :
                return moneyfmt( Decimal( value.toString() ), 4, "US$" )
            elif index.column() == COSTOEX:
                return moneyfmt( Decimal( value.toString() ), 4, "C$" )
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
            elif section == PRECIOEX:
                return "Precio Unit."
            elif section == COSTOEX:
                return "Costo C$"
            elif section == IDARTICULOEX:
                return "Id"
            elif section == EXISTENCIAEX:
                return "Existencia"
            elif section == IDBODEGAEX:
                return "Bodega"
        return int( section + 1 )
