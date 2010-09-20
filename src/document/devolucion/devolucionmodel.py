# -*- coding: utf-8 -*-
'''
Created on 19/05/2010

@author: Andrés Reyes Monge
'''
import unittest
if __name__ == "__main__":
    import sip
    sip.setapi( 'QString', 2 )
from decimal import Decimal
import logging
    
from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt, QDateTime, QCoreApplication
from PyQt4.QtSql import QSqlQuery, QSqlDatabase


from document.devolucion.lineadevolucion import LineaDevolucion

from utility.moneyfmt import moneyfmt
from utility.movimientos import movFacturaCredito
from utility import constantes

DESCRIPCION, PRECIO, CANTIDADMAX, CANTIDAD, TOTALPROD = range( 5 )
class DevolucionModel( QAbstractTableModel ):
    """
    Esta clase es el modelo utilizado en la tabla en la que se editan los documentos
    """
    __documentType = constantes.IDNC
    """
    @cvar: El id del tipo de documento
    @type: int
    """
    def __init__( self ):
        super( DevolucionModel, self ).__init__()
        self.observations = ""
        """
        @ivar:Las observaciones del documento
        @type:string
        """
        self.lines = []
        u"""
        @ivar:Las lineas en esta devolución
        @type: LineaDevolucion[]
        """
        self.printedDocumentNumber = ""
        u"""
        @ivar:El numero de esta devolución
        @type:string
        """
        self.numnotacredito = ""
        u"""
        @ivar:El numero de el documento Nota de Credito
        @type:string
        """
        
        self.clientId = 0
        """
        @ivar:El id del cliente de esta devolución
        @type: int
        """
        self.invoiceId = 0
        """
        @ivar: El  id de la factura para la cual se realiza esta devolución
        @type:int
        """
        self.billPrinted = ""
        """
        @ivar:El numero impreso de la factura
        @type:string
        """
        self.datetime = QDateTime.currentDateTime()
        """
        @ivar:La hora y fecha del documento
        @type:string
        """
        self.uid = 0
        """
        @ivar: El id del usuario que realiza esta devolución
        @type: int
        """
        self.clientName = ""
        """
        @ivar: El nombre del cliente que realiza esta devolución
        @type: string
        """
        
        self.conceptId = 0
        u"""
        @ivar: El id del concepto de la devolución
        @type: int
        """ 

        self.ivaRate = Decimal( 0 )
        """
        @ivar: El porcentaje de IVA en esta devolucion, es el de la factura
        @type:Decimal
        """
        self.ivaRateId = 0
        """
        @ivar: El id de este porcentaje IVA
        @type: int
        """
        self.applyIva = True
        u"""
        @ivar: Si se aplica o no IVA en esta devolución
        type:bool
        """

        self.exchangeRateId = 0
        u"""
        @ivar: El id del tipo de cambio en esta devolución
        @type:int
        """
        self.exchangeRate = Decimal( 0 )
        u"""
        @ivar: EL tipo de cambio de esta devolución
        @type:Decimal
        """
        
        self.warehouseId = 0
        u"""
        @ivar: El id de la bodega en la cual se hace la devolución
        @type:Decimal
        """
        self.warehouseName = ""
        u"""
        @ivar: El nombre de la bodega en la cual se hace la devolución
        @type:string
        """


    @property
    def valid( self ):
        """
        Un documento es valido cuando 
        @rtype: bool
        """
        if not int( self.clientId ) != 0:
            self.validError = "No ha seleccionado un cliente"
            return False
        elif not  int( self.validLines ) > 0:
            self.validError = u"No existen lineas que guardar en la devolución"
            return False
        elif not int( self.uid ) != 0:
            self.validError = "No se puede determinar el usuario que realiza el documento"
            return False
        elif not int( self.invoiceId ) != 0:
            self.validError = "No se ha especificado el numero de factura"
            return False
        elif not self.printedDocumentNumber != "":
            self.validError = u"No se ha especificado el numero de devolución"
            return False
        elif not int( self.exchangeRateId ) != 0 :
            self.validError = "No hay un tipo de cambio para el documento"
            return False
        elif not int(self.conceptId) > 0:
            self.validError = u"No se ha especificado un concepto para la devolución"
            return False
        elif not int(self.warehouseId) > 0:
            self.validError = u"No se ha especificado la bodega para la devolución"
            return False
        return True
        

    @property
    def subtotalD( self ):
        """
        El total en dolares del documento
        @rtype: Decimal 
        """
        foo = sum( [ line.totalD for line in self.lines if line.valid ] )
        return foo if foo != 0 else Decimal( 0 )
    
    @property
    def totalD( self ):
        """
        El subtotal en dolares del documento
        @rtype: Decimal
        """
        return self.subtotalD * (1+ ( self.ivaRate / 100 ) )

    @property
    def totalC( self ):
        """
        El total en cordobas del documento
        @rtype: decimal
        """
        return self.totalD * self.exchangeRate

    @property
    def subtotalC( self ):
        """
        El subtotal en cordobas del documento
        @rtype: Decimal
        """
        return self.subtotalD * self.exchangeRate
    @property
    def ivaD( self ):
        """
        El iva en dolares
        @rtype: Decimal
        """
        return self.subtotalD * ( self.ivaRate / 100 )

    @property
    def ivaC( self ):
        """
        El iva en cordobas
        @rtype: Decimal
        """
        return self.ivaD * self.exchangeRate

    @property
    def totalCostD( self ):
        """
        El costo total del documento, en dolares
        @rtype: Decimal
        """
        foo = sum( [ line.costoD for line in self.lines if line.valid ] )
        return foo if foo != 0 else Decimal( 0 )

    @property
    def  totalCostC( self ):
        """
        El costo en cordobas del documento
        """
        return self.totalCostD * self.exchangeRate

    @property
    def validLines( self ):
        """
        la cantidad de lineas validas que hay en el documento
        @rtype: int
        """
        return len( [ line for line in self.lines if line.valid ] )

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
            if column == DESCRIPCION:
                return line.itemDescription
            elif column == PRECIO:
                return moneyfmt( Decimal( line.itemPrice ), 4, "US$" )
            elif column == CANTIDADMAX:
                return line.maxquantity
            elif column == CANTIDAD:
                return line.quantity
            elif column == TOTALPROD:
                return moneyfmt( line.totalD, 4, "US$" )

    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column() == CANTIDAD:
            return Qt.ItemFlags( QAbstractTableModel.flags( self, index ) | Qt.ItemIsEditable )
        else:
            return Qt.ItemIsEnabled


    def setData( self, index, value, role = Qt.EditRole ):
        """
        modificar los datos del modelo, este metodo se comunica con el delegate
        """
        if index.isValid() and 0 <= index.row() < len( self.lines ):
            line = self.lines[index.row()]
            if index.column() == CANTIDAD:
                line.quantity = value.toInt()[0]

            self.dirty = True

            self.dataChanged.emit(index, index)

            return True
        return False

    def insertRows( self, position, rows = 1, index = QModelIndex() ):
        self.beginInsertRows( QModelIndex(), position, position + rows - 1 )
        for row in range( rows ):
            self.lines.insert( position + row, LineaDevolucion( self ) )
        self.endInsertRows()
        self.dirty = True
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

            elif section == PRECIO:
                return "Precio Unitario"
            elif section == CANTIDADMAX:
                return "Maximo de unidades"
            elif section == CANTIDAD:
                return "Unidades"
            elif section == TOTALPROD:
                return "Total"
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
                raise Exception( u"No se puedo comenzar la transaccion" )
            #Insertar el documento
            if not query.prepare( """
            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,idestado,  observacion,total, idtipocambio, idconcepto, idbodega)
            VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:pendiente,:observacion,:total, :idtipocambio, :idconcepto, :idbodega)
            """ ):
                raise Exception(u"No se pudo preparar la consulta para añadir el documento")

            query.bindValue( ":ndocimpreso", 'S/N')
            query.bindValue( ":fechacreacion", self.datetime.toString( 'yyyyMMddhhmmss' ) )
            query.bindValue( ":idtipodoc", self.__documentType )
            query.bindValue( ":pendiente", constantes.PENDIENTE)
            query.bindValue( ":observacion", self.observations )
            query.bindValue( ":total", self.totalD.to_eng_string() )
            query.bindValue( ":idtipocambio", self.exchangeRateId )
            query.bindValue(":idconcepto", self.conceptId)
            query.bindValue(":idbodega", self.warehouseId)

            if not query.exec_():
                raise Exception( "No se pudo insertar el documento" )


            insertedId = query.lastInsertId().toInt()[0]
            
            #Insertar el usuario y cliente
            if not query.prepare("""
            INSERT INTO personasxdocumento (idpersona, iddocumento,idaccion)
            VALUES (:idpersona, :iddocumento,:accion)
            """):
                raise Exception("No se pudo preparar la consulta para los usuarios y las personas")

            query.bindValue(":idpersona", self.clientId )
            query.bindValue(":iddocumento", insertedId)
            query.bindValue(":accion", constantes.CLIENTE)

            if not query.exec_():
                raise Exception(u"No se pudo aniadir el cliente")

            if not query.prepare("""
            INSERT INTO personasxdocumento (idpersona, iddocumento,idaccion)
            VALUES (:idusuario, :iddocumento,:accion)
            """):
                raise Exception("No se pudo preparar la consulta para el usuario")
            query.bindValue(":idusuario", self.uid)
            query.bindValue(":iddocumento", insertedId)
            query.bindValue(":accion", constantes.AUTOR)

            if not query.exec_():
                raise Exception(u"No se pudo añadir el usuario")
            
            

