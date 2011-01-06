# -*- coding: utf-8 -*-
'''
Created on 13/07/2010

@author: Luis Carlos Mejia
'''
from PyQt4.QtSql import QSqlDatabase, QSqlQuery
from decimal import Decimal
from utility import constantes

class DatosDocModel( object ):
    def __init__( self ):

        self.idDoc = 0
        """
        @ivar: El id del documento
        @type: int
        """

        self.numeroDoc = ""
        """
        @ivar: Numero del formato impreso del documento
        @type: string
        """

        self.totalDoc = Decimal( 0 )
        """
        @ivar: Total en d�lares del documento
        @type: Decimal
        """

        self.fechaDoc = None
        """
        @ivar: fecha del documento
        @type: QDate
        """

        self.tipoDoc = 0
        """
        @ivar: El id que representa que tipo de documento es
        @type: int
        """       
        
        self.conceptoId =0
        """
        @ivar: El id del concepto elegido para el documento
        @type: int
        """

        self.observacionesDoc = ""
        """
        @ivar: Las observaciones del documento
        @type: string
        """

        self.bancoDoc = 0
        """
        @ivar: 1 si el documento fue elaborado por el banco y 0 si fue elaborado por la empresa
        @type: int
        """

        self.lineasDoc = []
        """
        @ivar: Arreglo de lineas relacionadas al documento. Almacena los datos del detalle del documento. Almacena objetos que heredan de clases especificas para cada documento Ej. LineaFactura, LineaRecibo, etc.
        @type: Array
        """

        self.mensajeError = ""
        """
        @ivar: Almacena un mensaje que describe el error producido.
        @type: string
        """

        self.cuentaBancaria = ""
        """
        @ivar: null si el documento no es cheque, de lo contrario almacena el id de la cuenta bancaria relacionada
        @type: string
        """

        self.autorId = 0
        """
        @ivar: El id del usuario que creo el documento
        @type: int
        """

    @property
    def valid( self ):
        """
        Verdadero si la informaci�n obligatoria para la elaboracion del documento esta correcta
        @rtype: bool
        """
        if self.totalDoc == 0 :
            self.mensajeError = "El total del documento no puede ser 0"
        elif self.tipoDoc == 0 :
            self.mensajeError = "Por favor especifique el tipo de documento"
        elif self.conceptoId == 0 :
            self.mensajeError = "Por favor especifique el concepto del documento"
        elif self.autorId == 0:
            self.mensajeError = "El id del usuario no puede ser 0"
        elif self.fechaDoc == None :
            self.mensajeError = "Por favor especifique la fecha del documento"
        else:
            return True
        return False

    def save( self ):
        """
        Verdadero si el documento fue guardado
        @rtype: bool 
        """

        query = QSqlQuery()

#        try:
        if not QSqlDatabase.database() .isOpen():
            raise Exception( "La conexion esta cerrada, no se pueden guardar los datos del documento" )
   
        if not QSqlDatabase.database().transaction():
            raise Exception( u"No se pudo comenzar la transacción" )
   
        query.prepare( """
            SELECT fnConsecutivo(:tipodoc,:cuenta);
        """)
        
        query.bindValue( ":tipodoc", self.tipoDoc )
        query.bindValue( ":cuenta", self.cuentaBancaria )
 

        if not query.exec_():
            raise Exception("No se pudo obtener el numero de deposito")
        query.first()
                    
        self.numeroDoc = query.value( 0 ).toString()

  
        if not query.prepare( """
        INSERT INTO documentos (ndocimpreso,total, fechacreacion, idconcepto, idtipodoc,observacion,delbanco) 
        VALUES (:ndocimpreso,:total, :fechacreacion, :idconcepto,:idtipodoc,:observacion,:externo)
        """ ):
            raise Exception( "No se pudo preparar la consulta para guardar el documento" )
        
        query.bindValue( ":ndocimpreso", self.numeroDoc )
        query.bindValue( ":total", self.totalDoc.to_eng_string() )
        query.bindValue( ":fechacreacion", self.fechaDoc.toString("yyyyMMddhhmmss"))  
        query.bindValue( ":idconcepto", self.conceptoId) 
        query.bindValue( ":idtipodoc",self.tipoDoc)
        query.bindValue( ":observacion",self.observacionesDoc)
        query.bindValue( ":externo",self.bancoDoc)

        if not query.exec_():
            raise Exception( "No se pudo ejecutar la consulta para guardar el documento" )


        self.idDoc = query.lastInsertId().toString()
        
        
        if not query.prepare( """
        INSERT INTO personasxdocumento (idpersona, iddocumento,idaccion) 
        VALUES (:usuario, :documento,:accion)
        """ ):
            raise Exception( "No se pudo preparar la consulta para insertar el usuario" )
        
        query.bindValue( ":usuario", self.autorId )
        query.bindValue( ":documento", self.idDoc )
        query.bindValue( ":accion", constantes.AUTOR )

        if not query.exec_():
            raise Exception( u"No se pudo guardar la relacion con el usuario" )


        for nLinea, linea in enumerate( self.lineasDoc ):
            if linea.valid:
                linea.save( self.idDoc, nLinea + 1 )
            else:
                raise Exception ("Linea Invalida")

        if not QSqlDatabase.database().commit():
            raise Exception( "No se pudo hacer commit" )
        return True

#        except Exception as inst:
#            logging.critical( query.lastError().text() )
#            logging.critical( unicode( inst ) )
#            QSqlDatabase.database().rollback()
#            
#        finally:
#            if QSqlDatabase.database().isOpen():
#                QSqlDatabase.database().close()
#                
        return False

