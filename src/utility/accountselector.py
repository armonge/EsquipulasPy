# -*- coding: utf-8 -*-
'''
Created on 30/05/2010

@author: Andrés Reyes Monge

Este modulo tiene el codigo necesario para crear una tabla en la que se editaran montos
para cuentas contables, para utilizarlo es necesario asignar el modelo y el delegado 
a un QTableView, el delegado necesita como parametro una consulta SQL que retorne una tabla del tipo
IDCUENTA, CODIGO, DESCRIPCION
'''
from decimal import  Decimal
from PyQt4.QtGui import  QStyledItemDelegate, QDoubleSpinBox
from PyQt4.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant, SIGNAL, QSize
from PyQt4.QtSql import QSqlQuery
from utility.widgets.searchpanel import SearchPanel
from utility.moneyfmt import moneyfmt
from utility.singleselectionmodel import SingleSelectionModel

IDCUENTA, CODCUENTA, NCUENTA, MONTO = range( 4 )


class AccountsSelectorModel( QAbstractTableModel ):
    def __init__( self ):
        QAbstractTableModel.__init__( self )
        self.lines = []

    @property
    def valid( self ):
        return True if self.currentSum == 0 and self.validLines > 0 else False
    @property
    def validLines( self ):
        return len( [line for line in self.lines if line.valid] )

    @property
    def currentSum( self ):
        currentsum = sum( [line.amount for line in  self.lines if line.valid ] )
        return currentsum if currentsum != 0 else Decimal( 0 )

    def columnCount( self, index = QModelIndex() ):
        return 4

    def rowCount( self, index = QModelIndex() ):
        return len( self.lines )

    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemIsEnabled | Qt.ItemIsEditable


    def insertRows( self, position, rows = 1, index = QModelIndex ):
        self.beginInsertRows( QModelIndex(), position, position + rows - 1 )
        for row in range( rows ):
            self.lines.insert( position + row, AccountsSelectorLine() )
            self.lines[-1].amount = self.currentSum * -1
        self.endInsertRows()
        self.dirty = True
        return True

    def removeRows( self, position, rows = 1, parent = QModelIndex ):
        self.beginRemoveRows( QModelIndex(), position, position + rows - 1 )
        self.lines = self.lines[:position] + self.lines[position + rows:]
        self.endRemoveRows()
        self.dirty = True
        return True


    def data( self, index, role = Qt.DisplayRole ):
        """
        darle formato a los campos de la tabla
        """
        if not index.isValid() or not ( 0 <= index.row() < len( self.lines ) ):
            return ""
        line = self.lines[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == IDCUENTA:
                return line.itemId
            elif column == NCUENTA:
                return line.name
            elif column == CODCUENTA:
                return line.code
            elif column == MONTO:
                return moneyfmt( line.amount, 4, "C$" ) if line.amount != 0 else ""
        if role == Qt.EditRole:
            if column == MONTO:
                return line.amount

    def setData( self, index, value, role = Qt.EditRole ):
        if index.isValid() and 0 <= index.row() < len( self.lines ):
            line = self.lines[index.row()]
            column = index.column()
            if column in ( NCUENTA, CODCUENTA ):
                line.itemId = value[0]
                line.code = value[1]
                line.name = value[2]
            if column == MONTO:
                line.amount = Decimal( value.toString() ) if type( value ) != Decimal else value


            if not self.valid and self.lines[-1].valid:
                self.insertRow( len( self.lines ) )
            elif not self.valid and not self.lines[-1].valid:
                self.lines[-1].amount = self.currentSum * -1
            elif self.valid and not self.lines[-1].valid:
                if len( self.lines ) > 1:
                    self.removeRows( len( self.lines ) - 1, 1 )
            self.emit( SIGNAL( "dataChanged(QModelIndex, QModelIndex)" ), index, index )
            self.emit( SIGNAL( "dataChanged(QModelIndex, QModelIndex)" ), self.index(MONTO, len(self.lines) ),self.index(MONTO, len(self.lines) ))
            
            return True
        return False

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignLeft | Qt.AlignVCenter
            return Qt.AlignRight | Qt.AlignVCenter

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == IDCUENTA:
                return "Id"
            elif section == CODCUENTA:
                return "Codigo"
            elif section == NCUENTA:
                return "Nombre"
            elif section == MONTO:
                return "Monto C$"

        return int( section + 1 )


class AccountsSelectorDelegate( QStyledItemDelegate ):
    def __init__( self, query,showTable=False ):
        QStyledItemDelegate.__init__( self )
        self.showTable=showTable
        query.exec_()
        if not query.size() > 0:
            raise UserWarning("No hay cuentas contables en el modelo")
        self.accounts = SingleSelectionModel()
        self.accounts.headers = ["idcuenta", "codigo", "descripcion"]
        while query.next():
            self.accounts.items.append( [
                                        query.value( 0 ).toInt()[0],
                                        query.value( 1 ).toString(),
                                        query.value( 2 ).toString()
                                        ] )



    def createEditor( self, parent, option, index ):
        
        if index.column() in ( CODCUENTA, NCUENTA ):
            if index.data() != "":
                self.accounts.items.append( [
                                         index.model().lines[index.row()].itemId,
                                         index.model().lines[index.row()].code,
                                         index.model().lines[index.row()].name
                                         ] )
            sp = SearchPanel( self.accounts, parent,self.showTable )
            sp.setColumn( index.column() )
            return sp
        elif index.column() == MONTO:
            doublespinbox = QDoubleSpinBox( parent )
            doublespinbox.setMinimum( -1000000 )
            doublespinbox.setMaximum( 1000000 )
            doublespinbox.setDecimals( 4 )

            return doublespinbox

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
            model.setData( index, [
                                   self.accounts.index( editor.currentIndex(), 0 ).data(),
                                   self.accounts.index( editor.currentIndex(), 1 ).data(),
                                   self.accounts.index( editor.currentIndex(), 2 ).data()
                                   ] )
            del self.accounts.items[editor.currentIndex()]
        else:
            QStyledItemDelegate.setModelData( self, editor, model, index )

    def sizeHint( self, option, index ):
        u"""
        El tamaño sugerido de los datos en el modelo
        """
        fm = option.fontMetrics
        if index.column() == CODCUENTA:
            return QSize( 130, fm.height() )
        if index.column() == NCUENTA:
            return QSize( 250, fm.height() )
        
        if index.column() == MONTO:
            return QSize( 80, fm.height() )
        
        return QStyledItemDelegate.sizeHint( self, option, index )

class AccountsSelectorLine(object):
    def __init__( self ):
        self.itemId = 0
        self.amount = Decimal( 0 )
        self.code = ""
        self.name = ""

    @property
    def valid( self ):
        return self.amount != 0 and self.itemId != 0

    def save( self, iddocumento, linea ):
        """
        Este metodo guarda el movimiento 
        @param iddocumento: El id del documento al que esta asociado el movimiento
        @param linea: El numero de la linea en el documento
        """
        if not self.valid:
            raise Exception( "Se intento guardar un movimiento no valido" )

        query = QSqlQuery()

        if not query.prepare( """
        INSERT INTO cuentasxdocumento (idcuenta, iddocumento, monto, nlinea) VALUES ( :idcuenta, :iddocumento, :monto, :nlinea)
        """ ):
            raise Exception( "No se pudo preparar la consulta para insertar un movimiento" )
        query.bindValue( ":idcuenta", self.itemId )
        query.bindValue( ":iddocumento", iddocumento )
        query.bindValue( ":monto", self.amount.to_eng_string() )
        query.bindValue( ":nlinea", linea )

        if not query.exec_():
            print query.lastError().text()
            raise Exception( "Error al insertar uno de los movimientos" )
                

