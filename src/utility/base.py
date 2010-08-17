# -*- coding: utf-8 -*-
from decimal import  Decimal
import functools

from PyQt4.QtCore import  pyqtSlot,  QSettings
from PyQt4.QtSql import QSqlDatabase, QSqlQuery
from PyQt4.QtGui import QMessageBox, QDataWidgetMapper

class Base( object ):
    """
    Esta clase sirve de base para muchos  formularios de inventario
    """
    def __init__( self ):
        self.mapper = QDataWidgetMapper( self )
        u"""
        @type: QDataWidgetMapper
        @ivar: El mapper que se encarga de asignar los datos del modelo de navegación a los distintos widgets
        """

        self.database = QSqlDatabase.database()
        """
        @type: QSqlDatabase
        @ivar: La base de datos a la cual se conecta el sistema
        """

        settings = QSettings()
        self.restoreGeometry( settings.value( self.windowTitle() + "/Geometry" ).toByteArray() )
        self.restoreState( settings.value( self.windowTitle() + "/State" ).toByteArray() )

        self.parentWindow.addToolBar( self.toolBar )
        """
        @ivar: El MainWindow al que pertenece este widget
        """
        self.mapper.currentIndexChanged[int].connect(self.updateDetailFilter)
        self.actionGoFirst.triggered.connect(functools.partial(self.navigate, 'first'))
        self.actionGoPrevious.triggered.connect(functools.partial(self.navigate, 'previous'))
        self.actionGoNext.triggered.connect(functools.partial(self.navigate, 'next'))
        self.actionGoLast.triggered.connect(functools.partial(self.navigate, 'last'))

    def closeEvent( self, event ):
        u"""
        Guardar el tamaño, la posición en la pantalla y la posición de la barra de tareas
        Preguntar si realmente se desea cerrar la pestaña cuando se esta en modo edición
        """
        if not self.status:
            if not QMessageBox.question(self,
            "Llantera Esquipulas",
            u"¿Está seguro que desea salir?",
            QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
                event.ignore()
                
        settings = QSettings()
        settings.setValue( self.windowTitle() + "/Geometry", self.saveGeometry() )
        settings.setValue( self.windowTitle() + "/State", self.saveState() )
        self.parentWindow.removeToolBar( self.toolBar )



    def hideEvent( self, event ):
        """
        Ocultar la barra de tareas cuando se oculta el widget
        """
        if not event.spontaneous():
            self.toolBar.setVisible( False )

    def showEvent( self, event ):
        if not event.spontaneous():
            self.toolBar.setVisible( True )

    def editCell( self ):
        """
        Editar la celda actualmente seleccionada de self.tableedit
        """
        self.tabledetails.edit( self.tabledetails.selectionModel().currentIndex() )

    @pyqtSlot( "QDateTime" )
    def on_dtPicker_dateTimeChanged( self, datetime ):
        """
        Cambiar el tipo de cambio del modelo de edición si cambia la fecha
        @param datetime: La fecha contenida en self.dtPicker
        @type datetime: QDateTime
        """
        if not self.editmodel is None:
            try:
                if not self.database.isOpen():
                    if not self.database.open():
                        raise Exception( "No se pudo conectar a la base de datos para recuperar los tipos de cambio" )

                query = QSqlQuery( "SELECT idtc, tasa FROM tiposcambio WHERE fecha = " + datetime.toString( "yyyyMMdd" ) + " LIMIT 1" )
                if not query.exec_():
                    raise UserWarning( "No se pudieron recuperar los tipos de cambio" )
                if not query.first():
                    raise UserWarning( u"La consulta para el tipo de cambio no devolvio ningun valor" )
                
                self.editmodel.exchangeRateId = query.value( 0 ).toInt()[0]
                self.editmodel.exchangeRate = Decimal( query.value( 1 ).toString() )
                self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.index( 0, 0 ).data() )
                self.editmodel.datetime = datetime
            except UserWarning  as inst :
                QMessageBox.critical( self, "Llantera Esquipulas", str( inst ), QMessageBox.Ok )
                self.dtPicker.setDateTime( self.editmodel.datetime )
            except Exception as inst:
                print inst
                self.dtPicker.setDateTime( self.editmodel.datetime )



    def navigate( self, to ):
        """
        Esta funcion se encarga de navegar entro los distintos documentos
        @param to: es una string que puede tomar los valores 'next' 'previous' 'first' 'last'
        """
        if self.mapper.currentIndex != -1:
            row = self.mapper.currentIndex()
            if to == "next":
                row += 1
                if row >= self.navproxymodel.rowCount():
                    row = self.navproxymodel.rowCount() - 1
                self.mapper.setCurrentIndex( row )
            elif to == "previous":
                if row <= 1: row = 0
                else: row = row - 1
                self.mapper.setCurrentIndex( row )
            elif to == "first":
                self.mapper.toFirst()
            elif to == "last":
                self.mapper.toLast()
        else:
            self.mapper.toLast()()
        
        self.tabledetails.resizeColumnsToContents()
        self.tabledetails.horizontalHeader().setStretchLastSection(True)
        self.tablenavigation.selectRow( self.mapper.currentIndex() )


    def updateDetailFilter( self, index ):
        """
        Esta función se debe implementar en los formularios para que al navegar se actualize
        el filtro de la tabla detalles
        @param index: Este es el indice del mapper en el que actualmente se encuentra navegando
        @type index: int 
        """
        raise NotImplementedError()

    def loadModels( self ):
        """
        Esta función se ejecuta en el constructor del formulario mediante un QTimer,
        carga los formularios por primera vez
        """
        self.updateModels()
        self.navigate( 'last' )
        self.status = True

    def setStatus( self, stat ):
        """
        @param stat:  False = editando, True = navegando
        @type stat: bool
        """
        self.__status = stat
        self.setControls( self.__status )
    def getStatus( self ):
        """
        esta propiedad cambia entre navegar y editar
        """
        return self.__status

    status = property( getStatus, setStatus )

    @pyqtSlot( "QString" )
    def on_txtSearch_textChanged( self, searchstring ):
        """
        Cambiar el filtro para el navigation model
        @param searchstring: Es el contenido por el cual se va a filtrar el modelo de navegación
        @type searchstring: string
        """
        self.navproxymodel.setFilterFixedString( searchstring )

    @pyqtSlot( "QModelIndex" )
    def on_tablenavigation_doubleClicked( self, index ):
        """
        Al hacer doble click en la tabla de navegación el se cambia a la pestaña detalles 
        mostrando el documento seleccionado
        @param index: El indice de la tabla en la que se dio doble click
        @type index: QModelIndex 
        """
        self.mapper.setCurrentIndex( index.row() )
        self.tabWidget.setCurrentIndex( 0 )

    @pyqtSlot( "QModelIndex" )
    def on_tablenavigation_clicked( self, index ):
        self.mapper.setCurrentIndex( index.row() )


    @pyqtSlot(  )
    def on_actionSave_activated( self ):
        """
        Guardar el documento actual
        """
        if QMessageBox.question(self, "Llantera Esquipulas", u"¿Esta seguro que desea guardar?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            if self.editmodel.valid:
                if not QSqlDatabase.database().isOpen():
                    QSqlDatabase.database().open()
    
                if self.editmodel.save():
                    QMessageBox.information( None,
                         "Llantera Esquipulas" ,
                         """El documento se ha guardado con exito""" ) 
                    self.editmodel = None
                    self.updateModels()
                    self.navigate( 'last' )
                    self.status = True
                else:
                    QMessageBox.critical( None,
                        "Llantera Esquipulas" ,
                         """Ha ocurrido un error al guardar el documento""" ) 
    
                if QSqlDatabase.database().isOpen():
                    QSqlDatabase.database().close()
    
            else:
                try:
                    QMessageBox.warning( None,
                        "Llantera Esquipulas" ,
                        self.editmodel.validError,
                        QMessageBox.StandardButtons( \
                            QMessageBox.Ok ),
                        QMessageBox.Ok )
                except AttributeError:
                    QMessageBox.warning( None,
                        "Llantera Esquipulas" ,
                        u"""El documento no puede guardarse ya que la información no esta completa""",
                        QMessageBox.StandardButtons( \
                            QMessageBox.Ok ),
                        QMessageBox.Ok )

    def setControls( self, status):
        """
        Habilitar o deshabilitar los controles según status
        @param status: 
        @type status: bool
        """
        raise NotImplementedError()

    def addLine( self ):
        """
        añadir una linea a table edit, solo se llama directamente en una ocasion, al
        comenzar la edicion de un documento
        """
        row = self.editmodel.rowCount()
        self.editmodel.insertRows( row )


    @pyqtSlot(  )
    def on_actionPreview_activated( self ):
        """
        Funcion usada para mostrar los reportes
        """
        raise NotImplementedError()

    @pyqtSlot( )
    def on_actionNew_activated( self ):
        """
        Realizar todo el procesamiento necesario para crear un nuevo documento, crear y llenar los
        modelos necesarios, etc.
        """
        raise NotImplementedError()

    @pyqtSlot(  )
    def on_actionCancel_activated( self ):
        """
        Borrar todos los modelos que se hallan creado para el modo edición, asignar los modelos de navegación a las 
        vistas
        """
        raise NotImplementedError()

    @pyqtSlot( )
    def on_actionRefresh_activated( self ):
        """
        Actualizar los modelos de edición
        """
        self.updateEditModels()

    @pyqtSlot( )
    def on_actionDeleteRow_activated( self ):
        """
        Funcion usada para borrar lineas de la tabla
        """
        index = self.tabledetails.currentIndex()

        if not index.isValid():
            return
        row = index.row()

        self.editmodel.removeRows( row, 1 )
        self.updateLabels()

    @pyqtSlot(  )
    def on_txtObservations_textChanged( self ):
        """
        Asignar las observaciones al editmodel
        """
        if not self.editmodel is None:
            self.editmodel.observations = self.txtObservations.toPlainText()