#Insertar la revercion de los articulos
            for linea in self.lines:
                if linea.valid:
                    linea.save( insertedId )
            
            #            Crear la relacion con su padre
            if not query.prepare( """
            INSERT INTO docpadrehijos (idpadre, idhijo) VALUES (:idpadre, :idhijo)
            """ ):
                raise Exception(u"No se pudo preparar la consulta para insertar la relación de la devolución con la factura")
            
            query.bindValue( ":idpadre", self.invoiceId )
            query.bindValue( ":idhijo", insertedId )

            if not query.exec_():
                raise Exception(u"No se pudo crear la relacion de la devolución con la factura" )

#            
#            
#            #Insertar el documento de Nota de Credito
#            if not query.prepare( """
#            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,anulado,total, idtipocambio, idconcepto, idbodega)
#            VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:anulado,:total, :idtipocambio, :idconcepto, :idbodega)
#            """ ):
#                raise Exception(u"No se pudo preparar la consulta para añadir el documentoNotaCredito")
#
#            query.bindValue( ":ndocimpreso", self.numnotacredito )
#            query.bindValue( ":fechacreacion", self.datetime.toString( 'yyyyMMddhhmmss' ) )
#            query.bindValue( ":idtipodoc", constantes.IDNOTACREDITO )
#            query.bindValue( ":idusuario", self.uid )
#            query.bindValue( ":anulado", 0 )
#            query.bindValue( ":idpersona", self.clientId )
#            query.bindValue( ":total", self.totalD.to_eng_string() )
#            query.bindValue( ":idtipocambio", self.exchangeRateId )
#            query.bindValue(":idconcepto", self.conceptId)
#            query.bindValue(":idbodega", self.warehouseId)
#
#            if not query.exec_():
#                raise Exception( "No se pudo insertar el documento Nota Credito" )
#            insertedIdNC=query.lastInsertId()
#            
#            # Crear la relacion con su padre Devolucion
#            if not query.prepare( """
#            INSERT INTO docpadrehijos (idpadre, idhijo) VALUES (:idpadre, :idhijo)
#            """ ):
#                raise Exception(u"No se pudo preparar la consulta para insertar la relación de la deovulución con la NotaCredito")
#            
#            query.bindValue( ":idpadre", insertedId )
#            query.bindValue( ":idhijo", insertedIdNC )
#
#            
#            
#            if not query.exec_():
#                raise Exception(u"No se creo la relacion de la devolución con la factura" )


