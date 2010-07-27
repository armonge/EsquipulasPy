# -*- coding: utf-8 -*-
'''
Created on 03/07/2010

@author: armonge
'''
from decimal import Decimal

from PyQt4.QtSql import QSqlDatabase, QSqlQuery
from PyQt4.QtCore import QAbstractItemModel, QModelIndex, Qt, pyqtSlot, SIGNAL, SLOT, QRegExp
from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QDialog, QLineEdit, \
QVBoxLayout, QHBoxLayout, QDialogButtonBox, QCheckBox, QLabel, QRegExpValidator, QValidator, \
QMessageBox
from ui.Ui_cuentas import Ui_frmAccounts
from utility.moneyfmt import moneyfmt

CODIGO, DESCRIPCION, ESDEBE, HIJOS, MONTO, PADRE, IDCUENTA, ACUMULADO = range( 8 )
headers = [ "Codigo", u"Descripción", "Es Debe", "hijos", "Monto", "Padre", "Id", "Acumulado"]
class frmAccounts( QMainWindow, Ui_frmAccounts ):
    def __init__( self, user, parent = None ):
        super( frmAccounts, self ).__init__( parent )
        self.setupUi( self )
        self.user = user

        QSqlDatabase.database().open()
#        self.accountsTree.setModel( AccountsModel( 1 ) )



        self.model = AccountsModel( 1 )

        self.filtermodel = QSortFilterProxyModel()
        self.filtermodel.setSourceModel( self.model )
        self.filtermodel.setFilterKeyColumn( -1 )
        self.filtermodel.setFilterCaseSensitivity( Qt.CaseInsensitive )

        self.accountsTree.setModel( self.filtermodel )

        self.accountsTree.setColumnHidden( IDCUENTA, True )
        self.accountsTree.setColumnHidden( HIJOS, True )
        self.accountsTree.setColumnHidden( PADRE, True )

        self.accountsTree.setColumnWidth( CODIGO, 240 )
        self.accountsTree.setColumnWidth( DESCRIPCION, 240 )
        self.accountsTree.expandAll()

    @pyqtSlot(  )
    def on_btnAdd_clicked( self ):
        proxyindex = self.accountsTree.currentIndex()
        row  = proxyindex.row()
        index = self.accountsTree.model().mapToSource(self.accountsTree.model().index(row, CODIGO, proxyindex.parent())) 
        

        dlg = dlgAccountMod( self )
        if dlg.exec_() == QDialog.Accepted:
            self.accountsTree.model().sourceModel().insertRows( 
                                                 index.row(),
                                                 1,
                                                 index,
                                                 " ".join([txt.text() for txt in dlg.txtCodes ]),
                                                 dlg.txtDescription.text(),
                                                 1 if dlg.cbEsdebe.checkState() == Qt.CheckState else 0
                                                   )

    @pyqtSlot(  )
    def on_btnModify_clicked( self ):
        index = self.accountsTree.currentIndex()
        dlg = dlgAccountMod( self )
        row = index.row()
        codes = self.accountsTree.model().index( row, CODIGO, index.parent()).data().toString()
        codes = codes.split( ' ')
        for id, code in enumerate(codes):
            dlg.txtCodes[id].setText(code)
        
        
        
        
        
        
        
        dlg.txtDescription.setText( self.accountsTree.model().index( row, DESCRIPCION, index.parent() ).data().toString() )
        dlg.cbEsdebe.setCheckState( Qt.Checked if self.accountsTree.model().index( row, ESDEBE, index.parent() ).data().toInt()[0] else Qt.Unchecked )
        if dlg.exec_() == QDialog.Accepted:
            self.accountsTree.model().setData( self.accountsTree.model().index( row, DESCRIPCION, index.parent() ), dlg.txtDescription.text() )
            self.accountsTree.model().setData( self.accountsTree.model().index( row, CODIGO, index.parent() ), " ".join([txt.text() for txt in dlg.txtCodes ]) )
            self.accountsTree.model().setData( self.accountsTree.model().index( row, ESDEBE, index.parent() ), 1 if dlg.cbEsdebe.checkState() == Qt.Checked else 0 )


    @pyqtSlot( "QString" )
    def on_txtSearch_textChanged( self, text ):
        self.filtermodel.setFilterRegExp( text )



