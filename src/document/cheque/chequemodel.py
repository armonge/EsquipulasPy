# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: armonge
'''
from PyQt4.QtGui import QMessageBox
from PyQt4 import QtGui
from PyQt4.QtSql import QSqlDatabase, QSqlQuery
from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt, SIGNAL, QDateTime
from decimal import Decimal
from utility.moneyfmt import moneyfmt
from utility.accountselector import AccountsSelectorModel
from utility import constantes
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
        self.total=Decimal(0)
        """
        @ivar: El total del documento
        @type: Decimal
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

        self.retencionId = 0
        """
        @ivar: El id de la retención de este documento
        @type: int
        """
        self.retencionNumero = 0
        """
        @ivar: El numero de retención de este documento
        @type: int
        """
        
        self.iva=Decimal(0)
        """
        @ivar: El iva de este documento
        @type: Decimal
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
        
    @property
    def valid( self ):
        """
        Un documento es valido cuando 
        self.printedDocumentNumber != ""
        self.providerId !=0
        self.validLines >0
        self.__idIVA !=0
        self.uid != 0
        self.warehouseId != 0 
        """
        if  self.printedDocumentNumber == "":
            self.validError = "No existe numero de doc impreso" 
            return False
        elif int( self.proveedorId ) < 1:
            self.validError = "No existe un cliente seleccionado" 
            return False
        elif int( self.uid ) == 0:
            self.validError = "No hay un usuario" 
            return False
        elif int( self.conceptoId ) == 0:
            self.validError = "No hay un concepto" 
            return False
        elif self.exchangeRateId == 0:
            self.validError = "no hay un tipo de cambio para la fecha" + self.datetime 
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
            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,anulado, observacion,total,idtipocambio,idconcepto) 
            VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:anulado,:observacion,:total,:idtc,:concepto)
            """ )
            
            query.bindValue( ":ndocimpreso", self.printedDocumentNumber )
            query.bindValue( ":fechacreacion", self.datetime.toString( 'yyyyMMddhhmmss' ) )
            query.bindValue( ":idtipodoc", self.__documentType )
            query.bindValue( ":anulado", 0 )
            query.bindValue( ":observacion", self.observations )
            query.bindValue( ":total", self.total.to_eng_string())
            query.bindValue( ":idtc", self.exchangeRateId )
            query.bindValue( ":concepto", self.conceptoId )
            
            if not query.exec_():
                raise UserWarning( "No se pudo crear el Cheque" )
            insertedId = query.lastInsertId().toInt()[0]
                    
            #INSERTAR EL BENEFICIARIO Y USUARIO
            query.prepare("INSERT INTO personasxdocumento(iddocumento,idpersona) VALUES(:iddocumento,:idusuario)")
            query.bindValue( ":iddocumento", insertedId )
            query.bindValue( ":idusuario", self.uid)
            if not query.exec_():
                raise UserWarning( "No se pudo regitrar el usuario que creo el cheque" )
            
            query.prepare("INSERT INTO personasxdocumento(iddocumento,idpersona) VALUES(:iddocumento,:idproveedor)")
            query.bindValue( ":iddocumento", insertedId )
            query.bindValue( ":idproveedor", self.proveedorId)
            if not query.exec_():
                raise UserWarning( "No se pudo insertar el beneficiario" )
            

            #INSERTAR EL DOCUMENTO RETENCION            
            query.prepare( """
            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,anulado, observacion,total,escontado,idtipocambio,idconcepto) 
            VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:anulado,:observacion,:total,:escontado,:idtc,:concepto)
            """ )
            query.bindValue( ":ndocimpreso", self.printedDocumentNumber )
            query.bindValue( ":fechacreacion", self.datetime )
            query.bindValue( ":idtipodoc", constantes.IDRETENCION )
            query.bindValue( ":anulado", 0 )
            query.bindValue( ":observacion", self.observations )
            query.bindValue( ":total", self.retencionNumero.to_eng_string())
            query.bindValue( ":escontado", 1 )
            query.bindValue( ":idtc", self.exchangeRateId )
            query.bindValue( ":concepto", self.conceptoId )
            if not query.exec_():
                raise UserWarning( "No se Inserto la retencion" )
            idret = query.lastInsertId().toInt()[0]
            
            #INSERTAR EL BENEFICIARIO Y USUARIO DE LA RETENCION
            query.prepare("INSERT INTO personasxdocumento(iddocumento,idpersona) VALUES(:iddocumento,:idusuario)")
            query.bindValue( ":iddocumento", idret )
            query.bindValue( ":idusuario", self.uid)
            if not query.exec_():
                raise UserWarning( "No se pudo regitrar el usuario que creo la retencion" )
            
            query.prepare("INSERT INTO personasxdocumento(iddocumento,idpersona) VALUES(:iddocumento,:idproveedor)")
            query.bindValue( ":iddocumento", idret )
            query.bindValue( ":idproveedor", self.proveedorId)
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
            query.bindValue( ":iddocumento", insertedId )
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
            self.status = True
            #QMessageBox.warning(self, "Llantera Esquipulas", str(inst))
            print   inst
            self.status = True
            QSqlDatabase.database().rollback()
            return False
            
    
    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled
        elif index.row() != 0:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable
        else:
            return Qt.ItemIsEnabled