# -*- coding: utf-8 -*-
'''
Created on 15/07/2010

@author: Luis Carlos Mejia
'''
from decimal import Decimal

from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QPrinter
from PyQt4.QtSql import QSqlDatabase, QSqlQueryModel
from PyQt4.QtCore import QDate, pyqtSlot, QAbstractItemModel, QModelIndex, Qt

from ui.Ui_balancegeneral import Ui_frmBalanceGeneral

from utility.moneyfmt import moneyfmt
from utility.reports import frmReportes

CODIGO, DESCRIPCION, ESDEBE, HIJOS, MONTO, PADRE, IDCUENTA, ACUMULADO = range( 8 )
headers = [ u"Código", u"Descripción", "Es Debe", "hijos", "Saldo", "Padre", "Id", "Total"]
class FrmBalanceGeneral( QMainWindow, Ui_frmBalanceGeneral ):
    """
    Formulario para crear nuevas conciliaciones bancarias
    """
    def __init__( self, user, parent = None ):
        """
        Constructor
        """
        super( FrmBalanceGeneral, self ).__init__( parent )
        self.setupUi( self )
#        self.dtPicker.setCalendarPopup(True)
        self.dtPicker.setMaximumDate( QDate.currentDate() )
        self.dtPicker.setDate( QDate.currentDate() )

        self.user = user

    def updateModel( self ):
        try:

            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open():
                    raise UserWarning( "No se pudo abrir la base de datos" )

            self.model = CuentasModel( self.dtPicker.date() )
            self.activofiltermodel = QSortFilterProxyModel()
            self.activofiltermodel.setSourceModel( self.model )
            self.activofiltermodel.setFilterKeyColumn( ESDEBE )
            self.activofiltermodel.setFilterRegExp( "1" )
            self.activofiltermodel.setFilterCaseSensitivity( Qt.CaseInsensitive )

            self.activoTree.setModel( self.activofiltermodel )
            self.activoTree.setColumnHidden( IDCUENTA, True )
            self.activoTree.setColumnHidden( HIJOS, True )
            self.activoTree.setColumnHidden( PADRE, True )
            self.activoTree.setColumnHidden( ESDEBE, True )
            self.activoTree.setColumnWidth( CODIGO, 80 )
            self.activoTree.setColumnWidth( DESCRIPCION, 200 )

            total = Decimal( 0 )
            for i in range( self.activofiltermodel.rowCount() ):
                total += Decimal( self.activofiltermodel.index( i, ACUMULADO ).data( Qt.EditRole ).toString() )
            self.txtactivo.setText( moneyfmt( total, 4, 'C$' ) )

    #        self.pasivoModel = CuentasModel()
            self.pasivofiltermodel = QSortFilterProxyModel()
            self.pasivofiltermodel.setSourceModel( self.model )
            self.pasivofiltermodel.setFilterKeyColumn( ESDEBE )
            self.pasivofiltermodel.setFilterRegExp( "0" )


            self.pasivoTree.setModel( self.pasivofiltermodel )
            self.pasivoTree.setColumnHidden( IDCUENTA, True )
            self.pasivoTree.setColumnHidden( HIJOS, True )
            self.pasivoTree.setColumnHidden( PADRE, True )
            self.pasivoTree.setColumnHidden( ESDEBE, True )
            self.pasivoTree.setColumnWidth( CODIGO, 80 )
            self.pasivoTree.setColumnWidth( DESCRIPCION, 200 )

            total1 = Decimal( 0 )
            for i in range( self.pasivofiltermodel.rowCount() ):
                total1 += Decimal( self.pasivofiltermodel.index( i, ACUMULADO ).data( Qt.EditRole ).toString() )
            self.txtpasivo.setText( moneyfmt( total1, 4, 'C$' ) )

            self.capitalfiltermodel = QSortFilterProxyModel()
            self.capitalfiltermodel.setSourceModel( self.model )
            self.capitalfiltermodel.setFilterKeyColumn( ESDEBE )
            self.capitalfiltermodel.setFilterRegExp( "2" )

            self.capitalTree.setModel( self.capitalfiltermodel )
            self.capitalTree.setColumnHidden( IDCUENTA, True )
            self.capitalTree.setColumnHidden( HIJOS, True )
            self.capitalTree.setColumnHidden( PADRE, True )
            self.capitalTree.setColumnHidden( ESDEBE, True )
            self.capitalTree.setColumnWidth( CODIGO, 80 )
            self.capitalTree.setColumnWidth( DESCRIPCION, 200 )

            total2 = Decimal( 0 )
            for i in range( self.capitalfiltermodel.rowCount() ):
                total2 += Decimal( self.capitalfiltermodel.index( i, ACUMULADO ).data( Qt.EditRole ).toString() )

            self.txtcapital.setText( moneyfmt( total2, 4, 'C$' ) )
            self.txtpasivocapital.setText( moneyfmt( total1 + total2, 4, 'C$' ) )


    #        self.capitalTree.expandAll()
    #        self.activoTree.expandAll()
    #        self.pasivoTree.expandAll()
        except Exception as inst:
            print inst
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()

    @pyqtSlot( "QDateTime" )
    def on_dtPicker_dateTimeChanged( self, _datetime ):
        """
        Asignar la fecha al objeto __document
        """
        self.updateModel()

    @pyqtSlot()
    def on_actionPreview_activated( self ):
        printer = QPrinter()
        printer.setPageSize( QPrinter.Letter )
        web = "balancegeneral.php?date=%d+%d" % ( self.dtPicker.date().month() , self.dtPicker.date().year() )
        report = frmReportes( web , printer, self )
        report.exec_()


