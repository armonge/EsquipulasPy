# -*- coding: utf-8 -*-

'''
Created on 19/05/2010

@author: armonge
'''
from PyQt4.QtGui import QStyledItemDelegate, QSpinBox
from PyQt4.QtCore import Qt
DESCRIPCION, PRECIO, CANTIDADMAX, CANTIDAD, TOTALPROD = range( 5 )
class DevolucionDelegate( QStyledItemDelegate ):

    def createEditor( self, parent, option, index ):
        if index.column() == CANTIDAD:
            spinbox = QSpinBox( parent )
            spinbox.setRange( 0, index.model().lines[index.row()].maxquantity )
            spinbox.setSingleStep( 1 )
            return spinbox
        else:
            QStyledItemDelegate.createEditor( self, parent, option, index )

    def setEditorData( self, editor, index ):
        if index.column() == CANTIDAD:
            editor.setValue( index.data( Qt.DisplayRole ).toInt()[0] )
        else:
            QStyledItemDelegate.setEditorData( self, editor, index )


