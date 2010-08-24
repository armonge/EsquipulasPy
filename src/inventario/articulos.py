# -*- coding: utf-8 -*-
'''
Created on 28/05/2010

@author: Andrés Reyes Monge
'''
import logging

from PyQt4.QtCore import SIGNAL, SLOT, pyqtSlot, Qt , QVariant, pyqtSlot
from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QAbstractItemView, QDialog, QDoubleValidator, QMessageBox, QInputDialog, QItemSelection
from PyQt4.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from utility.catgeneric import Ui_frmCatGeneric
from ui.Ui_articulos import Ui_frmArticlesNew
from categoriesmodel import CategoriesModel
from utility.treefilterproxymodel import TreeFilterProxyModel

ID, DESCRIPCION, DAI, ISC, COMISION, GANANCIA, ACTIVO = range( 7 )

class frmArticulos ( QMainWindow, Ui_frmCatGeneric ):
    def __init__( self, user, parent = None ):
        """
        @param user: El id del usuario que ha creado este documento 
        """
        super( frmArticulos, self ).__init__( parent )
        self.setupUi( self )
        self.user = user
        
        self.database = QSqlDatabase.database()
        
#        self.__status = True
        self.backmodel = ArticlesModel()
        self.updateModels()
#        self.tableview.addActions( ( self.actionEdit, self.actionNew ) )
        self.tableview.setColumnHidden( 0, True )
        self.tableview.resizeColumnsToContents()
        self.setWindowTitle( "Catalogo de Articulos" )
        self.tableview.setEditTriggers( QAbstractItemView.AllEditTriggers )
        self.actionEdit.setVisible( True )
        self.actionSave.setVisible( False )
        self.actionCancel.setVisible(False)
        

    def updateModels( self ):
        """
        Actualizar los modelos, despues de toda operacion que cambie la base de datos se tienen que actualizar los modelos
        """
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning("No se pudo abrir la base de datos")
            self.backmodel.setQuery( """
                SELECT idarticulo, descripcion, dai, isc, comision, ganancia, activo
                FROM vw_articulosconcostosactuales v
            """ )
            if self.backmodel.rowCount()==0:
                self.actionEdit.setEnabled(False)
            self.filtermodel = QSortFilterProxyModel()
            self.filtermodel.setSourceModel( self.backmodel )
            self.filtermodel.setFilterKeyColumn( -1 )
            self.filtermodel.setFilterCaseSensitivity( Qt.CaseInsensitive )
            self.tableview.setModel( self.filtermodel )
        except UserWarning as inst:
            logging.error(inst)
            QMessageBox.critical(self, "Llantera Esquipulas", unicode(inst))
        except Exception as inst:
            loggin.critical(inst)
            QMessageBox.critical(self, "Llantera Esquipulas", "Hubo un error al cargar la lista de articulos")
        finally:
            if self.database.isOpen():
                self.database.close()



    @pyqtSlot(  )
    def on_actionEdit_triggered( self ):
        """
        Permite la edicion en el TableView
        """
        self.tableview.setEditTriggers( QAbstractItemView.AllEditTriggers )
        self.tableview.edit( self.tableview.selectionModel().currentIndex() )

    def on_buttonBox_accepted( self ):
        """
        Guardar los cambios
        """
        ###self.backmodel.setData(index, value)

    @pyqtSlot( "QString" )
    def on_txtSearch_textChanged( self, text ):
        """
        @param text: El texto del filtro a buscar
        
        """
        self.filtermodel.setFilterRegExp( text )
    @pyqtSlot(  )
    def on_actionNew_triggered( self ):
        """
        Llama al Dialog para insertar un nuevo articulo
        """
        self.nuevoarticulo = frmArticlesNew( self.user )
        if self.nuevoarticulo.exec_() == QDialog.Accepted:
            self.updateModels()
            
    

        
