# -*- coding: utf-8 -*-
'''
Created on 04/07/2010

@author: Luis Carlos Mejia
'''
from decimal import Decimal
from PyQt4.QtSql import QSqlQuery
#FIXME: para que sirve parent aca???
class LineaConciliacion( object ):
    def __init__( self, parent ):
        self.idDoc = 0
        self.fecha = ""
        self.concepto = ""
        self.monto = Decimal( 0 )
        self.saldo = Decimal( 0 )
        self.conciliado = 0
        self.delBanco = 0
        self.idTipoDoc = 0
        self.concepto2 = ""
        self.datos = None

    @property
    def valid( self ):
        """
        @rtype: bool
        """
        if self.idDoc != 0 or self.datos is not None:
            return True
        return False

    def save( self, iddocumento ):
        if not self.valid:
            raise Exception( "Se intento guardar una linea no valida" )

#insertar el documento relacionado
        if self.datos != None:
            if not self.datos.save():
                raise Exception( "No se pudo guardar el documento hijo" )
            self.idDoc = self.datos.idDoc
        if self.idDoc == 0:
            raise Exception( "No se puede insertar un documento con id 0" )

        query = QSqlQuery()
        query.prepare( 
        """
        INSERT INTO docpadrehijos (idpadre,idhijo ) 
        VALUES( :idconciliacion,:iddocumento)
        """ )
        query.bindValue( ":idconciliacion", iddocumento )
        query.bindValue( ":iddocumento", self.idDoc )

        if not query.exec_():
            raise Exception( "No se pudo guardar la linea con el articulo %d" %
                              self.idDoc )
