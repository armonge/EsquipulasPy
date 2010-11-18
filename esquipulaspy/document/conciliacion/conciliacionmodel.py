# -*- coding: utf-8 -*-
'''
Created on 03/07/2010

@author: Luis Carlos Mejia
'''
from PyQt4.QtCore import QAbstractTableModel, QVariant, QModelIndex, Qt
from PyQt4.QtSql import QSqlQuery, QSqlDatabase
from decimal import Decimal
from document.conciliacion.lineaconciliacion import LineaConciliacion
from utility import constantes
from utility.moneyfmt import moneyfmt
import logging
#from utility.constantes import IDCONCILIACION, IDDEPOSITO, IDNC, IDND, IDCHEQUE, IDERROR
#CAMBIAR columncount()
FECHA, CONCEPTO, DEBE, HABER, SALDO, CONCILIADO, DELBANCO, IDTIPODOC = range( 8 )
FECHA, BANCO, CUENTABANCO, MONEDA, CUENTACONTABLE, SALDOBANCO, IDDOC = range( 7 )
class ConciliacionModel( QAbstractTableModel ):
    """
    Esta clase es el modelo utilizado en la tabla en la que se editan los documentos
    """
    __documentType = str( constantes.IDCONCILIACION )
    """
    @cvar: El id del tipo de documento
    @type: int
    """
    def __init__( self,usuarioId ):
        super( ConciliacionModel, self ).__init__()

        self.validError = "La conciliacion no es valida"
        self.lines = []
        """
        @ivar:Las lineas en esta conciliación
        @type: LineaConciliacion[]
        """
        self.printedDocumentNumber = ""
        """
        @ivar:El numero de esta conciliación
        @type:string
        """
        self.idCuentaContable = 0
        """
        @ivar: El  id de la cuenta contable relacionada a la cuenta bancaria
        @type:int
        """
        self.saldoInicialLibro = Decimal( 0 )
        """
        @ivar: Saldo segun libro
        @type:Decimal
        """

        self.saldoInicialBanco = Decimal( 0 )
        """
        @ivar: Saldo segun banco
        @type:Decimal
        """
        self.cheques = Decimal ( 0 )
        """
        @ivar: total de cheques en tránsito
        @type:Decimal
        """

        self.notascredito = Decimal ( 0 )
        """
        @ivar: total de las notas de crédito que no habian sido registradas
        @type:Decimal
        """

        self.notasdebito = Decimal ( 0 )
        """
        @ivar: total de las notas de débito que no habian sido registradas
        @type:Decimal
        """

        self.depositos = Decimal( 0 )
        """
        @ivar: total de depositos en transito
        @type:Decimal
        """
        self.cheques = Decimal( 0 )
        """
        @ivar: total de cheques en transito
        @type:Decimal
        """
        self.notasdebito = Decimal( 0 )
        """
        @ivar: total de notas de debito
        @type:Decimal
        """
        self.notascredito = Decimal( 0 )
        """
        @ivar: total de notas de credito
        @type:Decimal
        """
        self.fechaConciliacion = None
        """
        @ivar: Fecha de la conciliacion
        @type:QDate
        """
        self.uid = usuarioId
        """
        @ivar: El id del usuario que realiza esta conciliación
        @type: int
        """

    @property
    def valid( self ):
        """
        Un documento es valido cuando 
        @rtype: bool
        """
        if int( self.idCuentaContable ) != 0 and int( self.uid ) != 0:
            return True
        return False

    @property
    def totalBanco( self ):
        """
        Es el saldo que la cuenta tiene al final del mes
        @rtype: Decimal 
        """
        tmpsubtotal = self.saldoInicialLibro + self.notascredito + self.notasdebito
        return tmpsubtotal if tmpsubtotal != 0 else Decimal( 0 )

    @property
    def totalLibro( self ):
        """
        El subtotal del documento, esto es el total antes de aplicarse el IVA
        """
        self.depositos = Decimal ( 0 )
        self.cheques = Decimal ( 0 )
        self.notascredito = Decimal ( 0 )
        self.notasdebito = Decimal ( 0 )
        for linea in self.lines:
            if linea.conciliado:
                if linea.delBanco == 0:
                    if linea.idTipoDoc in ( constantes.IDCHEQUE, constantes.IDND, constantes.IDERROR ):
                        self.cheques = self.cheques + linea.monto
                    else:
                        self.depositos = self.depositos + linea.monto
                else:
                    if linea.idTipoDoc in ( constantes.IDCHEQUE, constantes.IDND ):
                        self.notasdebito = self.notasdebito + linea.monto
                    else:
                        self.notascredito = self.notascredito + linea.monto



        tmpsubtotal = ( self.saldoInicialBanco ) + self.depositos + self.cheques
        return tmpsubtotal if tmpsubtotal != 0 else Decimal( 0 )

    @property
    def diferencia( self ):
        """
        Es el saldo que la cuenta tiene al final del mes
        @rtype: Decimal 
        """
        return abs( self.totalBanco - self.totalLibro )

    def rowCount( self, _index = QModelIndex() ):
        return len( self.lines )

    def columnCount( self, _index = QModelIndex() ):
        return 8

    def data( self, index, role = Qt.DisplayRole ):
        """
        Esta funcion redefine data en la clase base, es el metodo que se utiliza para mostrar los datos del modelo
        """

        if not index.isValid():
            return None

        column = index.column()
        line = self.lines[index.row()]

        if column == CONCILIADO and role in ( Qt.CheckStateRole, Qt.DisplayRole ) and index.row() > 0:
            if role == Qt.CheckStateRole:
                value = QVariant( Qt.Checked ) if self.lines[index.row()].conciliado == 1 else QVariant( Qt.Unchecked )
                return value
        elif role == Qt.EditRole:
            if column in ( DEBE, HABER ):
                return str( line.monto )
            elif column == IDTIPODOC:
                return str( line.idTipoDoc )
            elif column == CONCILIADO:
                return line.conciliado
            elif column == DELBANCO:
                return str( line.delBanco )

        elif role == Qt.DisplayRole:
            if column == HABER:
                return moneyfmt( line.monto * -1, 4, "C$" ) if line.monto < 0 else ""
            elif column == CONCEPTO:
                return line.concepto
            elif column == DEBE:
                return moneyfmt( line.monto, 4, "C$" ) if line.monto > 0 else ""
            elif column == SALDO:
                if line.idDoc != 0 or index.row() == 0:
                    return moneyfmt( line.saldo, 4, "C$" )
            elif column == FECHA:
                return line.fecha
            elif column == DELBANCO:
                return "Si" if line.delBanco == 1 else "No"
            elif column == IDTIPODOC:
                return str( line.idTipoDoc )

        elif role == Qt.ToolTipRole:
            if column == CONCEPTO:
                return line.concepto2

        else:
            return None

    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

        if index.column() == CONCILIADO:

            if self.lines[index.row()].delBanco == 1:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable
            return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData( self, index, data, role = Qt.DisplayRole ):
        if not index.isValid():
            return False
        if index.column() == CONCILIADO and role == Qt.CheckStateRole:
            if index.row() > 0:
                self.lines[index.row()].conciliado = 1 if data.toBool() else 0
                self.dataChanged.emit( index, index )
            return True



    def insertRows( self, position, rows = 1, _index = QModelIndex() ):
        self.beginInsertRows( QModelIndex(), position, position + rows - 1 )
        for row in range( rows ):
            self.lines.insert( position + row, LineaConciliacion( self ) )
        self.endInsertRows()
