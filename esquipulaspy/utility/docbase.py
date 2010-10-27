#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       
#       Copyright 2010 Andrés Reyes Monge <armonge@armonge-laptop.site>
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
Created on 16/08/2010

@author: Andrés Reyes Monge
'''

from PyQt4.QtCore import QAbstractTableModel, QDateTime


class DocumentBase( QAbstractTableModel ):

    """
    Esta se convertira en un futuro en la clase base para los nuevos documentos
    idealmente aca irian todas las propiedades que de todos modos todos los
    documentos tienen Eg: exchangeRate, exchangeRateId, observaciones

    ademas de algunos metodos como validLines
    """
    __documentType = NotImplementedError()

    def __init__( self ):
        super( DocumentBase, self ).__init__()



        self.printedDocumentNumber = ""
        """
        @ivar:El numero de documento impreso del documento
        @type:string
        """

        self.datetime = QDateTime.currentDateTime()
        u"""
        @ivar:La fecha de la liquidación
        @type:QDateTime
        """



        self.observations = ""
        """
        @ivar:Las observaciones de este documento
        @type:string
        """

        self._validError = ""
        """
        @ivar: Si existe algún error de validación aca es que se muestra
        @type:string
        """

    @property
    def validError( self ):
        return self._validError

    @property
    def validLines( self ):
        """
        El total de lineas con la propiedad valid = True
        @rtype: int
        """
        return len( [line for line in self.lines if line.valid] )

    @property
    def valid( self ):
        raise NotImplementedError( "El metodo valid deberia de ser"\
                                  + " implementado en todos los documentos" )

    def save( self ):
        raise NotImplementedError()

class LineaBase( object ):
    u"""
    Esta se convertira en un futuro en la clase base para las nuevas lineas,
    con suerte se podran pasar aca muchos metodos genericos
    """
    @property
    def valid( self ):
        """
        Es esta linea valida
        @rtype: bool
        """
        raise NotImplementedError( "No se ha implementado la propiedad Valid" )

    def save( self, iddocumento, nlinea ):
        """
        Este metodo guarda la linea en la base de datos
        @param iddocumento: el id del documento al que esta enlazada la linea
        @rtype: bool
        @return: Si se pudo o no guardar el documento
        """
        raise NotImplementedError( "No se ha implementado el metodo save" )
