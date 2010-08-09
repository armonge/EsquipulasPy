# -*- coding: utf-8 -*-
'''
Created on 07/06/2010

@author: Andrés Reyes Monge
'''
from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt, SIGNAL, QDateTime
from PyQt4.QtSql import QSqlQuery, QSqlDatabase
from document.arqueo.lineaarqueo import LineaArqueo

from utility.moneyfmt import moneyfmt
from decimal import Decimal
from  utility import constantes

CANTIDAD, DENOMINACION, TOTAL = range( 3 )
class ArqueoModel( QAbstractTableModel ):
    """
    Esta clase es el modelo utilizado para crear nuevos arqueos
    """
    __documentType = constantes.IDARQUEO
    """
    @cvar: El tipo de documento de arqueo
    @type: int 
    """
    def __init__( self ):
        super( ArqueoModel, self ).__init__()
        self.database = QSqlDatabase.database()
        """
        @ivar: La base de datos que se ocupa en el sistema
        @type: QSqlDatabase
        """
        self.dirty = False
        self.datetime = QDateTime.currentDateTime()
        """
        @ivar:La fecha del arqueo
        @type:string 
        """

        self.lines = []
        """
        @ivar:Las lineas de este arqueo
        @type: LineaArqueo[]
        """

        self.exchangeRate = Decimal( 0 )
        """
        @ivar:El tipo de cambio para el dia
        @type:Decimal
        """
        self.exchangeRateId = 0
        """
        @ivar:El id del tipo de cambio
        @type: int
        """

        self.expectedTotal = Decimal( 0 )
        """
        @ivar:El total que se espera tenga el arqueo
        @type:Decimal
        """
        self.printedDocumentNumber = ""
        """
        @ivar:El numero impreso del documento
        @type:Decimal
        """

        self.observations = ""
        """
        @ivar:Las observaciones del documento
        @type:Decimal
        """

    @property
    def total ( self ):
        """
        El total en el modelo
        
        M{TOTAL = S{sum}TOTALLINEA, LINEA.VALID = True}
        @rtype: Decimal
        """
        tmp = sum( [line.total for line in self.lines if line.valid] )
        return tmp if tmp != 0 else Decimal( 0 )

    @property
    def validLines( self ):
        """
        El numero de lineas validas en el modelo
        @rtype: int
        """
        return len( [line for line in self.lines if line.valid ] )

    @property
    def valid( self ):
        """
        Si un documento es valido
        @rtype: bool
        """
        return self.validLines > 0 and self.exchangeRateId != 0 and self.printedDocumentNumber != ""

    def data( self, index, role = Qt.DisplayRole ):
        """
        Retornar los datos del modelo
        """
        if not index.isValid() or not ( 0 <= index.row() < len( self.lines ) ):
            return None

        line = self.lines[ index.row() ]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == CANTIDAD:
                return line.quantity
            elif column == TOTAL:
                return moneyfmt( line.total, 4, "US$" )
            elif column == DENOMINACION:
                return line.denomination
        elif role == Qt.EditRole:
            if column == DENOMINACION:
                return line.denomination

    def setData( self, index, value, role = Qt.EditRole ):
        """
        Cambiar un dato en el modelo
        @return: Si se pudo cambiar el dato
        @rtype: bool
        """
        if index.isValid() and 0 <= index.row() < len( self.lines ):
            line = self.lines[index.row()]
            if index.column() == CANTIDAD:
                line.quantity = value.toInt()[0]
            elif index.column() == DENOMINACION:
                line.denominationId = value[0]
                line.denomination = value[1]
                line.value = value[2]
                line.currencyId = value[3]


            if index.row() == len( self.lines ) - 1 and line.valid:
                self.insertRow( len( self.lines ) )
            self.dirty = True

            self.emit( SIGNAL( "dataChanged(QModelIndex,QModelIndex)" ), index, index )
            return True
        return False

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        """
        El texto de los headers en el modelo
        """
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignLeft | Qt.AlignVCenter
            return Qt.AlignRight | Qt.AlignVCenter

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == CANTIDAD:
                return "Cantidad"
            elif section == DENOMINACION:
                return u"Denominación"
            elif section == TOTAL:
                return "Total US$"
            return int( section + 1 )

    def rowCount( self, index = QModelIndex() ):
        """
        El numero de filas en el modelo
        @rtype: int
        """
        return len( self.lines )

    def columnCount( self, index = QModelIndex() ):
        """
        El numero de columnas en el modelo
        @rtype: int
        """
        return 3

    def save( self ):
        """
        Guardar el documento
        @return: Si se pudo o no guardar el documento
        @rtype: bool
        """
        if not self.valid:
            raise Exception( "El documento a salvar no es valido" )

        query = QSqlQuery()

        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning(u"No se pudo abrir la base de datos")
                
            if not self.database.transaction():
                raise Exception( u"No se pudo comenzar la transacción" )

            if not query.prepare( """
            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,anulado,  observacion,total,  idtipocambio) 
            VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:anulado,:observacion,:total, :idtc)
            """ ):
                raise Exception( "No se pudo preparar la consulta para guardar el arqueo" )
            query.bindValue( ":ndocimpreso", self.printedDocumentNumber )
            query.bindValue( ":fechacreacion", self.datetime.toString( 'yyyyMMddhhmmss' ) )
            query.bindValue( ":idtipodoc", self.__documentType )
            query.bindValue( ":anulado", 0 )
            query.bindValue( ":observacion", self.observations )
            query.bindValue( ":total", self.total.to_eng_string() )
            query.bindValue( ":idtc", self.exchangeRateId )

            if not query.exec_():
                raise  Exception( "No se pudo guardar el arqueo" )

            insertedId = query.lastInsertId()

            if not query.prepare( """
            INSERT INTO personasxdocumento (idpersona, iddocumento)
            VALUES (:idpersona, :iddocumento) 
            """ ):
                raise  Exception( "No se pudo preparar la consulta guardar el usuario" )
            query.bindValue( ":idpersona", self.uid )
            query.bindValue( ":iddocumento", insertedId )
            if not query.exec_():
                raise Exception( "No se pudo guardar el usuario" )


            for line in self.lines:
                if line.valid:
                    line.save( insertedId )


            if not self.database.commit():
                raise Exception( "No se pudo hacer commit" )
            return True
        except UserWarning as inst:
            self.saveError = str(inst)
            print query.lastError().text()
            self.database.rollback()
            return False
        except Exception, e:
            print e
            print query.lastError().text()
            self.database.rollback()
            return False
        finally:
            if self.database.isOpen():
                self.database.close()



    def insertRows( self, position, rows = 1, index = QModelIndex() ):
        """
        @rtype: bool
        """
        self.beginInsertRows( QModelIndex(), position, position + rows - 1 )
        for row in range( rows ):
            self.lines.insert( position + row, LineaArqueo( self ) )
        self.endInsertRows()
        self.dirty = True
        return True

    def removeRows( self, position, rows = 1, index = QModelIndex ):
        """
        @rtype: bool
        """
        if len( self.lines ) > 1 and self.lines[position].valid:
            self.beginRemoveRows( QModelIndex(), position, position + rows - 1 )
            for n in range( rows ):
                del self.lines[position + n]
            self.endRemoveRows()
            self.dirty = True
            return True
        else:
            return False

    def flags( self, index ):
        """
        @rtype: Qt.ItemFlags
        """
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column() != TOTAL:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable
        else:
            return Qt.ItemIsEnabled


