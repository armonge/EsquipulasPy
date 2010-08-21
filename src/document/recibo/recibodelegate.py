# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: Luis Carlos Mejia Garcia
'''
from PyQt4.QtGui import QSortFilterProxyModel,QStyledItemDelegate,QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QCompleter
from PyQt4.QtCore import Qt, QSize,QVariant
from utility.widgets.searchpanel import SearchPanel
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from utility.singleselectionmodel import SingleSelectionModel
IDTIPOPAGO,DESCRIPCION,  REFERENCIA,  MONTO = range(4)
class ReciboDelegate(QStyledItemDelegate):
    
    def __init__(self, parent=None):
        super(ReciboDelegate, self).__init__(parent)
        
        query = QSqlQuery("""
            SELECT
                idtipomovimiento,
                CONCAT(descripcion, ' ' , moneda) as tipopago,
                idtipomoneda,
                m.simbolo
                FROM tiposmoneda m
            JOIN tiposmovimientocaja p
            ;
        """)
        self.filtrados = [] 
        query.exec_()
        while query.next():
            self.filtrados.append(query.value(1).toString())
            
        self.abonosmodel =QSqlQueryModel()
        self.abonosmodel.setQuery(query)
        self.proxymodel = QSortFilterProxyModel()
        self.proxymodel.setSourceModel(self.abonosmodel)
        self.proxymodel.setFilterKeyColumn(1)
        self.completer = QCompleter()            
        self.completer.setModel(self.proxymodel)
        
        self.completer.setCompletionColumn(1)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        


    def createEditor( self, parent, option, index ):
        if index.column() == DESCRIPCION:             
            combo = QComboBox(parent)
            combo.setEditable(True)
            value = index.data().toString()
            self.filtrados.append(value)
            self.proxymodel.setFilterRegExp(self.filter())
            combo.setModel(self.proxymodel)
            combo.setModelColumn(1)
            combo.setCompleter(self.completer)
            return combo
        
        elif index.column() == MONTO:
            doublespinbox = QDoubleSpinBox( parent )
            doublespinbox.setMinimum( -1000000 )
            doublespinbox.setMaximum( 1000000 )
            doublespinbox.setDecimals( 4 )
            doublespinbox.setAlignment(Qt.AlignHCenter)
            return doublespinbox
        elif index.column() == REFERENCIA:
            textbox = QStyledItemDelegate.createEditor(self, parent, option,index)
            textbox.setAlignment(Qt.AlignHCenter)
            return textbox
            
    def removeFromFilter(self,value):
        try:
            self.filtrados.remove(value)
            return True
        except:
            return False
        
    def filter(self):
        filtro =  "$|^".join(self.filtrados)
        if filtro !="":
            filtro = "^" + filtro + "$"
        return filtro

    def setEditorData( self, editor, index ):
        data = index.data()
        if index.column() == DESCRIPCION:
            i = editor.findText( data if type( data ) != QVariant else data.toString() )
            if i == -1:
                i = 0
            editor.setCurrentIndex( i )
        elif index.column() == MONTO:
            editor.setValue( index.model().data( index, Qt.EditRole ) if index.model().data( index, Qt.EditRole ) != "" else 0 )
        else:
            QStyledItemDelegate.setEditorData( self, editor, index )

    def setModelData( self, editor, model, index ):

        if index.column()==DESCRIPCION:
            modelo = self.proxymodel
            if modelo.rowCount()>0:
                fila = editor.currentIndex()
                model.setData(index,  [
                                           modelo.index(fila,0).data().toInt()[0],  
                                           modelo.index(fila,1).data().toString(),
                                           modelo.index(fila,2).data().toInt()[0],
                                           modelo.index(fila,3).data().toString()
                    ])
                self.removeFromFilter(modelo.index(fila,1).data().toString())
                self.proxymodel.setFilterRegExp(self.filter())

        else:
            QStyledItemDelegate.setModelData( self, editor, model, index )

    def sizeHint( self, option, index ):
        u"""
        El tamaño sugerido de los datos en el modelo
        """
        fm = option.fontMetrics
        if index.column() == DESCRIPCION:
            return QSize( 250, fm.height() )
        else:
            return QSize( 150, fm.height() )
        
        return QStyledItemDelegate.sizeHint( self, option, index )
