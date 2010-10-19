# -*- coding: utf-8 -*-
'''
Created on 09/08/2010

@author: Andrés Reyes Monge
'''
import logging
from decimal import Decimal

from PyQt4.QtCore import QAbstractTableModel, Qt, QModelIndex, QDateTime
from PyQt4.QtSql import QSqlDatabase, QSqlQuery

from utility.moneyfmt import moneyfmt
from utility import constantes
from utility.accountselector import AccountsSelectorModel
from document.kardexother.lineakardexother import LineaKardexOther

IDARTICULO, DESCRIPCION, COSTO, CANTIDAD, COSTOT = range( 5 )
IDCUENTA, CODCUENTA, NCUENTA, MONTO = range( 4 )
class KardexOtherModel( QAbstractTableModel ):
    '''
    Esta clase es el modelo utilizado en la tabla en la que se editan documentos
    de tipo kardex generados por entradas o salidas extraordinarias, son del tipo AJUSTEBODEGA
    '''
    __documentType = constantes.IDAJUSTEBODEGA
    def __init__( self ):
        '''
        Constructor
        '''
        super( KardexOtherModel, self ).__init__()

        self.accountsmodel = KardexOtherAccountsModel()
        """
        @ivar: Este objeto mantiene la lista de cuentas contables para este documento
        @type: KardexOtherAccountsModel
        """

        self.printedDocumentNumber = ""
        """
        @ivar: El numero de kardex impreso
        @type: string
        """

        self.datetime = QDateTime.currentDateTime()
        """
        @ivar:La hora y fecha del documento
        @type:QDateTime
        """

        self.uid = 0
        """
        @ivar: El id del usuario que realiza este kardex
        @type: int
        """

        self.observations = ""
        """
        @ivar: Las  observaciones del documento kardex
        @type:string
        """

        self.lines = []
        """
        @ivar: Las lineas del documento kardex
        @type: OtherKardexLine
        """

        self.warehouseId = 0
        """
        @ivar: El id de la bodega en que se hace el movimiento
        @type: int
        """

        self.exchangeRateId = 0
        """
        @ivar: El id del tipo  de cambio
        @type: int
        """
        self.exchangeRate = Decimal( 0 )
        """
        @ivar: El tipo de cambio
        @type: Decimal
        """

        self.conceptId = 0
        """
        @ivar: El id del concepto del documento
        @type: int
        """

        self.validError = ""
        """
        @ivar:
        @type: string
        """

        self.dataChanged[QModelIndex, QModelIndex].connect( self.updateAccounts )

    def updateAccounts( self, _index1, _index2 ):
        """
        Actualizar el modelo de cuentas contables
        """
        self.accountsmodel.setData( self.accountsmodel.index( 0, MONTO ), self.totalCostC )

    @property
    def totalCostC( self ):
        return self.totalCost * self.exchangeRate

    @property
    def totalCost( self ):
        """
        El costo total en dolares
        """
        tmp = sum( [line.totalCost for line in self.lines if line.valid] )
        return tmp if tmp != 0 else Decimal( 0 )

    @property
    def validLines( self ):
        return len( [line for line in self.lines if line.valid] )

    @property
    def valid( self ):
        try:
            if not  self.validLines > 0:
                raise UserWarning( "No hay lineas validas en la tabla" )
            elif not  self.exchangeRateId != 0:
                raise UserWarning( "No hay un tipo de cambio para "\
                                   + "el documento" )
            elif not self.warehouseId > 0:
                raise UserWarning( "No ha seleccionado una bodega para "\
                                   + "el documento" )
            elif not self.conceptId > 0:
                raise UserWarning( "No ha seleccionado un concepto para"\
                                   " el documento" )
            elif not self.accountsmodel.valid:
                raise UserWarning( "Tiene un error con sus cuentas contables" )
            elif not self.uid > 0:
                raise UserWarning( "No se ha especificado el usuario de "\
                                   "este documento" )
        except UserWarning as inst:
            self.validError = unicode( inst )
            return False

        return True

    def data( self, index, role = Qt.DisplayRole ):
        if not index.isValid() or not ( 0 <= index.row() < len( self.lines ) ):
            return None
        line = self.lines[index.row()]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == IDARTICULO:
                return line.itemId
            elif column == DESCRIPCION:
                return line.description
            elif column == CANTIDAD:
                return line.quantity
            elif column == COSTO:
                return moneyfmt( line.itemCost, 4, "US$" )
            elif column == COSTOT:
                return moneyfmt( line.totalCost, 4, "US$" )
        elif role == Qt.EditRole:
            if column == COSTO:
                return line.itemCost
            if column == COSTOT:
                return line.totalCost

    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column() != IDARTICULO:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable
        else:
            return Qt.ItemIsEnabled

    def insertRows( self, position, rows = 1, _index = QModelIndex() ):
        self.beginInsertRows( QModelIndex(), position, position + rows - 1 )
        for row in range( rows ):
            self.lines.insert( position + row, LineaKardexOther() )
        self.endInsertRows()
        return True

    def setData( self, index, value, _role = Qt.EditRole ):
        """
        modificar los datos del modelo, este metodo se comunica con el delegate
        """
        if index.isValid() and 0 <= index.row() < len( self.lines ):
            line = self.lines[index.row()]
            if index.column() in ( DESCRIPCION, IDARTICULO, COSTO ):
                line.itemId = value[0]
                line.description = value[1]
                line.itemCost = value[2]
            elif index.column() == CANTIDAD:
                line.quantity = value.toInt()[0]
            self.dirty = True

            if index.row() == len( self.lines ) - 1 and line.valid:
                self.insertRow( len( self.lines ) )

            self.dataChanged.emit( index, index )


            return True
        return False

    def removeRows( self, position, rows = 1, index = QModelIndex() ):
        """
        Borrar filas del modelo
        @rtype: bool
        @return: si se pudo o no borrar la fila
        """
        self.beginRemoveRows( QModelIndex(), position, position + rows - 1 )
        for n in range( rows ):
            try:
                del self.lines[position + n]
            except IndexError:
                pass
        self.endRemoveRows()
        self.dirty = True
        self.dataChanged.emit( index, index )

        if len( self.lines ) == 0:
            self.insertRow( 0 )
        return True

    def rowCount( self, _index = QModelIndex() ):
        return len( self.lines )

    def columnCount( self, _index = QModelIndex() ):
        return 5

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        """
        El contenido que aparece en las cabeceras del modelo
        """
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignLeft | Qt.AlignVCenter
            return Qt.AlignRight | Qt.AlignVCenter

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == IDARTICULO:
                return "Id"
            elif section == DESCRIPCION:
                return u"Descripción"
            elif section == CANTIDAD:
                return "Cantidad"
            elif section == COSTO:
                return "Costo"
            elif section == COSTOT:
                return "Costo Total"

    def save( self ):
        """
        Este metodo guarda el documento actual en la base de datos
        @rtype: bool
        @return: Si el documento se pudo guardar o no
        """
        if not self.valid:
            raise Exception ( "El documento a salvar no es valido" )
        query = QSqlQuery()
        try:
            if not QSqlDatabase.database().transaction():
                raise Exception( u"No se pudo comenzar la transacción" )

            #insertar el documento
            if not query.prepare( """
            INSERT INTO documentos(ndocimpreso, fechacreacion, idtipodoc, idestado, observacion, idtipocambio, total, idbodega, idconcepto)
            VALUES( :ndocimpreso, :fechacreacion, :idtipodoc, :estado, :observacion, :tipocambio, :total, :idbodega, :idconcepto)
            """ ):
                raise Exception( "No se pudo preparar la consulta para ingresar el documento" )

            query.bindValue( ":ndocimpreso", self.printedDocumentNumber )
            query.bindValue( ":fechacreacion", self.datetime.toString( 'yyyyMMddhhmmss' ) )
            query.bindValue( ":idtipodoc", self.__documentType )
            query.bindValue( ":estado", constantes.CONFIRMADO )
            query.bindValue( ":observacion", self.observations )
            query.bindValue( ":tipocambio", self.exchangeRateId )
            query.bindValue( ":total", self.totalCostC.to_eng_string() )
            query.bindValue( ":idbodega", self.warehouseId )
            query.bindValue( ":idconcepto", self.conceptId )

            if not query.exec_():
                raise Exception( "No se pudo insertar el documento" )


            insertedId = query.lastInsertId() #el id del documento que se acaba de insertar

            #insertar el usuario
            if not query.prepare( """
            INSERT INTO personasxdocumento (idpersona, iddocumento, idaccion)
            VALUE (:idusuario, :iddocumento, :accion)
            """ ):
                raise Exception( "No se pudo preparar la consulta para ingresar el usuario" )
            query.bindValue( ":idusuario", self.uid )
            query.bindValue( ":iddocumento", insertedId )
            query.bindValue( ":accion", constantes.AUTOR )

            if not query.exec_():
                raise Exception( "No se pudo insertar  el usuario" )



            #Guardar las cuentas contables
            for i, line in enumerate( [line for line in self.accountsmodel.lines if line.valid] ):
                line.save( insertedId, i )

            #Guardar las lineas
            for i, line in enumerate( [line for line in self.lines if line.valid] ):
                line.save( insertedId, i )


            if not QSqlDatabase.database().commit():
                raise Exception( "No se pudo hacer commit" )

            return True
        except Exception as inst:
            logging.critical( unicode( inst ) )
            logging.critical( query.lastError().text() )
            QSqlDatabase.database().rollback()
            return False


class KardexOtherAccountsModel( AccountsSelectorModel ):
    def __init__( self ):
        super( KardexOtherAccountsModel, self ).__init__()

    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled
        elif index.row() != 0:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable
        else:
            return Qt.ItemIsEnabled

    @property
    def valid( self ):
        return super( KardexOtherAccountsModel, self ).valid and self.lines[0].valid
