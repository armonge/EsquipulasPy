# -*- coding: utf-8 -*-
'''
Created on 13/07/2010

@author: Luis Carlos Mejia
'''
from PyQt4.QtGui import  QStyledItemDelegate, QDoubleSpinBox,QSortFilterProxyModel
from utility.widgets.searchpanel import SearchPanel
from PyQt4.QtSql import QSqlQueryModel
from PyQt4.QtCore import  QSize,QVariant,Qt


IDCUENTA, CODCUENTA, NCUENTA, MONTO = range( 4 )
class SearchPanelDelegate( QStyledItemDelegate ):
    def __init__( self, query,showTable=False   ):
        QStyledItemDelegate.__init__( self )
        self.accounts = QSqlQueryModel()
        self.accounts.setQuery(query)
        self.proxymodel = QSortFilterProxyModel()
        self.proxymodel.setFilterKeyColumn(0)
        self.proxymodel.setSourceModel(self.accounts)
        self.showTable = showTable
        self.filtrados =[]
        
    def createEditor( self, parent, option, index ):
        if index.column() in ( CODCUENTA, NCUENTA ):
            value = index.model().index(index.row(),0).data().toString()
            self.removeFromFilter(value)            
            self.proxymodel.setFilterRegExp(self.filter())
            sp = SearchPanel( self.proxymodel, parent,self.showTable )
            sp.setColumn( index.column() )
            return sp
        elif index.column() == MONTO:
            doublespinbox = QDoubleSpinBox( parent )
            doublespinbox.setMinimum( -1000000 )
            doublespinbox.setMaximum( 1000000 )
            doublespinbox.setDecimals( 4 )

            return doublespinbox

    def removeFromFilter(self,value):
        try:
            self.filtrados.remove(value)
            return True
        except:
            return False
        
    def filter(self):
        filtro =  "|^".join(self.filtrados)
        if filtro !="":
            filtro = "[^" + filtro + "]"
        return filtro

    def setEditorData( self, editor, index ):
        
        data = index.data()
        if index.column() in ( CODCUENTA, NCUENTA ):
            i = editor.findText( data if type( data ) != QVariant else data.toString() )
            if i == -1:
                i = 0
            editor.setCurrentIndex( i )
        elif index.column() == MONTO:
            editor.setValue( index.model().data( index, Qt.EditRole ) if index.model().data( index, Qt.EditRole ) != "" else 0 )
        else:
            QStyledItemDelegate.setEditorData( self, editor, index )

    def setModelData( self, editor, model, index ):

        if index.column() in ( NCUENTA, CODCUENTA ):
            if self.proxymodel.rowCount()>0:
                fila = editor.currentIndex()
                modelo = self.proxymodel
                model.setData( index, [
                                       modelo.index(fila , 0 ).data(),
                                       modelo.index(fila, 1 ).data(),
                                       modelo.index( fila, 2 ).data()
                                       ] )
                self.filtrados.append(modelo.index(fila , 0 ).data().toString())
                self.proxymodel.setFilterRegExp(self.filter())
        else:
            QStyledItemDelegate.setModelData( self, editor, model, index )

    def sizeHint( self, option, index ):
        u"""
        El tama�o sugerido de los datos en el modelo
        """
        fm = option.fontMetrics
        if index.column() == CODCUENTA:
            return QSize( 130, fm.height() )
        if index.column() == NCUENTA:
            return QSize( 250, fm.height() )
        
        if index.column() == MONTO:
            return QSize( 80, fm.height() )
        
        return QStyledItemDelegate.sizeHint( self, option, index )
