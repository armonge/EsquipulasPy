#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       
#       Copyright 2010 Andrés Reyes Monge <armonge@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#TODO: unittest
from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt, QDateTime
from PyQt4.QtSql import QSqlQuery, QSqlDatabase
from decimal import Decimal
from document.kardex.lineakardex import LineaKardex
from utility import constantes
from utility.decorators import return_decimal
from utility.docbase import DocumentBase
from utility.movimientos import movKardex
import logging

'''
Created on 19/05/2010

@author: Andrés Reyes Monge
'''




IDARTICULO, DESCRIPCION, NUMDOC, NUMAJUSTE, NUMTOTAL = range( 5 )
class KardexModel( DocumentBase ):
    """
    Esta clase es el modelo utilizado en la tabla en la que se editan
     los documentos kardex
    """
    __documentType = constantes.IDKARDEX
    """
    @cvar: El id del tipo de documento
    @type: int
    """
    def __init__( self ):
        super( KardexModel, self ).__init__()
        self.observations = ""
        """
        @ivar:Las observaciones del documento
        @type:string
        """

        self.lines = []
        """
        @ivar:Las lineas en esta devolucion
        @type: LineaKardex[]
        """
        self.printedDocumentNumber = ""
        """
        @ivar:El numero de este kardex
        @type:string
        """

        self.parentId = 0
        """
        @ivar: El  id del documento para el cual se realiza este kardex
        @type:int
        """
        self.parentPrinted = ""
        """
        @ivar: El numero impreso del padre
        @type: string 
        """

        self.datetime = QDateTime.currentDateTime()
        """
        @ivar:La hora y fecha del documento
        @type:string
        """

        self.uid = 0
        """
        @ivar: El id del usuario que realiza este kardex
        @type: int
        """

        self.warehouseId = 0
        """
        @ivar: El id de la bodega
        @type: int
        """
        self.warehouseName = ""
        """
        @ivar: El nombre de la bodega
        @type: string
        """

        self.exchangeRate = Decimal( 0 )
        """
        @ivar: El tipo de cambio
        @type: Decimal
        """
        self.exchangeRateId = 0
        """
        @ivar: El id del tipo de cambio
        @type:int
        """


    @property
    @return_decimal
    def ajusteTotalD( self ):
        return sum( [ line.ajusteMonetario for line in self.lines if line.dirty ] )

    @property
    def ajusteTotalC( self ):
        return self.ajusteTotalD * self.exchangeRate

    @property
    def valid( self ):
        """
        Un documento es valido cuando 
        @rtype: bool
        """
        try:
            if not len( self.lines ) != 0:
                raise UserWarning( "No existen lineas en el kardex" )
            elif not self.exchangeRateId > 0:
                raise UserWarning( "No se ha definido el tipo de "
                + "cambio del documento" )
            elif not self.uid != 0:
                raise UserWarning( "No se ha especificado el usuario"
                + " que realiza este kardex" )
        except UserWarning as inst:
            self._valid_error = unicode( inst )
            return False

        return True



    def columnCount( self, _index = QModelIndex() ):
        return 5

    def data( self, index, role = Qt.DisplayRole ):
        """
        darle formato a los campos de la tabla
        """
        if not index.isValid() or not ( 0 <= index.row() < len( self.lines ) ):
            return None
        line = self.lines[index.row()]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == IDARTICULO:
                return line.itemId
            elif column == DESCRIPCION:
                return line.itemDescription
            elif column == NUMDOC:
                return line.numdoc
            elif column == NUMAJUSTE:
                return line.numajuste if line.numajuste <= 0 else "+%d" % line.numajuste
            elif column == NUMTOTAL:
                return line.numfinal
        elif role == Qt.EditRole:
            if column == NUMAJUSTE:
                return line.numajuste
            
        elif role == Qt.TextAlignmentRole:
            if column == NUMDOC:
                return Qt.AlignHCenter | Qt.AlignCenter

    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column() == NUMAJUSTE:
            return Qt.ItemFlags( QAbstractTableModel.flags( self, index ) |
                                 Qt.ItemIsEditable )
        return Qt.ItemIsEnabled


    def setData( self, index, value, _role = Qt.EditRole ):
        """
        modificar los datos del modelo, este metodo se comunica con el delegate
        """
        if index.isValid() and 0 <= index.row() < len( self.lines ):
            line = self.lines[index.row()]
            if index.column() == NUMAJUSTE:
                line.numajuste = value.toInt()[0]

            self.dirty = True


            self.dataChanged.emit( index, index )

            return True
        return False

    def insertRows( self, position, rows = 1, _index = QModelIndex() ):
        self.beginInsertRows( QModelIndex(), position, position + rows - 1 )
        for row in range( rows ):
            self.lines.insert( position + row, LineaKardex() )
        self.endInsertRows()
        return True

    def removeRows( self, position, rows = 1, index = QModelIndex ):
        raise NotImplementedError()

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignLeft | Qt.AlignVCenter
            return Qt.AlignRight | Qt.AlignVCenter

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == DESCRIPCION:
                return "Articulo"
            elif section == NUMDOC:
                return "Cantidad en Documento"
            elif section == NUMAJUSTE:
                return "Ajuste"
            elif section == NUMTOTAL:
                return "Cantidad Final"
        return int( section + 1 )


    def save( self ):
        """
        Este metodo guarda el documento actual en la base de datos
        """
        query = QSqlQuery()
        try:
            if not self.valid:
                raise Exception( "El documento a salvar no es valido" )

            if not QSqlDatabase.database().transaction():
                raise Exception( u"No se puedo comenzar la transacción" )

            if not query.prepare( """
            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc, 
            observacion,total, idtipocambio, idbodega)
            VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:observacion,
            :total, :idtipocambio, :idbodega)
            """ ):
                raise Exception( "No se pudo preparar la consulta para "
                                 + "insertar el kardex" )
            query.bindValue( ":ndocimpreso", self.printedDocumentNumber )
            query.bindValue( ":fechacreacion",
                             self.datetime.toString( 'yyyyMMddhhmmss' ) )
            query.bindValue( ":idtipodoc", self.__documentType )

            query.bindValue( ":observacion", self.observations )
            query.bindValue( ":total", str( self.ajusteTotalC ) )
            query.bindValue( ":idtipocambio", self.exchangeRateId )
            query.bindValue( ":idbodega", self.warehouseId )

            if not query.exec_():
                raise Exception( "No se pudo insertar el documento" )

            inserted_id = query.lastInsertId().toInt()[0]

            if not query.prepare( """
            INSERT INTO personasxdocumento (idpersona, iddocumento,idaccion) 
            VALUE (:idusuario, :iddocumento,:accion)
            """ ):
                raise Exception( "No se pudo preparar la consulta para "
                                 + "ingresar el usuario" )
            query.bindValue( ":idusuario", self.uid )
            query.bindValue( ":iddocumento", inserted_id )
            query.bindValue( ":accion", constantes.AUTOR )

            if not query.exec_():
                raise Exception( "No se pudo insertar  el usuario" )

            for i, line in  enumerate( [ line for line in self.lines if line.dirty and line.valid ] ):
                line.save( inserted_id , i )

            if not query.prepare( """
            INSERT INTO docpadrehijos (idpadre, idhijo) 
            VALUES (:padre, :hijo)
            """ ):
                raise Exception( "No se pudo preparar la relacion entre "
                                 + "el documento kardex y el documento padre" )
            query.bindValue( ":padre", self.parentId )
            query.bindValue( ":hijo", inserted_id )
            if not query.exec_():
                raise Exception( "No se pudo insertar la relacion entre "
                                 + "el documento kardex y el documento padre" )

            if self.ajusteTotalC != 0:
                movKardex( inserted_id, self.ajusteTotalC )

            if not QSqlDatabase.database().transaction():
                raise Exception( "No se pudo ejecutar la transaccion" )

            return True
        except Exception as inst:
            logging.critical( query.lastError().text() )
            logging.critical( unicode( inst ) )
            QSqlDatabase.database().rollback()

            return False