#            query.prepare( """
#                SELECT
#                s.iddocumento,
#                s.ndocimpreso,
#                s.Saldo,
#                IFNULL(ca.valorcosto,0) as tasaiva,
#                s.idpersona
#            FROM vw_saldofacturas s
#            LEFT JOIN costosxdocumento cxd ON s.iddocumento= cxd.iddocumento
#            LEFT JOIN costosagregados ca ON ca.idcostoagregado = cxd.idcostoagregado AND ca.idtipocosto=%d
#            WHERE s.idpersona=%d
#            ORDER BY CAST(s.ndocimpreso AS SIGNED)"""%(constantes.IVA,self.clientId) )
#            if not query.exec_():
#                query.lastError().text()
#                raise Exception( "Ocurrio un error al ejecutar la consulta del saldo" )
#            #FIXME
#            query.first()
#            saldo=Decimal(query.value(2).toString())
#            if saldo<=self.totalD():
#                movFacturaCredito( insertedIdNC, self.subtotalC * -1, self.ivaC * -1, self.totalCostC * -1 )
#            else:
#                subsaldo=saldo/1+(self.ivaRate/100)             
#                subiva=saldo-subsaldo
#                
#                diferencia=(self.totalD()-saldo)/1+(self.ivaRate/100)
#                ivad=diferencia-saldo 
#                #FIXME               
#                movFacturaCredito( insertedIdNC, subsaldo * -1, subiva * -1, self.totalCostC * -1 )
##                movPagoRealizado( insertedIdNC, diferencia * -1, ivad * -1, self.totalCostC * -1 )
#=======
#            query.bindValue( ":ndocimpreso", self.numnotacredito )
#            query.bindValue( ":fechacreacion", self.datetime.toString( 'yyyyMMddhhmmss' ) )
#            query.bindValue( ":idtipodoc", constantes.IDNOTACREDITO )
#            query.bindValue( ":idusuario", self.uid )
#            query.bindValue( ":idpersona", self.clientId )
#            query.bindValue( ":total", self.totalD.to_eng_string() )
#            query.bindValue( ":idtipocambio", self.exchangeRateId )
#            query.bindValue(":idconcepto", self.conceptId)
#            query.bindValue(":idbodega", self.warehouseId)
#>>>>>>> .r246

            if not QSqlDatabase.database().commit():
                raise Exception( "No se pudo hacer commit" )


        except Exception as inst:
            logging.critical( query.lastError().text() )
            logging.critical(unicode( inst ))
            QSqlDatabase.database().rollback()

            return False

        return True

class TestDevolucionModel(unittest.TestCase):
    def setUp(self):
        app = QCoreApplication([])

        self.devolucion = DevolucionModel()
        self.devolucion.insertRow(0)

    def test_total(self):
        self.assertEqual(self.devolucion.totalC, Decimal('0') )
        self.assertEqual(self.devolucion.totalD, Decimal('0') )

    def test_cost(self):
        self.assertEqual(self.devolucion.totalCostC, Decimal('0'))
        self.assertEqual(self.devolucion.totalCostD, Decimal('0'))
        
    def test_numrows(self):
        self.assertEqual(self.devolucion.rowCount(), 1)

    def test_validLines(self):
        self.assertEqual(self.devolucion.validLines, 0)

    def test_valid(self):
        self.assertFalse(self.devolucion.valid)

    def test_subtotal(self):
        self.assertEqual(self.devolucion.subtotalD, Decimal('0') )
        self.assertEqual(self.devolucion.subtotalC, Decimal('0') )

if __name__ == "__main__":
    unittest.main()