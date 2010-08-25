# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: Luis Carlos Mejia Garcia
'''
from PyQt4 import QtGui
from PyQt4.QtSql import QSqlDatabase, QSqlQuery
from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt, SIGNAL, QDateTime
from lineafactura import LineaFactura
from decimal import Decimal
from utility.moneyfmt import moneyfmt
from utility import constantes
from utility.movimientos import movFacturaContado , movFacturaCredito
from utility import constantes

IDARTICULO, DESCRIPCION, CANTIDAD, PRECIO, TOTALPROD = range( 5 )
class FacturaModel( QAbstractTableModel ):
    """
    esta clase es el modelo utilizado en la tabla en la que se editan los documentos
    """
    def __init__( self, datosSesion ):
        super( FacturaModel, self ).__init__()

        
        self.dirty = False
        self.__documentType = 5
        
        self.clienteId = 0
        self.vendedorId =0
        self.bodegaId = 0
        self.observaciones = ""
        self.ivaTasa = Decimal( 0 )
        self.ivaId = 0
        self.lines = []
        self.printedDocumentNumber = ""
#        self.datetime =None #QDateTime.currentDateTime()
#        
##        self.sesionId = sesion
##        self.userId = 0
##        self.tipoCambioId = 0
##        self.tipoCambioOficial = Decimal( 0 )
        self.datosSesion = datosSesion

        self.escontado = 1
        self.costototal = Decimal( 0 )

        self.warehouseId = 0
        self.warehouseName = ""
        



    def removeRows( self, position, rows = 1, index = QModelIndex ):
        nrows = len( self.lines )
        if nrows > 0 and nrows > position:
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

    @property
    def subtotal( self ):
        """
        El subtotal del documento, esto es el total antes de aplicarse el IVA
        """

        tmpsubtotal = sum( [linea.total for linea in self.lines if linea.valid] )
        self.costototal = sum( [linea.costototal for linea in self.lines if linea.valid] )
        return tmpsubtotal if tmpsubtotal != 0 else Decimal( 0 )



    @property
    def total( self ):
        """
        El total neto del documento, despues de haber aplicado IVA
        @rtype: Decimal
        """
        return self.subtotal + self.IVA

    @property
    def IVA( self ):
        """
        El IVA total del documento, se calcula en base a subtotal y rateIVA
        """
        return ( Decimal( 0 ) if self.bodegaId != 1 else self.subtotal * ( self.ivaTasa / Decimal( 100 ) ) )

    @property
    def validLines( self ):
        """
        la cantidad de lineas validas que hay en el documento
        """
        foo = 0
        for line in self.lines:
            if line.valid:foo += 1
        return foo

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
            if column == IDARTICULO:
                return line.itemId
#            Esto es lo que se muestra en la tabla
            elif column == DESCRIPCION:
                return line.itemDescription
            elif column == CANTIDAD:
                return line.quantity if line.quantity != 0 else ""
            elif column == PRECIO:
                return moneyfmt( Decimal( line.itemPrice ), 4, "US$" ) if line.itemPrice != 0 else ""
            elif column == TOTALPROD:
                return moneyfmt( line.total , 4, "US$" ) if line.itemId!=0 else ""
        elif role == Qt.EditRole:
            if column == PRECIO:
                return line.itemPrice
        elif role == Qt.TextAlignmentRole:
#            if column==:
#                return Qt.AlignHCenter | Qt.AlignVCenter
            if column in (CANTIDAD,PRECIO,TOTALPROD):
                return Qt.AlignRight | Qt.AlignVCenter

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
                line.itemId = value[0]
                line.itemDescription = value[1]
                line.sugerido = Decimal( value[2] )
                line.itemPrice = line.sugerido
                line.costodolar = Decimal( value[3] )
                line.costo = Decimal( value[4] )
                line.existencia = value[5]
                if line.existencia < line.quantity :
                    line.quantity = line.existencia
                line.idbodega = value[6]
            elif column == CANTIDAD:
                line.quantity = value.toInt()[0]
            elif column == PRECIO:
                line.itemPrice = Decimal( value.toString() )

            self.dirty = True



            self.emit( SIGNAL( "dataChanged(QModelIndex, QModelIndex)" ), index, index )
            #si la linea es valida y es la ultima entonces aniadir una nueva
            if  index.row() == len( self.lines ) - 1 and line.valid:
                self.insertRows( len( self.lines ) )

            return True
        return False

    def insertRows( self, position, rows = 1, index = QModelIndex ):
        self.beginInsertRows( QModelIndex(), position, position + rows - 1 )
        for row in range( rows ):
            self.lines.insert( position + row, LineaFactura( self ) )
        self.endInsertRows()
        self.dirty = True
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
                return u"Descripción"
            elif section == PRECIO:
                return "Precio"
            elif section == TOTALPROD:
                return "TOTAL"
            elif section == CANTIDAD:
                return "Cantidad"
        return int( section + 1 )

#TODO: INSERCION
    def save( self , otrosDatosModel):
        """
        Este metodo guarda la factura en la base de datos
        """
        query = QSqlQuery()

        try:

            if not QSqlDatabase.database().transaction():
                raise Exception( u"No se pudo comenzar la transacción" )

#            if not self.escontado:
#                self.printedDocumentNumber = "S/N"
#                
            if not query.prepare( """
            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,observacion,total,idbodega,escontado,idtipocambio,idcaja,idestado) 
            VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:observacion,:total,:bodega,:escontado,:idtc,:caja,:estado)
            """ ):
                raise Exception( "No se pudo guardar el documento" )
            query.bindValue( ":ndocimpreso", self.printedDocumentNumber )
            query.bindValue( ":fechacreacion", self.datosSesion.fecha.toString( 'yyyyMMdd' ) + QDateTime.currentDateTime().toString("hhmmss") )
            query.bindValue( ":idtipodoc", self.__documentType )
            query.bindValue( ":observacion", self.observaciones )
            query.bindValue( ":total", self.total.to_eng_string() )
            query.bindValue( ":bodega", self.bodegaId )
            query.bindValue( ":escontado", self.escontado )
            query.bindValue( ":idtc", self.datosSesion.tipoCambioId )
            query.bindValue( ":caja", self.datosSesion.cajaId)
            query.bindValue( ":estado", constantes.CONFIRMADO if self.escontado else constantes.PENDIENTE)

            if not query.exec_():
                raise Exception( "No se pudo insertar el documento" )

            
            insertedId = query.lastInsertId().toString()
            self.facturaId = query.lastInsertId().toString()
#INSERTAR LA RELACION CON LA SESION DE CAJA            
            query.prepare( """
                INSERT INTO docpadrehijos (idpadre,idhijo)
                VALUES (:idsesion,:idfac)
                """ )

            query.bindValue( ":idsesion", self.datosSesion.sesionId )
            query.bindValue( ":idfac", insertedId )

            if not query.exec_():
                raise Exception( "No se Inserto la relacion entre la sesion de caja y la factura" )

#INSERTAR LA RELACION CON El USUARIO , EL CLIENTE Y EL PROVEEDOR            
            query.prepare( 
                "INSERT INTO personasxdocumento (iddocumento,idpersona,idaccion) VALUES" +  
                "(" + insertedId + ",:iduser,:autor),"
                "(" + insertedId + ",:idcliente,:cliente),"
                "(" + insertedId + ",:idvendedor,:vendedor)" 
                )

            query.bindValue( ":iduser", self.datosSesion.usuarioId )
            query.bindValue( ":idcliente", self.clienteId )
            query.bindValue( ":idvendedor", self.vendedorId )
            query.bindValue( ":autor", constantes.AUTOR)
            query.bindValue( ":cliente", constantes.CLIENTE)
            query.bindValue( ":vendedor",constantes.VENDEDOR )

            if not query.exec_():
                raise Exception( "No se Inserto la relacion entre el documento y las personas" )

            i = 0
            for linea in self.lines:
                if linea.valid:
                    linea.save( insertedId, i )
                    i = i + 1

#VERIFICO SI el id del iva es cero. NO SERA CERO CUANDO LA BODEGA=1 PORQUE ESTA NO ES exonerada                     
            
            if self.bodegaId == 1 :
                query.prepare( """
                INSERT INTO costosxdocumento (iddocumento, idcostoagregado) VALUES( :iddocumento, :idcostoagregado )
                """ )
                query.bindValue( ":iddocumento", insertedId )
                query.bindValue( ":idcostoagregado", self.ivaId )
                
                if not query.exec_():
                    print insertedId
                    print self.ivaId
                    raise Exception( "El iva NO SE INSERTO" )

            #manejar las cuentas contables en Cordobas
            # el costo no se multiplica porque ya esta en cordobas                
            
            guardar = True
            if self.escontado:
                movFacturaCredito( insertedId, self.subtotal * self.datosSesion.tipoCambioOficial , self.IVA * self.datosSesion.tipoCambioOficial, self.costototal )
                # Como es al contado el modelo otrosDatosModel guarda datos del recibo
                otrosDatosModel.lineasAbonos[0].idFac= insertedId
                guardar = otrosDatosModel.save(False)
            else:
                # Como es al credito el modelo otrosDatosModel guarda datos del credito
                query.prepare( """
                INSERT INTO creditos (iddocumento, fechatope,tasamulta) VALUES( :iddocumento, :fechatope, :multa )
                """ )
                query.bindValue( ":iddocumento", insertedId )
                query.bindValue( ":fechatope", self.ivaId )
                query.bindValue( ":multa", self.ivaId )
                
                guardar = query.exec_() 
                if not guardar:
                    print insertedId
                    print self.ivaId
                    raise Exception( "El iva NO SE INSERTO" )


            if not guardar or not QSqlDatabase.database().commit():
                raise Exception( "No se pudo guardar la factura" )
        except Exception as inst:
            print  query.lastError().databaseText()
            print query.lastError().driverText()
            print inst.args
            QSqlDatabase.database().rollback()
            return False

        return True
