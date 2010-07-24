'''
Created on 03/06/2010

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL,SLOT,pyqtSlot, Qt
from PyQt4.QtGui import QWidget, QSortFilterProxyModel,QAbstractItemView
from PyQt4.QtSql import QSqlDatabase, QSqlQueryModel
from utility.catgeneric import frmCatGeneric
#from utility.catgeneric import frmCatGeneric

class frmBanks (frmCatGeneric):
    
    def __init__( self, parent = None ):
        super( frmBanks, self ).__init__( "bancos", parent )
        self.setWindowTitle( "Catalogo de Bancos" )
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

    def setData(self):
        pass

    def on_txtSearch_textChanged( self, text ):
        """
        Cambiar el filtro de busqueda
        """
        self.filtermodel.setFilterRegExp( text )