class AccountsModel( QAbstractItemModel ):
    def __init__( self, parentId, parent = None ):
        super( AccountsModel, self ).__init__( parent )

        query = """
            SELECT
                cc.codigo,
                cc.descripcion,
                cc.esdebe,
                COUNT(ch.idcuenta) nhijos,
                SUM(IFNULL(monto,0)) monto,
                cc.padre,
                cc.idcuenta
            FROM cuentascontables cc
            LEFT JOIN cuentascontables ch ON cc.idcuenta = ch.padre
            LEFT JOIN cuentasxdocumento cxd ON cc.idcuenta = cxd.idcuenta
            WHERE cc.padre = %d
            GROUP BY cc.idcuenta
        """ % parentId

        query = QSqlQuery( query )
        query.exec_()
        query.first()

        self.rootItem = Account( 
                                QModelIndex(),
                                parentId,
                                query.value( CODIGO ).toString(),
                                query.value( DESCRIPCION ).toString(),
                                Decimal(query.value( MONTO ).toString()),
                                query.value( ESDEBE ).toInt()[0],
                                query.value( HIJOS ).toInt()[0] )

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
            self.emit( SIGNAL( "dataChanged(QModelIndex, QModelIndex)" ), index, index )

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

class Account( object ):
    def __init__( self, parent, id = 0 , code = "", description = "", monto = Decimal(0), esdebe = 0, childCount = 0 ):
        self.parentItem = parent
        self.id = id
        self.code = code
        self.description = description
        self.monto = monto
        self.esdebe = esdebe
        self.__childCount = childCount


        self.childItems = []

        if self.__childCount > 0 and self.id != 0:
            query = """
            SELECT                 
                cc.codigo,
                cc.descripcion,
                cc.esdebe,
                COUNT(ch.idcuenta) nhijos,
                cc.monto,
                cc.padre,
                cc.idcuenta 
            FROM 
            (
                SELECT 
                    cc.* , 
                    SUM(IFNULL(cxd.monto,0)) monto
                FROM cuentascontables cc
                LEFT JOIN cuentasxdocumento cxd ON cxd.idcuenta = cc.idcuenta
                WHERE cc.padre = %d
                GROUP BY cc.idcuenta
            ) cc
            LEFT JOIN cuentascontables ch ON cc.idcuenta = ch.padre
            GROUP BY cc.idcuenta
            """ % self.id
            query = QSqlQuery( query )
            query.exec_()
            while query.next():
                self.appendChild( Account( 
                self, #PADRE 
                query.value( IDCUENTA ).toInt()[0],
                query.value( CODIGO ).toString(),
                 query.value( DESCRIPCION ).toString(),
                 Decimal(query.value( MONTO ).toString()),
                 query.value( ESDEBE ).toInt()[0],
                 query.value( HIJOS ).toInt()[0] ,
                ) )
        elif self.id == 0:
            query = QSqlQuery()
            if not query.prepare( """
            INSERT INTO cuentascontables (padre, codigo, descripcion, esdebe) 
            VALUES (:padre, :codigo, :descripcion, :esdebe)
            """ ):
                raise Exception( "No se pudo preparar la consulta" )
            query.bindValue( ":padre", self.parentItem.id )
            query.bindValue( ":codigo", self.code )
            query.bindValue( ":descripcion", self.description )
            query.bindValue( ":esdebe", self.esdebe )
            if not query.exec_():
                raise Exception( "No se pudo insertar la cuenta contable" )
            self.id = query.lastInsertId().toInt()[0]

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
        for row in range( count ):
            item = Account( self, code = data[0], description = data[1], esdebe = data[2] )
            self.childItems.insert( position, item )

        return True

    def childCount( self ):
        return len( self.childItems )

    def columnCount( self ):
        return 8

    def setData( self, column, value ):
        if column < 0:
            return False

        if column == CODIGO:
            return self.updateCode( value.toString() )
        elif column == DESCRIPCION:
            return self.updateDescription( value.toString() )
        elif column == ESDEBE:
            return self.updateEsdebe( value.toInt()[0] )

        return True

    def updateEsdebe( self, esdebe ):
        if self.id == 0:
            return False
        query = QSqlQuery()
        if not query.prepare( """
        UPDATE cuentascontables 
        SET esdebe = :esdebe WHERE idcuenta = :id LIMIT 1
        """ ):
            print query.lastError().text()
            return False
        query.bindValue( ":esdebe", esdebe )
        query.bindValue( ":id", self.id )
        if not query.exec_():
            print query.lastError().text()
            return False
        if query.numRowsAffected() < 1:
            return False

        self.esdebe = esdebe
        return True

    def updateCode( self, code ):
        if self.id == 0:
            return False
        query = QSqlQuery()
        if not query.prepare( """
        UPDATE cuentascontables 
        SET codigo = :code WHERE idcuenta = :id LIMIT 1
        """ ):
            print query.lastError().text()
            return False
        query.bindValue( ":code", code.strip() )
        query.bindValue( ":id", self.id )
        if not query.exec_():
            print query.lastError().text()
            return False
        if query.numRowsAffected() < 1:
            return False

        self.code = code
        return True

    def updateDescription( self, description ):
        if self.id == 0:
            return False
        query = QSqlQuery()
        if not query.prepare( """
        UPDATE cuentascontables SET descripcion = :desc WHERE idcuenta = :id LIMIT 1
        """ ):
            print query.lastError().text()
            return False
        query.bindValue( ":desc", description.strip() )
        query.bindValue( ":id", self.id )
        if not query.exec_():
            print query.lastError().text()
            return False
        if query.numRowsAffected() < 1:
            return False

        self.description = description
        return True



    def data( self, column, role ):
        if role == Qt.DisplayRole :
            if column == IDCUENTA:
                self.id
            elif column == CODIGO:
                return self.code
            elif column == DESCRIPCION:
                return self.description
            elif column == MONTO:
                return moneyfmt(self.monto, 4, 'C$')
            elif column == ACUMULADO:
                return moneyfmt(self.acumulado,4,"C$")
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

    def parent( self ):
        return self.parentItem

    def row( self ):
        if self.parentItem:
            return self.parentItem.childItems.index( self )
        return None


