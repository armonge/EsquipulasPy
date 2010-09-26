# -*- coding: utf-8 -*-
'''
Created on 18/05/2010

@author: Luis Carlos Mejia Garcia
'''
from decimal import  Decimal
from utility import constantes
from utility.movimientos import redondear

class PagoModel( object ):
    def __init__( self ,datosSesion):
        object.__init__(self)
        
        self.__documentType = constantes.IDPAGO
        
        
        self.docImpreso = ""
        self.observaciones = ""
        self.totalC =Decimal(0)
        self.totalD =Decimal(0) 
        self.datosSesion = datosSesion
        self.conceptoId = 0
        self.beneficiarioId = 0
        
        self.aplicarRet = False
        self.retencionId = 0
        self.ivaId = 0
        
        self.__retencionTasa = Decimal(0)
        self.__ivaTasa = Decimal(0)
        self.aplicarIva = True
        self.errorMessage = ""
    
    def getIvaTasa(self):
        return self.__ivaTasa if self.aplicarIva else Decimal(0)
    
    def setIvaTasa(self,value):
        self.__ivaTasa = value
     

    def getRetencionTasa(self):
        print "tasa ret"
        print  self.__retencionTasa
        print "aplicar ret" 
        print self.aplicarRet 
        return self.__retencionTasa if self.aplicarRet else Decimal(0)
    
    def setRetencionTasa(self,value):
        self.__retencionTasa = value
        
    ivaTasa = property(getIvaTasa,setIvaTasa)
    retencionTasa = property(getRetencionTasa,setRetencionTasa)
    
    def save(self):
        query = QSqlQuery()

        try:

            if not QSqlDatabase.database().transaction():
                raise Exception( u"No se pudo comenzar la transacción" )

            if not query.prepare( """
            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,observacion,total,escontado,idtipocambio,idcaja,idestado) 
            VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:observacion,:total,:escontado,:idtc,:caja,:estado)
            """ ):
                raise Exception( "No se pudo guardar el documento" )
            query.bindValue( ":ndocimpreso", self.docImpreso )
            query.bindValue( ":fechacreacion", self.datosSesion.fecha.toString( 'yyyyMMdd' ) + QDateTime.currentDateTime().toString("hhmmss") )
            query.bindValue( ":idtipodoc", self.__documentType )
            query.bindValue( ":observacion", self.observaciones )
            total = self.total
            query.bindValue( ":total", total.to_eng_string() )
            query.bindValue( ":escontado", self.escontado )
            query.bindValue( ":idtc", self.datosSesion.tipoCambioId )
            query.bindValue( ":caja", self.datosSesion.cajaId)
            query.bindValue( ":estado",  constantes.INCOMPLETO)

            if not query.exec_():
                raise Exception( "No se pudo insertar el documento" )

            
            insertedId = query.lastInsertId().toString()
    
#INSERTAR LA RELACION CON LA SESION DE CAJA            
            query.prepare( """
                INSERT INTO docpadrehijos (idpadre,idhijo)
                VALUES (:idsesion,:idpago)
                """ )

            query.bindValue( ":idsesion", self.datosSesion.sesionId )
            query.bindValue( ":idpago", insertedId )

            if not query.exec_():
                raise Exception( "No se Inserto la relacion entre la sesion de caja y el pago" )

#INSERTAR LA RELACION CON El USUARIO , EL CLIENTE Y EL PROVEEDOR            
            query.prepare( 
                "INSERT INTO personasxdocumento (iddocumento,idpersona,idaccion) VALUES" +  
                "(" + insertedId + ",:iduser,:autor),"
                "(" + insertedId + ",:idbeneficiario,:beneficiario)"
                )

            query.bindValue( ":iduser", self.datosSesion.usuarioId )
            query.bindValue( ":autor", constantes.AUTOR)
            query.bindValue( ":idbeneficiario", self.beneficiarioId )
            query.bindValue( ":beneficiario", constantes.PROVEEDOR)
            

            if not query.exec_():
                raise Exception( "No se Inserto la relacion entre el documento y las personas" )


#VERIFICO SI el id del iva es cero. NO SERA CERO CUANDO LA BODEGA=1 PORQUE ESTA NO ES exonerada                                 
            if self.aplicarIva:
                query.prepare( """
                INSERT INTO costosxdocumento (iddocumento, idcostoagregado) VALUES( :iddocumento, :idcostoagregado )
                """ )
                query.bindValue( ":iddocumento", insertedId )
                query.bindValue( ":idcostoagregado", self.ivaId )
                
                if not query.exec_():
                    print insertedId
                    print self.ivaId
                    raise Exception( "El iva NO SE INSERTO" )

            if self.aplicarRet:
                query.prepare( """
                INSERT INTO costosxdocumento (iddocumento, idcostoagregado) VALUES( :iddocumento, :idcostoagregado )
                """ )
                query.bindValue( ":iddocumento", insertedId )
                query.bindValue( ":idcostoagregado", self.retencionId )
                
                if not query.exec_():
                    print insertedId
                    print self.retencionId
                    raise Exception( "La retencion NO SE INSERTO" )

            if not QSqlDatabase.database().commit():
                raise Exception( "No se pudo guardar el pago" )
            
        except Exception as inst:
            print  query.lastError().databaseText()
            print query.lastError().driverText()
            print inst.args
            QSqlDatabase.database().rollback()
            return False

        return True

    
    @property
    def valid(self):
        if self.docImpreso == "":
            raise Exception("El documento no tiene el numero impreso")
        else:
            return True
        
        return False
    
    @property
    def totalDolar( self ):
        total = self.totalD + redondear(self.totalC / self.datosSesion.tipoCambioBanco)
        return total if total != 0 else Decimal( 0 )     

    @property
    def totalCordoba( self ):
        total = self.totalC + redondear(self.totalD * self.datosSesion.tipoCambioBanco)
        return total if total != 0 else Decimal( 0 )
    
    @property
    def subTotalDolar(self):
        sub = redondear(self.totalDolar / (1 + (self.ivaTasa/100)))
        return sub if sub != 0 else Decimal(0)

    @property
    def subTotalCordoba(self):
        sub = redondear(self.totalCordoba / (1 + (self.ivaTasa/100)))
        return sub if sub != 0 else Decimal(0)

    @property
    def tieneRetencion(self):
        sub = self.subTotalCordoba
        return sub>1000 
        
    @property
    def retencionDolar(self):
        rt = self.retencionTasa
        if rt >0 :
            ret = self.totalDolar / ( (100 + self.ivaTasa)/rt)
            return ret if ret != 0 else Decimal(0)
        else:
            return Decimal(0)
        
    