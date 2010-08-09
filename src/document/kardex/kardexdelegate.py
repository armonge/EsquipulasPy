# -*- coding: utf-8 -*-
'''
Created on 16/07/2010

@author: Andrés Reyes Monge
'''
from PyQt4.QtGui import QStyledItemDelegate, QSpinBox
from PyQt4.QtCore import Qt
IDARTICULO, DESCRIPCION, NUMDOC, NUMAJUSTE, NUMTOTAL = range( 5 )
class KardexDelegate(QStyledItemDelegate):
 
    def createEditor( self, parent, option, index ):
        if index.column() == NUMAJUSTE:
            spinbox = QSpinBox( parent )
            spinbox.setRange( -1000, 1000)
            spinbox.setSingleStep( 1 )
            return spinbox
        else:
            QStyledItemDelegate.createEditor( self, parent, option, index )

    def setEditorData( self, editor, index ):
        if index.column() == NUMAJUSTE:
            editor.setValue( index.data( Qt.EditRole ).toInt()[0] )
        else:
            QStyledItemDelegate.setEditorData( self, editor, index )


