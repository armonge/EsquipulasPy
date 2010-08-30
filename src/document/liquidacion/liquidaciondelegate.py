# -*- coding: utf-8 -*-
'''
Created on 21/05/2010

@author: Andrés Reyes Monge
'''
from PyQt4.QtCore import Qt, QSize, QAbstractTableModel, QModelIndex
from PyQt4.QtGui import QStyledItemDelegate, QSpinBox, QDoubleSpinBox
from PyQt4.QtSql import QSqlQuery
from decimal import Decimal
from utility.moneyfmt import moneyfmt
from utility.widgets.searchpanel import SearchPanel


IDARTICULO, ARTICULO, CANTIDAD, COSTOUNIT, FOB, FLETE, SEGURO, OTROS, CIF, IMPUESTOS, COMISION, AGENCIA, ALMACEN, PAPELERIA, TRANSPORTE, TCOSTOD, COSTOD, TCOSTOC, COSTOC = range( 19 )
class LiquidacionDelegate( QStyledItemDelegate ):
    '''
    classdocs
    '''
    def __init__( self, parent = None ):
        '''
        Constructor
        '''
        super( LiquidacionDelegate, self ).__init__( parent )

        self.prods = ArticlesModel()
        self.ids = []
        self.update(QSqlQuery())



    def createEditor( self, parent, option, index ):
        if index.column() == CANTIDAD:
            spinbox = QSpinBox( parent )
            spinbox.setRange( 1, 1000 )
            spinbox.setSingleStep( 1 )
            spinbox.setAlignment( Qt.AlignRight | Qt.AlignVCenter )
            return spinbox
        elif index .column() == COSTOUNIT:
            spinbox = QDoubleSpinBox( parent )
            spinbox.setRange( 0.0001, 10000 )
            spinbox.setDecimals( 4 )
            spinbox.setSingleStep( 1 )
            spinbox.setAlignment( Qt.AlignRight | Qt.AlignVCenter )
            return spinbox
        elif index.column() == ARTICULO:
            if index.data() != "":
                self.prods.items.append( [
                                         index.model().lines[index.row()].itemId,
                                         index.model().lines[index.row()].itemDescription,
                                         index.model().lines[index.row()].rateDAI,
                                         index.model().lines[index.row()].rateISC,
                                         index.model().lines[index.row()].comisionValue
                                         ] )
            sp = SearchPanel( self.prods, parent,True )
            return sp

        else:
            QStyledItemDelegate.createEditor( self, parent, option, index )

    def update(self, query):
        """
        Actualizar todos los valores de los articulos
        @param query: El objeto consulta en el que se van a tratar de obtener los nuevos valores de los articulos
        @type query: QSqlQuery
        """
        inset = list([  itemId for itemId in self.ids if itemId not in [prod[0] for prod in self.prods.items]    ])
        
        listos = ",".join([str(x) for x in inset])
        if len(inset) > 0:
            query.prepare( """
            SELECT
                idarticulo,
                Descripcion AS 'Articulo',
                dai,
                isc,
                Comision as comision
            FROM vw_articulosconcostosactuales
            WHERE activo=1 AND idarticulo NOT IN (%s)
            """ % listos)
        else:
            query.prepare( """
            SELECT
                idarticulo,
                Descripcion AS 'Articulo',
                dai,
                isc,
                Comision as comision
            FROM vw_articulosconcostosactuales
            WHERE activo=1 
            """)
        
        query.exec_()
        self.prods = ArticlesModel()
        while query.next():
            self.prods.items.append( [
                query.value( 0 ).toInt()[0],
                query.value( 1 ).toString(),
                Decimal( query.value( 2 ).toString() ),
                Decimal( query.value( 3 ).toString() ),
                Decimal( query.value( 4 ).toString() ),
                                    ] )
        self.ids = list([item[0] for item in self.prods.items])
        self.ids.extend(inset)
                                    

    def setEditorData( self, editor, index ):
        text = index.data( Qt.DisplayRole ).toString()
        if index.column() == CANTIDAD:
            editor.setValue( index.model().data( index, Qt.DisplayRole ) if index.model().data( index, Qt.DisplayRole ) != "" else 0 )
        elif index.column() == ARTICULO:
            i = editor.findText( text )
            if i == -1:
                i = 1
            editor.setCurrentIndex( i )
            editor.lineEdit().selectAll()
        elif index.column() == COSTOUNIT:
            editor.setValue( index.data( Qt.EditRole ).toDouble()[0] if index.data( Qt.EditRole ).toDouble()[0] != 0 else 1 )
        else:
            QStyledItemDelegate.setEditorData( self, editor, index )

    def setModelData( self, editor, model, index ):
        if index.column() == ARTICULO:
            try:
                model.setData( index, self.prods.items[editor.currentIndex()] )
                del self.prods.items[editor.currentIndex()]
            except IndexError as inst:
                print inst
        else:
            QStyledItemDelegate.setModelData( self, editor, model, index )

    def sizeHint( self, option, index ):
        fm = option.fontMetrics
        if index.column() == IDARTICULO:
            return QSize( fm.width( "99" ), fm.height() )
        if index.column() == ARTICULO:
            return QSize( 250, fm.height() )

        return QStyledItemDelegate.sizeHint( self, option, index )


class ArticlesModel( QAbstractTableModel ):
    def __init__( self ):
        super( ArticlesModel, self ).__init__()
        self.items = []

    def data( self, index, role = Qt.DisplayRole ):
        """
        darle formato a los campos de la tabla
        """
        if not index.isValid() or not ( 0 <= index.row() < len( self.items ) ):
            return ""
        line = self.items[index.row()]
        if role == Qt.DisplayRole:
            if index.column() in ( 2, 3 ):
                return line[index.column()].to_eng_string() + "%"
            elif index.column() == 4:
                return moneyfmt( line[index.column()], 4, "US$" )
            return line[index.column()]
# 0 = id articulo, 1 = descripcion articulo, 2 = dai, 3 = isc, 4 = comision        
        elif role == Qt.EditRole:
                return line[index.column()]



    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignLeft | Qt.AlignVCenter
            return Qt.AlignRight | Qt.AlignVCenter

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == 0:
                return "id"
            elif section == 1:
                return "Articulo"
            elif section == 2:
                return "DAI"
            elif section == 3:
                return "ISC"
            elif section == 4:
                return u"Comisión"
        return int( section + 1 )

    def rowCount( self, index = QModelIndex() ):
        return len( self.items )

    def columnCount( self, index = QModelIndex ):
        return 5

