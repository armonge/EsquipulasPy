# -*- coding: utf-8 -*-
'''
Created on 21/08/2010

@author: Luis Carlos Mejia
'''
import logging
from utility import constantes
from PyQt4.QtCore import pyqtSlot,Qt
from PyQt4.QtGui import QMainWindow,QDataWidgetMapper,QMessageBox,QSortFilterProxyModel
from ui.Ui_persona import Ui_frmPersona
from utility.base import Base
from PyQt4.QtSql import QSqlQueryModel,QSqlQuery, QSqlDatabase

TIPO,ID,NOMBRE,DIRECCION,TELEFONO,CORREO,RUC,ACTIVO = range(8)

class frmPersona(Ui_frmPersona,QMainWindow,Base):
    def __init__( self,tipo,rol,parent = None):
        super( frmPersona, self ).__init__( parent )
        self.setupUi( self )
        self.parentWindow = parent
        self.tabledetails = None
        Base.__init__( self )
        self.setWindowModality(Qt.WindowModal)
        self.setWindowFlags(Qt.Dialog)
        self.parentWindow.removeToolBar(self.toolBar)
        self.addToolBar(self.toolBar)

        self.tipo = tipo
        self.rol = rol
        self.lbltitulo.setText(u"<B>Datos del %s</B>"%rol)

        self.editmodel = None
        self.parent = parent

        self.navmodel = QSqlQueryModel()
        
        self.navproxymodel = QSortFilterProxyModel()
        self.navproxymodel.setFilterKeyColumn(-1)
        self.navproxymodel.setSourceModel(self.navmodel)
        self.navproxymodel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.tablenavigation.setModel(self.navproxymodel)

        self.actionPreview.setVisible(False)
        self.actionPrint.setVisible(False)
        self.updateModels()
        self.status = True
        
    def updateDetailFilter( self, index ):
        if self.navmodel.record( index ).value( "activo" ).toBool():  
            self.rbactivo.setChecked(True)
        else:
            self.rbinactivo.setChecked(True)
     
    def updateModels( self ):
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( "No se pudo abrir la base de datos" )

            #TODO: Esta consulta tiene que mejorar para definir realmente quien es el que realiza el arqueo
            query = u"""
            SELECT
                tipopersona,
                idpersona,
                Nombre,
                direccion as 'Dirección',
                telefono as 'Teléfono',
                email as 'E-mail',
                ruc as Ruc,
                activo
            FROM personas p
          --  WHERE idpersona =%d
            """ % constantes.CLIENTE
            self.navmodel.setQuery(query)
            self.navproxymodel.setSourceModel(self.navmodel)
            self.tablenavigation.setModel(self.navproxymodel)
            
            self.mapper.setSubmitPolicy( QDataWidgetMapper.ManualSubmit )
            self.mapper.setModel( self.navproxymodel )
            self.mapper.addMapping( self.txtnombre,NOMBRE)
            self.mapper.addMapping( self.txtdireccion,DIRECCION)
            self.mapper.addMapping( self.txttelefono,TELEFONO)
            self.mapper.addMapping( self.txtcorreo,CORREO)
            self.mapper.addMapping( self.txtruc,RUC)
            


            self.tablenavigation.setColumnHidden(TIPO,True)
            self.tablenavigation.setColumnHidden(ID,True)
            self.tablenavigation.setColumnHidden(ACTIVO,True)  
            
            self.tablenavigation.setColumnWidth(NOMBRE,200)
                              
            self.navigate( 'last' )
            
