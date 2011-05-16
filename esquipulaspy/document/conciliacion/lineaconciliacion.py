# -*- coding: utf-8 -*-
'''
Created on 04/07/2010

@author: Luis Carlos Mejia
'''
from decimal import Decimal
from PyQt4.QtSql import QSqlQuery
from PyQt4.QtCore import QDate
from utility.accountselector import AccountsSelectorModel

class LineaConciliacion( AccountsSelectorModel ):
    def __init__( self , del_banco = False, saldo_inicial = Decimal( 0 ), monto = Decimal( 0 ), fecha = QDate.currentDate(), tipo_doc = 0, id_documento = 0, descripcion = '' ):
        super( LineaConciliacion, self ).__init__()

        self.id_documento = id_documento

        self.fecha = fecha
        self.descripcion = descripcion
        self.monto = Decimal( 0 )

        self._saldo_inicial = saldo_inicial

        self.conciliado = False
        self.tipo_doc = tipo_doc
        self.observaciones = ""

        self._del_banco = del_banco

        self.id_concepto = 0
        self.concepto = ''



    @property
    def del_banco( self ):
        return self._del_banco

    @property
    def saldo( self ):
        return self._saldo_inicial + self.monto

   


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
