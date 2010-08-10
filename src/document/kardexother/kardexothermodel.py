'''
Created on 09/08/2010

@author: armonge
'''
from PyQt4.QtCore import QAbstractTableModel, Qt

from utility import constantes

class KardexOtherModel(QAbstractTableModel):
    '''
    Esta clase es el modelo utilizado en la tabla en la que se editan documentos
    de tipo kardex generados por entradas o salidas extraordinarias
    '''
    __documentType = constantes.IDKARDEX    
    def __init__(self):
        '''
        Constructor
        '''
        super(KardexOtherModel, self).__init__()
        
        self.observations = ""
        """
        @ivar: Las  observaciones del documento kardex
        @type:string
        """
        
        self.lines = []
        """
        @ivar: Las lineas del documento kardex
        @type: OtherKardexLine
        """
        
    def data( self, index, role = Qt.DisplayRole ):
        return None
        
        