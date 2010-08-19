# -*- coding: utf-8 -*-
'''
Created on 07/06/2010

@author: Andrés Reyes Monge
'''
from document import arqueo
from PyQt4.QtGui import QStyledItemDelegate, QSpinBox, QDoubleSpinBox
from PyQt4.QtCore import Qt
from utility.widgets.searchpanel import SearchPanel

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
                row = index.model().mapToSource(index).row()
                model = index.model().sourceModel()
                self.denominationsmodel.items.append( [
                                         model.lines[row].denominationId,
                                         model.lines[row].denomination,
                                         model.lines[row].value.to_eng_string(),
                                         model.lines[row].currencyId,
                                         model.lines[row].symbol
                                         ] )
            sp= SearchPanel(self.denominationsmodel, parent )
            sp.setColumnHidden(0)
            sp.setColumnHidden(2)
            sp.setColumnHidden(3)
            
            sp.setEditable(True)
            sp.setModel( self.denominationsmodel )
            sp.setModelColumn( 1 )
            return sp
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
            try:
                model.setData( index, self.denominationsmodel.items[editor.currentIndex()] )
                del self.denominationsmodel.items[editor.currentIndex()]
            except IndexError as inst:
                logging.error(inst)
        else:
            QStyledItemDelegate.setModelData( self, editor, model, index )


