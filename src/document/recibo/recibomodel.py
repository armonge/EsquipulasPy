# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: armonge
'''
from PyQt4 import QtGui
from PyQt4.QtSql import QSqlDatabase, QSqlQuery
from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt, SIGNAL, QDateTime

from linearecibo import LineaRecibo

from decimal import Decimal
from utility.moneyfmt import moneyfmt
#from utility.movimientos import movAbonoDeCliente

IDARTICULO, DESCRIPCION, REFERENCIA, MONTO, TOTALPROD, MONEDA = range( 6 )
class ReciboModel( QAbstractTableModel ):
    """
    esta clase es el modelo utilizado en la tabla en la que se editan los documentos
    """
    def __init__( self ):
        super( ReciboModel, self ).__init__()

#        self.sesion = sesion

        self.dirty = False
#        self.__documentType = 18
#        self.clienteId = 0
#        self.observations = ""
#        self.observationsRET = ""

#        self.aplicarRet = True

        self.lines = []


#        self.printedDocumentNumber = ""
#        self.datetime = QDateTime.currentDateTime()
#        self.uid = 0
#        self.idtc = 0
#        self.tc = Decimal( 0 )
#        self.tasabanco = Decimal( 0 )
#        self.escontado = 1
#        self.conceptoId = 0

#        self.retencionId = 0
#        self.retencionTasa = Decimal( 0 )
#        self.retencionNumero = 0


#    @property
#    def valid( self ):
#        """
#        Un documento es valido cuando 
#        self.printedDocumentNumber != ""
#        self.providerId !=0
#        self.validLines >0
#        self.__idIVA !=0
#        self.uid != 0
#        self.warehouseId != 0 
#        """
#        if  self.printedDocumentNumber == "":
#            print( "No existe numero de doc impreso" )
#            return False
#        elif int( self.clienteId ) == 0:
#            print( "No existe un cliente seleccionado" )
#            return False
#        elif int( self.validLines ) < 1:
#            print( "No Hay ninguna linea no valida" )
#            return False
#        elif int( self.retencionId ) == 0:
#            print( "No hay tasa de retencion" )
#            return False
#        elif int( self.uid ) == 0:
#            print( "No hay un usuario" )
#            return False
#        elif int( self.conceptoId ) == 0:
#            print( "No hay un concepto" )
#            return False
#        elif self.idtc == 0:
#            print( "no hay un tipo de cambio para la fecha" + self.datetime )
#            return False
#        else:
#            return True

#
#    @property
#    def getRetencion( self ):
##        return ( self.total * ( self.retencionTasa / Decimal( 100 ) ) ) if self.aplicarRet else 0
#
#    @property
#    def getRateRET( self ):
#        """
#        El porcentaje de IVA que se le aplica a esta linea
#        """
#        return self.retencionTasa

#    @property
#    def validLines( self ):
#        """
#        la cantidad de lineas validas que hay en el documento
#        """
#        foo = 0
#        for line in self.lines:
#            if line.valid:foo += 1
#        return foo


    #Clases especificas del modelo
    def rowCount( self, index = QModelIndex ):
        return len( self.lines )

    def columnCount( self, index = QModelIndex ):
        return 5

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
                return line.nref
            elif column == MONTO:
                return moneyfmt( Decimal( line.monto ), 4, "US$" ) if line.monto != 0 else ""
            elif column == TOTALPROD:
                return moneyfmt( line.total , 4, "US$" )
            elif column == MONEDA:
                return line.itemDescription
        elif role == Qt.EditRole:
#            Esto es lo que recibe el delegate cuando va a mostrar la el widget 
            if column == MONTO:
                return line.monto

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
            if column == DESCRIPCION:
                line.pagoId = value[0]
                line.pagoDescripcion = value[1]
                line.monedaId = value[2]
            elif column == REFERENCIA:
                line.nref = value
            elif column == MONTO:
                line.monto = Decimal( value.toString() )


            self.dirty = True



            self.emit( SIGNAL( "dataChanged(QModelIndex, QModelIndex)" ), index, index )
            #si la linea es valida y es la ultima entonces aniadir una nueva
            if  index.row() == len( self.lines ) - 1 and line.valid:
                self.insertRows( len( self.lines ) )

            return True
        return False

#    @property
#    def total( self ):
#        """
#        El total del documento, esto es el total antes de aplicarse el IVA
#        """
#        tmpsubtotal = sum( [linea.monto for linea in self.lines if linea.valid] )
#        return tmpsubtotal if tmpsubtotal > 0 else Decimal( 0 )

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
# borrar el rango de lineas indicado de la ascendente para que no halla problema con el indice de las lineas 
# muestro la fila de la tabla facturas que esta relacionada a la linea que borre
            while n >= position:
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
            if  section == DESCRIPCION:
                return u"Descripción"
            elif section == MONTO:
                return "MONTO"
            elif section == TOTALPROD:
                return "TOTAL"
            elif section == REFERENCIA:
                return "REFERENCIA"
            elif section == MONEDA:
                return "MONEDA"
        return int( section + 1 )

#    def save( self, lineas ):
#        """
#        Este metodo guarda el documento actual en la base de datos
#        """
#
#        if not self.valid:
#            raise Exception( "El documento a salvar no es valido" )
#
#        query = QSqlQuery()
#
#        try:
#
#            if not QSqlDatabase.database().transaction():
#                raise Exception( u"No se pudo comenzar la transacción" )
##INSERTAR RECIBO
#            query.prepare( """
#            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,idusuario,anulado, idpersona, observacion,total,escontado,idtipocambio,idconcepto) 
#            VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:idusuario,:anulado,:idpersona,:observacion,:total,:escontado,:idtc,:concepto)
#            """ )
#            query.bindValue( ":ndocimpreso", self.printedDocumentNumber )
#            query.bindValue( ":fechacreacion", self.datetime.toString( 'yyyyMMddhhmmss' ) )
#            query.bindValue( ":idtipodoc", self.__documentType )
#            query.bindValue( ":idusuario", self.uid )
#            query.bindValue( ":anulado", 0 )
#            query.bindValue( ":idpersona", self.clienteId )
#            query.bindValue( ":observacion", self.observations )
#            query.bindValue( ":total", self.total.to_eng_string() )
#            query.bindValue( ":escontado", self.escontado )
#            query.bindValue( ":idtc", self.idtc )
#            query.bindValue( ":concepto", self.conceptoId )
#
#            if not query.exec_():
#                raise Exception( "No se pudo insertar el recibo" )
#            insertedId = query.lastInsertId().toInt()[0]
#
#
##INSERTAR LA RELACION CON LA SESION DE CAJA            
#            query.prepare( """
#                INSERT INTO docpadrehijos (idpadre,idhijo)
#                VALUES (:idsesion,:idrecibo)
#                """ )
#
#            query.bindValue( ":idsesion", self.sesion )
#            query.bindValue( ":idrecibo", insertedId )
#
#            if not query.exec_():
#                print( insertedId )
#                print( self.sesion )
#                raise Exception( "No se Inserto la relacion entre la sesion de caja y el recibo" )
#
#
##INSERTAR LOS TIPOS DE PAGO
#            i = 0
#            for linea in self.lines:
#                if linea.valid:
#                    linea.save( insertedId, i )
#                    i = i + 1
##INSERTAR los abonos
#            print( lineas )
#            for l in lineas:
#                print( l.idFac )
#                if l.valid:
#                    l.save( insertedId )
#
##VERIFICO SI se aplicara la retencion                     
#            if self.aplicarRet :
#
##INSERTAR EL DOCUMENTO RETENCION            
#                query.prepare( """
#                INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,idusuario,anulado, idpersona, observacion,total,escontado,idtipocambio,idconcepto) 
#                VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:idusuario,:anulado,:idpersona,:observacion,:total,:escontado,:idtc,:concepto)
#                """ )
#                query.bindValue( ":ndocimpreso", self.retencionNumero )
#                query.bindValue( ":fechacreacion", self.datetime )
#                query.bindValue( ":idtipodoc", 19 )
#                query.bindValue( ":idusuario", self.uid )
#                query.bindValue( ":anulado", 0 )
#                query.bindValue( ":idpersona", self.clienteId )
#                query.bindValue( ":observacion", self.observationsRET )
#                query.bindValue( ":total", self.getRetencion.to_eng_string() )
#                query.bindValue( ":escontado", self.escontado )
#                query.bindValue( ":idtc", self.idtc )
#                query.bindValue( ":concepto", self.conceptoId )
#                if not query.exec_():
#                    raise Exception( "No se Inserto la retencion" )
#
#                idret = query.lastInsertId().toInt()[0]
#
#                query.prepare( """
#                INSERT INTO docpadrehijos (idpadre,idhijo)
#                VALUES (:idrecibo,:idretencion)
#                """ )
#
#                query.bindValue( ":idrecibo", insertedId )
#                query.bindValue( ":idretencion", idret )
#
#                if not query.exec_():
#                    print( insertedId )
#                    print( idret )
#                    raise Exception( "No se Inserto la relacion entre la retencion y el recibo" )
#
#
## INSERTAR EL ID DEL COSTO RETENCION                
#                query.prepare( """
#                INSERT INTO costosxdocumento (iddocumento, idcostoagregado) VALUES( :iddocumento, :idcostoagregado )
#                """ )
#                query.bindValue( ":iddocumento", insertedId )
#                query.bindValue( ":idcostoagregado", self.retencionid )
#                if not query.exec_():
#                    raise Exception( "el costo Retencion  NO SE INSERTO" )
#
#
#            #manejar las cuentas contables
#            print( "cuentas" )
#            movAbonoDeCliente( insertedId, self.total * self.tc, self.getRetencion * self.tc )
#
#            if not QSqlDatabase.database().commit():
#                raise Exception( "No se pudo hacer commit" )
#        except Exception as inst:
#            print  query.lastError().databaseText()
#            print query.lastError().driverText()
#            print inst.args
#            QSqlDatabase.database().rollback()
#            return False
#
#        return True
