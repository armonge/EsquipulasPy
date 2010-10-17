# -*- coding: utf-8 -*-
"""
Module implementing Base
"""
from PyQt4.QtCore import pyqtSlot, QSettings, QUrl, QDateTime, QModelIndex, \
    QTimer
from PyQt4.QtGui import QMessageBox, QDataWidgetMapper, QIcon, QAction, \
    QProgressBar, QPrinter, QPrintDialog, QDialog, qApp, QShortcut, QKeySequence, \
    QMainWindow
from PyQt4.QtSql import QSqlDatabase, QSqlQuery
from PyQt4.QtWebKit import QWebView
from decimal import Decimal
import functools
import logging
import reports
import user



class Base( QMainWindow ):
    """
    Esta clase sirve de base para muchos  todos aquello formularios que siguen el estandar de dos pestañas, una para navegación
    y otra para edición
    """
    orientation = QPrinter.Portrait
    pageSize = QPrinter.Letter
    web = ""

    def __init__( self , parent = None ):
        super( Base, self ).__init__( parent )
        self.parentWindow = parent
        self.user = user.LoggedUser
        self.__status = True



        self.database = QSqlDatabase.database()
        """
        @type: QSqlDatabase
        @ivar: La base de datos a la cual se conecta el sistema
        """

        self.mapper = QDataWidgetMapper( self )
        u"""
        @type: QDataWidgetMapper
        @ivar: El mapper que se encarga de asignar los datos del modelo de navegación a los distintos widgets
        """

        self.printProgressBar = QProgressBar( self )

        self.startUi()


    def startUi( self ):
        self.setupUi( self )




        settings = QSettings()
        self.restoreGeometry( settings.value( self.windowTitle()
                                              + "/Geometry" ).toByteArray() )
        self.restoreState( settings.value( self.windowTitle()
                                            + "/State" ).toByteArray() )

        self.parentWindow.addToolBar( self.toolBar )
        """
        @ivar: El MainWindow al que pertenece este widget
        """
        self.createActions()


        self.printProgressBar.setVisible( False )

        _tab1shortcut = QShortcut( QKeySequence( "Ctrl+1" ),
                                   self,
                                   functools.partial( self.tabWidget.setCurrentIndex, 0 ) )
        _tab2shortcut = QShortcut( QKeySequence( "Ctrl+2" ),
                                   self,
                                   functools.partial( self.tabWidget.setCurrentIndex, 1 ) )


        self.mapper.currentIndexChanged[int].connect( self.updateDetailFilter )
        self.actionGoFirst.triggered.connect( functools.partial( 
                                                                self.navigate,
                                                                 'first' ) )
        self.actionGoPrevious.triggered.connect( functools.partial( 
                                                                   self.navigate,
                                                                    'previous' ) )
        self.actionGoNext.triggered.connect( functools.partial( 
                                                               self.navigate,
                                                               'next' ) )
        self.actionGoLast.triggered.connect( functools.partial( 
                                                                self.navigate,
                                                                 'last' ) )

        self.actionCut.setVisible( False )
        self.actionPaste.setVisible( False )
        self.actionCopy.setVisible( False )

    def closeEvent( self, event ):
        u"""
        Guardar el tamaño, la posición en la pantalla y la posición de la barra de tareas
        Preguntar si realmente se desea cerrar la pestaña cuando se esta en modo edición
        """
        if not self.status:
            if not QMessageBox.question( self,
            qApp.organizationName(),
            u"¿Está seguro que desea salir?",
            QMessageBox.Yes | QMessageBox.No ) == QMessageBox.Yes:
                event.ignore()

        #Guardar el tamaño y la posición
        settings = QSettings()
        settings.setValue( self.windowTitle() + "/Geometry", self.saveGeometry() )
        settings.setValue( self.windowTitle() + "/State", self.saveState() )

        #quitar la toolbar
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

    @pyqtSlot( QDateTime )
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
                        raise Exception( "No se pudo conectar a la base de "\
                                         + "datos para recuperar los tipos de cambio" )

                q = """
                    SELECT idtc, tasa
                    FROM tiposcambio
                    WHERE fecha = %s
                    LIMIT 1
                """ % datetime.toString( "yyyyMMdd" )
                query = QSqlQuery()

                if not query.exec_( q ):
                    logging.critical( query.lastError().text() )
                    raise UserWarning( "No se pudieron recuperar los tipos de "\
                                       + "cambio" )
                if not query.size() == 1:
                    logging.critical( u"La consulta para obtener tipos de "\
                                      + "cambio no devolvio exactamente un valor" )
                    raise UserWarning( u"Hubo un error al obtener los tipos "\
                                       + "de cambio" )

                query.first()
                self.editmodel.exchangeRateId = query.value( 0 ).toInt()[0]
                self.editmodel.exchangeRate = Decimal( query.value( 1 ).toString() )

                #self.editmodel.setData( self.editmodel.index( 0, 0 ), self.editmodel.index( 0, 0 ).data() )

                self.editmodel.datetime = datetime
            except UserWarning  as inst :
                QMessageBox.critical( self, qApp.organizationName(), str( inst ), QMessageBox.Ok )
                self.dtPicker.setDateTime( self.editmodel.datetime )
                logging.error( inst )
            except Exception as inst:
                print "in exception"
                QMessageBox.critical( self, qApp.organizationName(),
                                      u"Hubo un error al obtener los tipos de"\
                                      + " cambio" )
                logging.critical( inst )
                self.dtPicker.setDateTime( self.editmodel.datetime )



    def navigate( self, to ):
        """
        Esta funcion se encarga de navegar entro los distintos documentos
        @param to: es una string que puede tomar los valores 'next' 'previous'
         'first' 'last'
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

        if self.tabledetails != None:
            self.tabledetails.resizeColumnsToContents()
            self.tabledetails.horizontalHeader().setStretchLastSection( True )
        self.tablenavigation.selectRow( self.mapper.currentIndex() )


    def updateDetailFilter( self, unused_index ):
        """
        Esta función se debe implementar en los formularios para que al 
        navegar se actualize el filtro de la tabla detalles
        @param index: Este es el indice del mapper en el que actualmente 
        se encuentra navegando
        @type index: int 
        """
        QMessageBox.information( self, qApp.organizationName(),
                                  u"Esta parte del sistema no ha sido implementada" )
        raise NotImplementedError()

    def loadModels( self ):
        """
        Esta función se ejecuta en el constructor del formulario mediante
        un QTimer, carga los formularios por primera vez
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

    @pyqtSlot( unicode )
    def on_txtSearch_textChanged( self, searchstring ):
        """
        Cambiar el filtro para el navigation model
        @param searchstring: Es el contenido por el cual se va a 
        filtrar el modelo de navegación
        @type searchstring: string
        """
        self.navproxymodel.setFilterFixedString( searchstring )

    @pyqtSlot( QModelIndex )
    def on_tablenavigation_doubleClicked( self, index ):
        """
        Al hacer doble click en la tabla de navegación el se cambia a la
        pestaña detalles mostrando el documento seleccionado
        @param index: El indice de la tabla en la que se dio doble click
        @type index: QModelIndex 
        """
        self.mapper.setCurrentIndex( index.row() )
        self.tabWidget.setCurrentIndex( 0 )

    @pyqtSlot( QModelIndex )
    def on_tablenavigation_clicked( self, index ):
        self.mapper.setCurrentIndex( index.row() )


    def save( self , ask = True ):
        """
        Guardar el documento actual
        @param ask: Si se deberia o no preguntar al usuario si 
            esta seguro antes de proceder
        @type ask: bool
        """
        if ask == False or QMessageBox.question( self, qApp.organizationName(),
                         u"¿Esta seguro que desea guardar?",
                         QMessageBox.Yes | QMessageBox.No ) == QMessageBox.Yes:
            if self.editmodel.valid:
                if self.editmodel.save():
                    QMessageBox.information( self,
                         qApp.organizationName() ,
                         u"El documento se ha guardado con éxito" )
                    self.editmodel = None
                    self.updateModels()
                    self.navigate( 'last' )
                    self.status = True
                else:
                    QMessageBox.critical( self,
                        qApp.organizationName() ,
                         "Ha ocurrido un error al guardar el documento" )


            else:
                try:
                    QMessageBox.warning( self, qApp.organizationName() ,
                                         self.editmodel.validError )
                except AttributeError:
                    QMessageBox.warning( self, qApp.organizationName() ,
                                         u"El documento no puede guardarse"\
                                         + " ya que la información no esta completa" )

    def setControls( self, unused_status ):
        """
        Habilitar o deshabilitar los controles según status
        @param status: 
        @type status: bool
        """
        QMessageBox.information( self, qApp.organizationName(),
                                 u"Esta parte del sistema no ha sido implementada" )
        raise NotImplementedError()

    def addLine( self ):
        """
        añadir una linea a table edit, solo se llama directamente 
        en una ocasion, al comenzar la edicion de un documento
        """
        row = self.editmodel.rowCount()
        self.editmodel.insertRows( row )

    def createAction( self, text, slot = None, shortcut = None, icon = None,
        tip = None, checkable = False, signal = "triggered" ):
        """
        Crear un objeto acción
        @param text: El texto de la acción
        @type text: string

        @param slot: El slot que se ejecutara cuando se dispare esta acción
        @type slot: callable

        @param shortcut: El acceso directo que tiene asignada esta acción
        @type shortcut: QKeySequence

        @param icon: El icono de esta acción
        @type icon: string

        @param tip: El tooltip que tendra esta acción
        @type tip: string

        @param checkable: Si esta acción es checkable o no
        @type checkable: bool

        @param signal: La señal en la que esta acción ejecutara el slot
        @type signal: string

        @rtype: QAction
        """
        action = QAction( text, self )
        if icon is not None:
            action.setIcon( QIcon( icon ) )
        if shortcut is not None:
            action.setShortcut( shortcut )
        if tip is not None:
            action.setToolTip( tip )
            action.setStatusTip( tip )
        if slot is not None:
            getattr( action, signal ).connect( slot )
        if checkable:
            action.setCheckable( True )
        return action

    def newDocument( self ):
        """
        Empezar la edición de un nuevo documento
        """
        QMessageBox.information( self, qApp.organizationName(),
                                 u"Esta parte del sistema no ha sido implementada" )
        raise NotImplementedError()


    def cancel( self ):
        """
        Cancelar la edición del nuevo documento
        """
        QMessageBox.information( self, qApp.organizationName(),
                                 u"Esta parte del sistema no ha sido implementada" )
        raise NotImplementedError()

    @property
    def printIdentifier( self ):
        """
        La identificación de este documento para reporte,
         normalmente sera el iddocumento o el ndocimpreso
        @rtype:string
        """
        raise NotImplementedError( u"printIdentifier debe implementarse para "\
                                   + "poder imprimir" )

    def preview( self ):
        """
        Muestra el dialogo de vista previa de impresión
        """
        try:
            printer = QPrinter()
            printer.setOrientation( self.orientation )
            printer.setPageSize( self.pageSize )
            web = self.web + self.printIdentifier
            report = reports.frmReportes( web, printer, self )
            report.exec_()
        except NotImplementedError as inst:
            QMessageBox.information( self, qApp.organizationName(),
            u"No se ha implementado la función de impresión para este modulo" )
            logging.error( unicode( inst ) )
        except UserWarning as inst:
            QMessageBox.critical( self, qApp.organizationName(),
                                   unicode( inst ) )
            logging.error( unicode( inst ) )
        except Exception as inst:
            QMessageBox.critical( self, qApp.organizationName(),
                                "Hubo un error al intentar mostrar su reporte" )
            logging.critical( unicode( inst ) )

    def printDocument( self ):
        try:

            base = reports.Reports.url

            if base == "":
                raise UserWarning( u"No existe una configuración para el "\
                                   + "servidor de reportes" )

            self.printer = QPrinter()
            self.printer.setOrientation( self.orientation )
            self.printer.setPageSize( self.pageSize )

            self.webview = QWebView()
            web = base + self.web + self.printIdentifier + "&uname=" + \
                self.user.user + "&hash=" + self.user.hash
            self.loaded = False


            self.webview.load( QUrl( web ) )


            self.webview.loadFinished[bool].connect( self.on_webview_loadFinished )
            self.webview.loadProgress[int].connect( self.on_webview_loadProgress )
        except NotImplementedError as inst:
            logging.error( unicode( inst ) )
            QMessageBox.information( self, qApp.organizationName(),
                                 u"La función de impresión no se ha "\
                                 + "implementado para este modulo" )
        except UserWarning as inst:
            logging.error( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(),
                                   unicode( inst ) )
        except Exception as inst:
            logging.critical( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(),
                                   "Hubo un problema al intentar imprimir"\
                                   + " su reporte" )

    def on_webview_loadProgress( self, progress ):
        self.printProgressBar.setValue( progress )


    def on_webview_loadFinished( self, status ):
        if self.printProgressBar.isVisible():
            self.printProgressBar.hide()
        if not status:
            QMessageBox.critical( self, qApp.organizationName(),
                                   "El reporte no se pudo cargar" )
            logging.error( "No se pudo cargar el reporte" )

        self.loaded = True

        printdialog = QPrintDialog( self.printer, self )
        if printdialog.exec_() == QDialog.Accepted:
            self.webview.print_( self.printer )

        del self.webview
        del self.printer


    def deleteRow( self ):
        """
        Funcion usada para borrar lineas de la tabla
        """
        index = self.tabledetails.currentIndex()

        if not index.isValid():
            return
        row = index.row()

        self.editmodel.removeRows( row, 1 )
        self.updateLabels()


    def createActions( self ):
        self.actionNew = self.createAction( text = "Nuevo",
                                         tip = "Crear un nuevo documento",
                                         icon = ":/icons/res/document-new.png",
                                          shortcut = "Ctrl+n",
                                          slot = self.newDocument )
        self.actionPreview = self.createAction( text = "Previsualizar",
                                                 tip = u"Vista de impresión del documento",
                                                 icon = ":/icons/res/document-preview.png",
                                                 shortcut = "Ctrl+p",
                                                  slot = self.preview )
        self.actionPrint = self.createAction( text = "Imprimir",
                                              tip = "Imprimir el documento",
                                               icon = ":/icons/res/document-print.png",
                                               slot = self.printDocument )
        self.actionSave = self.createAction( text = "Guardar",
                                             tip = "Guardar el documento",
                                             icon = ":/icons/res/document-save.png",
                                             shortcut = "Ctrl+g",
                                             slot = self.save )
        self.actionCancel = self.createAction( text = "Cancelar",
                                               tip = "Cancelar la creación del nuevo documento",
                                               icon = ":/icons/res/dialog-cancel.png",
                                               shortcut = "Esc",
                                               slot = self.cancel )

        #edicion, TODO: QUE FUNCIONEN ESTAS ACCIONES
        self.actionCopy = self.createAction( text = "Copiar",
                                              icon = ":/icons/res/edit-copy.png",
                                              shortcut = "Ctrl+c" )
        self.actionCut = self.createAction( text = "Cortar",
                                            icon = ":/icons/res/edit-cut.png",
                                            shortcut = "Ctrl+x" )
        self.actionPaste = self.createAction( text = "Pegar",
                                              icon = ":/icons/res/edit-paste.png",
                                              shortcut = "Ctrl+v" )

        #navegación
        self.actionGoFirst = self.createAction( text = "Primer documento",
                                                tip = "Ir al primer documento",
                                                icon = ":/icons/res/go-first.png" )
        self.actionGoPrevious = self.createAction( text = "Documento anterior",
                                                   tip = "Ir al documento anterior",
                                                   icon = ":/icons/res/go-previous.png" )
        self.actionGoLast = self.createAction( text = "Ultimo documento",
                                               tip = "Ir al ultimo documento",
                                               icon = ":/icons/res/go-last.png" )
        self.actionGoNext = self.createAction( text = "Documento siguiente",
                                               tip = "Ir al siguiente documento" ,
                                               icon = ":/icons/res/go-next.png" )

        self.actionDeleteRow = self.createAction( text = "Borrar la fila",
                                                  icon = ":/icons/res/edit-delete.png",
                                                  slot = self.deleteRow )

        self.addActionsToToolBar()

    def addActionsToToolBar( self ):
        self.toolBar.addActions( [
            self.actionNew,
            self.actionPreview,
            self.actionPrint,
            self.actionSave,
            self.actionCancel
        ] )
        self.toolBar.addSeparator()

        self.toolBar.addActions( [
            self.actionGoFirst,
            self.actionGoPrevious,
            self.actionGoLast,
            self.actionGoNext,
            self.actionGoLast
        ] )




    @pyqtSlot()
    def on_txtObservations_textChanged( self ):
        """
        Asignar las observaciones al editmodel
        """
        if not self.editmodel is None:
            self.editmodel.observations = self.txtObservations.toPlainText().strip()

