# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: armonge
'''
from PyQt4.QtGui import QMessageBox
from PyQt4 import QtGui
from PyQt4.QtSql import QSqlDatabase, QSqlQuery
from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt, SIGNAL, QDateTime
from decimal import Decimal,InvalidOperation
from utility.moneyfmt import moneyfmt
from utility.accountselector import AccountsSelectorModel
from utility import constantes
from math import ceil
IDARTICULO, DESCRIPCION, REFERENCIA, MONTO, TOTALPROD, MONEDA = range( 6 )
class ChequeModel( AccountsSelectorModel ):
    """
    esta clase es el modelo utilizado en la tabla en la que se editan los documentos
    """
    
    __documentType = constantes.IDCHEQUE
    """
    @ivar:El tipo de documento
    @type: int
    """ 
    def __init__( self  ):
        super( ChequeModel, self ).__init__()

        self.proveedorId = 0
        """
        @ivar: El id del proveedor en este documento
        @type: int
        """
        self.observations = ""
        """
        @ivar: Las observaciones que podria tener el documento
        @type: string
        """ 
        self.printedDocumentNumber = ""
        """
        @ivar: El numero de documento impreso
        @type:string
        """
        self.datetime = QDateTime.currentDateTime()
        """
        @ivar: La fecha en la que se hizo el documento
        @type: QDateTime
        """ 
        self.uid = 0
        """
        @ivar: El id del usuario que esta haciendo este documento
        @type: int
        """
        self.conceptoId = 0
        """
        @ivar: El id del concepto de este documento
        @type: int
        """ 
        
        self.simbolo = ""
        """
        @ivar: El simbolo de la moneda del documento
        @type: String
        """


        self.retencionId = 0
        """
        @ivar: El id de la retención de este documento
        @type: int
        """
        self.retencionPorcentaje = 0
        """
        @ivar: El porcentaje de retención de este documento
        @type: int
        """
        
        self.ivaRate=Decimal(0)
        """
        @ivar: El porcentaje del iva a aplicar en este documento
        @type: Decimal
        """ 
        
        self.moneda=""
        """
        @ivar: El simbolo de la moneda a aplicar en este documento
        @type: String
        """ 
        
        self.exchangeRateId=0
        """
        @ivar: El id del tipo de cambio de este documento
        @type: int
        """
        self.exchangeRate= Decimal(0)
        """
        @ivar: El tipo de cambio usado en este documento
        @type: Decimal
        """
        
        self.validError = ""
        """
        @ivar: Si existe o no un error de validación en este documento entonces se muestra aca
        @type: string
        """
        self.hasretencion=False
        """
        @ivar: Para verificar si tiene retencion o no
        @type: Boolean
        """
        self.subtotal=Decimal(0)
        """
        @ivar: El subtotal del documento
        @type: Decimal
        """
        self.hasiva=False
        """
        @ivar: Para determinar si el cheque lleva IVA o no
        @type: Boolean
        """
        self.ivaId=0
        """
        @ivar: El ID del costo agregado IVA
        @type: Int
        """
    @property
    def valid( self ):
        """
        Un documento es valido cuando 
        self.printedDocumentNumber != ""
        self.providerId !=0
        self.validLines >0
        self.__idIVA !=0
        self.uid != 0
        self.total>0 
        """
        if  self.printedDocumentNumber == "":
            self.validError = "No existe numero de doc impreso" 
            return False
        elif int( self.proveedorId ) < 1:
            self.validError = "No ha seleccionado ningun cliente" 
            return False
        elif Decimal( self.subtotal ) <=0:
            self.validError = "Escriba una cantidad para el documento" 
            return False
        elif int( self.uid ) == 0:
            self.validError = "Existe un error con el Usario que esta creando el documento" 
            return False
        elif int( self.conceptoId ) == 0:
            self.validError = "No hay un concepto seleccionado" 
            return False
        elif self.exchangeRateId == 0:
            self.validError = "No hay un tipo de cambio para la fecha" + self.datetime 
            return False
        elif self.hasretencion==True and self.retencionPorcentaje==0:
            self.validError = "No existe un porcentaje de Retencion seleccionado" 
            return False
        elif not super(ChequeModel, self).valid :
            self.validError ="Hay un error en sus cuentas contables"
            return False
        else:
            return True



    #TODO: INSERCION
    def save( self ):
        """
        Este metodo guarda el documento actual en la base de datos
        """

        if not self.valid:
            raise UserWarning( "El documento a guardar no es valido" )

        query = QSqlQuery()

        try:

            if not QSqlDatabase.database().transaction():
                raise UserWarning( u"No se pudo iniciar la transacción" )
#           
            #INSERTAR CHEQUE
            query.prepare( """
            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,idestado, observacion,total,idtipocambio,idconcepto) 
            VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:estado,:observacion,:total,:idtc,:concepto)
            """ )
            
            query.bindValue( ":ndocimpreso", self.printedDocumentNumber )
            query.bindValue( ":fechacreacion", self.datetime.toString( 'yyyyMMddhhmmss' ) )
            query.bindValue( ":idtipodoc",self.__documentType )
            query.bindValue( ":estado", constantes.PENDIENTE )
            query.bindValue( ":observacion", self.observations )
            query.bindValue( ":total", self.totalDolares.to_eng_string())
            query.bindValue( ":idtc", self.exchangeRateId )
            query.bindValue( ":concepto", self.conceptoId )
            
            if not query.exec_():
                raise UserWarning( "No se pudo crear el Cheque" )
            insertedId = query.lastInsertId().toString()
            #INSERTAR LA RELACION CON El USUARIO , EL CLIENTE Y EL PROVEEDOR            
            if not query.prepare( 
                "INSERT INTO personasxdocumento (iddocumento,idpersona,idaccion) VALUES" +  
                "(" + insertedId + ",:iduser,:autor),"
                "(" + insertedId + ",:idproveedor,:proveedor)" 
                ):
                print query.lastQuery()
                raise Exception( "No se puedo preparar la consulta para insertar las personas" )
            
            query.bindValue( ":iduser", self.uid )
            query.bindValue( ":idproveedor", self.proveedorId )
            query.bindValue( ":autor", constantes.AUTOR)
            query.bindValue( ":proveedor",constantes.PROVEEDOR )

            if not query.exec_():
                raise Exception( "No se Inserto la relacion entre el documento y las personas" )
            
            if self.hasiva==True:
                # INSERTAR EL ID DEL COSTO IVA                
                query.prepare( """
                INSERT INTO costosxdocumento (iddocumento, idcostoagregado) VALUES( :iddocumento, :idcostoagregado )
                """ )
                query.bindValue( ":iddocumento", insertedId )
                query.bindValue( ":idcostoagregado", self.ivaId)
                if not query.exec_():
                    raise UserWarning( "el costo IVA no se inserto" )
            
            if self.retencion>=0 and self.retencionId>=0 and self.hasretencion==True:
                #INSERTAR EL DOCUMENTO RETENCION            
                query.prepare( """
                INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,idestado, observacion,total,escontado,idtipocambio,idconcepto) 
                VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:idestado,:observacion,:total,:escontado,:idtc,:concepto)
                """ )
                query.bindValue( ":ndocimpreso", self.printedDocumentNumber )
                query.bindValue( ":fechacreacion", self.datetime )
                query.bindValue( ":idtipodoc", constantes.IDRETENCION )
                query.bindValue( ":idestado", constantes.PENDIENTE )
                query.bindValue( ":observacion", self.observations )
                query.bindValue( ":total", self.retencion.to_eng_string())
                query.bindValue( ":escontado", 1 )
                query.bindValue( ":idtc", self.exchangeRateId )
                query.bindValue( ":concepto", self.conceptoId )
                if not query.exec_():
                    raise UserWarning( "No se Inserto la retencion" )
        
                idret = query.lastInsertId().toInt()[0]
    
                #INSERTAR EL BENEFICIARIO Y USUARIO DE LA RETENCION
                query.prepare("INSERT INTO personasxdocumento(iddocumento,idpersona,idaccion) VALUES(:iddocumento,:idusuario,:autor)")
                query.bindValue( ":iddocumento", idret )
                query.bindValue( ":idusuario", self.uid)
                query.bindValue( ":autor", constantes.AUTOR)
                if not query.exec_():
                    raise UserWarning( "No se pudo regitrar el usuario que creo la retencion" )
                
                
                query.prepare("INSERT INTO personasxdocumento(iddocumento,idpersona,idaccion) VALUES(:iddocumento,:idproveedor,:proveedor)")
                query.bindValue( ":iddocumento", idret )
                query.bindValue( ":idproveedor", self.proveedorId)
                query.bindValue( ":proveedor", constantes.PROVEEDOR)
                if not query.exec_():
                    raise UserWarning( "No se pudo insertar el beneficiario de la retencion" )
                
                #DOCUMENTO PADRE CHEQUE, DOCUMENTO HIJO RETENCION
                query.prepare( """
                INSERT INTO docpadrehijos (idpadre,idhijo)
                VALUES (:idcheque,:idretencion)
                """ )
        
                query.bindValue( ":idcheque", insertedId )
                query.bindValue( ":idretencion", idret )
        
                if not query.exec_():
                    print( insertedId )
                    print( idret )
                    raise UserWarning( "No se Inserto la relacion entre la retencion y el Cheque" )
        
        
                # INSERTAR EL ID DEL COSTO RETENCION                
                query.prepare( """
                INSERT INTO costosxdocumento (iddocumento, idcostoagregado) VALUES( :iddocumento, :idcostoagregado )
                """ )
                query.bindValue( ":iddocumento", idret )
                query.bindValue( ":idcostoagregado", self.retencionId)
                if not query.exec_():
                    raise UserWarning( "el costo Retencion  NO SE INSERTO" )
                            
            #INSERTAR LAS CUENTAS CONTABLES
            for lineid, line in enumerate( self.lines ):
                if line.valid:
                    line.save( insertedId, lineid + 1 )
                    
            if not QSqlDatabase.database().commit():
                raise UserWarning( "No se pudo realizar la Transaccion" )
            
            return True
        
        except UserWarning as inst:
            print inst
            print query.lastError().text()
            QSqlDatabase.database().rollback()
            return False
        except Exception as inst:
            print inst
            print query.lastError().text()
            QSqlDatabase.database().rollback()
            return False 
    @property
    def totalCordobas( self ):
        """
        El total neto del documento, despues de haber aplicado IVA y Retencion en Cordobas
        @rtype: Decimal
        """
        subtotalcordobas=self.subtotal if self.moneda==constantes.IDCORDOBAS else self.subtotal*self.exchangeRate
        retencion=self.retencion
        if self.hasiva==True:
            return subtotalcordobas+(subtotalcordobas*self.ivaRate/100) - (retencion if self.moneda==constantes.IDCORDOBAS else retencion*self.exchangeRate)
        else:
            return subtotalcordobas - (retencion if self.moneda==constantes.IDCORDOBAS else retencion*self.exchangeRate)
            
            
    @property
    def totalDolares( self ):
        """
        El total neto del documento, despues de haber aplicado IVA y Retencion en Dolares
        @rtype: Decimal
        """
        try:
            return self.totalCordobas/self.exchangeRate
        except InvalidOperation as ins:
            return Decimal(0)
         
            
    @property
    def iva( self ):
        """
        El valor del IVA en Cordobas
        @rtype: Decimal
        """
        if self.hasiva==True:
            return self.subtotal*(self.ivaRate/100)
        else: 
            return Decimal(0)
       
    @property
    def retencion( self ):
        """
        El valor de la retencion en cordobas
        @rtype: Decimal
        """
        subtotalcordobas=self.subtotal if self.moneda==constantes.IDCORDOBAS else self.subtotal*self.exchangeRate
        if subtotalcordobas>1000:
            return self.subtotal*(self.retencionPorcentaje/100)
        else:
            return Decimal(0)
        
    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled
        elif index.row() != 0:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable
        else:
            return Qt.ItemIsEnabled