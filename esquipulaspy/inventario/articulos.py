#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ${file}
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
Created on 28/05/2010

@author: Andrés Reyes Monge
'''
import logging
from decimal import Decimal

from PyQt4.QtCore import  Qt , QVariant, pyqtSlot
from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QAbstractItemView, \
QDialog, QMessageBox, QInputDialog, QItemSelection, qApp
from PyQt4.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel


from ui.Ui_articulos import Ui_frmArticlesNew

from categoriesmodel import CategoriesModel

from utility.catgeneric import Ui_FrmCatGeneric
from utility.treefilterproxymodel import TreeFilterProxyModel
from utility import user, constantes

ID, DESCRIPCION, DAI, ISC, COMISION, GANANCIA, ACTIVO = range( 7 )

class FrmArticulos ( QMainWindow, Ui_FrmCatGeneric ):
    def __init__( self, parent = None ):
        """
        @param parent: El formulario padre de este frm
        """
        super( FrmArticulos, self ).__init__( parent )
        self.setupUi( self )
        self.database = QSqlDatabase.database()

#        self.__status = True
        self.backmodel = ArticlesModel()
        self.filtermodel = QSortFilterProxyModel()
        self.filtermodel.setSourceModel( self.backmodel )
        self.filtermodel.setFilterCaseSensitivity( Qt.CaseInsensitive )

        self.update_models()
#        self.tableview.addActions( ( self.actionEdit, self.actionNew ) )
        self.tableview.setColumnHidden( 0, True )
        self.tableview.resizeColumnsToContents()
        self.setWindowTitle( "Catalogo de Articulos" )
        self.tableview.setEditTriggers( QAbstractItemView.AllEditTriggers )
        self.actionEdit.setVisible( True )
        self.actionSave.setVisible( False )
        self.actionCancel.setVisible( False )

        self.nuevoarticulo = None

    def update_models( self ):
        """
        Actualizar los modelos, despues de toda operacion que cambie la base 
        de datos se tienen que actualizar los modelos
        """
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( "No se pudo abrir la base de datos" )
            self.backmodel.setQuery( """
                SELECT 
                    idarticulo, 
                    descripcion, 
                    dai, 
                    isc, 
                    comision, 
                    ganancia, 
                    activo
                FROM vw_articulosconcostosactuales v
            """ )
            if self.backmodel.rowCount() == 0:
                self.actionEdit.setEnabled( False )

            self.filtermodel.setFilterKeyColumn( -1 )
            self.tableview.setModel( self.filtermodel )
        except UserWarning as inst:
            logging.error( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(),
                                  unicode( inst ) )
        except Exception as inst:
            logging.critical( unicode( inst ) )
            QMessageBox.critical( self,
                                  qApp.organizationName(),
                                  "Hubo un error al cargar la lista de "\
                                  + "articulos" )
        finally:
            if self.database.isOpen():
                self.database.close()



    @pyqtSlot()
    def on_actionEdit_triggered( self ):
        """
        Permite la edicion en el TableView
        """
        self.tableview.setEditTriggers( QAbstractItemView.AllEditTriggers )
        self.tableview.edit( self.tableview.selectionModel().currentIndex() )


    @pyqtSlot( unicode )
    def on_txtSearch_textChanged( self, text ):
        """
        @param text: El texto del filtro a buscar
        
        """
        self.filtermodel.setFilterRegExp( text )
    @pyqtSlot()
    def on_actionNew_triggered( self ):
        """
        Llama al Dialog para insertar un nuevo articulo
        """
        self.nuevoarticulo = FrmArticlesNew()
        if self.nuevoarticulo.exec_() == QDialog.Accepted:
            self.update_models()




class ArticlesModel( QSqlQueryModel ):
    """
    Este modelo se encarga de mostrar y editar los articulos de la tabla 
    articulos
    """
    def __init__( self, parent = None ):
        """
        Constructor de la clase para editar articulos en el tableview
        """
        super( ArticlesModel, self ).__init__( parent )
        self.queries = []
        self.dirty = False
        self.database = QSqlDatabase.database()
        if not self.database.isOpen():
            self.database.open()

    def setData( self, index, value, _role = Qt.EditRole ):
        """
        Guarda los datos editados en el modelo del tableview
        @param index: El Index del record del tableView
        @param value: El Valor a guardar en el record del Index
        @param role: El role para establecer la edicion        
        """
        if index.column() in ( DAI, ISC, COMISION, GANANCIA, ACTIVO ):
            keyindex = super( ArticlesModel, self ).index( index.row(), 0 )
            primarykey = self.data( keyindex ).toInt()[0]
            self.clear()
            result = False
            try:
                if not self.database.isOpen():
                    if not self.database.open():
                        raise UserWarning( "No se pudo abrir la base "\
                                           + "de datos" )
                if not self.database.transaction():
                    raise Exception( self.database.lastError().text() )

                if index.column() == DAI:
                    self.queries.append( set_dai( value.toString(),
                                                       primarykey ) )
                elif index.column() == ISC:
                    self.queries.append( set_isc( value.toString(),
                                                       primarykey ) )
                elif index.column() == COMISION:
                    self.queries.append( set_comision( value.toString(),
                                                            primarykey ) )
                elif index.column() == GANANCIA:
                    self.queries.append( set_ganancia( value.toString(),
                                                            primarykey ) )
                elif index.column() == ACTIVO:
                    self.queries.append( set_activo( value.toBool(),
                                                          primarykey ) )
                if not QSqlDatabase.database().commit():
                    raise Exception( self.database.lastError().text() )

                self.refresh()
                self.dirty = True
                self.dataChanged.emit( index, index )
                result = True

            except UserWarning as inst:
                QMessageBox.critical( None,
                                      qApp.organizationName(),
                                      unicode( inst ) )
                logging.error( unicode( inst ) )
            except Exception as inst:
                logging.critical( unicode( inst ) )
                QMessageBox.critical( None, qApp.organizationName(),
                                      "Hubo un error al guardar su cambio" )
        return result



    def refresh( self ):
        """
        Refresca los datos mostrados en el TableView
        """
        self.setQuery( """        
            SELECT 
                idarticulo, 
                descripcion, 
                dai, 
                isc, 
                comision, 
                ganancia, 
                activo
            FROM vw_articulosconcostosactuales v
        """ )

    def flags( self, index ):
        """
        Establece banderas para determinar el estado de edicion
        """
        if index.column() == DESCRIPCION:
            return Qt.ItemIsEnabled
        elif index.column() == ACTIVO:
            return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

    def data( self, index, role = Qt.DisplayRole ):
        if role == Qt.CheckStateRole and index.column() == ACTIVO:
            if index.column() == ACTIVO:
                return  QVariant( Qt.Checked ) if index.data( Qt.EditRole ).toBool() else QVariant( Qt.Unchecked )
        elif role == Qt.DisplayRole and index.column() == ACTIVO:
            return None
        return QSqlQueryModel.data( self, index, role )


class FrmArticlesNew( QDialog, Ui_frmArticlesNew ):
    '''
    classdocs
    '''

    def __init__( self, parent = None ):
        '''
        Constructor
        '''
        super( FrmArticlesNew, self ).__init__( parent )
        self.user = user.LoggedUser
        self.setupUi( self )
        self.catmodel = CategoriesModel()

        self.catproxymodel = TreeFilterProxyModel()
        self.catproxymodel.setSourceModel( self.catmodel )
        self.catproxymodel.setFilterKeyColumn( 0 )
        self.catproxymodel.setFilterCaseSensitivity( Qt.CaseInsensitive )



        self.catvalid = False
        self.cat_id = 0
        self.brand_id = 0
        self.isc = Decimal( 0 )
        self.dai = Decimal( 0 )
        self.comission = Decimal( 0 )
        self.profit = Decimal( 0 )


        self.categoriesview.setModel( self.catproxymodel )
        self.categoriesview.setColumnHidden( 1, True )
        self.categoriesview.resizeColumnToContents( 0 )

        self.brandsmodel = QSqlQueryModel()

        self.cargarMarcas()

        self.brandsproxymodel = QSortFilterProxyModel()
        self.brandsproxymodel.setSourceModel( self.brandsmodel )
        self.brandsproxymodel.setFilterKeyColumn( 1 )
        self.brandsproxymodel.setFilterCaseSensitivity( Qt.CaseInsensitive )
        self.brandsview.setModel( self.brandsproxymodel )
        self.brandsview.setModelColumn( 1 )



        self.buttonBox.rejected.connect( self.reject )
        self.categoriesview.selectionModel().selectionChanged[QItemSelection, QItemSelection].connect( self.update_category )
        self.brandsview.selectionModel().selectionChanged[QItemSelection, QItemSelection].connect( self.updateBrand )

    def cargarMarcas( self ):
        if not QSqlDatabase.database().isOpen():
            if not QSqlDatabase.database().open():
                raise Exception( "No se pudo abrir la base de datos" )

        self.brandsmodel.setQuery( """
        SELECT idmarca, nombre 
        FROM marcas
        """ )
        if  QSqlDatabase.database().isOpen():
            QSqlDatabase.database().close()


    @pyqtSlot()
    def on_buttonBox_accepted( self ):
        if self.valid:
            if QMessageBox.question( self,
                                     qApp.organizationName(),
                                     u"¿Esta seguro que desea añadir el producto?",
                                     QMessageBox.Ok |
                                     QMessageBox.Cancel ) == QMessageBox.Ok:
                if not self.save():
                    QMessageBox.critical( self,
                                          qApp.organizationName(),
                                          u"Lo sentimos pero no se ha"\
                                          + " podido guardar el articulo" )
                else:
                    super( FrmArticlesNew, self ).accept()
        else:
            QMessageBox.warning( self,
                                 qApp.organizationName(),
                                 u"Lo sentimos pero los datos no son"\
                                 + " validos, recuerde elegir una subcategoria"\
                                 + " y una marca" )


    def save( self ):
        """
        Guardar el nuevo articulo en la base de datos
        """
        query = QSqlQuery()
        result = False
        try:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.open():
                    raise UserWarning( u"No se pudo conectar con la"\
                                       + " base de datos" )


            query.prepare( """
                    CALL spAgregarArticulos(
                        :activo,
                        :marca, 
                        :subcategoria, 
                        :dai,
                        :isc, 
                        :comision, 
                        :ganancia 
                        )
                        """ )
            query.bindValue( ":activo", 1 )
            query.bindValue( ":marca", self.brand_id )
            query.bindValue( ":subcategoria", self.cat_id )
            query.bindValue( ":dai", str( self.dai ) )
            query.bindValue( ":isc", str( self.isc ) )
            query.bindValue( ":comision", str( self.comission ) )
            query.bindValue( ":ganancia", str( self.profit ) )

            if not query.exec_():
                raise Exception( "No se pudo ejecutar la consulta" )

            result = True

        except UserWarning as inst:
            logging.error( query.lastError().text() )
            logging.error( unicode( inst ) )
        except Exception as inst:
            logging.critical( query.lastError().text() )
            logging.critical( unicode( inst ) )

        return result

    @pyqtSlot( unicode )
    def on_txtCategorySearch_textChanged( self, text ):
        self.catproxymodel.setFilterFixedString( text )

    @pyqtSlot( unicode )
    def on_txtBrandSearch_textChanged( self, text ):
        self.brandsproxymodel.setFilterFixedString( text )

    @property
    def valid( self ):
        return self.catvalid and self.brand_id != 0

    @pyqtSlot()
    def on_btnAgregarMarca_pressed( self ):
        marca = ["", True]
        marca_descripcion = ""
        while marca_descripcion == "" and marca[1] == True:
            marca = QInputDialog.getText( self, "Agregar Marca",
                                          "Ingrese la Marca" )
            marca_descripcion = marca[0].strip()
            if marca_descripcion != "":
                proxy = self.brandsproxymodel
                proxy.setFilterRegExp( "^" + marca_descripcion + "$" )

                if proxy.rowCount() > 0:
                    QMessageBox.information( None, "Crear Marca",
                                         "La marca %s ya existe" %
                                          marca_descripcion )
                    marca = ["", True]
                    marca_descripcion = ""

        self.brandsproxymodel.setFilterRegExp( "" )

        if marca[1]:
            if QMessageBox.question( self, qApp.organizationName(),
                                      u"¿Está seguro que desea crear la marca %s ?" %
                                      marca_descripcion,
                                      QMessageBox.Yes | QMessageBox.No
                                       ) == QMessageBox.Yes:
                if not QSqlDatabase.database().isOpen():
                    if not QSqlDatabase.database().open():

                        raise Exception( "No se pudo abrir la base de datos" )
                query = QSqlQuery()
                query.prepare( "INSERT INTO marcas(nombre) VALUES (:marca)" )
                query.bindValue( ":marca", marca_descripcion )
                if not query.exec_():
                    logging.error( query.lastError().text() )
                    QMessageBox.warning( None, "Error al crear la marca",
                                          "No se pudo insertar la marca" )
                else:
                    self.cargarMarcas()


    @pyqtSlot( float )
    def on_sbDAI_valueChanged( self, value ):
        try:
            self.dai = Decimal( str( value ) )
        except ValueError:
            self.dai = 0

    @pyqtSlot( float )
    def on_sbISC_valueChanged( self, value ):
        try:
            self.isc = Decimal( str( value ) )
        except ValueError:
            self.isc = 0


    @pyqtSlot( float )
    def on_sbComission_valueChanged( self, value ):
        try:
            self.comission = Decimal( str( value ) )

        except ValueError:
            self.comission = 0

    @pyqtSlot( float )
    def on_sbProfit_valueChanged( self, value ):
        try:
            self.profit = Decimal( str( value ) )
        except ValueError:
            self.profit = 0

    def updateBrand( self, selected, _deselected ):
        if self.brandsproxymodel.rowCount() >= 0:
            self.brand_id = self.brandsproxymodel.index( 
                                   selected.indexes()[0].row(),
                                    0 ).data().toInt()[0]


    def update_category( self, selected, _deselected ):
        try:
            row = selected.indexes()[0].row()
            parent = selected.indexes()[0].parent()
            self.catvalid = parent.data().toString() != ""
            self.cat_id = self.catproxymodel.data( 
                              self.catproxymodel.index( row, 1,
                                         parent ), Qt.DisplayRole )
        except IndexError:
            pass


def set_activo( value, _id ):
    """
    Actualiza el estado de un articulo
    @param id: EL index del record del tableview 
    @param value: El valor a guardar en el record del index 
    """
    query = QSqlQuery()
    if not query.prepare( """
    UPDATE articulos 
    SET activo=:value 
    WHERE idarticulo=:idarticulo"""
     ):
        raise Exception( query.lastError().text() )
    query.bindValue( ":value", value )
    query.bindValue( ":idarticulo", _id )
    if not query.exec_():
        raise Exception( query.lastError().text() )

def set_dai( value, article_id ):
    """
    Actualiza el costo agregado dai de un articulo
    @param articleid: El Index del record del tableView
    @param value: El Valor a guardar en el record del Index        
    """
    query = QSqlQuery()
    if not query.exec_( """
    UPDATE costosagregados 
    SET activo=0
    WHERE idarticulo=%d AND idtipocosto=%d
    """ % ( article_id,
            constantes.DAI ) ):
        raise Exception( query.lastError().text() )

    if not query.prepare( """
        INSERT INTO costosagregados
        (valorcosto, activo, idtipocosto, idarticulo)
        VALUES(:valor, 1, %d, %d)
        """ % ( constantes.DAI,
                article_id ) ):
        raise Exception( query.lastError().text() )

    query.bindValue( ":valor", value )

    if not query.exec_():
        raise Exception( query.lastError().text() )

def set_isc( value, article_id ):
    """
    Actualiza el costo agregado isc de un articulo
    @param article_id: El Index del record del tableView
    @type article_id: int
    @param value: El Valor a guardar en el record del Index
    @type        
    """
    query = QSqlQuery()
    if not query.exec_( """
    UPDATE costosagregados 
    SET activo=0
    WHERE idarticulo = %d AND idtipocosto = %d
    """ % ( article_id,
            constantes.ISC ) ):
        raise Exception( query.lastError().text() )

    if not query.prepare( """
    INSERT INTO costosagregados
    (valorcosto, activo, idtipocosto,idarticulo)
    VALUES(:valor, 1, %d, %d)
    """ % ( constantes.ISC,
           article_id ) ):
        raise Exception( query.lastError().text() )

    query.bindValue( ":valor", value )


    if not query.exec_():
        raise Exception( query.lastError().text() )

def set_comision( value, article_id ):
    """
    Actualiza el costo agregado COMISION de un articulo
    @param article_id: El Index del record del tableView
    @param value: El Valor a guardar en el record del Index        
    """
    query = QSqlQuery()
    if not query.exec_( """
    UPDATE costosagregados 
    SET activo=0
    WHERE idarticulo=%d AND idtipocosto=%d
    """ % ( article_id,
           constantes.COMISION ) ):
        raise Exception( query.lastError().text() )

    if not query.prepare( """
    INSERT INTO costosagregados 
    (valorcosto,activo,idtipocosto,idarticulo) 
     VALUES (:valor,1,%d,%d) 
     """ % ( constantes.COMISION,
            article_id ) ):
        raise Exception( query.lastError().text() )
    query.bindValue( ":valor", value )

    if not query.exec_():
        raise Exception( query.lastError().text() )


def set_ganancia( value, article_id ):
    """
    Actualiza el costo agregado GANANCIA de un articulo
    @param article_id: El Index del record del tableView
    @param value: El Valor a guardar en el record del Index        
    """
    query = QSqlQuery()
    if not query.prepare( """
    UPDATE articulos 
    SET ganancia= :value 
    WHERE idarticulo= %d
    """ % article_id ):
        raise Exception( query.lastError().text() )
    query.bindValue( ":value", value )

    if not query.exec_():
        raise Exception( query.lastError().text() )