class dlgAccountMod( QDialog ):
    def __init__( self, parent = None ):
        super( dlgAccountMod, self ).__init__( parent )

        self.setupUi()

    def setupUi( self ):
        self.setWindowTitle( "Modificar Cuenta" )
        
        regexp = QRegExp(r"\d{3}")
        
        self.validators = [QRegExpValidator(self),QRegExpValidator(self), QRegExpValidator(self),QRegExpValidator(self),QRegExpValidator(self)]
        for validator in self.validators:
            validator.setRegExp(regexp)
            
        self.txtCodes = [QLineEdit(),QLineEdit(),QLineEdit(),QLineEdit(),QLineEdit()]
        for index, txtCode in enumerate(self.txtCodes):
            txtCode.setValidator(self.validators[index])
        
        
        self.txtDescription = QLineEdit()
        self.cbEsdebe = QCheckBox( "Es Debe" )
        self.buttonbox = QDialogButtonBox( QDialogButtonBox.Ok | QDialogButtonBox.Cancel )
        
        
        labelcode = QLabel("Codigo")
        horizontal1 = QHBoxLayout()
        horizontal1.addWidget(labelcode)
        for txtCode in self.txtCodes:
            horizontal1.addWidget(txtCode)
        
        horizontal2 = QHBoxLayout()
        horizontal2.addWidget(QLabel( u"Descripción"))
        horizontal2.addWidget(self.txtDescription)
                              

        verticallayout = QVBoxLayout()
        verticallayout.addLayout( horizontal1 )
        verticallayout.addLayout( horizontal2 )
        verticallayout.addWidget( self.cbEsdebe )
        verticallayout.addWidget( self.buttonbox )

        self.setLayout( verticallayout )

        self.connect( self.buttonbox, SIGNAL( "accepted()" ), self, SLOT( "accept()" ) )
        self.connect( self.buttonbox, SIGNAL( "rejected()" ), self, SLOT( "reject()" ) )

    def accept(self):
        result = True
        if self.txtDescription.text().strip() == '':
            QMessageBox.warning(self, "Llantera Esquipulas", u"Verifique la descripción de la cuenta")
            result = False
        if result:
            for index, validator in enumerate(self.validators):
                if validator.validate(self.txtCodes[index].text(),3)[0] != QValidator.Acceptable:
                    QMessageBox.warning(self, "Llantera Esquipulas", "Verifique el codigo de la cuenta")
                    result = False
                    break   
        if result:
            super(dlgAccountMod, self).accept()
    