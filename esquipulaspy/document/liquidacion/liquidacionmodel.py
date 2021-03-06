#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       
#       Copyright 2010 Andrés Reyes Monge <armonge@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
'''
Created on 21/05/2010

@author: Andrés Reyes Monge
'''


from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt4.QtSql import QSqlQuery, QSqlDatabase
from decimal import Decimal, ROUND_CEILING, InvalidOperation
from document.liquidacion.linealiquidacion import LineaLiquidacion
from utility import constantes
from utility.accountselector import AccountsSelectorModel
from utility.docbase import DocumentBase
from utility.moneyfmt import moneyfmt
import logging
from utility.decorators import return_decimal





IDARTICULO, ARTICULO, CANTIDAD, COSTOUNIT, FOB, FLETE, SEGURO, OTROS, CIF, IMPUESTOS, COMISION, AGENCIA, ALMACEN, PAPELERIA, TRANSPORTE, TCOSTOD, COSTOD, TCOSTOC, COSTOC = range( 19 )
class LiquidacionModel( DocumentBase ):
    """
    Este modelo es el que se utiliza para realizar todos los calculos relacionados a una liquidacion,
    de costos
    """
    __documentType = constantes.IDLIQUIDACION
    """
    @cvar:EL id del tipo de documento
    @type:int
    """

    def __init__( self, uid ):
        """
        @param uid: El id del usuario que ha creado este documento
        """
        super( LiquidacionModel, self ).__init__()
        self.__lines = []
        """
        @ivar:La lista de lineas en el documento
        @type:LineaLiquidacion[]
        """
        self.uid = uid
        """
        @ivar:El id del usuario
        @type:int
        """


        self.providerId = 0
        """
        @ivar:El id del proveedor
        @type:int
        """
        self.warehouseId = 0
        """
        @ivar:El id de la bodega
        @type:int
        """

        self.exchangeRateId = 0
        u"""
        @ivar:El id del tipo de cambio utilizado en la liquidación
        @type:int
        """
        self.exchangeRate = Decimal( 0 )
        u"""
        @ivar:El tipo de cambio utilizado en la liquidación
        @type:Decimal
        """



        self.origin = ""
        u"""
        @ivar:El país de origen de la liquidación
        @type:string
        """




        self.agencyTotalC = Decimal( 0 )
        u"""
        @ivar:El total en cordobas de agencia en la liquidación
        @type:Decimal
        """
        self.storeTotalC = Decimal( 0 )
        u"""
        @ivar:El total en cordobas de almacén en la liquidación
        @type:Decimal
        """


        self.weight = Decimal( 0 )
        u"""
        @ivar:El peso total usado en la liquidación
        @type:Decimal
        """
        self.weightFactor = 0
        u"""
        @ivar:El factor peso usado en la liquidación
        @type:int
        """

        self.freightTotal = Decimal( 0 )
        u"""
        @ivar:El total de flete en la liquidación
        @type:Decimal
        """
        self.insuranceTotal = Decimal( 0 )
        u"""
        @ivar:El total de seguro en la liquidación
        @type:Decimal
        """
        self.otherTotal = Decimal( 0 )
        u"""
        @ivar:El total de otros gastos en la liquidación
        @type:Decimal
        """

        self.speId = 0
        """
        @ivar:El id del SPE usado en la liquidación
        @type:int
        """
        self.speTotal = 0
        u"""
        @ivar:El SPE usado en la liquidación
        @type:int
        """


        self.tsimId = 0
        u"""
        @ivar:El id del TSIM usado en la liquidación
        @type:int
        """
        self.tsimRate = Decimal( 0 )
        """
        @ivar:El TSIM usado en la liquidación
        @type:Decimal
        """

        self.ivaId = 0
        u"""
        @ivar:El id del IVA usado en la liquidación
        @type:int
        """
        self.__iva_rate = Decimal( 0 )
        """
        @ivar:El IVA usado en la liquidación cuando self.applyIVA = True
        @type:Decimal
        """
        self.__apply_iva = True
        """
        @ivar:Si a esta liquidación se le aplica IVA o no
        @type:bool
        """

        self.isoId = 0
        u"""
        @ivar:El id del ISO usado en la liquidación
        @type:int
        """
        self.__iso_rate = Decimal( 0 )
        """
        @ivar:El ISO usado en la liquidación cuando self.applyISO = True
        @type:Decimal
        """
        self.applyISO = True
        """
        @ivar:Si a esta liquidación se le aplica ISO o no
        @type:bool
        """
        self.applyTaxes = True
        """
        @ivar: Si a esta liquidación se le aplican Impuestos o no
        @type:bool
        """

        self.paperworkRate = Decimal( 0 )
        """
        @ivar:El porcentaje de papeleria de esta liquidación
        @type:Decimal
        """
        self.transportRate = Decimal( 0 )
        """
        @ivar:El porcentaje de transporte de esta liquidación
        @type:Decimal
        """
        self.fobTotal = Decimal( 0 )
        """
        @ivar: El FOB total de esta liquidación
        @type:Decimal
        """



        self.totalsModel = LiquidacionTotalsModel( self )
        """
        @ivar:El modelo con los totales
        @type:LiquidacionTotalsModel
        """


    @property
    def lines( self ):
        return self.__lines


    @property
    def agencyTotal( self ):
        return self.agencyTotalC / self.exchangeRate

    @property
    def storeTotal( self ):
        return self.storeTotalC / self.exchangeRate


    def _set_iva_rate( self, ivarate ):
        self.__iva_rate = ivarate
    def _get_iva_rate( self ):
        """
        El porcentaje IVA usado en esta liquidacion
        @rtype: Decimal
        """
        return self.__iva_rate if self.applyIVA  else Decimal( 0 )
    ivaRate = property( _get_iva_rate, _set_iva_rate )

    @property
    def applyIVA( self ):
        """
        Si se deberia o no aplicar iva en esta liquidación
        @rtype: bool
        """
        return self.warehouseId == 1 and self.applyTaxes

    @property
    def valid( self ):
        """
        Una liquidación es valida cuando:
        =================================
            self.printedDocumentNumber != ""

            self.providerId > 0

            self.warehouseId > 0

            self.exchangeRateId > 0

            self.validLines > 0

            self.origin != ""

            self.tsimId   > 0

        @rtype: bool
        """
        try:
            if not self.printedDocumentNumber.strip() != "":
                raise UserWarning( "No ha introducido un numero de Poliza" )
            elif not int( self.providerId ) > 0:
                raise UserWarning( "No ha seleccionado un proveedor" )
            elif not  int( self.warehouseId ) > 0:
                raise UserWarning( "No ha seleccionado una bodega" )
            elif not int( self.exchangeRateId ) > 0:
                raise UserWarning( "No existe un tipo de cambio "
                                      + "para esta fecha" )
            elif not  int( self.validLines ) > 0:
                raise UserWarning( u"No existe ninguna linea valida en "
                                      + u"la liquidación" )
            elif not self.origin.strip() != "":
                raise UserWarning( "No ha escrito la procedencia" )
            elif not int( self.tsimId ) > 0:
                raise UserWarning( "No existe un valor TSIM" )
            elif not int( self.speId ) > 0:
                raise UserWarning( "No existe un valor SPE" )
        except UserWarning as inst:
            self._valid_error = unicode( inst )
            return False
        return True


    def _get_iso_rate( self ):
        """
        El porcentaje ISO usado en esta liquidacion
        @rtype: Decimal
        """
        return self.__iso_rate if self.applyISO and self.applyTaxes else Decimal( 0 )
    def _set_iso_rate( self, iso ):
        self.__iso_rate = iso
    isoRate = property( _get_iso_rate, _set_iso_rate )


    def updateFob( self ):
        """
        Esta función se ejecuta cuando se cambia el costo o
         la cantidad de un articulo
        """
        fob = sum( [linea.fobParcial for linea in self.__lines if linea.valid ] )
        self.fobTotal = fob if fob > 0 else Decimal( 0 )

    @property
    def fobTotalC( self ):
        """
        EL FOB total del documento en cordobas
        """
        return self.fobTotal * self.exchangeRate

    @property
    def cifTotalC( self ):
        """
        El CIF total del documento en cordobas
        """
        return self.cifTotal * self.exchangeRate

    @property
    def cifTotal( self ):
        """
        El CIF total del documento

        M{CIFTOTAL = FOBTOTAL + FLETETOTAL + SEGUROTOTAL + OTROSGASTOSTOTAL }
        @rtype: Decimal
        """
        return self.fobTotal + self.freightTotal + self.insuranceTotal + self.otherTotal

    @property
    @return_decimal
    def iscTotal( self ):
        """
        El ISC total del documento

        M{ISCTOTAL = S{sum}ISCPARCIAL}
        @rtype: Decimal
        """
        return sum( [ linea.iscParcial for linea in self.__lines if linea.valid ] )

    @property
    def isoTotal( self ):
        """
        El ISO Total del documento

        M{ISOTOTAL = CIFTOTAL * PORCENTAJEISO}
        @rtype: Decimal
        """
        return self.cifTotal * ( self.isoRate / Decimal( 100 ) )

    @property
    def taxesTotal( self ):
        """
        El total de impuestos del documento

        M{IMPUESTOSTOTAL = DAITOTAL + ISCTOTAL + IVATOTAL + TSIMTOTAL + SPETOTAL + ISOTOTAL}
        @rtype: Decimal
        """
        return self.daiTotal + self.iscTotal + self.ivaTotal + \
            self.tsimTotal + self.speTotal + self.isoTotal

    @property
    def taxesTotalC( self ):
        """
        El total en cordobas de los impuestos del documento
        """
        return self.taxesTotal * self.exchangeRate

    @property
    def ivaTotal( self ):
        """
        El iva total del documento

        M{IVATOTAL = TOTALDOLARES * PORCENTAJEIVA}
        @rtype: Decimal
        """
        return ( self.daiTotal + self.iscTotal + self.cifTotal + self.tsimTotal ) * ( self.ivaRate / 100 ) if self.applyIVA else Decimal( 0 )

    @property
    @return_decimal
    def daiTotal( self ):
        """
        La sumatoria de los dai parcial

        M{DAITOTAL = S{sum}DAIPARCIAL }
        @rtype: Decimal
        """
        return sum( [ line.daiParcial for line in self.__lines if line.valid] )

    @property
    def tsimTotal( self ):
        """
        El TSIM total del documento

        M{TSIMTOTAL = ( PESO / FACTORPESO )S{uarr} * PORCENTAJETSIM}
        @rtype: Decimal
        """
        try:
            return ( self.weight / self.weightFactor ).to_integral_exact( rounding = ROUND_CEILING ) * self.tsimRate
        except InvalidOperation:
            return Decimal( 0 )



    @property
    @return_decimal
    def totalD( self ):
        """
        La sumatoria de todos los totales parciales

        M{TOTALDOLARES = S{sum}COSTODOLARPARCIAL}
        @rtype: Decimal
        """
        return sum( [ line.costoDolarT for line in self.__lines if line.valid ] )

    @property
    def totalC( self ):
        """
        El total en cordobas del documento

        M{TOTALCORDOBAS = TOTALDOLARES * TIPOCAMBIO }
        @rtype: Decimal
        """
        return self.totalD * self.exchangeRate

    def removeRows( self, position, rows = 1, index = QModelIndex() ):
        """
        Borrar filas del modelo
        @rtype: bool
        @return: si se pudo o no borrar la fila
        """
        #if len( self.__lines ) > 1 and self.__lines[position].valid :
        self.beginRemoveRows( QModelIndex(), position, position + rows - 1 )
        for n in range( rows ):
            try:
                del self.__lines[position + n]
            except IndexError:
                pass
        self.endRemoveRows()
        self.updateFob()
        self.dataChanged.emit( index, index )

        if len( self.__lines ) == 0:
            self.insertRow( 0 )
        return True



    def updateLines( self, query ):
        for line in [line for line in self.lines if line.itemId != 0]:
            line.update( query )


    def save( self ):
        """
        Este metodo guarda el documento actual en la base de datos
        @rtype: bool
        @return: Si el documento se pudo guardar o no
        """
        if not self.valid:
            raise Exception ( "El documento a salvar no es valido" )

        query = QSqlQuery()
        try:
            if not QSqlDatabase.database().transaction():
                raise Exception( u"No se pudo comenzar la transacción" )


            #insertar el documento
            if not query.prepare( """
            INSERT INTO documentos(ndocimpreso, fechacreacion, idtipodoc,
            idestado, observacion, idtipocambio, total, idbodega)
            VALUES( :ndocimpreso, :fechacreacion, :idtipodoc, :estado,
            :observacion, :tipocambio, :total, :idbodega)
            """ ):
                raise Exception( "No se pudo preparar la consulta para"\
                                 + " ingresar el documento" )

            query.bindValue( ":ndocimpreso",
                             self.printedDocumentNumber.strip() )
            query.bindValue( ":fechacreacion",
                              self.datetime.toString( 'yyyyMMddhhmmss' ) )
            query.bindValue( ":idtipodoc", self.__documentType )
            query.bindValue( ":anulado", 0 )
            query.bindValue( ":observacion", self.observations )
            query.bindValue( ":tipocambio", self.exchangeRateId )
            query.bindValue( "total", self.totalD.to_eng_string() )
            query.bindValue( ":idbodega", self.warehouseId )
            query.bindValue( ":estado", constantes.INCOMPLETO )

            if not query.exec_():
                raise Exception( "No se pudo insertar el documento" )

            #el id del documento que se acaba de insertar
            insertedId = query.lastInsertId().toInt()[0]

            #insertar el usuario
            if not query.prepare( """
            INSERT INTO personasxdocumento (idpersona, iddocumento, idaccion)
            VALUE (:idusuario, :iddocumento, :accion)
            """ ):
                raise Exception( "No se pudo preparar la consulta para"\
                                 + " ingresar el usuario" )
            query.bindValue( ":idusuario", self.uid )
            query.bindValue( ":iddocumento", insertedId )
            query.bindValue( ":accion", constantes.AUTOR )

            if not query.exec_():
                raise Exception( "No se pudo insertar  el usuario" )

            #insertar el proveedor
            if not query.prepare( """
            INSERT INTO personasxdocumento (idpersona, iddocumento,idaccion)
            VALUE (:idproveedor, :iddocumento,:accion)
            """ ):
                raise Exception( "No se pudo preparar la consulta para"\
                                 + " ingresar proveedor" )
            query.bindValue( ":idproveedor", self.providerId )
            query.bindValue( ":iddocumento", insertedId )
            query.bindValue( ":accion", constantes.PROVEEDOR )

            if not query.exec_():
                raise Exception( "No se pudo insertar el proveedor" )



            #insertar la liquidacion
            if not query.prepare( """
            INSERT INTO liquidaciones (iddocumento, procedencia, totalagencia, 
            totalalmacen, porcentajepapeleria, porcentajetransporte, peso, 
            fletetotal, segurototal, otrosgastos)
            VALUES(:iddoc,:procedencia,:agencia,:almacen,:papeleria,
            :transporte,:peso,:flete,:seguro,:gastos)
            """ ):
                raise Exception( "No se pudo preparar la liquidacion" )

            query.bindValue( ":iddoc", insertedId )
            query.bindValue( ":procedencia", self.origin.strip() )
            query.bindValue( ":agencia", self.agencyTotal.to_eng_string() )
            query.bindValue( ":almacen", self.storeTotal.to_eng_string() )
            query.bindValue( ":papeleria", self.paperworkRate.to_eng_string() )
            query.bindValue( ":transporte", self.transportRate.to_eng_string() )
            query.bindValue( ":peso", self.weight.to_eng_string() )
            query.bindValue( ":flete", self.freightTotal.to_eng_string() )
            query.bindValue( ":seguro", self.insuranceTotal.to_eng_string() )
            query.bindValue( ":gastos", self.otherTotal.to_eng_string() )

            if not query.exec_():
                raise Exception( "No se pudieron insertar los "\
                                 + "datos de la liquidacion" )

            #insertar el tsim
            if not query.prepare( """
            INSERT INTO costosxdocumento ( iddocumento, idcostoagregado) 
            VALUES ( :iddocumento, :idcostoagregado)
            """ ):
                raise Exception( "No se pudo preparar la consulta"\
                                 + " para insertar el tsim" )
            query.bindValue( ":iddocumento", insertedId )
            query.bindValue( ":idcostoagregado", self.tsimId )

            if not query.exec_():
                raise Exception( "No se pudo insertar el tsim" )


            #insertar el spe
            if not query.prepare( """
            INSERT INTO costosxdocumento ( iddocumento, idcostoagregado) 
            VALUES (:iddocumento, :idcostoagregado )
            """ ):
                raise Exception( "No se pudo preparar la consulta para "\
                                 + "insertar el spe" )
            query.bindValue( ":iddocumento", insertedId )
            query.bindValue( ":idcostoagregado", self.speId )

            if not query.exec_():
                raise Exception( "No se pudo insertar el spe" )


            #insertar el iva si aplica
            if self.applyIVA:
                if not query.prepare( """
                INSERT INTO costosxdocumento ( iddocumento, idcostoagregado) 
                VALUES (:iddocumento, :idcostoagregado )
                """ ):
                    raise Exception( "No se pudo preparar la consulta para "\
                                     + "insertar el iva" )
                query.bindValue( ":iddocumento", insertedId )
                query.bindValue( ":idcostoagregado", self.ivaId )

                if not query.exec_():
                    raise Exception( "No se pudo insertar el iva" )

            #insertar el iso si aplica
            if self.applyISO and self.applyTaxes:
                if not query.prepare( """
                INSERT INTO costosxdocumento ( iddocumento, idcostoagregado) 
                VALUES (:iddocumento, :idcostoagregado )
                """ ):
                    raise Exception( "No se pudo preparar la consulta para "\
                                     + "insertar el iso" )
                query.bindValue( ":iddocumento", insertedId )
                query.bindValue( ":idcostoagregado", self.isoId )

                if not query.exec_():
                    raise Exception( "No se pudo insertar el iso" )



            for i, line in enumerate( [line for line in
                                       self.__lines if line.valid] ):
                line.save( insertedId, i )




            if not QSqlDatabase.database().commit():
                raise Exception( "No se pudo hacer commit" )

        except Exception as inst:
            logging.critical( query.lastError().text() )
            logging.critical( unicode( inst ) )
            QSqlDatabase.database().rollback()

            return False

        return True

    def columnCount( self, _index = QModelIndex() ):
        """
        El numero de columnas del modelo
        @rtype: int
        """
        return 19

    def rowCount( self, _index = QModelIndex() ):
        """
        EL numero de filas del modelo
        @rtype: int
        """
        return len( self.__lines )

    def flags( self, index ):
        """
        Las flags para las celdas del modelo
        @rtype: Qt.ItemFlags
        """
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column() in ( ARTICULO, CANTIDAD, COSTOUNIT ):
            return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        """
        El texto en las cabeceras del modelo
        """
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignLeft | Qt.AlignVCenter
            return Qt.AlignRight | Qt.AlignVCenter

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == IDARTICULO:
                return "Id"
            elif section == ARTICULO:
                return u"Descripción"
            elif section == CANTIDAD:
                return "Cantidad"
            elif section == COSTOUNIT:
                return "Costo Compra US$"
            elif section == FOB:
                return "FOB US$"
            elif section == FLETE:
                return "Flete US$"
            elif section == SEGURO:
                return "Seguro US$"
            elif section == OTROS:
                return "Otros Gastos US$"
            elif section == CIF:
                return "CIF US$"
            elif section == IMPUESTOS:
                return "Impuestos US$"
            elif section == COMISION:
                return "Comision US$"
            elif section == AGENCIA:
                return "Agencia US$"
            elif section == ALMACEN:
                return "Almacen US$"
            elif section == PAPELERIA:
                return "Papeleria US$"
            elif section == TRANSPORTE:
                return "Transporte US$"
            elif section == COSTOC:
                return "Costo Unitario C$"
            elif section == TCOSTOC:
                return "Total Costo C$"
            elif section == TCOSTOD:
                return "Total Costo US$"
            elif section == COSTOD:
                return "Costo Unitario US$"

        return int( section + 1 )

    def insertRows( self, position, rows = 1, _index = QModelIndex() ):
        """
        Insertar filas en el modelo
        @rtype: bool
        @return: Si se pudo insertar la fila en el modelo
        """
        self.beginInsertRows( QModelIndex(), position, position + rows - 1 )
        for row in range( rows ):
            self.__lines.insert( position + row, LineaLiquidacion( self ) )

        self.endInsertRows()

        return True

    def data( self, index, role = Qt.DisplayRole ):
        """
        darle formato a los campos de la tabla
        """
        if not index.isValid() or not ( 0 <= index.row() < len( self.__lines ) ):
            return None

        line = self.__lines[index.row()]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == IDARTICULO:
                return line.itemId if line.itemId != 0 else ""
            elif column == ARTICULO:
                return line.itemDescription
            elif column == CANTIDAD:
                return line.quantity if line.quantity > 0 else ""
            elif column == COSTOUNIT:
                return moneyfmt( line.itemCost, 4, "US$" ) if line.itemCost > Decimal( 0 ) else ""
            elif column == FOB:
                return moneyfmt( line.fobParcial, 4, "US$" ) if line.valid else ""
            elif column == FLETE:
                return moneyfmt( line.fleteParcial, 4, "US$" ) if line.valid else ""
            elif column == SEGURO:
                return moneyfmt( line.seguroParcial, 4, "US$" ) if line.valid else ""
            elif column == OTROS:
                return moneyfmt( line.otrosParcial, 4, "US$" ) if line.valid else ""
            elif column == CIF:
                return moneyfmt( line.cifParcial, 4, "US$" ) if line.valid else ""
            elif column == IMPUESTOS:
                return moneyfmt( line.impuestosParcial, 4, "US$" ) if line.valid else ""
            elif column == COMISION:
                return moneyfmt( line.comisionParcial, 4, "US$" ) if line.valid else ""
            elif column == AGENCIA:
                return moneyfmt( line.agenciaParcial, 4, "US$" ) if line.valid else ""
            elif column == ALMACEN:
                return moneyfmt( line.almacenParcial, 4, "US$" ) if line.valid else ""
            elif column == PAPELERIA:
                return moneyfmt( line.papeleriaParcial, 4, "US$" ) if line.valid else ""
            elif column == TRANSPORTE:
                return moneyfmt( line.transporteParcial, 4, "US$" ) if line.valid else ""
            elif column == TCOSTOD:
                return moneyfmt( line.costoDolarT, 4, "US$" ) if line.valid else ""
            elif column == COSTOD:
                return moneyfmt( line.costoDolar, 4, "US$" ) if line.valid else ""
            elif column == COSTOC:
                return moneyfmt( line.costoCordoba, 4, "C$" ) if line.valid else ""
            elif column == TCOSTOC:
                return moneyfmt( line.costoCordobaT, 4, "C$" ) if line.valid else ""
        elif role == Qt.EditRole:
            if column == COSTOUNIT:
                return line.itemCost
            elif column == IDARTICULO:
                return line.itemId
        elif role == Qt.ToolTipRole:
            if column == CIF:
                return "CIF Total = %s\nFOB Total = %s\nFOB Parcial %s" % ( \
                    moneyfmt( self.cifTotal, 4, "US$" ), \
                    moneyfmt( self.fobTotal, 4, "US$" ), \
                    moneyfmt( line.fobParcial, 4, "US$" )
                    )

            elif column == IMPUESTOS:
                return "DAI Parcial = %s\nISC Parcial = %s\nIVA Parcial = %s\nTSIM Parcial = %s\nSPE Parcial = %s\nISO Parcial = %s" % ( \
                    moneyfmt( line.daiParcial, 4, "US$" ) , \
                    moneyfmt( line.iscParcial, 4, "US$" ) , \
                    moneyfmt( line.ivaParcial, 4, "US$" ) , \
                    moneyfmt( line.tsimParcial, 4, "US$" ), \
                    moneyfmt( line.speParcial, 4, "US$" ), \
                    moneyfmt( line.isoParcial, 4, "US$" )
                    )

            elif column == FOB:
                return "Fob Total = % s" % moneyfmt( self.fobTotal, 4, "US$" )

            elif column == TCOSTOD:
                return u"""CIF Parcial = %s
Comisión Parcial = %s
Agencia Parcial = %s
Almacen Parcial = %s
Papeleria Parcial = %s
Transporte Parcial = %s
Impuestos Parcial = %s""" % ( \
                        moneyfmt( line.cifParcial, 4, "US$" ) , \
                        moneyfmt( line.comisionParcial, 4, "US$" ) , \
                        moneyfmt( line.agenciaParcial, 4, "US$" ) , \
                        moneyfmt( line.almacenParcial, 4, "US$" ), \
                        moneyfmt( line.papeleriaParcial, 4, "US$" ), \
                        moneyfmt( line.transporteParcial, 4, "US$" ), \
                        moneyfmt( line.impuestosParcial, 4, "US$" )
                        )


    def setData( self, index, value, _role = Qt.EditRole ):
        """
        Modificar los datos del modelo
        @param index: El indice en el que se van cambiar los datos
        @type index: QModelIndex

        @param value: El nuevo valor para el elemento del modelo
        @type value: Variant

        @param role: El rol al que se le van a cambiar los datos
        @type role: ItemDataRole

        @rtype: bool
        @return: Si se pudo o no cambiar el valor del modelo
        """
        if index.isValid() and 0 <= index.row() < len( self.__lines ):
            line = self.__lines[index.row()]
            column = index.column()
            if column == ARTICULO:
                line.itemId = value[0]
                line.itemDescription = value[1]
                line.rateDAI = value[2]
                line.rateISC = value[3]
                line.comisionValue = value[4]


            elif column == CANTIDAD:
                line.quantity = value.toInt()[0]
            elif column == COSTOUNIT:
                line.itemCost = Decimal( value.toString() )





            if column  in ( CANTIDAD, COSTOUNIT, ARTICULO, IDARTICULO ):
                self.updateFob()

            if index.row() == len( self.__lines ) - 1 and line.valid:
                self.insertRow( len( self.__lines ) )


            self.dataChanged.emit( index, index )

            return True
        return False



