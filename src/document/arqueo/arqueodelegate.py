# -*- coding: utf-8 -*-
'''
Created on 07/06/2010

@author: Andrés Reyes Monge
'''
from document import arqueo
from PyQt4.QtGui import QStyledItemDelegate, QSpinBox, QDoubleSpinBox, QComboBox
from PyQt4.QtCore import Qt

CANTIDAD, DENOMINACION, TOTAL = range( 3 )
class ArqueoDelegate( QStyledItemDelegate ):
    def __init__( self, denominations, parent = None ):
        super( ArqueoDelegate, self ).__init__( parent )
        self.denominationsmodel = denominations
    def createEditor( self, parent, option, index ):
        if index.column() == CANTIDAD:
            spinbox = QSpinBox( parent )
            spinbox.setRange( 0, 1000 )
            spinbox.setSingleStep( 1 )
            return spinbox
        elif index.column() == DENOMINACION:
            if index.data() != "":
                self.denominationsmodel.items.append( [
                                         index.model().lines[index.row()].denominationId,
                                         index.model().lines[index.row()].denomination,
                                         index.model().lines[index.row()].value,
                                         index.model().lines[index.row()].currencyId
                                         ] )
            combo = QComboBox( parent )
            combo.setModel( self.denominationsmodel )
            combo.setModelColumn( 1 )
            return combo
        else:
            return QStyledItemDelegate.createEditor( self, parent, option, index )

    def setEditorData( self, editor, index ):
        if index.column() == CANTIDAD:
            editor.setValue( index.data( Qt.DisplayRole ).toInt()[0] )
        elif index.column() == DENOMINACION:
            text = index.data( Qt.DisplayRole ).toString()
            i = editor.findText( text )
            if i == -1:
                i = 1
            editor.setCurrentIndex( i )
        else:
            QStyledItemDelegate.setEditorData( self, editor, index )

    def setModelData( self, editor, model, index ):
        if index.column() == DENOMINACION:
            print editor.rootModelIndex().data().toString()
            model.setData( index, self.denominationsmodel.items[editor.currentIndex()] )
            del self.denominationsmodel.items[editor.currentIndex()]
        else:
            QStyledItemDelegate.setModelData( self, editor, model, index )