#            self.mapper.setCurrentIndex( index.row() )
            
        except UserWarning as inst:
            logging.error(inst)
            QMessageBox.critical(self, "Llantera Esquipulas", unicode(inst))
        except Exception as inst:
            logging.critical(inst)
        finally:
            if self.database.isOpen():
                self.database.close()

        
    def save(self):
        editado = self.status == 2
        
        titulo = "Guardar los cambios" if editado else "Crear un nuevo %s"%self.rol 
    
        if self.txtnombre.text()=="":
            self.txtnombre.setFocus()
            QMessageBox.warning(None,titulo,"Por favor escriba el nombre del %s"%self.rol)
            return False
        
        
        if QMessageBox.question(None,titulo,u"¿Está seguro que desea guardar los cambios?" if editado else u"¿Está seguro que desea crear al %s?"%self.rol ,QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
            return False
        
        try:
            if not QSqlDatabase.database().isOpen():
                QSqlDatabase.database().open()
            
            query = QSqlQuery()
            
            pos = self.mapper.currentIndex()
            if editado:
                query.prepare("""
                UPDATE personas SET 
                direccion =:dir, 
                telefono=:tel,
                email=:correo,
                ruc=:ruc, 
                tipopersona = :tipo,
                activo=:activo
                WHERE 
                idpersona = :idpersona 
                LIMIT 1;
                """)
                query.bindValue(":idpersona",self.navmodel.record( self.mapper.currentIndex() ).value( "idpersona" ).toInt()[0])
            else:            
                query.prepare("""
                INSERT INTO personas(nombre,fechaingreso,direccion,telefono,email,ruc,tipopersona,activo) VALUES
                (:nombre,NOW(),:dir,:tel,:correo,:ruc,:tipo,:activo)
                """)
                query.bindValue(":nombre",self.txtnombre.text())
                
            query.bindValue(":dir",self.txtdireccion.text())
            query.bindValue(":tel",self.txttelefono.text())
            query.bindValue(":correo",self.txtcorreo.text())
            query.bindValue(":ruc",self.txtruc.text())
            query.bindValue(":tipo",self.tipo)
            query.bindValue(":activo",1 if self.rbactivo.isChecked() else 0)

            
            if not query.exec_():
                raise Exception(query.lastError().text())
            
            QMessageBox.information(None,titulo,"Los cambios fueron guardados" if editado else "El %s fue creado exitosamente"%self.rol)
            
            self.updateModels()
            self.status = True
            result = True
            if editado:
                self.mapper.setCurrentIndex(pos)
        except Exception as inst:
            print inst
            print query.lastError().text()
            QMessageBox.critical(None,titulo,"El %s no pudo ser creado"%self.rol)
            result = False
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()
                
        return result
        
    def cancel( self ):
        self.editmodel = None
        
        self.status = True
        self.navigate( 'last' )
           
    def setControls(self,status):
        
        self.tabWidget.setCurrentIndex(1 if status == False else 0)
        if status == False:
            self.txtnombre.setText("")
            self.txtdireccion.setText("")
            self.txtcorreo.setText("")
            self.txtruc.setText("")
            self.txttelefono.setText("")
            self.rbactivo.setChecked(True)
            self.txtnombre.setReadOnly(False)
        elif status == True:
            self.tablenavigation.setFocus()
            self.txtnombre.setReadOnly(True)
        else:
            status = False    
        
        self.rbactivo.setEnabled(not status)
        self.rbinactivo.setEnabled(not status)
        self.tablenavigation.setEnabled( status )
        self.tabnavigation.setEnabled( status )
        self.actionNew.setVisible( status )
        self.actionCancel.setVisible( not status )
        self.actionSave.setVisible( not status )
        self.actionEditar.setVisible(status )
        self.actionGoFirst.setEnabled(status)
        self.actionGoLast.setEnabled(status)
        self.actionGoNext.setEnabled(status)
        self.actionGoPrevious.setEnabled(status)
                
        self.txtcorreo.setReadOnly(status)
        self.txtdireccion.setReadOnly(status)
        self.txtruc.setReadOnly(status)
        self.txttelefono.setReadOnly(status)

    def setEditControls(self,status):

        self.rbactivo.setEnabled(not status)
        self.rbinactivo.setEnabled(not status)
        self.tablenavigation.setEnabled( status )
        self.tabnavigation.setEnabled( status )
        self.actionNew.setVisible( status )
        self.actionEditar.setVisible(status)
        self.actionCancel.setVisible( not status )
        self.actionSave.setVisible( not status )
        self.txtcorreo.setReadOnly(status)
        self.txtdireccion.setReadOnly(status)
        self.txtruc.setReadOnly(status)
        self.txttelefono.setReadOnly(status)
        
        self.actionGoFirst.setEnabled(status)
        self.actionGoLast.setEnabled(status)
        self.actionGoNext.setEnabled(status)
        self.actionGoPrevious.setEnabled(status)
        
        if not status:
            self.tabWidget.setCurrentIndex(0)
            self.txtdireccion.setFocus()
        else:
            self.tabWidget.setCurrentIndex(1)
            self.tablenavigation.setFocus()
            
            
            
    def newDocument( self ):
        self.status = False        
    
    
    @pyqtSlot(  )
    def on_actionEditar_activated( self ):
#        self.setEditControls(False)
#        self.setControls(2)
        self.status = 2
        
        
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
                