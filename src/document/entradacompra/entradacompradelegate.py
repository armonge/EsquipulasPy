# -*- coding: utf-8 -*-
'''
Created on 18/05/2010


@author: armonge
'''
from PyQt4.QtGui import QStyledItemDelegate, QSpinBox, QDoubleSpinBox
from PyQt4.QtCore import Qt, QSize
from utility.widgets.searchpanel import SearchPanel

IDARTICULO, DESCRIPCION, CANTIDAD, PRECIO, PRECIOD, TOTALPROD, TOTALD = range( 7 )
class EntradaCompraDelegate( QStyledItemDelegate ):

    def createEditor( self, parent, option, index ):
        """
        Aca se crean los widgets para edición
        """
        if index.column() == CANTIDAD:
            spinbox = QSpinBox( parent )
            spinbox.setRange( 1, 1000 )
            spinbox.setSingleStep( 1 )
            spinbox.setAlignment( Qt.AlignRight | Qt.AlignVCenter )
            return spinbox
        elif index.column() == DESCRIPCION :
            if index.data() != "":
                self.prods.items.append( [ index.model().data( index.model().index( index.row(), 0 ) ) , index.data().toString()] )

            sp = SearchPanel( self.prods, parent )
            return sp

        elif index.column() == TOTALPROD:
            return None

        elif index.column() in ( PRECIO, PRECIOD ):
            spinbox = QDoubleSpinBox( parent )
            spinbox.setRange( 0, 10000 )
            spinbox.setDecimals( 4 )
            spinbox.setSingleStep( 1 )
            spinbox.setAlignment( Qt.AlignRight | Qt.AlignVCenter )
            return spinbox
        else:
            return QStyledItemDelegate.createEditor( self, parent, option, index )

    def setEditorData( self, editor, index ):
        """
        En esta funcion se inicializan los datos a mostrarse en el editor
        se ejecuta justo en el momento en el que se muestra el editor
        """
        text = index.model().data( index, Qt.DisplayRole )
        if index.column() == CANTIDAD:
            editor.setValue( index.model().data( index, Qt.DisplayRole ) if index.model().data( index, Qt.DisplayRole ) != "" else 0 )
        elif index.column() in ( PRECIO, PRECIOD ):
            editor.setValue( index.model().data( index, Qt.EditRole ) if index.model().data( index, Qt.EditRole ) != 0 else 1 )
        elif index.column() == DESCRIPCION:
            i = editor.findText( text )
            if i == -1:
                i = 0
            editor.setCurrentIndex( i )
        else:
            QStyledItemDelegate.setEditorData( self, editor, index )

    def setModelData( self, editor, model, index ):
        """
        En este evento se toma el resultado del editor y se introduco en el modelo
        """
        if index.column() == DESCRIPCION:
            try:
                model.setData( index, [self.prods.items[editor.currentIndex()][0],
                                       self.prods.items[editor.currentIndex()][1]
                ] )
                del self.prods.items[editor.currentIndex()]
            except IndexError as inst:
                print inst
        else:
            QStyledItemDelegate.setModelData( self, editor, model, index )

    def sizeHint( self, option, index ):
        u"""
        El tamaño sugerido de los datos en el modelo
        """
        fm = option.fontMetrics
        if index.column() == IDARTICULO:
            return QSize( fm.width( "99" ), fm.height() )
        if index.column() == DESCRIPCION:
            return QSize( 250, fm.height() )

        return QStyledItemDelegate.sizeHint( self, option, index )
