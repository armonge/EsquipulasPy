# -*- coding: utf-8 -*-
'''
Created on 07/06/2010

@author: Andrés Reyes Monge
'''
import logging

from PyQt4.QtGui import QStyledItemDelegate, QSpinBox, QDoubleSpinBox
from PyQt4.QtCore import Qt

from utility.widgets.searchpanel import SingleSelectionSearchPanelDelegate

from document import arqueo
CANTIDAD, DENOMINACION,  TOTAL, MONEDA, IDDOCUMMENTOT, IDDENOMINACION = range( 6 )
class ArqueoDelegate( SingleSelectionSearchPanelDelegate ):
    def __init__( self, denominations, parent = None ):
        super( ArqueoDelegate, self ).__init__( parent )
        self.denominationsmodel = denominations

        self.proxymodel.setFilterKeyColumn( 0 )
        
    def filter(self, model, current):
        filtro =  "|^".join( [str(line.denominationId) for line in model.sourceModel().lines if line.denominationId != 0 and line.denominationId != current ] )

        if filtro !="":
            filtro = "[^" + filtro + "]"

        return filtro

    def createEditor( self, parent, option, index ):
        if index.column() == CANTIDAD:
            spinbox = QSpinBox( parent )
            spinbox.setRange( 0, 1000 )
            spinbox.setSingleStep( 1 )
            return spinbox
        elif index.column() == DENOMINACION:
            

            self.proxymodel.setSourceModel(self.denominationsmodel)
            
            current = index.model().data(index.model().index(index.row(), IDDENOMINACION) ).toInt()[0]
            print  index.model()
            print "**************************************"
            for column in range(index.model().columnCount()):
                print index.model().index(0, column).data().toString()
            print "***************************************"
            print "current: ", current, "filter", self.filter(index.model(), current )
            self.proxymodel.setFilterRegExp( self.filter(index.model(), current ))
            

            sp =  super(ArqueoDelegate, self).createEditor(parent, option, index)

            sp.setColumnHidden(0)
            sp.setColumnHidden(2)
            sp.setColumnHidden(3)

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
            editor.lineEdit().selectAll()
        else:
            QStyledItemDelegate.setEditorData( self, editor, index )

    def setModelData( self, editor, model, index ):
        if index.column() == DENOMINACION:
            try:
                proxyindex = self.proxymodel.index(editor.currentIndex() , 0 )
                sourceindex = self.proxymodel.mapToSource(proxyindex)
                model.setData(                index, self.denominationsmodel.items[sourceindex.row() ] )
            except IndexError as inst:
                logging.error(inst)
        else:
            QStyledItemDelegate.setModelData( self, editor, model, index )


