'''
Created on 18/05/2010

@author: Luis Carlos Mejia Garcia
'''
from decimal import Decimal
from PyQt4.QtSql import QSqlQuery
class LineaRecibo:
    def __init__( self, parent ):
        self.pagoId = 0
        self.monedaId = 0
        self.pagoDescripcion = ""
        self.nref = ""
        self.montoDolar = Decimal( 0 )
        self.monto = Decimal(0)
        self.simboloMoneda =""
#        self.tasa = Decimal( 0 )


    @property
    def valid( self ):
        """
        es esta linea valida
        """
        if  int( self.pagoId ) != 0   and Decimal( self.montoDolar ) > 0:
            if self.pagoId > 1 and self.nref == "":
                return False
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
        INSERT INTO pagos (recibo, tipopago, tipomoneda, monto,refexterna ) 
        VALUES( :iddocumento, :idpago, :idmoneda, :monto,:ref )
        """ ):
            raise Exception( "no esta preparada" )

        query.bindValue( ":iddocumento", iddocumento )
        query.bindValue( ":idpago", self.pagoId )
        query.bindValue( ":idmoneda", self.monedaId )

        query.bindValue( ":monto", self.montoDolar.to_eng_string() )
        query.bindValue( ":ref", self.nref )

        if not query.exec_():
            print( query.lastError().text() )
            raise Exception( "line" + str( self.itemId ) )



