# -*- coding: UTF-8 -*-
'''
Created on 29/05/2010

@author: armonge
'''

from PyQt4.QtGui import QTableView, QSortFilterProxyModel, QCompleter, QComboBox
from PyQt4.QtCore import Qt, SIGNAL, SLOT
from utility.singleselectionmodel import SingleSelectionModel

class SearchPanel( QComboBox ):
    def __init__( self, model, parent = None,showTable=False  ):
        QComboBox.__init__( self, parent )

        self.tabla =None        
        self.setFocusPolicy( Qt.StrongFocus )
        self.setEditable( True )
#        self.setModel( model )
        self.setEditable( True )
        self.completer = QCompleter( self );
        self.completer.setCompletionMode( QCompleter.UnfilteredPopupCompletion ) # always show all completions
        self.pFilterModel = QSortFilterProxyModel( self )
        self.pFilterModel.setFilterCaseSensitivity( Qt.CaseInsensitive )
        
        if model !=None:
            self.setModel(model )
#        self.pFilterModel.setSourceModel( model );
        
        
        self.completer.setModel( self.pFilterModel )
        self.completerTable = SearchPanelView()
        self.completer.setPopup( self.completerTable )
#Mostrar el Popup en forma de Tabla        
        if showTable:
            self.tabla = SearchPanelView()
            self.setView(self.tabla)
            
        self.setCompleter( self.completer )

        self.setColumn( 1 )

        self.connect( self.lineEdit(), SIGNAL( "textEdited(  QString )" ), self.pFilterModel, SLOT( "setFilterFixedString(  QString )" ) if showTable==False else SLOT( "setFilterWildcard(  QString )" ) )

    def setModel(self,model):
        QComboBox.setModel(self,model)
        self.pFilterModel.setSourceModel( model );
    
    def setColumn( self, column ):
        self.setModelColumn( 1 )
        self.completer.setCompletionColumn( column )
        self.pFilterModel.setFilterKeyColumn( column )
        self.setModelColumn( column )

    def view( self ):
        return self.completer.popup()

    def data( self ):
        return self.currentIndex()

    def index( self ):
        return self.currentIndex()
    
    def setColumnHidden(self,col):
        self.completerTable.hiddenColumns.append(col)
        self.tabla.hiddenColumns.append(col)




class SearchPanelView( QTableView ):
    '''
    classdocs
    '''
    def __init__( self, parent = None ):
        '''
        Constructor
        '''
        QTableView.__init__( self, parent )

        self.setSelectionBehavior( QTableView.SelectRows )
        self.setSelectionMode( QTableView.SingleSelection )
        self.setMinimumHeight( 150 )
        self.setMinimumWidth( 500 )
        self.verticalHeader().setVisible( False )
        self.set = False
        self.hiddenColumns = []



    def paintEvent( self, event ):
        if not self.set:
            self.resizeColumnsToContents()
            self.setColumnHidden( 0, True )
            self.set = True
            self.horizontalHeader().setStretchLastSection( True )
        
        for column in self.hiddenColumns:
            self.setColumnHidden( column, True )
        QTableView.paintEvent( self, event )



