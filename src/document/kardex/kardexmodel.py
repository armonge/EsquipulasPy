# -*- coding: utf-8 -*-
'''
Created on 19/05/2010

@author: Andrés Reyes Monge
'''
from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt, QDateTime, SIGNAL
from PyQt4.QtSql import QSqlQuery, QSqlDatabase

from decimal import Decimal
from document.kardex.lineakardex import LineaKardex
from utility.moneyfmt import moneyfmt
import utility
from utility.movimientos import movKardex

IDARTICULO, DESCRIPCION, NUMDOC, NUMAJUSTE, NUMTOTAL = range( 5 )
class KardexModel( QAbstractTableModel ):
    """
    Esta clase es el modelo utilizado en la tabla en la que se editan los documentos
    """
    __documentType = utility.constantes.IDKARDEX
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
        
        self.exchangeRate = Decimal(0)
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
    def ajusteTotalD(self):
        ajuste = sum([ line.ajusteMonetario for line in self.lines if line.dirty ])
        return ajuste if ajuste != 0 else Decimal(0)
    
    @property
    def ajusteTotalC(self):
        return self.ajusteTotalD * self.exchangeRate
    
    @property
    def valid( self ):
        """
        Un documento es valido cuando 
        @rtype: bool
        """
        if not len(self.lines) != 0:
            self.validError = "No existen lineas en el kardex"
            return False
        if not self.exchangeRateId != 0:
            self.validError = "No esta definido un tipo de cambio"
            return False
        
        return True

    #Clases especificas del modelo
    def rowCount( self, index = QModelIndex() ):
        return len( self.lines )

    def columnCount( self, index = QModelIndex() ):
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
                return line.numajuste if line.numajuste <=0 else "+%d"%line.numajuste
            elif column == NUMTOTAL:
                return line.numfinal
        elif role == Qt.EditRole:
            if column == NUMAJUSTE:
                return line.numajuste 
    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column() == NUMAJUSTE:
            return Qt.ItemFlags( QAbstractTableModel.flags( self, index ) | Qt.ItemIsEditable )
        else:
            return Qt.ItemIsEnabled


    def setData( self, index, value, role = Qt.EditRole ):
        """
        modificar los datos del modelo, este metodo se comunica con el delegate
        """
        if index.isValid() and 0 <= index.row() < len( self.lines ):
            line = self.lines[index.row()]
            if index.column() == NUMAJUSTE:
                line.numajuste = value.toInt()[0]

            self.dirty = True

            self.emit( SIGNAL( "dataChanged(QModelIndex, QModelIndex)" ), index, index )

            return True
        return False

    def insertRows( self, position, rows = 1, index = QModelIndex() ):
        self.beginInsertRows( QModelIndex(), position, position + rows - 1 )
        for row in range( rows ):
            self.lines.insert( position + row, LineaKardex( ) )
        self.endInsertRows()
        return True

    def removeRows( self, position, rows = 1, index = QModelIndex ):
        raise NotImplementedError

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
            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,anulado, observacion,total, idtipocambio)
            VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:anulado,:observacion,:total, :idtipocambio)
            """ ):
                raise Exception("No se pudo preparar la consulta para insertar el kardex")
            query.bindValue( ":ndocimpreso", self.printedDocumentNumber )
            query.bindValue( ":fechacreacion", self.datetime.toString( 'yyyyMMddhhmmss' ) )
            query.bindValue( ":idtipodoc", self.__documentType )
            query.bindValue( ":anulado", 0 )
            query.bindValue( ":observacion", self.observations )
            query.bindValue( ":total", self.ajusteTotalC.to_eng_string() )
            query.bindValue( ":idtipocambio", self.exchangeRateId )

            if not query.exec_():
                raise Exception( "No se pudo insertar el documento" )

            insertedId = query.lastInsertId().toInt()[0]

            if not query.prepare( """
            INSERT INTO personasxdocumento (idpersona, iddocumento) 
            VALUE (:idusuario, :iddocumento)
            """ ):
                raise Exception( "No se pudo preparar la consulta para ingresar el usuario" )
            query.bindValue( ":idusuario", self.uid )
            query.bindValue( ":iddocumento", insertedId )

            if not query.exec_():
                raise Exception( "No se pudo insertar  el usuario" )

            for line in  self.lines :
                if line.dirty:
                    line.save( insertedId )
            if not query.prepare("""
            INSERT INTO docpadrehijos (idpadre, idhijo) VALUES (:padre, :hijo)
            """):
                raise Exception("No se pudo preparar la relacion entre el documento kardex y el documento padre")
            query.bindValue(":padre", self.parentId)
            query.bindValue(":hijo", insertedId)
            if not query.exec_():
                raise Exception("No se pudo insertar la relacion entre el documento kardex y el documento padre")
            
            if self.ajusteTotalC != 0:
                movKardex(insertedId, self.ajusteTotalC)
            
            if not QSqlDatabase.database().transaction():
                raise Exception("No se pudo ejecutar la transaccion")
            
            return True
        except Exception as inst:
            print query.lastError().text()
            print inst
            QSqlDatabase.database().rollback()

            return False

        
