'''
Created on 03/06/2010

@author: Administrator
'''
from PyQt4.QtCore import  Qt
from PyQt4.QtGui import  QSortFilterProxyModel
from utility.catgeneric import FrmCatGeneric

class FrmCajas ( FrmCatGeneric ):

    def __init__( self, parent = None ):
        super( FrmCajas, self ).__init__( "cajas", parent )
        self.setWindowTitle( "Catalogo de Puntos de Caja" )
        self.updateModels()
    def updateModels( self ):
        try:
            self.database.open()
            self.backmodel.setTable( self.table )
            self.backmodel.select()
            self.filtermodel = QSortFilterProxyModel()
            self.filtermodel.setSourceModel( self.backmodel )
            self.filtermodel.setFilterKeyColumn( -1 )
            self.filtermodel.setFilterCaseSensitivity( Qt.CaseInsensitive )
            self.tableview.setModel( self.filtermodel )
            self.database.close()

            self.tableview.setColumnHidden( 0, True )
            return True

        except Exception as inst:
            print inst

            if self.database.isOpen():
                self.database.close()

            return False

    def setData( self ):
        pass

    def on_txtSearch_textChanged( self, text ):
        """
        Cambiar el filtro de busqueda
        """
        self.filtermodel.setFilterRegExp( text )
