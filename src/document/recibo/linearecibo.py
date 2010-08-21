'''
Created on 18/05/2010

@author: Luis Carlos Mejia Garcia
'''
from decimal import Decimal
from PyQt4.QtSql import QSqlQuery
from utility import constantes
class LineaRecibo:
    def __init__( self, parent ):
        self.pagoId = 0
        self.bancoId = 0
        self.monedaId = 0
        self.pagoDescripcion = ""
        self.referencia = ""
        self.montoDolar = Decimal( 0 )
        self.monto = Decimal(0)
        self.simboloMoneda ="US$"
        
#        self.tasa = Decimal( 0 )


    @property
    def valid( self ):
        """
        es esta linea valida
        """
        if  int( self.pagoId ) != 0   and Decimal( self.montoDolar ) > 0:
            if self.pagoId > 1 and self.referencia == "":
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

        idbanco = 'null' if self.pagoId in (constantes.IDPAGOEFECTIVO,constantes.IDPAGOTARJETA) else str(self.bancoId)
        query = QSqlQuery()
        if not query.prepare("INSERT INTO movimientoscaja(iddocumento, idtipomovimiento, idtipomoneda, monto,refexterna,idbanco,nlinea )" +  
        "VALUES( :iddocumento, :idpago, :idmoneda, :monto,:ref," + idbanco +",:linea )"):
            raise Exception( "la linea #%d de los pagos no esta preparada"%linea )

        query.bindValue( ":iddocumento", iddocumento )
        query.bindValue( ":idpago", self.pagoId )
        query.bindValue( ":idmoneda", self.monedaId )
        query.bindValue( ":monto", self.monto.to_eng_string() )
        query.bindValue( ":ref", self.referencia )
        query.bindValue( ":linea", linea )

        if not query.exec_():
            print( query.lastError().text() )
            raise Exception( "No se pudo insertar la linea " + str( linea ) )



