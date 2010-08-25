# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: Luis Carlos Mejia Garcia
'''
from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt, SIGNAL, QDateTime,QSize

from lineaabono import LineaAbono
from PyQt4.QtGui import QStyledItemDelegate, QDoubleSpinBox,QSortFilterProxyModel
#from utility.singleselectionmodel import SingleSelectionModel 
from decimal import Decimal
from utility.moneyfmt import moneyfmt
from PyQt4.QtSql import QSqlQueryModel

#IDARTICULO, DESCRIPCION, REFERENCIA, MONTO, MONTODOLAR, MONEDA = range( 6 )
IDFAC, NFAC, TOTALFAC,SUBABONO,ABONO,SALDO = range( 6 )
class AbonoModel( QAbstractTableModel ):
    """
    esta clase es el modelo utilizado en la tabla en la que se editan los documentos
    """
    def __init__( self ,lineas):
        super( AbonoModel, self ).__init__()

        self.dirty = False
        self.lines =lineas


    @property
    def valid( self ):
        """
        Un documento es valido cuando 
            self.printedDocumentNumber != ""
            self.providerId !=0
            self.validLines >0
            self.__idIVA !=0
            self.uid != 0
            self.warehouseId != 0 
        """
        if int( self.validLines ) < 1:
            print( "No Hay ninguna linea no valida" )
            return False
        else:
            return True

    @property
    def validLines( self ):
        """
        la cantidad de lineas validas que hay en el documento
        """
        foo = 0
        for line in self.lines:
            if line.valid:foo += 1
        return foo

# Se reimplemento este procedimiento que por defecto toma dos argumentos, aunque no se usen
    def rowCount( self, index = QModelIndex ):
        return len( self.lines )

    def columnCount( self, index = QModelIndex ):
        return 6

    def data( self, index, role = Qt.DisplayRole ):
        """
        darle formato a los campos de la tabla
        """
        if not index.isValid() or not ( 0 <= index.row() < len( self.lines ) ):
            return ""
        line = self.lines[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == NFAC:
                return line.nFac
            elif column == ABONO:
                return moneyfmt( Decimal( line.monto ), 4, "US$" ) if line.monto != 0 else ""
            elif column == TOTALFAC:
                return moneyfmt(line.totalFac ,  4,  "US$")
            elif column == SUBABONO:
                return moneyfmt(line.subMonto ,  4,  "US$")
            elif column == SALDO:
                return moneyfmt(line.saldo ,  4,  "US$")
        elif role == Qt.EditRole:
#            Esto es lo que recibe el delegate cuando va a mostrar la el widget 
            if column == ABONO:
                return line.monto
            elif column == SUBABONO:
                return line.subMonto
            

    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags( QAbstractTableModel.flags( self, index ) | Qt.ItemIsEditable )

    def setData( self, index, value, role = Qt.EditRole ):
        """
        modificar los datos del modelo, este metodo se comunica con el delegate
        """
        if index.isValid() and 0 <= index.row() < len( self.lines ) :
            line = self.lines[index.row()]
            column = index.column()
            if column == NFAC:
                line.idFac = value[0]
                line.nFac = value[1]
                line.totalFac = value[2]
            elif column == ABONO:
                valor = Decimal( value.toString() )
                line.monto= valor if valor <= line.totalFac else line.totalFac
#                line.setMonto( valor if valor <= line.totalFac else line.totalFac)
                line.saldo = line.totalFac - line.monto
            self.dirty = True

            self.emit( SIGNAL( "dataChanged(QModelIndex, QModelIndex)" ), index, index )
#            #si la linea es valida y es la ultima entonces aniadir una nueva
#            if  index.row() == len(self.lines) -1 and line.valid:
#                self.insertRows(len(self.lines))

            return True
        return False

    @property
    def total( self ):
        """
        El total del documento, esto es el total antes de aplicarse el IVA
        """
        tmpsubtotal = sum( [linea.monto for linea in self.lines if linea.valid] )
        return tmpsubtotal if tmpsubtotal > 0 else Decimal( 0 )

    def insertRows( self, position, rows = 1, index = QModelIndex ):
        self.beginInsertRows( QModelIndex(), position, position + rows - 1 )
        for row in range( rows ):
            self.lines.insert( position + row, LineaAbono( self ) )
        self.endInsertRows()
        self.dirty = True
        return True

    def removeRows( self, position, tabla, rows = 1, index = QModelIndex ):
        if len( self.lines ) > 0:
            self.beginRemoveRows( QModelIndex(), position, position + rows - 1 )
            n = position + rows - 1
# borrar el rango de lineas indicado de la ascendente para que no halla problema con el indice de las lineas 
# muestro la fila de la tabla facturas que esta relacionada a la linea que borre
            while n >= position:
                    tabla.setRowHidden( self.lines[n].nlinea, False )
                    del self.lines[n]
                    n = n - 1

            self.endRemoveRows()
            self.dirty = True
            return True
        else:
            return False

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignLeft | Qt.AlignVCenter
            return Qt.AlignRight | Qt.AlignVCenter
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if  section == NFAC:
                return u"No. Factura"
            elif section == ABONO:
                return "Abono"
            elif section == TOTALFAC:
                return "Total"
            elif section == SALDO:
                return "Saldo Pendiente"
            elif section == SUBABONO:
                return "Abono sin Iva"
        return int( section + 1 )

class AbonoDelegate(QStyledItemDelegate):
    def sizeHint( self, option, index ):
        fm = option.fontMetrics
        if index.column() == NFAC:
            return QSize( 250, fm.height() )
        return QStyledItemDelegate.sizeHint( self, option, index )



    def createEditor(self,  parent,  option,  index):
        if index.column()==ABONO:
            spinbox = QDoubleSpinBox(parent)
            max= index.model().lines[index.row()].totalFac
            
            spinbox.setRange(0.0001,max)
            spinbox.setDecimals(4)
            spinbox.setSingleStep(1)
            spinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return spinbox
        else:
            None
    
    def setEditorData(self, editor, index):
        """
        En esta funcion se inicializan los datos a mostrarse en el editor
        se ejecuta justo en el momento en el que se muestra el editor
        """
        if index.column() == ABONO:
            valortemp=index.model().data(index, Qt.EditRole)
            editor.setValue( valortemp )
        else:
            QStyledItemDelegate.setEditorData(self, editor, index)
