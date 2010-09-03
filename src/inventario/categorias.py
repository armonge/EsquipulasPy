# -*- coding: utf-8 -*-
'''
Created on 10/07/2010

@author: Andrés Reyes Monge
'''
from PyQt4.QtGui import QMainWindow, QLineEdit, QVBoxLayout, QFormLayout, QDialogButtonBox, QDialog, QSortFilterProxyModel, QMessageBox, qApp
from PyQt4.QtCore import  Qt, SIGNAL, SLOT, pyqtSlot
from PyQt4.QtSql import  QSqlDatabase

from ui.Ui_categorias import Ui_frmCategorias
from utility.treefilterproxymodel import TreeFilterProxyModel
from categoriesmodel import CategoriesModel

class frmCategorias(QMainWindow, Ui_frmCategorias):
    '''
    classdocs
    '''

    def __init__(self,parent=None):
        '''
        Constructor
        '''
        super(frmCategorias, self).__init__(parent)
        self.setupUi(self)
        QSqlDatabase.database().open()

        self.model = CategoriesModel()

        self.catproxymodel = TreeFilterProxyModel()
        self.catproxymodel.setSourceModel(self.model)
        self.catproxymodel.setFilterKeyColumn(0)
        self.catproxymodel.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.view.setModel(self.catproxymodel)
        self.view.setColumnWidth(0, 200)
        self.view.setColumnHidden(1,True)
    
    @pyqtSlot()
    def on_actionAddSub_triggered(self):
        index = self.view.selectionModel().currentIndex()
        model = self.view.model()

        dlg = dlgCategoriesMod(self)
        if dlg.exec_() == QDialog.Accepted:
            if not model.insertRow(0, index):
                return QMessageBox.critical(self, qApp.organizationName(), "No se pudo insertar la categoria")
    
            for column in range(model.columnCount(index)):
                child = model.index(0, column, index)
                model.setData(child, [dlg.txtName.text(),0], Qt.EditRole)
                
    @pyqtSlot()
    def on_actionAdd_triggered(self):
        index = self.view.selectionModel().currentIndex()
        model = self.view.model()
        
        dlg = dlgCategoriesMod(self)
        if dlg.exec_() == QDialog.Accepted:
            if not model.insertRow(index.row()+1, index.parent()):
                return QMessageBox.critical(self, qApp.organizationName(), "No se pudo insertar la categoria")
    
    
            for column in range(model.columnCount(index.parent())):
                child = model.index(index.row()+1, column, index.parent())
                model.setData(child, [ dlg.txtName.text(),0], Qt.EditRole)

    @pyqtSlot()
    def on_actionEditar_triggered(self):
        index = self.view.selectionModel().currentIndex()
        model = self.view.model()
        
        dlg = dlgCategoriesMod(self)
        dlg.txtName.setText(index.data().toString())
        if dlg.exec_() == QDialog.Accepted:
            if not model.setData(index,[dlg.txtName.text(), index.data()] ):
                raise Exception("No se pudo editar la categoria")
            
            



    @pyqtSlot()
    def on_actionDelete_triggered(self):
        index = self.view.selectionModel().currentIndex()
        if not self.model.removeRow(index.row(), index.parent()):
            QMessageBox.critical(self, qApp.organizationName(), """
No se pudo borrar la categoria
tenga en cuenta que no podra borrar categorias que el sistema ya este utilizando
            """)

    @pyqtSlot( "QString" )
    def on_txtSearch_textEdited( self ,text):
        self.catproxymodel.setFilterRegExp( text)
        
class dlgCategoriesMod( QDialog ):
    def __init__( self, parent = None ):
        super( dlgCategoriesMod, self ).__init__( parent )

        self.setupUi()

    def setupUi( self ):
        self.setWindowTitle( "Modificar Categoria" )
        self.txtName = QLineEdit()
        self.buttonbox = QDialogButtonBox( QDialogButtonBox.Ok | QDialogButtonBox.Cancel )

        formlayout = QFormLayout()
        formlayout.addRow( "Nombre", self.txtName )

        verticallayout = QVBoxLayout()
        verticallayout.addLayout( formlayout )
        verticallayout.addWidget( self.buttonbox )

        self.setLayout( verticallayout )

        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)
