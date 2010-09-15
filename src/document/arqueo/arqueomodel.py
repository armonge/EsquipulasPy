# -*- coding: utf-8 -*-
'''
Created on 07/06/2010

@author: Andrés Reyes Monge
'''
#TODO: Creo que podria utilizar un arreglo o algún tipo de estructura para los totales en lugar de utilizar una variable para uno
import logging

from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt, QDateTime
from PyQt4.QtGui import QSortFilterProxyModel
from PyQt4.QtSql import QSqlQuery, QSqlDatabase
from document.arqueo.lineaarqueo import LineaArqueo

from utility.moneyfmt import moneyfmt
from decimal import Decimal
from  utility import constantes
from utility import movimientos

CANTIDAD, DENOMINACION,  TOTAL, MONEDA, IDDOCUMMENTOT = range( 5 )
class ArqueoModel( QAbstractTableModel ):
    """
    Esta clase es el modelo utilizado para crear nuevos arqueos
    """
    __documentType = constantes.IDARQUEO
    """
    @cvar: El tipo de documento de arqueo
    @type: int 
    """
    def __init__( self , datosSesion):
        super( ArqueoModel, self ).__init__()
        self.datosSesion = datosSesion
        
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

        self.expectedCashD = Decimal(0)
        """
        @ivar: EL efectivo en dolar que se espera del arqueo
        @type:Decimal
        """
        self.expectedCashC = Decimal(0)
        """
        @ivar: El efectivo en cordobas que se espera del arqueo
        @type: Decimal
        """
        self.expectedCkD = Decimal(0)
        """
        @ivar: El total esperado en cheques en dolares
        @type:Decimal
        """
        self.expectedCkC = Decimal(0)
        """
        @ivar: El total esperado en cheques en cordobas
        @type:Decimal
        """
        self.expectedDepositD = Decimal(0)
        """
        @ivar: El total esperado en depositos en dolares
        @type:Decimal
        """
        self.expectedDepositC = Decimal(0)
        """
        @ivar: El total esperado en depositos en cordobas
        @type: Decimal
        """
        self.expectedTransferD = Decimal(0)
        """
        @ivar: El total esperado en transferencias en Dolares
        @type:Decimal
        """
        self.expectedTransferC = Decimal(0)
        """
        @ivar: El total esperado en transferencias en cordobas
        @type:Decimal
        """
        self.expectedCardD = Decimal(0)
        """
        @ivar:El total esperado en pagos en tarjetas en dolares
        @type:Decimal
        """
        self.expectedCardC = Decimal(0)
        """
        @ivar: El total esperado en pagos en tarjetas en cordobas
        @type: Decimal
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

        self.totalCkC = Decimal(0)
        self.totalCkD = Decimal(0)
        
        self.totalCardC = Decimal(0)
        self.totalCardD = Decimal(0)
        
        self.totalDepositC = Decimal(0)
        self.totalDepositD = Decimal(0)

        self.totalTransferC = Decimal(0)
        self.totalTransferD = Decimal(0)

        self.authorizationId = 0
        """
        @ivar: El id del usuario que autoriza el arqueo
        @type: int
        """
    @property
    def differenceD(self):
        """
        La diferencia en dolares entre el arqueo y la sesión
        @rtype:Decimal
        """
        tmp = Decimal(0)
        tmp += self.totalCardD - self.expectedCardD
        tmp += self.totalCashD - self.expectedCashD
        tmp += self.totalDepositD - self.expectedDepositD
        tmp += self.totalTransferD -self.expectedTransferD
        tmp += self.totalCkD - self.expectedCkD

        return tmp

    @property
    def differenceC(self):
        """
        La diferencia en cordobas entre el arqueo y la sesión
        @rtype:Decimal
        """
        tmp = 0
        tmp += self.totalCardC - self.expectedCardC
        tmp += self.totalCashC - self.expectedCashC
        tmp += self.totalDepositC - self.expectedDepositC
        tmp += self.totalTransferC - self.expectedTransferC
        tmp += self.totalCkC - self.expectedCkC
        return tmp

    @property
    def totalDifferenceC(self):
        """
        La diferencia total en cordobas, es decir la suma de las diferencias en cordobas más
        las diferencias en dolares multiplicadas por el tipo de cambio
        @rtype:Decimal
        """
        return self.differenceC + self.differenceD * self.exchangeRate

    @property
    def subtotalC(self):
        """
        El subtotal en cordobas de este arqueo
        @rtype:Decimal
        """
        return self.totalCardC + self.totalCashC + self.totalDepositC + self.totalTransferC + self.totalCkC

    @property
    def subtotalD(self):
        """
        El subtotal en dolares de este arqueo
        @rtype:Decimal
        """
        return self.totalCardD + self.totalCashD + self.totalDepositD + self.totalTransferD + self.totalCkD

    @property
    def totalC(self):
        """
        El total en cordobas de este arqueo
        @rtype:Decimal
        """
        return self.subtotalC + self.subtotalD * self.exchangeRate

    @property
    def totalD(self):
        """
        El total en cordobas de este arqueo
        @rtype:Decimal
        """
        return self.subtotalD + self.subtotalC / self.exchangeRate
    
    @property
    def totalCashC ( self ):
        """
        El total en el modelo

        M{TOTAL = S{sum}TOTALLINEA, LINEA.VALID = True}
        @rtype: Decimal
        """
        tmp = sum( [line.total for line in self.lines if line.valid and line.currencyId == constantes.IDCORDOBAS ] )
        return tmp if tmp != 0 else Decimal( 0 )

    @property
    def totalCashD(self):
        """
        El total en el modelo

        M{TOTAL = S{sum}TOTALLINEA, LINEA.VALID = True}
        @rtype: Decimal
        """
        tmp = sum( [line.total for line in self.lines if line.valid and line.currencyId == constantes.IDDOLARES ] )
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
        if not self.exchangeRateId != 0:
            self.validError = "No se ha definido un tipo de cambio"
            return False
        elif not self.printedDocumentNumber != "":
            self.validError = "No se especificado el numero del arqueo"
            return False
        elif not self.authorizationId != 0:
            self.validError = "No se ha autorizado el arqueo"
            return False
        return True

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
                return moneyfmt( line.total, 4, line.symbol )
            elif column == DENOMINACION:
                return line.denomination
            elif column == MONEDA:
                return line.currencyId
                
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
                value = value.toList()
                line.denominationId = value[0].toInt()[0]
                line.denomination = value[1].toString()
                line.value = Decimal(value[2].toString())
                line.currencyId = value[3].toInt()[0]
                
            elif index.column() == MONEDA:
                if value in (constantes.IDDOLARES, constantes.IDCORDOBAS):
                    line.currencyId = value 

                
            self.dirty = True

            self.dataChanged.emit(index, index)
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
                return "Total"
            elif section == MONEDA:
                return "Moneda"
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
        return 4

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
            #Insertar el documento
            if not query.prepare( """
            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,  observacion,total,  idtipocambio)
            VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:observacion,:total, :idtc)
            """ ):
                raise Exception( "No se pudo preparar la consulta para guardar el arqueo" )
            query.bindValue( ":ndocimpreso", self.printedDocumentNumber )
            query.bindValue( ":fechacreacion", self.datetime.toString( 'yyyyMMddhhmmss' ) )
            query.bindValue( ":idtipodoc", self.__documentType )
            query.bindValue( ":observacion", self.observations )
            query.bindValue( ":total", self.totalD.to_eng_string() )
            query.bindValue( ":idtc", self.exchangeRateId )

            
            if not query.exec_():
                raise  Exception( "No se pudo guardar el arqueo" )

            insertedId = query.lastInsertId().toInt()[0]

            #Insertar el padre del arqueo
            if not query.prepare("""
            INSERT INTO docpadrehijos (idpadre, idhijo)
            VALUES (:idpadre, :idhijo)
            """):
                raise Exception(u"No se pudo preparar la relación con la sesión")

            query.bindValue(":idpadre",self.datosSesion.sesionId )
            query.bindValue(":idhijo", insertedId)

            if not query.exec_():
                raise Exception(u"No se pudo insertar la relación con la sesión")
            #Insertar el usuario
            if not query.prepare( """
            INSERT INTO personasxdocumento (idpersona, iddocumento, idaccion)
            VALUES (:idpersona, :iddocumento, :idaccion) 
            """ ):
                raise  Exception( "No se pudo preparar la consulta guardar el usuario" )
            query.bindValue( ":idpersona", self.datosSesion.usuarioId )
            query.bindValue( ":iddocumento", insertedId )
            query.bindValue( ":idaccion", constantes.ACCCREA)
            if not query.exec_():
                raise Exception( "No se pudo guardar el usuario" )

            #Insertar el usuario que autoriza
            if not query.prepare( """
            INSERT INTO personasxdocumento (idpersona, iddocumento, idaccion)
            VALUES (:idpersona, :iddocumento, :idaccion)
            """ ):
                raise  Exception( "No se pudo preparar la consulta guardar el usuario" )
            query.bindValue( ":idpersona", self.authorizationId )
            query.bindValue( ":iddocumento", insertedId )
            query.bindValue( ":idaccion", constantes.ACCAUTORIZA)
            if not query.exec_():
                raise Exception( u"No se pudo guardar el usuario que da la autorización" )

            #Insertar los totales
            if not query.prepare(
            " INSERT INTO movimientoscaja (iddocumento, idtipomovimiento, idtipomoneda, monto)" +
            " VALUES ( " + str(insertedId) +" , " + str(constantes.IDPAGOEFECTIVO) + " , " + str(constantes.IDDOLARES )+ " , :cashD )," +
            " ( " + str(insertedId) +" , " + str(constantes.IDPAGOEFECTIVO )+ " , " + str(constantes.IDCORDOBAS )+ " , :cashC )," +
            " ( " + str(insertedId) +" , " + str(constantes.IDPAGOCHEQUE)+ " , " + str(constantes.IDDOLARES )+ " , :ckD )," +
            " ( " + str(insertedId) +" , " + str(constantes.IDPAGOCHEQUE)+ " , " + str(constantes.IDCORDOBAS )+ " , :ckC )," +
            " ( " + str(insertedId) +" , " + str(constantes.IDPAGODEPOSITO )+ " , " + str(constantes.IDDOLARES )+ " , :depositD )," +
            " ( " + str(insertedId) +" , " + str(constantes.IDPAGODEPOSITO )+ " , " + str(constantes.IDCORDOBAS )+ " , :depositC )," +
            " ( " + str(insertedId) +" , " + str(constantes.IDPAGOTRANSFERENCIA )+ " , " + str(constantes.IDDOLARES )+ " , :transferD )," +
            " ( " + str(insertedId) +" , " + str(constantes.IDPAGOTRANSFERENCIA )+ " , " + str(constantes.IDCORDOBAS )+ " , :transferC )," +
            " ( " + str(insertedId) +" , " + str(constantes.IDPAGOTARJETA )+ " , " + str(constantes.IDDOLARES )+ " , :cardD )," +
            " ( " + str(insertedId) +" , " + str(constantes.IDPAGOTARJETA )+ " , " + str(constantes.IDCORDOBAS )+ " , :cardC )" 
            ):
                raise Exception("No se pudo preparar la consulta para guardar los totales del arqueo")

            query.bindValue(":cashD", self.totalCashD.to_eng_string())
            query.bindValue(":cashC", self.totalCashC.to_eng_string())
            query.bindValue(":ckD", self.totalCkD.to_eng_string())
            query.bindValue(":depositC", self.totalCkC.to_eng_string())
            query.bindValue(":depositD", self.totalDepositD.to_eng_string())
            query.bindValue(":depositC", self.totalDepositC.to_eng_string())
            query.bindValue(":cardD", self.totalCardD.to_eng_string())
            query.bindValue(":cardC", self.totalCardC.to_eng_string())
            query.bindValue(":transferD", self.totalTransferD.to_eng_string())
            query.bindValue(":transferC", self.totalTransferC.to_eng_string())

            if not query.exec_():
                raise Exception("No se pudieron insertar los pagos")


            if self.totalDifferenceC != 0:
                movimientos.movArqueo(insertedId, self.totalDifferenceC)
            
            for line in self.lines:
                if line.valid:
                    line.save( insertedId )


            if not self.database.commit():
                raise Exception( "No se pudo hacer commit" )
            return True
        except UserWarning as inst:
            self.saveError = unicode(inst)
            logging.error(inst)
            logging.error(query.lastError().text())
            self.database.rollback()
            return False
        except Exception as inst:
            logging.critical(unicode(inst))
            logging.critical(query.lastError().text())
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
            #self.lines[row].currencyId = 1
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


class ArqueoProxyModel(QSortFilterProxyModel):
    def setData( self, index, value, role = Qt.EditRole ):
        result = super(ArqueoProxyModel, self).setData(index, value, role)
        row = self.mapToSource(  index  ).row()
        line = self.sourceModel().lines[row]
        if line.valid and index.row() == self.rowCount()-1:
            self.sourceModel().insertRow(self.sourceModel().rowCount())
            self.sourceModel().setData( self.sourceModel().index(self.sourceModel().rowCount()-1, MONEDA), line.currencyId)
        return result    