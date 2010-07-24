'''
Created on 18/05/2010

@author: armonge
'''
from decimal import Decimal
from PyQt4.QtSql import QSqlQuery
class LineaFactura:
    def __init__( self, parent ):
        self.quantity = 0
        self.itemDescription = ""
        self.price = Decimal( 0 )
        self.costodolar =  Decimal( 0 )
        self.itemId = 0
        self.parent = parent
        self.costo = 0
        self.sugerido = Decimal( 0 )
        self.existencia = 0
        self.idbodega = 0



    def getPrice( self ):
        """
        el precio unitario del producto en esta linea
        """
        return self.price
    def setPrice( self, price ):
        self.price = Decimal( price )

    itemPrice = property( getPrice, setPrice )

    @property
    def total( self ):
        """
        el total de esta linea
        """
        return Decimal( self.quantity * self.itemPrice ) if self.valid else Decimal( 0 )

    @property
    def costototal( self ):
        """
        el costo total de esta linea
        """
        return Decimal( self.quantity * self.costo ) if self.valid else Decimal( 0 )


    @property
    def valid( self ):
        """
        es esta linea valida
        """
        if  int( self.itemId ) != 0   and Decimal( self.itemPrice ) > 0 and int( self.quantity ) > 0 :
            return True
        return False

    def save( self, iddocumento, linea ):
        """
        Este metodo guarda la linea en la base de datos
        @param iddocumento: el id del documento al que esta enlazada la linea
        """
        if not self.valid:
            raise Exception( "Se intento guardar una linea no valida" )

        query = QSqlQuery()
        if not query.prepare( 
        """
        INSERT INTO articulosxdocumento (iddocumento, idarticulo, unidades,costounit, precioventa,nlinea ) 
        VALUES( :iddocumento, :idarticulo, :unidades,:costo, :precio,:linea )
        """ ):
            raise Exception( "no esta preparada" )

        query.bindValue( ":iddocumento", iddocumento )
        query.bindValue( ":idarticulo", self.itemId )
        query.bindValue( ":unidades", self.quantity * -1 )
        query.bindValue( ":costo", self.costodolar.to_eng_string() )
        query.bindValue( ":precio", self.itemPrice.to_eng_string() )
        query.bindValue( ":linea", linea )


        if not query.exec_():
            print( query.lastError().text() )
            raise Exception( "line" + str( self.itemId ) )



