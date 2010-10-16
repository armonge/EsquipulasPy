# -*- coding: utf-8 -*-
'''
Created on 21/05/2010

@author: Andrés Reyes Monge
'''

import logging
from decimal import Decimal, InvalidOperation

from PyQt4.QtSql import QSqlQuery

from utility.docbase import LineaBase
from utility.decorators import ifValid

class LineaLiquidacion( LineaBase ):
    def __init__( self, parent ):

        self.parent = parent
        """
        @type: LiquidacionModel
        @ivar: El documento al que pertenece esta linea 
        """
        self.itemId = 0
        """
        @type:int
        @ivar: El id del articulo en esta linea
        """
        self.itemDescription = ""
        u"""
        @type: string
        @ivar: La descripción del articulo
        """

        self.quantity = 0
        """
        @type: int
        @ivar: La cantidad de unidades del articulo en esta linea
        """
        self.itemCost = Decimal( 0 )
        """
        @type:Decimal
        @ivar: El costo de compra del articulo 
        """

        self.comisionValue = Decimal( 0 )
        """
        @ivar:El valor de comisión para el articulo
        @type:Decimal 
        """
        self.__rateISC = Decimal( 0 )
        """
        @type: Decimal
        @ivar: El porcentaje ISC del articulo
        """

        self.__rateDAI = Decimal( 0 )
        """
        @type: Decimal
        @ivar: El porcentaje DAI del articulo
        """

    def setRateDAI( self, dai ):
        self.__rateDAI = dai

    def getRateDAI( self ):
        return self.__rateDAI if self.parent.applyTaxes else Decimal( 0 )

    rateDAI = property( getRateDAI, setRateDAI )

    def setRateISC( self, isc ):
        self.__rateISC = isc

    def getRateISC( self ):
        return self.__rateISC if self.parent.applyTaxes else Decimal( 0 )

    rateISC = property( getRateISC, setRateISC )

    @property
    def valid( self ):
        """
        Una linea es valida cuando self.quantity > 0 and self.itemCost > 0 and self.itemId != 0 
        @rtype: bool
        """
        return self.quantity > 0 and self.itemCost > 0 and self.itemId != 0 and self.parent.exchangeRateId > 0

    @property
    @ifValid
    def fobParcial( self ):
        """
        El FOB de este articulo
        
        M{FOBPARCIAL = CANTIDAD * COSTOCOMPRA }
        @rtype: Decimal
        """
        return self.quantity * self.itemCost

    @property
    def cifParcial( self ):
        """
        El CIF de un articulo
        
        M{CIFPARCIAL = ( CIFTOTAL / FOBTOTAL ) * FOBPARCIAL}
        @rtype: Decimal
        """
        try:
            return ( self.parent.cifTotal / self.parent.fobTotal ) * self.fobParcial
        except ZeroDivisionError:
            return Decimal( 0 )
        except InvalidOperation:
            return Decimal( 0 )
    @property
    def daiParcial( self ):
        """
        El DAI parcial de un articulo
        
        M{DAIPARCIAL = CIFPARCIAL * PORCENTAJEDAI} 
        @rtype: Decimal
        """
        return self.cifParcial * ( self.rateDAI / 100 )

    @property
    def iscParcial( self ):
        """
        El ISC Parcial
        
        M{ISCPARCIAL = DAIPARCIAL + CIFPARCIAL * PORCENTAJEISC}
        @rtype: Decimal
        """
        return ( self.daiParcial + self.cifParcial ) * ( Decimal( self.rateISC ) / 100 )

    @property
    def tsimParcial( self ):
        """
        EL TSIM parcial de un articulo
        
        M{TSIMPARCIAL = ( TSIMTOTAL / CIFTOTAL ) * CIFPARCIAL} 
        @rtype: Decimal
        """
        try:
            return ( self.parent.tsimTotal / self.parent.cifTotal ) * self.cifParcial
        except ZeroDivisionError:
            return Decimal( 0 )
        except InvalidOperation:
            return Decimal( 0 )

    @property
    def isoParcial( self ):
        """
        El ISO parcial de un articulo
        
        M{ISOPARCIAL = CIFPARCIAL / PORCENTAJEISO} 
        @rtype: Decimal
	    """
        return self.cifParcial * ( Decimal( self.parent.isoRate ) / 100 )

    @property
    def speParcial( self ):
        """
        El SPE Parcial de un articulo
        
        M{SPEPARCIAL = ( SPETOTAL / CIFTOTAL ) * CIFPARCIAL}
        @rtype: Decimal 
        """
        try:
            return ( self.parent.speTotal / self.parent.cifTotal ) * self.cifParcial
        except ZeroDivisionError:
            return Decimal( 0 )
        except InvalidOperation:
            return Decimal( 0 )

    @property
    def ivaParcial( self ):
        """
        El IVA Parcial de un articulo
        
        M{IVAPARCIAL = ( CIFPARCIAL + DAIPARCIAL + ISCPARCIAL + TSIMPARCIAL ) *  PORCENTAJEIVA}
        @rtype: Decimal
        """
        return ( self.cifParcial + self.daiParcial + self.iscParcial + self.tsimParcial ) * ( self.parent.ivaRate / Decimal( 100 ) )

    @property
    def fleteParcial( self ):
        """ 
        El FLETE Parcial de un articulo
        
        M{FLETEPARCIAL = ( FLETETOTAL / FOBTOTAL ) * FOBPARCIAL }
        @rtype: Decimal
        """
        try:
            return ( self.parent.freightTotal / self.parent.fobTotal ) * self.fobParcial
        except ZeroDivisionError:
            return Decimal( 0 )
        except InvalidOperation:
            return Decimal( 0 )

    @property
    def seguroParcial( self ):
        """
        El seguro parcial de un articulo
        
        M{SEGUROPARCIAL = ( SEGUROTOTAL / FOBTOTAL ) * FOBPARCIAL}
        @rtype: Decimal
        """
        try:
            return ( self.parent.insuranceTotal / self.parent.fobTotal ) * self.fobParcial
        except ZeroDivisionError:
            return Decimal( 0 )
        except InvalidOperation:
            return Decimal( 0 )

    @property
    def impuestosParcial( self ):
        """
        Impuestos parcial
        
        M{IMPUESTOSPARCIAL= DAIPARCIAL + ISCPARCIAL + IVAPARCIAL + TSIMPARCIAL + SPEPARCIAL + ISOPARCIAL}
        @rtype: Decimal
        """
        return self.daiParcial + self.iscParcial + self.ivaParcial + self.tsimParcial + self.speParcial + self.isoParcial

    @property
    def comisionParcial( self ):
        """
        La comisión parcial
        
        M{COMISIONPARCIAL =  VALORCOMISION * CANTIDAD }
        @rtype: Decimal
        """
        return self.comisionValue * self.quantity

    @property
    def agenciaParcial( self ):
        """
        El total de agencia prorrateado
        
        M{AGENCIAPARCIAL =  ( AGENCIATOTAL / CIFTOTAL ) / CIFPARCIAL }
        @rtype: Decimal
        """
        try:
            return ( self.parent.agencyTotal / self.parent.cifTotal ) * self.cifParcial
        except ZeroDivisionError:
            return Decimal( 0 )
        except InvalidOperation:
            return Decimal( 0 )

    @property
    def almacenParcial( self ):
        """
        El total de almacen prorrateado
        
        M{ ALMACENPARCIAL = ( ALMACENTOTAL / CIFTOTAL ) * CIFPARCIAL}
        @rtype: Decimal
        """
        try:
            return ( self.parent.storeTotal / self.parent.cifTotal ) * self.cifParcial
        except ZeroDivisionError:
            return Decimal( 0 )
        except InvalidOperation:
            return Decimal( 0 )

    @property
    def papeleriaParcial( self ):
        """
        El total de papeleria prorrateado
        
        M{PAPELERIAPARCIAL =   PORCENTAJEPAPELERIA * CANTIDAD }
        @rtype: Decimal
        """
        return ( self.parent.paperworkRate / 100 ) * self.quantity

    @property
    def transporteParcial( self ):
        """
        El transporte prorrateado
        
        M{TRANSPORTEPARCIAL =  PORCENTAJETRANSPORTE * CANTIDAD}
        @rtype: Decimal
        """
        return ( self.parent.transportRate / 100 ) * self.quantity

    @property
    def costoCordobaT( self ):
        """
        El costo total en cordobas de esta linea
        
        M{COSTOTOTALCORDOBA =  COSTODOLAR * TIPOCAMBIO}
        @rtype: Decimal
        """
        return self.costoDolarT * self.parent.exchangeRate

    @property
    def costoCordoba( self ):
        """
        El costo unitario en cordobas
        
        M{COSTOCORDOBA =  COSTOTOTALCORDOBA / CANTIDAD }
        @rtype: Decimal
        """
        try:
            return self.costoCordobaT / self.quantity
        except ZeroDivisionError:
            return Decimal( 0 )
        except InvalidOperation:
            return Decimal( 0 )

    @property
    def costoDolarT( self ):
        """
        El Costo total en dolares
        
        M{COSTOTOTALDOLAR =  CIFPARCIAL + COMISIONPARCIAL + AGENCIAPARCIAL + ALMACENPARCIAL + PAPELERIAPARCIAL + TRANSPORTEPARCIAL + IMPUESTOSPARCIAL}
        @rtype: Decimal
        """
        return self.cifParcial + self.comisionParcial + self.agenciaParcial + self.almacenParcial + self.papeleriaParcial + self.transporteParcial + self.impuestosParcial

    @property
    def costoDolar( self ):
        """
        El costo unitario en dolares
        
        M{COSTODOLAR =  COSTOTOTALDOLARES / CANTIDAD }
        @rtype: Decimal
        """
        try:
            return self.costoDolarT / self.quantity
        except ZeroDivisionError:
            return Decimal( 0 )
        except InvalidOperation:
            return Decimal( 0 )

    @property
    def otrosParcial( self ):
        """
        El total prorrateado de otros gastos
        
        M{OTROSGASTOSPARCIAL = ( OTROSGASTOSTOTAL / FOBTOTAL ) * FOBPARCIAL}
        @rtype: Decimal
        """
        try:
            return ( self.parent.otherTotal / self.parent.fobTotal ) * self.fobParcial
        except ZeroDivisionError:
            return Decimal( 0 )
        except InvalidOperation:
            return Decimal( 0 )

    def update( self, query ):
        """
        Actualizar los porcentajes de DAI, ISC y COMISION
        @param query: La query en la que se ejecuta todo el proceso de actualización
        @type query: QSqlQuery
        """
        qDESCRIPTION, qDAI, qISC, qCOMISION = range( 4 )
        q = """
        SELECT
            Descripcion AS 'Articulo',
            dai,
            isc,
            Comision as comision
        FROM vw_articulosconcostosactuales
        WHERE idarticulo = %d
        LIMIT 1
        """ % self.itemId
        if not query.exec_( q ):
            raise Exception( u"No se ejecutar la consulta para actualizar los valores del articulo %s " % self.itemDescription )
        if not query.size() == 1:
            raise Exception( u"No se pudieron obtener los valores para el articulo %s " % self.itemDescription )

        query.first()
        self.itemDescription = query.value( qDESCRIPTION ).toString()
        self.__rateDAI = Decimal( query.value( qDAI ).toString() )
        self.__rateISC = Decimal( query.value( qISC ).toString() )
        self.comisionValue = Decimal( query.value( qCOMISION ).toString() )




    def save( self, iddocumento, nlinea ):
        """
        Este metodo guarda la linea en la base de datos
        
        @param iddocumento: El id del documento al que esta enlazada la LineAddrTable
        @type iddocumento: int

        @param nlinea: El numero de la linea en el documento
        @type nlinea: int
        """
        if not self.valid:
            raise Exception ( "Se intento guardar una linea no valida" )

        query = QSqlQuery()
        if not query.prepare( """
        INSERT INTO articulosxdocumento (iddocumento, idarticulo, unidades, costounit, costocompra,nlinea)
        VALUES( :iddocumento,:idarticulo,  :unidades, :costounit, :costocompra,:linea)
        """ ):
            raise Exception( "No se pudo preparar la consulta para insertar una de las lineas del documento" )

        query.bindValue( ":iddocumento", iddocumento )
        query.bindValue( ":idarticulo", self.itemId )
        query.bindValue( ":unidades", self.quantity )
        query.bindValue( ":costounit", str(self.costoDolar))
        query.bindValue( ":costocompra", str(self.itemCost) )
        query.bindValue( ":linea", nlinea )


        if not query.exec_():
            logging.critical( query.lastError().text() )
            raise Exception( "Error al insertar una de las lineas del documento" )

        idarticuloxdocumento = query.lastInsertId()

        if not query.prepare( """
        INSERT INTO costosxarticuloliquidacion ( idarticuloxdocumento, dai, isc, comision ) 
        VALUES (:idarticuloxdocumento, :dai, :isc, :comision)
        """ ):
            raise Exception( "Error al preparar la consulta para insertar una de las lineas del documento" )

        query.bindValue( ":idarticuloxdocumento", idarticuloxdocumento )
        query.bindValue( ":dai", str(self.daiParcial) )
        query.bindValue( ":isc", str(self.iscParcial) )
        query.bindValue( ":comision", str(self.comisionParcial) )

        if not query.exec_():
            logging.error( query.lastError().text() )
            raise Exception( "Error al insertar los costos de una de las lineas de la factura " )