class CuentasModel( QAbstractItemModel ):
    def __init__( self, fecha, parent = None ):
        super( CuentasModel, self ).__init__( parent )
        self.rootItem = Cuenta( QModelIndex(), fecha, 1, "", "", 0, 0 )

    def getItem( self, index ):
        if index.isValid():
            item = index.internalPointer()
        if item:
            return item
        return self.rootItem
    def insertRows( self, position, rows, parent, code, description, esdebe ):
        parentItem = self.getItem( parent )
        self.beginInsertRows( parent, position, position + rows - 1 )
        success = parentItem.insertChildren( position, rows, [code, description, esdebe] );
        self.endInsertRows()
        return success
    def columnCount( self, parent ):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data( self, index, role ):
        if not index.isValid():
            return None

#        if role != Qt.DisplayRole:
#            return None

        item = index.internalPointer()
        return item.data( index.column(), role )
    def setData( self, index, value, role ):
        if role != Qt.EditRole:
            return False

        item = self.getItem( index )
        result = item.setData( index.column(), value )

        if result:
            self.dataChanged.emit( index, index )

        return result


    def flags( self, index ):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def headerData( self, section, orientation, role ):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:

            return headers[section]

        return None

    def index( self, row, column, parent ):
        if not self.hasIndex( row, column, parent ):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child( row )

        if childItem:
            return self.createIndex( row, column, childItem )
        else:
            return QModelIndex()

    def parent( self, index ):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex( parentItem.row(), 0, parentItem )

    def rowCount( self, parent ):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

class Cuenta( object ):
    def __init__( self, parent, fecha, id = 0 , code = "", description = "", monto = Decimal( 0 ), esdebe = 0 ):
        self.parentItem = parent
        self.id = id
        self.code = code
        self.description = description
        self.monto = monto
        self.esdebe = esdebe

        self.childItems = []

        if self.id != 0:
            self.model = QSqlQueryModel()
            self.model.setQuery( "CALL spBalance( %s )" % fecha.toString( "yyyyMMdd" ) )

            modelo = self.model
            agregados = []

            for i in range( modelo.rowCount() ):
                if modelo.index( i, IDCUENTA ).data().toInt()[0] not in agregados:
                    c = CuentaPadre( self, modelo, modelo, i, agregados )
                    self.appendChild( c )

    def appendChild( self, item ):
        self.childItems.append( item )

    def child( self, row ):
        return self.childItems[row]

    def childCount( self ):
        return len( self.childItems )

    def columnCount( self ):
        return 8

    @property
    def acumulado( self ):
        total = self.monto
        for child in self.childItems:
            total += child.acumulado
        return total



class CuentaPadre( object ):
    def __init__( self, parent, modelo, modeloSinProxy, fila, agregados ):
        self.parentItem = parent
        self.childItems = []


        self.id = modelo.index( fila, IDCUENTA ).data().toInt()[0]
        agregados.append( self.id )

        self.code = modelo.index( fila, CODIGO ).data().toString()
        self.description = modelo.index( fila, DESCRIPCION ).data().toString()
        self.monto = Decimal( modelo.index( fila, MONTO ).data().toString() )

        self.esdebe = modelo.index( fila, ESDEBE ).data().toInt()[0]
        self.idpadre = modelo.index( fila, PADRE ).data().toInt()[0]

        hijos = modelo.index( fila, HIJOS ).data().toInt()[0]

#        print "idcuenta " + str(self.id) + " padre " + str(self.idpadre) + " hijos " + str(hijos)
#        print agregados
        if hijos > 0:

            proxy = QSortFilterProxyModel()
            proxy.setSourceModel( modeloSinProxy )
            proxy.setFilterKeyColumn( PADRE )
            proxy.setFilterRegExp( "^%d$" % self.id )
            modelo2 = proxy

            for j in range( modelo2.rowCount() ):
                if modelo2.index( j, IDCUENTA ).data().toInt()[0] not in agregados:
                    hijo = CuentaPadre( self, modelo2, modeloSinProxy, j, agregados )
                    self.appendChild( hijo )



    @property
    def acumulado( self ):
        total = self.monto
        for child in self.childItems:
            total += child.acumulado
        return total

    def appendChild( self, item ):
        self.childItems.append( item )

    def child( self, row ):
        return self.childItems[row]

    def insertChildren( self, position, count, data ):
        if position < 0:
            return False
        for _row in range( count ):
            item = Cuenta( self, code = data[0], description = data[1], esdebe = data[2] )
            self.childItems.insert( position, item )

        return True

    def childCount( self ):
        return len( self.childItems )

    def columnCount( self ):
        return 8

    def data( self, column, role ):
        if role == Qt.DisplayRole :
            if column == IDCUENTA:
                return self.id
            elif column == CODIGO:
                return self.code
            elif column == DESCRIPCION:
                return self.description
            elif column == MONTO:
                return moneyfmt( self.monto, 4, 'C$' ) if self.monto != 0 else ""
            elif column == ACUMULADO:
                value = moneyfmt( self.acumulado, 4, 'C$' )
                return value if value != 0 else ""
            elif column == ESDEBE:
                return self.esdebe
            elif column == PADRE:
                return self.parent().id
            elif column == HIJOS:
                return self.childCount()
        elif role == Qt.EditRole:
            if column == CODIGO:
                return self.code
            elif column == DESCRIPCION:
                return self.description
            elif column == ESDEBE:
                return self.esdebe
            elif column == IDCUENTA:
                return self.id
            elif column == MONTO:
                return self.monto
            elif column == ACUMULADO:
                return self.acumulado.to_eng_string()


    def parent( self ):
        return self.parentItem

    def row( self ):
        if self.parentItem:
            return self.parentItem.childItems.index( self )
        return None
