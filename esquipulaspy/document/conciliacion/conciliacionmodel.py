# -*- coding: utf-8 -*-
'''
Created on 03/07/2010

@author: Luis Carlos Mejia
'''
from PyQt4.QtCore import  QVariant, QModelIndex, Qt, QDate
from decimal import Decimal
from lineaconciliacion import LineaConciliacion
from utility import constantes
from utility.moneyfmt import moneyfmt
from utility.docbase import DocumentBase
from utility.decorators import return_decimal

#from utility.constantes import IDCONCILIACION, IDDEPOSITO, IDNC, IDND, IDCHEQUE, IDERROR
#CAMBIAR columncount()
FECHA, CONCEPTO, DEBE, HABER, SALDO, CONCILIADO, DELBANCO, IDTIPODOC = range( 8 )
FECHA, BANCO, CUENTABANCO, MONEDA, CUENTACONTABLE, SALDOBANCO, IDDOC = range( 7 )

class ConciliacionModel( DocumentBase ):
    __documentType = constantes.IDCONCILIACION

    def __init__( self, saldo_inicial_libro, fecha, banco, cuenta_bancaria, id_cuenta_contable, codigo_cuenta_contable, moneda ):
        """
        @ivar saldo_inicial_libro: El saldo inicial del libro
        @type saldo_inicial_libro: Decimal 
        """
        super( ConciliacionModel, self ).__init__()

        self._saldo_inicial_libro = saldo_inicial_libro

        self.datetime = fecha
        self._banco = banco
        self._id_cuenta_contable = id_cuenta_contable
        self._cuenta_bancaria = cuenta_bancaria
        self._codigo_cuenta_contable = codigo_cuenta_contable
        self._moneda = moneda
        self.lines = []
        self.saldo_inicial_banco = Decimal( 0 )


    @property
    def valid( self ):
        try:
            if not self.id_cuenta_contable > 0:
                raise UserWarning( "No ha elegido la cuenta bancaria" )
            elif self.diferencia != 0:
                raise UserWarning(u"Los saldos según banco y según libro no están conciliados")
        except UserWarning as inst:
            self._valid_error = unicode( inst )
            return False
        return True

    @property
    def fecha_conciliacion( self ):
        return QDate( self.datetime.year(), self.datetime.month(), self.datetime.daysInMonth() )

    @property
    def id_cuenta_contable( self ):
        return self._id_cuenta_contable

    @property
    def cuenta_bancaria( self ):
        return self._cuenta_bancaria

    @property
    def codigo_cuenta_contable( self ):
        return self._codigo_cuenta_contable

    @property
    def cuenta_contable( self ):
        return self._cuenta_contable

    @property
    def moneda( self ):
        return self._moneda

    @property
    def banco( self ):
        return self._banco

    @property
    @return_decimal
    def saldo_inicial_libro( self ):
        return self._saldo_inicial_libro

    @property
    def diferencia( self ):
        return abs( self.total_banco - self.total_libro )

    @property
    @return_decimal
    def total_libro( self ):
        return self.saldo_inicial_banco + self.total_depositos - self.total_cheques

    @property
    @return_decimal
    def total_banco( self ):
        return self.saldo_inicial_libro + self.total_nota_credito - self.total_nota_debito

    @property
    @return_decimal
    def total_depositos( self ):
        return sum( [ line.monto for line in self.lines if line.conciliado and line.tipo_doc == constantes.IDDEPOSITO ])

    @property
    @return_decimal
    def total_cheques( self ):
        return sum([ line.monto for line in self.lines if line.conciliado and line.tipo_doc == constantes.IDCHEQUE ])

    @property
    @return_decimal
    def total_nota_credito( self ):
        return sum( [ line.monto for line in self.lines if line.conciliado and line.tipo_doc == constantes.IDNOTACREDITO ])

    @property
    @return_decimal
    def total_nota_debito( self ):
        return sum([ line.monto for line in self.lines if line.conciliado and line.tipo_doc == constantes.IDND ])

    def columnCount( self, _index = QModelIndex() ):
        return 8

    def data( self, index, role = Qt.DisplayRole ):
        if not index.isValid() or not ( 0 <= index.row() < len( self.lines ) ):
            return None

        line = self.lines[index.row()]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == FECHA:
                return line.fecha
            elif column == CONCEPTO:
                return line.descripcion
            elif column == DEBE:
                return moneyfmt( line.monto, 4, self.moneda ) if line.monto > 0 else None
            elif column == HABER:
                return moneyfmt( abs( line.monto ), 4, self.moneda ) if line.monto < 0 else None
            elif column == SALDO:
                return moneyfmt( line.saldo, 4, self.moneda )
            elif column == DELBANCO:
                return 'Si' if line.del_banco else 'No'
            elif column == IDTIPODOC:
                return str( line.tipo_doc )

        elif role == Qt.EditRole:
            if column == IDTIPODOC:
                return str( line.tipo_doc )
            elif column == DELBANCO:
                return "1" if line.del_banco else "0"
            elif column == CONCILIADO:
                return "1" if line.conciliado else "0"

        elif role == Qt.CheckStateRole and column == CONCILIADO and index.row() > 0:
            return QVariant( Qt.Checked if line.conciliado else Qt.Unchecked )


    def flags( self , index ):
        if not index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

        if index.column() == CONCILIADO:
            return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData( self, index, data, role = Qt.DisplayRole ):
        if not index.isValid():
            return False
        if index.column() == CONCILIADO and role == Qt.CheckStateRole:
            if index.row() > 0:
                self.lines[index.row()].conciliado = data.toBool()
                self.dataChanged.emit( index, index )

            return True

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int( Qt.AlignLeft | Qt.AlignVCenter )
            return int( Qt.AlignRight | Qt.AlignVCenter )

        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == FECHA:
                return "Fecha"
            elif section == CONCEPTO:
                return "Concepto"
            elif section == DEBE:
                return "DEBE"
            elif section == HABER:
                return "HABER"
            elif section == SALDO:
                return "SALDO"
            elif section == CONCILIADO:
                return "Conciliar"
            elif section == DELBANCO:
                return "Doc. Externo"

    def insertRows( self, position, rows = 1, _index = QModelIndex() ):
        """
        Insertar filas en el modelo
        @rtype: bool
        @return: Si se pudo insertar la fila en el modelo
        """

        self.beginInsertRows( QModelIndex(), position, position + rows - 1 )
        for row in range( rows ):
            self.lines.insert( position + row, LineaConciliacion( self ) )

        self.endInsertRows()

        return True


    def removeRows( self, position, rows = 1, index = QModelIndex() ):
        self.beginRemoveRows( index, position, position + rows - 1 )

        for _i in range( rows ):
            self.lines.pop( position )

        self.endRemoveRows()