class ArticlesModel( QSqlQueryModel ):
    def __init__( self, parent = None ):
        """
        Constructor de la clase para editar articulos en el tableview
        """
        super( ArticlesModel, self ).__init__( parent )
        self.queries = []
        self.dirty = False
        if not QSqlDatabase.database().isOpen():
                QSqlDatabase.open()

    def setData( self, index, value, role = Qt.EditRole ):
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
            try:
                if not QSqlDatabase.database().isOpen():
                    if not QSqlDatabase.open():
                        raise UserWarning("No se pudo abrir la base de datos")
                if index.column() == DAI:
                    self.queries.append( self.setDAI( value.toString(), primarykey ) )
                elif index.column() == ISC:
                    self.queries.append( self.setISC( value.toString(), primarykey ) )
                elif index.column() == COMISION:
                    self.queries.append( self.setCOMISION( value.toString(), primarykey ) )
                elif index.column() == GANANCIA:
                    self.queries.append( self.setGANANCIA( value.toString(), primarykey ) )
                elif index.column() == ACTIVO:
                    self.queries.append( self.setACTIVO( value.toBool(), primarykey ) )
                self.refresh()
                self.dirty = True
                self.emit( SIGNAL( "dataChanged(QModelIndex,QModelIndex)" ), index, index )
                return True
            except UserWarning as inst:
                QMessageBox.critical(self, "Llantera Esquipulas", unicode(inst))
                logging.error(inst)
            except Exception as inst:
                logging.critical(inst)
                QMessageBox.critical(self, "Llantera Esquipulas", "Hubo un error al guardar su cambio")
        return False
            
    def setACTIVO( self, value, id ):
        """
        Actualiza el estado de un articulo
        @param id: EL index del record del tableview 
        @param value: El valor a guardar en el record del index 
        """
        query = QSqlQuery()
        if not query.prepare( "update articulos set activo=:value where idarticulo=:idarticulo" ):
            raise Exception( "No se pudo preparar el update" )
        query.bindValue( ":value", value )
        query.bindValue( ":idarticulo", id )
        if not query.exec_():
            raise Exception( "No se pudo ejecutar el update" )

    def setDAI( self, value, id ):
        """
        Actualiza el costo agregado DAI de un articulo
        @param id: El Index del record del tableView
        @param value: El Valor a guardar en el record del Index        
        """
        query = QSqlQuery()
        if not query.prepare( "update costosagregados set activo=0 where idarticulo=:idarticulo and idtipocosto=3" ):
            raise Exception( "No se pudo preparar el update" )
        query.bindValue( ":idarticulo", id )
        if not query.exec_():
            raise Exception( "No se pudo ejecutar el update" )

        if not query.prepare( "insert into costosagregados (valorcosto,activo,idtipocosto,idarticulo) values(:valor,1,3,:idarticulo)" ):
            raise Exception( "No se pudo preparar el insert" )
        query.bindValue( ":idarticulo", id )
        query.bindValue( ":valor", value )
        if not query.exec_():
            raise Exception( "No se pudo insertar" )

    def setISC( self, value, id ):
        """
        Actualiza el costo agregado ISC de un articulo
        @param id: El Index del record del tableView
        @param value: El Valor a guardar en el record del Index        
        """
        query = QSqlQuery()
        if not query.prepare( "update costosagregados set activo=0 where idarticulo=:idarticulo and idtipocosto=2" ):
            raise Exception( "No se pudo preparar el update" )
        query.bindValue( ":idarticulo", id )
        if not query.exec_():
            raise Exception( "No se pudo ejecutar el update" )

        if not query.prepare( "insert into costosagregados (valorcosto,activo,idtipocosto,idarticulo) values(:valor,1,2,:idarticulo)" ):
            raise Exception( "No se pudo preparar el insert" )
        query.bindValue( ":idarticulo", id )
        query.bindValue( ":valor", value )
        if not query.exec_():
            raise Exception( "No se pudo insertar" )

    def setCOMISION( self, value, id ):
        """
        Actualiza el costo agregado COMISION de un articulo
        @param id: El Index del record del tableView
        @param value: El Valor a guardar en el record del Index        
        """
        query = QSqlQuery()
        if not query.prepare( "update costosagregados set activo=0 where idarticulo=:idarticulo and idtipocosto=7" ):
            raise Exception( "No se pudo preparar el update" )
        query.bindValue( ":idarticulo", id )
        if not query.exec_():
            raise Exception( "No se pudo ejecutar el update" )

        if not query.prepare( "insert into costosagregados (valorcosto,activo,idtipocosto,idarticulo) values(:valor,1,7,:idarticulo)" ):
            raise Exception( "No se pudo preparar el insert" )
        query.bindValue( ":idarticulo", id )
        query.bindValue( ":valor", value )
        if not query.exec_():
            raise Exception( "No se pudo insertar" )
            

    def setGANANCIA( self, value, id ):
        """
        Actualiza el costo agregado GANANCIA de un articulo
        @param id: El Index del record del tableView
        @param value: El Valor a guardar en el record del Index        
        """
        query = QSqlQuery()
        if not query.prepare( "UPDATE articulos SET ganancia= :value WHERE idarticulo= :idarticulo" ):
            raise Exception( "No se pudo preparar el update" )
        query.bindValue( ":value", value )
        query.bindValue( ":idarticulo", id )
        if not query.exec_():
            raise Exception( "No se pudo ejecutar el update" )

    def refresh( self ):
        """
        Refresca los datos mostrados en el TableView
        """
        self.setQuery( """        
            SELECT idarticulo, descripcion, dai, isc, comision, ganancia, activo
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


class frmArticlesNew(QDialog, Ui_frmArticlesNew):
    '''
    classdocs
    '''


    def __init__(self, user,parent=None):
        '''
        Constructor
        '''
        super(frmArticlesNew, self).__init__(parent)
        self.user = user
        self.setupUi(self)
        self.catmodel = CategoriesModel()
        
        self.catproxymodel = TreeFilterProxyModel()
        self.catproxymodel.setSourceModel(self.catmodel)
        self.catproxymodel.setFilterKeyColumn(0)
        self.catproxymodel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        
        
        
        self.catvalid = False
        self.catId = 0
        self.brandId = 0
        self.ISC = 0
        self.DAI = 0
        self.comission = 0
        self.profit = 0
        
        
        self.categoriesview.setModel(self.catproxymodel)
        self.categoriesview.setColumnHidden(1,True)
        self.categoriesview.resizeColumnToContents(0)
        
        self.brandsmodel = QSqlQueryModel()
        
        self.cargarMarcas()
        
        self.brandsproxymodel = QSortFilterProxyModel()
        self.brandsproxymodel.setSourceModel(self.brandsmodel)
        self.brandsproxymodel.setFilterKeyColumn(1)
        self.brandsproxymodel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.brandsview.setModel(self.brandsproxymodel)
        self.brandsview.setModelColumn(1)
        
        self.validator = QDoubleValidator(0, 500,4,self)
        self.txtComission.setValidator(self.validator)
        self.txtISC.setValidator(self.validator)
        self.txtDAI.setValidator(self.validator)
        self.txtProfit.setValidator(self.validator)


        self.buttonBox.rejected.connect(self.reject)
        self.categoriesview.selectionModel().selectionChanged[QItemSelection, QItemSelection].connect(self.updateCategory)
        self.brandsview.selectionModel().selectionChanged[QItemSelection, QItemSelection].connect(self.updateBrand)

    def cargarMarcas(self):
        if not QSqlDatabase.database().isOpen():
            if not QSqlDatabase.database().open():
                raise Exception("No se pudo abrir la base de datos")
        
        self.brandsmodel.setQuery("""
        SELECT idmarca, nombre 
        FROM marcas
        """)
        if  QSqlDatabase.database().isOpen():
            QSqlDatabase.database().close()
        

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        if self.valid:
            if QMessageBox.question(self, "Llantera Esquipulas", u"¿Esta seguro que desea añadir el producto?", QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Ok:
                if not self.save():
                    QMessageBox.critical(self, "Llantera Esquipulas", "Lo sentimos pero no se ha podido guardar el articulo")
                else:
                    super(frmArticlesNew, self).accept()
        else:
            QMessageBox.warning(self, "Llantera Esquipulas", "Lo sentimos pero los datos no son validos, recuerde elegir una subcategoria y una marca")
    
    
    def save(self):
        query = QSqlQuery()
        result = False
        try:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.open():
                    raise UserWarning("No se pudo conectar con la base de datos")
                
            
            query.prepare("CALL spAgregarArticulos(:activo,:marca, :subcategoria, :dai, :isc, :comision, :ganancia )")
            query.bindValue(":activo", 1)
            query.bindValue(":marca", self.brandId)
            query.bindValue(":subcategoria", self.catId)
            query.bindValue(":dai", self.DAI)
            query.bindValue(":isc", self.ISC)
            query.bindValue(":comision", self.comission)
            query.bindValue(":ganancia", self.profit)
            
            if not query.exec_():
                raise Exception("No se pudo ejecutar la consulta")
            
            result = True
            
        except UserWarning as inst:
            logging.error(query.lastError().text())
            logging.error(unicode(inst))
        except Exception as inst:
            logging.critical(query.lastError().text())
            logging.critical(unicode(inst))

        return result
        
    @pyqtSlot("QString")
    def on_txtCategorySearch_textChanged(self, text):
        self.catproxymodel.setFilterFixedString(text)
        
    @pyqtSlot("QString")
    def on_txtBrandSearch_textChanged(self,text):
        self.brandsproxymodel.setFilterFixedString(text)
            
    @property
    def valid(self):
        return self.catvalid and self.brandId != 0

    @pyqtSlot( )
    def on_btnAgregarMarca_pressed(self):
        marca =["",True]
        while marca[0]=="" and marca[1]==True:
            marca = QInputDialog.getText(self,"Agregar Marca","Ingrese la Marca")
            if marca[0]!="":
                proxy = self.brandsproxymodel
                proxy.setFilterRegExp("^" + marca[0] + "$")
    
                if proxy.rowCount()>0:
                    QMessageBox.information(None,"Crear Marca","La marca " + marca[0] + " ya existe")
                    marca = ["",True]
        
        self.brandsproxymodel.setFilterRegExp("")
        
        if marca[1]:
            if QMessageBox.question(None,"Crear Marca",u"¿Está seguro que desea crear la marca " + marca[0] + "?", QMessageBox.Yes | QMessageBox.No)==QMessageBox.Yes:
                if not QSqlDatabase.database().isOpen():
                    if not QSqlDatabase.database().open():
                
                        raise Exception("No se pudo abrir la base de datos")
                query = QSqlQuery()
                query.prepare("INSERT INTO marcas(nombre) VALUES (:marca)")
                query.bindValue(":marca",marca[0])
                if not query.exec_():
                    logging.error(query.lastError().text())
                    QMessageBox.warning(None,"Error al crear la marca","No se pudo insertar la marca")
                else:
                    self.cargarMarcas()
        
    
    @pyqtSlot("QString")
    def on_txtDAI_textChanged(self, text):
        try:
            self.DAI = float(text)
        except ValueError:
            self.DAI = 0
    
    @pyqtSlot("QString")
    def on_txtISC_textChanged(self, text):
        try:
            self.ISC = float(text)
        except ValueError:
            self.ISC = 0
            

    @pyqtSlot("QString")
    def on_txtComission_textChanged(self, text):
        try:
            self.comission = float(text)
            
        except ValueError:
            self.comission = 0
        
    @pyqtSlot("QString")
    def on_txtProfit_textChanged(self, text):
        try:
            self.profit = float(text)
        except ValueError:
            self.profit = 0
    
    def updateBrand(self, selected, deselected):            
        if self.brandsproxymodel.rowCount()>=0:
            self.brandId =  self.brandsproxymodel.index(selected.indexes()[0].row(),0).data().toInt()[0]
        
        
    def updateCategory(self, selected, deselected):
        try:
            row = selected.indexes()[0].row()
            parent = selected.indexes()[0].parent()
            self.catvalid = parent.data().toString() != ""
            self.catId =  self.catproxymodel.data(self.catproxymodel.index(row, 1, parent), Qt.DisplayRole)
        except IndexError:
            pass
