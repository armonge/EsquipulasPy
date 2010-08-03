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
            idtipopago,
            CONCAT(descripcion, ' ' , moneda) as tipopago,
            idtipomoneda        
            FROM tiposmoneda m
        JOIN tipospago p
        ;
        """) 
        self.prods = SingleSelectionModel()
        query.exec_()
        while query.next():
            self.prods.items.append([
                query.value(0).toInt()[0],
                query.value(1).toString(),
                query.value(2).toInt()[0]
                                    ])



    def createEditor( self, parent, option, index ):
        if index.column() == DESCRIPCION:
            completer = QCompleter()            
            combo = QComboBox(parent)
            combo.setEditable(True)
            

            combo.setModel(self.prods)
            completer.setModel(self.prods)
            combo.setModelColumn(1)
            completer.setCompletionColumn(1)
            tabla=index.model()
            if index.data() != "":
                self.prods.items.append([tabla.index( index.row(),0 ).data().toInt()[0]  ,
                                        index.data().toString(),
                                        tabla.index( index.row(),2 ).data().toInt()[0]
                                         ])

            
                
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
            combo.setCompleter(completer)
            return combo
        if index.column() == MONTO:
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
            if self.prods.rowCount()>0:
                try:
                    model.setData(index,  [
                                           self.prods.items[editor.currentIndex()][0],  
                                           self.prods.items[editor.currentIndex()][1],
                                           self.prods.items[editor.currentIndex()][2]
                    ])
                    del self.prods.items[editor.currentIndex()]
                except IndexError as inst:
                    print inst
        else:
            QStyledItemDelegate.setModelData( self, editor, model, index )

    def sizeHint( self, option, index ):
        u"""
        El tama�o sugerido de los datos en el modelo
        """
        fm = option.fontMetrics
        if index.column() == DESCRIPCION:
            return QSize( 250, fm.height() )
        elif index.column() == MONTO:
            return QSize( 80, fm.height() )
        
        return QStyledItemDelegate.sizeHint( self, option, index )
    
#    def __init__(self, parent=None):
#        super(ReciboDelegate, self).__init__(parent)
#        
#        query = QSqlQuery("""
#        SELECT 
#            idtipopago,
#            CONCAT(descripcion, ' ' , moneda) as tipopago,
#            idtipomoneda
#            
#            FROM tiposmoneda m
#        JOIN tipospago p
#        ;
#        """) 
#        self.prods = SingleSelectionModel()
#        query.exec_()
#        while query.next():
#            self.prods.items.append([
#                query.value(0).toInt()[0],
#                query.value(1).toString(),
#                query.value(2).toInt()[0]
#                                    ])
#             
#    def sizeHint( self, option, index ):
#        fm = option.fontMetrics
#        if index.column() == DESCRIPCION:
#            return QSize( 250, fm.height() )
#
#        return QStyledItemDelegate.sizeHint( self, option, index )
#
#
#
#    def createEditor(self,  parent,  option,  index):
#        if index.column() == REFERENCIA:
#            textbox = QLineEdit(parent)
#            return textbox
#        elif index.column() == DESCRIPCION :           
#            completer = QCompleter()            
#            combo = QComboBox(parent)
#            combo.setEditable(True)
#            
#
#            combo.setModel(self.prods)
#            completer.setModel(self.prods)
#            combo.setModelColumn(1)
#            completer.setCompletionColumn(1)
#            tabla=index.model()
#            if index.data() != "":
#                self.prods.items.append([tabla.index( index.row(),0 ).data().toInt()[0]  ,
#                                        index.data().toString(),
#                                        tabla.index( index.row(),2 ).data().toInt()[0]
#                                         ])
#
#            
#                
#            completer.setCaseSensitivity(Qt.CaseInsensitive)
#            completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
#            combo.setCompleter(completer)
#            return combo
#        elif index.column()==MONTO:
#            spinbox = QDoubleSpinBox(parent)
#            spinbox.setRange(1,  999999999)
#            spinbox.setDecimals(4)
#            spinbox.setSingleStep(1)
#            spinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
#            return spinbox
#        else:
#            QStyledItemDelegate.createEditor(self,  parent,  option,  index)
#    
#    def setEditorData(self, editor, index):
#        """
#        En esta funcion se inicializan los datos a mostrarse en el editor
#        se ejecuta justo en el momento en el que se muestra el editor
#        """
#        text = index.model().data(index, Qt.DisplayRole)
##        if index.column() == REFERENCIA:
##            editor.setValue( index.model().data(index, Qt.DisplayRole) if index.model().data(index, Qt.DisplayRole) != "" else 0 )
##        el
#        if index.column() == MONTO:
#            valortemp =index.model().data(index, Qt.EditRole) if index.model().data(index, Qt.EditRole) != "" else 0
#            #if index.model().tasabanco !=0 and  
#            editor.setValue( valortemp )
#        elif index.column() == DESCRIPCION:
#            i = editor.findText(text)
#            if i == -1:
#                i = 0
#            editor.setCurrentIndex(i)
#        else:
#            QStyledItemDelegate.setEditorData(self, editor, index)
#
#    def setModelData(self,  editor,  model,  index):
#        """
#        En este evento se toma el resultado del editor y se introduco en el modelo
#        """
#        text = index.model().data(index,  Qt.DisplayRole)
#        if index.column() == DESCRIPCION:
#            try:
#                model.setData(index,  [
#                                       self.prods.items[editor.currentIndex()][0],  
#                                       self.prods.items[editor.currentIndex()][1],
#                                       self.prods.items[editor.currentIndex()][2]
#                ])
#                del self.prods.items[editor.currentIndex()]
#            except IndexError as inst:
#                print inst
#        else:
#            QStyledItemDelegate.setModelData(self,  editor,  model,  index)
#