#        self.dirty = True 
        return True

    def removeRows( self, position, rows = 1, index = QModelIndex() ):
        self.beginRemoveRows( index, position, position + rows - 1 )
        for _i in range( rows ):
            self.lines.pop( position )
        self.endRemoveRows()

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int( Qt.AlignLeft | Qt.AlignVCenter )
            return int( Qt.AlignRight | Qt.AlignVCenter )
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:

            if  section == FECHA:
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
#OBTENER NUMERO DE DOCUMENTO
            query.prepare( """SELECT fnConsecutivo(:tipodoc,null)
                ;
                """ )
            query.bindValue( ":idtipodoc", self.__documentType )
            query.exec_()
            query.first()
            self.printedDocumentNumber = query.value( 0 ).toString()

#INSERTAR DOCUMENTO
            query.prepare( """
            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,total)
            VALUES ( :ndocimpreso,NOW(),:idtipodoc,:total)
            """ )
            query.bindValue( ":ndocimpreso", self.printedDocumentNumber )
            query.bindValue( ":idtipodoc", self.__documentType )
            query.bindValue( ":total", self.totalBanco.to_eng_string() )

            if not query.exec_():
                print query.lastError().databaseText()
                raise Exception( "No se pudo insertar el documento" )

            
            insertedId = query.lastInsertId().toInt()[0]
#INSERTAR RELACION CON EL USUARIO                        
            query.prepare( """
            INSERT INTO personasxdocumento(iddocumento,idpersona,idaccion)
            VALUES (:iddoc,:idusuario,:accion)
            """ )

            query.bindValue( ":iddoc", insertedId )
            query.bindValue( ":idusuario", self.uid )
            query.bindValue( ":accion", constantes.AUTOR )

            if not query.exec_():
                raise Exception( "No se pudo insertar la relacion"\
                                 + " con el usuario" )
#INSERTAR DATOS CONCILIACION
            query.prepare( """
            INSERT INTO conciliaciones(iddocumento,saldobanco,saldolibro,fecha,
            idcuentabancaria)
            VALUES (:iddoc,:saldobanco,:saldolibro,LAST_DAY(:fecha),:idcuenta);
            """ )
            query.bindValue( ":iddoc", insertedId )
#            print self.saldoInicialBanco.to_eng_string()
            query.bindValue( ":saldobanco", str( self.saldoInicialBanco ) )
            query.bindValue( ":saldolibro", str( self.saldoInicialLibro ) )
            query.bindValue( ":fecha", self.fechaConciliacion.toString( "yyyyMMdd" ) )
            query.bindValue( ":idcuenta", self.idCuentaContable )

            if not query.exec_():
                raise Exception( "No se pudo insertar la conciliacion" )
#INSERTAR LAS LINEAS                        
            for linea in self.lines:
#                if linea.valid and linea.conciliado:
                if linea.conciliado:
                    linea.save( insertedId )


            if not QSqlDatabase.database().commit():
                raise Exception( "No se pudo hacer commit" )


        except Exception as inst:
            logging.error( unicode( inst ) )
            logging.error( query.lastError().text() )
            logging.error( QSqlDatabase.database().lastError().text())
            QSqlDatabase.database().rollback()

            return False

        return True



