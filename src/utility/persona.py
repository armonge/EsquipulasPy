# -*- coding: utf-8 -*-
'''
Created on 21/08/2010

@author: Luis Carlos Mejia
'''
from PyQt4.QtCore import pyqtSlot,Qt
from PyQt4.QtGui import QDialog,QCompleter,QMessageBox,QSortFilterProxyModel
from ui.Ui_persona import Ui_dlgPersona
from PyQt4.QtSql import QSqlQueryModel,QSqlQuery, QSqlDatabase

class dlgPersona(Ui_dlgPersona,QDialog):
    def __init__( self,tipo,rol,parent = None):
        super( dlgPersona, self ).__init__( parent )
        self.setupUi( self )
        
        self.tipo = tipo
        self.rol = rol
        self.lbltitulo.setText("<B>Crear un %s</B>"%rol)
#        self.lblnombre.setText("<B>%s</B>"%rol)
        if not QSqlDatabase.database().isOpen():
            QSqlDatabase.database().open()
            
        
        self.personasModel = QSqlQueryModel()
        self.personasModel.setQuery( """
            SELECT
                tipopersona,
                idpersona,
                nombre,
                direccion,
                telefono,
                email,
                ruc
            FROM personas p
            WHERE idpersona <> 1
            ;""")
        self.navmodel = QSortFilterProxyModel()
        self.navmodel.setSourceModel(self.personasModel)
        self.navmodel.setFilterKeyColumn(0)
        self.navmodel.setFilterRegExp('^%d$'%self.tipo)
        
        
        self.combomodel = QSortFilterProxyModel()
        self.combomodel.setSourceModel(self.personasModel)
        self.combomodel.setFilterKeyColumn(0)
        self.combomodel.setFilterRegExp('[^%d$]'%self.tipo)
        
        self.navproxymodel = QSortFilterProxyModel()
        self.navproxymodel.setFilterKeyColumn(-1)
        self.navproxymodel.setSourceModel(self.navmodel)
        self.navproxymodel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.tablenavigation.setModel(self.navproxymodel)
        self.tablenavigation.setColumnHidden(0,True)
        self.tablenavigation.setColumnHidden(1,True)
        
        if QSqlDatabase.database().isOpen():
            QSqlDatabase.database().close()
        
        if self.combomodel.rowCount()==0:
            self.esNuevo = False
            self.btncancel.setVisible(False)
        else:
            self.esNuevo = True
            self.cbnombre.setModel(self.combomodel)
            self.cbnombre.setCurrentIndex( -1 )
            self.cbnombre.setFocus()
            self.cbnombre.setModelColumn( 2 )
            completer = QCompleter()
            completer.setCaseSensitivity( Qt.CaseInsensitive )
            completer.setModel( self.combomodel )
            completer.setCompletionColumn( 1 )
            self.cbnombre.setCompleter(completer)
            self.btnadd.clicked.connect(self.setControls)
            self.btncancel.clicked.connect(self.setControls)
        
        self.setControls()
        
    def accept(self):
        titulo = "Crear un nuevo %s"%self.rol 
        if self.esNuevo:
            if self.txtnombre.text()=="":
                self.txtnombre.setFocus()
                QMessageBox.warning(None,titulo,"Por favor escriba el nombre del %s"%self.rol)
                return
        else:
            if self.cbnombre.currentIndex()==-1:
                self.cbnombre.setFocus()
                QMessageBox.warning(None,titulo,"Por favor elija una la persona")
                return


        try:
            if not QSqlDatabase.database().isOpen():
                QSqlDatabase.database().open()
            
            query = QSqlQuery()
            
                
                    
            query.prepare("""
            INSERT INTO personas(nombre,fechaingreso,direccion,telefono,email,ruc,tipopersona) VALUES
            (:nombre,NOW(),:dir,:tel,:correo,:ruc,:tipo)
            """)
            query.bindValue(":nombre",self.txtnombre.text() if self.esNuevo else self.cbnombre.currentText())
            query.bindValue(":dir",self.txtdireccion.text())
            query.bindValue(":tel",self.txttelefono.text())
            query.bindValue(":correo",self.txtcorreo.text())
            query.bindValue(":ruc",self.txtruc.text())
            query.bindValue(":tipo",self.tipo)
            
            if not query.exec_():
                raise Exception(query.lastError().text())
            
            QMessageBox.information(None,titulo,"El %s fue creado exitosamente"%self.rol)
            return QDialog.accept(self)
        except Exception as inst:
            print inst
            print query.lastError().text()
        
            QMessageBox.critical(None,titulo,"El %s no pudo ser creado"%self.rol)
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()
        
    
    def setControls(self):
        self.esNuevo = not self.esNuevo
        self.swnombre.setCurrentIndex(1 if self.esNuevo else 0)
        self.txtcorreo.setEnabled(self.esNuevo)
        self.txtdireccion.setEnabled(self.esNuevo)
        self.txtruc.setEnabled(self.esNuevo)
        self.txttelefono.setEnabled(self.esNuevo)

    @pyqtSlot( "int" )
    def on_cbnombre_currentIndexChanged( self, index ):
        """
        asignar proveedor al objeto self.editmodel
        """
        index = self.combomodel.mapToSource(self.combomodel.index(index,0))
        index = index.row()
        self.personaId = self.personasModel.record( index ).value( "idpersona" ).toInt()[0]
        self.txtcorreo.setText(self.personasModel.record( index ).value( "email" ).toString())
        self.txtdireccion.setText(self.personasModel.record( index ).value( "direccion" ).toString())
        self.txtruc.setText(self.personasModel.record( index ).value( "ruc" ).toString())
        self.txttelefono.setText(self.personasModel.record( index ).value( "telefono" ).toString())

    @pyqtSlot( "QString" )
    def on_txtSearch_textChanged( self, searchstring ):
        """
        Cambiar el filtro para el navigation model
        @param searchstring: Es el contenido por el cual se va a filtrar el modelo de navegación
        @type searchstring: string
        """
        self.navproxymodel.setFilterFixedString( searchstring )
                