'''
Created on 18/05/2010

@author: Luis Carlos Mejia Garcia

'''
from decimal import Decimal
from PyQt4.QtSql import QSqlQuery
#FIXME: para que sirve parent???? creo que esto se da por copiar y pegar....
class LineaAbono( object ):
    def __init__( self, parent ):
        self.idFac = 0
        self.nFac = ""
        self.__monto = Decimal( 0 )
        self.totalFac = Decimal( 0 )
        self.saldo = Decimal( 0 )
        self.tasaIva = Decimal( 0 )
        self.subMonto = Decimal( 0 )

    def __setMonto( self, monto ):
        self.__monto = monto
        if self.tasaIva == 0:
            self.subMonto = monto
        else:
            self.subMonto = Decimal( str( round( monto / ( 1 + self.tasaIva / 100 ), 4 ) ) )
    def __getMonto( self ):
        return self.__monto
    monto = property( __getMonto, __setMonto )


    @property
    def valid( self ):
        """
        es esta linea valida
        """
        if  Decimal( self.__monto ) > 0:
            return True
        return False

    def save( self, iddocumento, linea ):
        """
        Este metodo guarda la linea en la base de datos
        @param iddocumento: el id del documento al que esta enlazada la linea
        """
        if not self.valid or self.idFac == 0:
            raise Exception( "Se intento guardar una linea no valida" )

        query = QSqlQuery()
        if not query.prepare( 
        """
        INSERT INTO docpadrehijos(idpadre,idhijo,monto,nlinea) 
        VALUES (:idfac,:iddocumento, :monto,:linea) 
        """ ):
            raise Exception( "La linea # %d del abono no pudo ser preparada" % linea )

        query.bindValue( ":idfac", self.idFac )
        query.bindValue( ":iddocumento", iddocumento )
        query.bindValue( ":monto", self.monto.to_eng_string() )
        query.bindValue( ":linea", linea )

        if not query.exec_():
            print( query.lastError().text() )
            raise Exception( "no se pudo insertar la linea" + str( linea ) )



