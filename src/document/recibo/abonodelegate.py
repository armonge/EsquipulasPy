# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: armonge
'''
from PyQt4.QtGui import QStyledItemDelegate,QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QCompleter
from PyQt4.QtCore import Qt, QSize
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from utility.singleselectionmodel import SingleSelectionModel 
#IDTIPOPAGO,DESCRIPCION,  REFERENCIA,  MONTO,  TOTALPROD = range(5)
IDFAC,NFAC,ABONO = range(3)
class AbonoDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(AbonoDelegate, self).__init__(parent)
        
        
        
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
             
    def sizeHint( self, option, index ):
        fm = option.fontMetrics
        if index.column() == NFAC:
            return QSize( 250, fm.height() )

        return QStyledItemDelegate.sizeHint( self, option, index )



    def createEditor(self,  parent,  option,  index):
#        if index.column() == REFERENCIA:
#            textbox = QLineEdit(parent)
#            return textbox
#        el
        if index.column() == NFAC :           
            return None
        elif index.column()==ABONO:
            spinbox = QDoubleSpinBox(parent)
            spinbox.setRange(0.0001,999999999)
            spinbox.setDecimals(4)
            spinbox.setSingleStep(1)
            spinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return spinbox
        else:
            QStyledItemDelegate.createEditor(self,  parent,  option,  index)
    
    def setEditorData(self, editor, index):
        """
        En esta funcion se inicializan los datos a mostrarse en el editor
        se ejecuta justo en el momento en el que se muestra el editor
        """
        if index.column() == ABONO:
#            valortemp =index.model().data(index, Qt.EditRole) if index.model().data(index, Qt.EditRole) != "" else 0
            valortemp=index.model().data(index, Qt.EditRole)
            editor.setValue( valortemp )
        else:
            QStyledItemDelegate.setEditorData(self, editor, index)

    def setModelData(self,  editor,  model,  index):
        """
        En este evento se toma el resultado del editor y se introduco en el modelo
        """
#        text = index.model().data(index,  Qt.DisplayRole)
#        if index.column() == NFAC:
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
        QStyledItemDelegate.setModelData(self,  editor,  model,  index)


