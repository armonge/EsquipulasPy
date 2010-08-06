'''
Created on 18/05/2010

@author: Luis Carlos Mejia Garcia

'''
from decimal import Decimal
from PyQt4.QtSql import QSqlQuery
class LineaAbono:
    def __init__(self, parent):    
        self.idFac=0
        self.nFac=""
        self.monto= Decimal(0)
        self.totalFac=0
        self.saldo=Decimal(0)
        
    
    def getPrice(self):    
        """
        el precio unitario del producto en esta linea
        """
        return self.price
    def setPrice(self,  price):
        self.price = Decimal(price)
        
    itemPrice = property(getPrice,  setPrice)
    
#    @property
#    def total(self):
#        """
#        el total de esta linea
#        """
#        return Decimal(self.quantity * self.itemPrice ) if self.valid else Decimal(0) 
    
    @property
    def valid(self):
        """
        es esta linea valida
        """
        if  Decimal(self.monto) > 0:
            return True
        return False
       
    def save(self,  iddocumento, linea):
        """
        Este metodo guarda la linea en la base de datos
        @param iddocumento el id del documento al que esta enlazada la linea
        """
        if not self.valid:
            raise Exception("Se intento guardar una linea no valida")
        
        query = QSqlQuery()
        if not query.prepare(
        """
        INSERT INTO docpadrehijos(idpadre,idhijo,monto,nlinea) 
        VALUES (:idfac,:iddocumento, :monto,:linea) 
        """):
            raise Exception("no esta preparada")
        
        query.bindValue(":idfac",  self.idFac)
        query.bindValue(":iddocumento",  iddocumento)
        query.bindValue(":monto",  self.monto.to_eng_string())
        query.bindValue( ":linea", linea )

        if not query.exec_():
            print(query.lastError().text())
            raise Exception("line" + str(linea))
            
            

