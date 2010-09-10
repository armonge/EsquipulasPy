# -*- coding: utf-8 -*-
'''
Created on 20/07/2010

@author: Luis Carlos Mejia
'''
from decimal import Decimal

from PyQt4.QtGui import QMainWindow,QAbstractItemView
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase
from PyQt4.QtCore import QDate,pyqtSlot,Qt

from ui.Ui_estadoresultado import Ui_frmEstadoResultado

from utility.moneyfmt import moneyfmt
from utility import user
CODIGO , DESCRIPCION, SALDO , TOTAL,ORDEN = range(5)
class frmEstadoResultado( QMainWindow, Ui_frmEstadoResultado ):
    """
    Formulario para crear nuevas conciliaciones bancarias
    """
    def __init__( self,  parent = None ):
        """
        Constructor
        """
        
        super(frmEstadoResultado, self).__init__(  parent )
        self.setupUi( self )
        self.parentWindow = parent        
#        self.editmodel = None
        self.user = user.LoggedUser
        self.status = True
        self.dtPicker.setMaximumDate(QDate.currentDate())
        self.dtPicker.setDate(QDate.currentDate())

    @pyqtSlot( "QDateTime" )
    def on_dtPicker_dateTimeChanged( self, datetime ):
        """
        Asignar la fecha al objeto __document
        """
        self.updateModel(datetime)
                
    def updateModel(self,fecha):
        try:

            if not QSqlDatabase.database().isOpen():
                QSqlDatabase.database().open()
            self.model = RODetailsModel()
            self.model.setQuery("CALL spEstadoResultado(" + fecha.toString("yyyyMMdd") + ")")
#            self.tabledetails.setSpan(3,1,1,2)
#            self.tabledetails.setSpan(4,1,1,2)
            
            self.tabledetails.setModel(self.model)
            self.tabledetails.setColumnHidden(ORDEN,True)
            pos=0
            self.tabledetails.clearSpans()
            for i in range(self.model.rowCount()):
                pos=self.model.index(i,ORDEN).data().toInt()[0]
                
                if pos == 4:
                    self.tabledetails.setSpan(i,0,1,4)
                elif pos in (11,12,3):
                    self.tabledetails.setSpan(i,1,1,2)
                    
                              
            self.tabledetails.resizeColumnsToContents()
            
        except Exception as inst:
            print inst
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()  



class RODetailsModel(  QSqlQueryModel ):
    """
    El modelo que maneja la tabla en la que se previsualizan los os,
    basicamente esta creado para darle formato al total y al precio
    """
#
#    def columnCount( self, index = QModelIndex() ):
#        return 5

#    def headerData( self, section, orientation, role = Qt.DisplayRole ):
#        if role == Qt.TextAlignmentRole:
#            if orientation == Qt.Horizontal:
#                return int( Qt.AlignLeft | Qt.AlignVCenter )
#            return int( Qt.AlignRight | Qt.AlignVCenter )
#        if role != Qt.DisplayRole:
#            return None
#        if orientation == Qt.Horizontal:
#            if  section == DESCRIPCION:
#                return u"Descripción"
#            elif section == PRECIO:
#                return "Precio"
#            elif section == TOTALPROD:
#                return "TOTAL"
#            elif section == CANTIDAD:
#                return "Cantidad"
#        return int( section + 1 )

    def data( self, index, role = Qt.DisplayRole ):
        """
        Esta funcion redefine data en la clase base, es el metodo que se utiliza para mostrar los datos del modelo
        """
        value = QSqlQueryModel.data( self, index, role )
        if not value.isValid():
            return None
        
        if index.column() in (SALDO,TOTAL):
            if role == Qt.DisplayRole:
                value = value.toString()
                value =moneyfmt( Decimal(value),4,"C$") if value !="" else ""
                
        
        return value


