# -*- coding: utf-8 -*-
'''
Created on 03/06/2010

@author: Administrator
'''
import logging

from PyQt4.QtGui import QMainWindow, QMessageBox, QAbstractItemView, QSortFilterProxyModel,\
 QLineEdit, QRegExpValidator, QStyledItemDelegate, QTextDocument, QIntValidator, qApp
from PyQt4.QtCore import pyqtSlot, Qt, SIGNAL, QTimer, QSize, QRegExp, QVariant
from PyQt4.QtSql import QSqlTableModel, QSqlDatabase
from ui.Ui_catgeneric import Ui_frmCatGeneric
class frmCatGeneric( QMainWindow, Ui_frmCatGeneric ):
    """
    Catalogo generico, deberia de poder mostrar cualquier tabla y buscar sobre ella
    """
    def __init__( self, table, parent = None ):
        """
        @param table: Esta es la tabla que se mostrara
        """
        super( frmCatGeneric, self ).__init__( parent )
        self.setupUi( self )

        self.status = False #: El estado del formulario true=editando

        self.actionDelete.setVisible( False )

        self.tableview.addActions( ( self.actionEdit, self.actionNew ) )
        self.database = QSqlDatabase.database()
        self.table = table
        self.tableview.addActions( ( self.actionEdit, self.actionNew, self.actionDelete ) )
        self.backmodel = CatalogModel( self, self.database )
        self.backmodel.setEditStrategy( QSqlTableModel.OnManualSubmit )



        self.filtermodel = QSortFilterProxyModel( self )
        self.filtermodel.setSourceModel( self.backmodel )
        self.filtermodel.setDynamicSortFilter( True )
        self.filtermodel.setFilterKeyColumn( -1 )
        self.filtermodel.setFilterCaseSensitivity( Qt.CaseInsensitive )


        self.connect( self.actionEdit, SIGNAL( "triggered()" ), self.edit )
        self.connect( self.actionNew, SIGNAL( "triggered()" ), self.new )

        QTimer.singleShot( 0, self.updateModels )

    def contextMenuEvent( self, event ):
        self.actionDelete.setEnabled( False )

    def updateModels( self ):
        """
        Actualizar los modelos, despues de toda operacion que cambie la base de datos se tienen que actualizar los modelos
        """
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( "No se pudo abrir la base de datos" )

            self.backmodel.setTable( self.table )
            self.backmodel.select()

        except UserWarning as inst:
            logging.error(inst)
        except Exception as inst:
            logging.critical(inst)
            return False
        finally:
            if self.database.isOpen():
                self.database.close()

        return True
    @pyqtSlot( )
    def on_actionDelete_triggered( self ):
        self.backmodel.removeRows( self.tableview.currentIndex().row(), 1 )

    @pyqtSlot( "QString" )
    def on_txtSearch_textChanged( self, text ):
        """
        Cambiar el filtro de busqueda
        """
        self.filtermodel.setFilterRegExp( text )

    @pyqtSlot(  )
    def on_actionSave_triggered( self ):
        """
        Guardar los cambios
        """
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( u"No se pudo abrir la conexión con la base de datos para guardar los cambios" )
            result = self.backmodel.submitAll()
            if not result:
                raise Exception( self.backmodel.lastError().text() )
            else:
                QMessageBox.information( None,
                 qApp.organizationName() ,
                 """Sus cambios han sido guardados""" )
                self.status = False
                self.updateModels()
        except UserWarning as inst:
            QMessageBox.critical(self, qApp.organizationName(), unicode(inst))
            logging.error(inst)
        except Exception as ins:
            QMessageBox.critical( self,
                     qApp.organizationName() ,
                     """Hubo un error al guardar sus cambios""" )
            logging.critical(inst)
            logging.critical(self.backmodel.lastError().text())
        finally:
            if self.database.isOpen():
                self.database.close()

    @pyqtSlot(  )
    def on_actionCancel_triggered( self ):
        """
        Cancelar los cambios
        """
        if QMessageBox.warning( None,
             qApp.organizationName() ,
             """Sus cambios seran borrados""" ,
            QMessageBox.StandardButtons( \
                QMessageBox.Cancel | \
                QMessageBox.Ok ) ) == QMessageBox.Ok:
                    self.backmodel.revertAll()
                    self.status = False


    def new( self ):
        self.backmodel.insertRow( self.backmodel.rowCount() )
        self.status = True



    def edit( self ):
        self.status = True

    def setStatus( self, status ):

        if status:
            self.tableview.setEditTriggers( QAbstractItemView.AllEditTriggers )
            self.tableview.edit( self.tableview.selectionModel().currentIndex() )
        else:
            self.tableview.setEditTriggers( QAbstractItemView.NoEditTriggers )

        self.actionNew.setVisible( not status )


        self.actionDelete.setVisible( status )
        self.actionCancel.setVisible( status )
        self.actionSave.setVisible( status )

    def getStatus( self ):
        return self.__status

    status = property( getStatus, setStatus )


class CatalogModel( QSqlTableModel ):
    def __init__( self, parent, database ):
        QSqlTableModel.__init__( self, parent, database )

    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        elif index.row() != self.rowCount() - 1:
            return Qt.ItemIsEnabled
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

    def setData( self, index, value, role = Qt.EditRole ):
        value = value.toString().strip() if type( value ) == QVariant else value
        return QSqlTableModel.setData( self, index, value, role )


IDPERSONA, NOMBRE, FECHACREACION, TELEFONO, EMAIL, RUC, ESTADO, TIPOPERSONA, CUENTA = range( 9 )
class PeopleDelegate( QStyledItemDelegate ):
    def __init__( self, parent = None ):
        super( PeopleDelegate, self ).__init__( parent )

    def createEditor( self, parent, option, index ):
        """
        Aca se inicializa el control que se usara para editar
        """
        if index.column() == EMAIL:
            lineedit = QLineEdit( parent )
            #accepts only mail
            validator = QRegExpValidator( QRegExp( r"^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$" ), self )
            lineedit.setValidator( validator )
            return lineedit
        elif index.column() == TELEFONO:
            lineedit = QLineEdit( parent )
            validator = QIntValidator( self )
            lineedit.setValidator( validator )
            return lineedit
        else:
            return QStyledItemDelegate.createEditor( self, parent, option, index )

    def sizeHint( self, option, index ):
        fm = option.fontMetrics
        if index.column() in ( NOMBRE, TELEFONO, RUC, EMAIL ):
            text = index.model().data( index ).toString()
            document = QTextDocument()
            document.setDefaultFont( option.font )
            document.setHtml( text )
            return QSize( document.idealWidth() + 5, fm.height() )
        elif index.column() == ESTADO:
                return QSize( fm.width( "9" ), fm.height() )
        else:
            return QStyledItemDelegate.sizeHint( self, option, index )


    def setEditorData( self, editor, index ):
        """
        Aca se definen los datos iniciales que tendra el control, justo antes de mostrarlo
        """
        if index.column() in ( NOMBRE, TELEFONO, RUC, EMAIL ):
            text = index.model().data( index, Qt.DisplayRole )
            editor.setText( text.toString() )
        else:
            QStyledItemDelegate.setEditorData( self, editor, index )

