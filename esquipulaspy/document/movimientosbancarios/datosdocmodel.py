# -*- coding: utf-8 -*-
'''
Created on 13/07/2010

@author: Luis Carlos Mejia
'''
from PyQt4.QtSql import QSqlDatabase, QSqlQuery
class DatosDocModel(object):
    def __init__( self):
        self.idConcepto =0
        self.idTipoDoc = 0
        self.idDoc = 0
        self.dateTime = None
        self.lineas = []
        self.observaciones = ""
        self.idUser = 0
        self.total = None
        self.delBanco = 0
    
    @property
    def valid( self ):
        if self.idUser ==0 or self.idCuentaContable == 0 or self.idTipoDoc ==0 or self.idConcepto == 0 or len(self.lineas) < 2 or self.dateTime == None:
            raise Exception( "los datos del documento estan incompletos" )
        return True    
    
    
    def save(self):
        """
        Este metodo guarda el documento 
        """
        
        query = QSqlQuery()
        try:
            if not QSqlDatabase.database() .isOpen():
                raise Exception( "La conexion esta cerrada, no se pueden guardar los datos del documento para NOTAS de CREDITO y DEBITO" )
       
#               Cargar el numero del asiento actual
            query.prepare( """
                SELECT
                  MAX(CAST(ndocimpreso AS SIGNED))+1
            FROM documentos d
            WHERE idtipodoc=:idtipodoc
            """)
            
            query.bindValue( ":idtipodoc", self.idTipoDoc )

            query.exec_()
            query.first()
            
            n = query.value( 0 ).toString()
            if n == "0" or n =="" :
                n = "1"
      
            if not query.prepare( """
            INSERT INTO documentos (ndocimpreso,total, fechacreacion, idconcepto, idtipodoc,observacion,delbanco) 
            VALUES (:ndocimpreso,:total, :fechacreacion, :idconcepto,:idtipodoc,:observacion,:externo)
            """ ):
                raise Exception( "No se pudo preparar la consulta para guardar el documento" )
            query.bindValue( ":ndocimpreso", n )
            query.bindValue( ":total", self.total.to_eng_string() )
            query.bindValue( ":fechacreacion", self.dateTime.toString("yyyyMMddhhmmss"))  
            query.bindValue( ":idconcepto", self.idConcepto) 
            query.bindValue( ":idtipodoc",self.idTipoDoc)
            query.bindValue( ":observacion",self.observaciones)
            query.bindValue( ":externo",self.delBanco)

            if not query.exec_():
                raise Exception( "No se pudo ejecutar la consulta para guardar el documento" )

            insertedId = query.lastInsertId().toInt()[0]
            self.idDoc = insertedId
            
            if not query.prepare( """
            INSERT INTO personasxdocumento (idpersona, iddocumento) 
            VALUES (:usuario, :documento)
            """ ):
                raise Exception( "No se pudo preparar la consulta para insertar el usuario" )
            
            query.bindValue( ":usuario", self.idUser )
            query.bindValue( ":documento", insertedId )

            if not query.exec_():
                raise Exception( u"No se pudo guardar la relaci�n con el usuario" )

            for lineid, line in enumerate( self.lineas ):
                if line.valid:
                    line.save( insertedId, lineid + 1 )

            return True
        except Exception as e:
            print e
            print query.lastError().text()
        
        return False