FOBTOTAL, CIFTOTAL, IMPUESTOSTOTAL, COSTODTOTAL, COSTOCTOTAL = range( 5 )
class LiquidacionTotalsModel( QAbstractTableModel ):
    """
    Este modelo maneja la vista de los totales en el formulario de liquidación
    """
    def __init__( self, parent ):
        """
        @param parent: Este es el modelo LiquidacionModel del cual se manejan los totales
        @type parent: LiquidacionModel
        """
        super( LiquidacionTotalsModel, self ).__init__()
        self.parent = parent
        self.parent.dataChanged[QModelIndex, QModelIndex].connect( self.update )

    def update( self, _index1, _index2 ):
        """
        actualizar los totales cuando cambien los datos en el modelo Liquidacion
        """
        self.dataChanged.emit( self.index( 0, 0 ), self.index( 0, self.columnCount() ) )


    def columnCount( self, _index = QModelIndex() ):
        """
        El numero de columnas del modelo
        @rtype: int
        """
        return 5

    def rowCount ( self, _index = QModelIndex() ):
        """
        El numero de filas del modelo
        @rtype: int
        """
        return 1

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        """
        El contenido que aparece en las cabeceras del modelo
        """
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignLeft | Qt.AlignVCenter
            return Qt.AlignRight | Qt.AlignVCenter

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == FOBTOTAL:
                return "FOB"
            elif section == COSTOCTOTAL:
                return "Total C$"
            elif section == COSTODTOTAL:
                return "Total US$"
            elif section == CIFTOTAL:
                return "CIF"
            elif section == IMPUESTOSTOTAL:
                return "Impuestos"
        return int( section + 1 )

    def data( self, index, role = Qt.DisplayRole ):
        """
        El contenido del modelo
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            if index.column() == FOBTOTAL:
                return "%s / %s" % ( 
                            moneyfmt( self.parent.fobTotal, 4, "US$" ) ,
                            moneyfmt( self.parent.fobTotalC, 4, "C$" ) )
            elif index.column() == CIFTOTAL:
                return "%s / %s" % ( 
                                     moneyfmt( self.parent.cifTotal, 4, "US$" ),
                                     moneyfmt( self.parent.cifTotalC, 4, "C$" ) )
            elif index.column() == IMPUESTOSTOTAL:
                return  "%s / %s" % ( moneyfmt( self.parent.taxesTotal, 4, "US$" ),
                                      moneyfmt( self.parent.taxesTotalC, 4, "C$" ) )
            elif index.column() == COSTOCTOTAL:
                return moneyfmt( self.parent.totalC, 4, "C$" )
            elif index.column() == COSTODTOTAL:
                return moneyfmt( self.parent.totalD, 4, "US$" )

        if role == Qt.ToolTipRole:
            if index.column() == IMPUESTOSTOTAL:
                return "DAI = %s \nISC = %s \nIVA = %s \nSPE = %s \nTSIM = %s \nISO = %s" % \
                ( moneyfmt( self.parent.daiTotal, 4, "US$" ), \
                moneyfmt( self.parent.iscTotal, 4, "US$" ), \
                moneyfmt( self.parent.ivaTotal, 4, "US$" ), \
                moneyfmt( self.parent.speTotal, 4, "US$" ),
                moneyfmt( self.parent.tsimTotal, 4, "US$" ), \
                moneyfmt( self.parent.isoTotal, 4, "US$" )
                )

class LiquidacionAccountsModel( AccountsSelectorModel ):
    """
    Esta clase trabaja en las cuentas contables de liquidación
    """
    IDCUENTA, CODCUENTA, NCUENTA, MONTO = range( 4 )

    def __init__( self, docid, user ):
        super( LiquidacionAccountsModel, self ).__init__()
        self.docid = docid
        self.user = user

    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled
        elif index.row() != 0:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable
        else:
            return Qt.ItemIsEnabled

    def removeRows( self, position, rows = 1, _parent = QModelIndex() ):
        if position > 0:
            return super( LiquidacionAccountsModel, self ).removeRows( position, rows, _parent )
        return False

    def save( self ):
        query = QSqlQuery()
        try:
            if not self.valid:
                raise Exception ( "Existe un error con las cuentas contables" )
            if not QSqlDatabase.database().transaction():
                raise Exception( u"No se pudo comenzar la transacción" )

            if not query.prepare( """
            UPDATE documentos SET idestado = :estado WHERE iddocumento = :iddocumento LIMIT 1
            """ ):
                raise Exception( "No se pudo preparar la consulta para actualizar el documento" )

            query.bindValue( ":estado", constantes.CONFIRMADO )
            query.bindValue( ":iddocumento", self.docid )

            if not query.exec_():
                raise Exception( "No se pudo actualizar el documento" )

            if not query.prepare( """
            INSERT INTO personasxdocumento (idpersona, iddocumento, idaccion)
            VALUES (:idpersona, :iddocumento, :accion)
            """ ):
                raise Exception( u"No se pudo preparar la relación del usuario con el documento" )

            query.bindValue( ":idpersona", self.user.uid )
            query.bindValue( ":iddocumento", self.docid )
            query.bindValue( ":accion", constantes.ACCCONTABILIZA )

            for number, line in enumerate( [ linea for linea in self.lines if linea.valid ] ):
                line.save( self.docid, number )



            if not QSqlDatabase.database().commit():
                raise Exception( "No se pudo hacer commit" )

            return True
        except Exception as inst:
            logging.critical( unicode( inst ) )
            logging.critical( query.lastError().text() )
            return False





