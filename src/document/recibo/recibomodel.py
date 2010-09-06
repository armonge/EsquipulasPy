# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: Luis Carlos Mejia Garcia
'''

from utility.accountselector import AccountsSelectorModel,QModelIndex
from utility.moneyfmt import moneyfmt
from linearecibo import LineaRecibo
from decimal import  Decimal
from PyQt4.QtCore import QAbstractTableModel, Qt,SIGNAL

IDPAGO, DESCRIPCION, REFERENCIA,BANCO, MONTO, MONTODOLAR, IDMONEDA = range( 7 )
class ReciboModel( AccountsSelectorModel ):
    def __init__( self ,lineas, tipocambio):
        AccountsSelectorModel.__init__( self )
        self.total =Decimal(0) 
        self.tipoCambio = Decimal(tipocambio)
        if self.tipoCambio == 0:
            raise Exception("el tipo de cambio del banco es 0")
        self.lines = lineas
        
    def asignarTotal(self,valor):     
        self.total = valor
        nfilas = self.rowCount()
        if valor <=0:
            self.removeRows(0,nfilas)
            self.insertRow(0)
        elif nfilas>0: 
                valor = self.lines[nfilas-1].monto            
                self.setData(self.index(nfilas-1,MONTO),valor)
        
    def columnCount( self, index = QModelIndex() ):
        return 6

    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled
        
        if self.bloqueada(index):
            return Qt.ItemIsEnabled
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable
    
    def bloqueada(self,index):
        if self.lines[index.row()].monto<0:
            return True 

        if index.column() == REFERENCIA:
            line = self.lines[index.row()]
            return line.pagoId in (0,1)
        elif index.column() == BANCO:
            return self.lines[index.row()].sinBanco
        else:
            return False
    
    @property
    def currentSum( self ):
        currentsum = sum( [line.montoDolar for line in  self.lines] )
        return currentsum if currentsum != 0 else Decimal( 0 )     
#        else:
#            
#            
#            return index.column() in (1,2) and index.row() == 0      
          
    def data( self, index, role = Qt.DisplayRole ):
        """
        darle formato a los campos de la tabla
        """
        if not index.isValid() or not ( 0 <= index.row() < len( self.lines ) ):
            return ""
        line = self.lines[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == DESCRIPCION:
                return line.pagoDescripcion
            elif column == REFERENCIA:
                return line.referencia
            elif column == MONTO:
                value = moneyfmt( line.monto,4, line.simboloMoneda) if line.monto != 0 else ""
                return value
            elif column == MONTODOLAR:
                return moneyfmt( line.montoDolar , 4, "US$" ) if line.montoDolar != 0 else ""
            elif column == IDMONEDA:
                return line.monedaId
            elif column == BANCO:
                return line.banco
            elif column == IDPAGO:
                return line.pagoId
        elif role == Qt.EditRole:
#            Esto es lo que recibe el delegate cuando va a mostrar la el widget 
            if column == MONTO:
                return line.monto
            elif column == IDMONEDA:
                return line.monedaId
            elif column == REFERENCIA:
                return line.referencia
        elif role == Qt.TextAlignmentRole:
            if column != DESCRIPCION:
                return Qt.AlignHCenter | Qt.AlignVCenter 

    def setData( self, index, value, role = Qt.EditRole ):
        if  not index.isValid():
            return None        
        line = self.lines[index.row()]
        column = index.column()
        if column== DESCRIPCION:    
            line.pagoId = value[0]
            line.pagoDescripcion = value[1]
            line.monedaId = value[2]
            line.simboloMoneda = value[3]
            index = self.index(index.row(),MONTO)
            line.monto =Decimal(str(line.montoDolar * self.tipoCambio)) if line.monedaId == 1 else line.montoDolar
            if line.sinBanco:
                line.referencia = ""
                line.bancoId = 0
                line.banco = ""
        elif column == BANCO:
            line.bancoId = value[0]
            print line.bancoId
            line.banco = value[1]
        elif column == MONTO:
            return self.asignarMonto(index,value)
        elif column == REFERENCIA:
            line.referencia= value
            return True
        return False

    def asignarMonto(self,index,value,monedaId=None):
        line = self.lines[index.row()]
        if monedaId==None:
            monedaId = line.monedaId
            
        if type(value) != Decimal:
            value =Decimal( value.toString())
        
        value = Decimal( str(round(value,4)))
        line.monto = value
        line.montoDolar = round(value  / self.tipoCambio,4) if  monedaId==1 else value
        line.montoDolar = Decimal( str(line.montoDolar))

        
        suma = self.currentSum

        suma =  self.total - suma
        suma = Decimal(str(round(suma,4)))
        ultimaFila = len(self.lines)-1
        line = self.lines[ultimaFila] 
        if  suma !=0:
            if line.valid:
                ultimaFila+=1
                self.insertRow(ultimaFila)
                line =self.lines[ultimaFila] 

            line.montoDolar+=suma
            monedaId= line.monedaId    
            line.monto =  round(line.montoDolar * self.tipoCambio,4) if  monedaId==1 else line.montoDolar
            line.monto = Decimal(str(line.monto))

         
            self.emit( SIGNAL( "dataChanged(QModelIndex, QModelIndex)" ), index, index )
            index = self.index(index.row(),MONTODOLAR)
            self.emit( SIGNAL( "dataChanged(QModelIndex, QModelIndex)" ), index, index )
#            print line.montoDolar
            if ultimaFila >0:
                if 0== line.montoDolar:
                    self.removeRows(ultimaFila,1)
        
        return True

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignLeft | Qt.AlignVCenter
            return Qt.AlignRight | Qt.AlignVCenter
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if  section == DESCRIPCION:
                return u"Tipo de Pago"
            elif section == MONTO:
                return "Monto"
            elif section == BANCO:
                return "Banco"
            elif section == MONTODOLAR:
                return u"Monto US$"
            elif section == REFERENCIA:
                return "Referencia"
        return int( section + 1 )

    def insertRows( self, position, rows = 1, index = QModelIndex ):
        self.beginInsertRows( QModelIndex(), position, position + rows - 1 )
        for row in range( rows ):
            self.lines.insert( position + row, LineaRecibo( self ) )
        self.endInsertRows()
        self.dirty = True
        return True

    def removeRows( self, position, rows = 1, index = QModelIndex ):
        if len( self.lines ) > 0:
            self.beginRemoveRows( QModelIndex(), position, position + rows - 1 )
            n = position + rows - 1
            while n >= position:
                    del self.lines[n]
                    n = n - 1

            self.endRemoveRows()
            self.dirty = True
            return True
        else:
            return False