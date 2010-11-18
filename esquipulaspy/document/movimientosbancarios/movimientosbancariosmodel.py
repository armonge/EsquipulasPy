# -*- coding: utf-8 -*-
'''
Created on 13/07/2010

@author: Luis Carlos Mejia
'''
from PyQt4.QtCore import Qt, QDate
from utility import constantes
from utility.accountselector import AccountsSelectorModel
from datosdocmodel import DatosDocModel
from decimal import Decimal

class MovimientosBancariosModel( AccountsSelectorModel, DatosDocModel ):
    def __init__( self ):
        DatosDocModel.__init__(self)
        AccountsSelectorModel.__init__( self )

    def setData( self, index, value, _role = Qt.EditRole ):
        if index.row()==0 and index.column()==3  and Decimal(value.toString()) <0:
            return False
        AccountsSelectorModel.setData(self, index, value, _role)
        
    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled

        if self.bloqueada( index ):
            return Qt.ItemIsEnabled
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable

    def bloqueada( self, index ):
        """
        Verdadero si el monto de la cuenta contable no debe de ser editada
        @rtype: bool
        """
#        if self.tipoDoc == constantes.IDDEPOSITO:
        if index.row() == 0:
            return index.column() in ( 1, 2 )
        else:
            return False
#        else:
#            return index.column() in ( 1, 2 ) and index.row() == 0

