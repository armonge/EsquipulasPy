# -*- coding: utf-8 -*-
'''
Created on 25/05/2010

@author: Luis Carlos Mejia
'''
from PyQt4.QtCore import Qt, QTimer
from PyQt4.QtGui import QSortFilterProxyModel, QAbstractItemView, \
    QDataWidgetMapper, QMessageBox, qApp
from PyQt4.QtSql import QSqlQueryModel
from document.movimientosbancarios import MovimientosBancariosModel
from ui.Ui_frmmovimientosbancarios import Ui_frmMovimientosBancarios
from utility import constantes
from utility.base import Base
from utility.widgets.searchpanel import SearchPanel
import logging




IDDOCUMENTO, FECHA, CUENTA, TIPODOC, CONCEPTO, OBSERVACION, NCUENTA = range( 7 )
class FrmMovimientosBancarios( Ui_frmMovimientosBancarios, Base ):

    def __init__( self, parent ):
        super( FrmMovimientosBancarios, self ).__init__( parent )

        self._iniciarClase( parent )
        self._iniciarInterfaz()

        #Carga los modelos de forma paralela a la ejecucion del sistema
        QTimer.singleShot( 0, self.loadModels )

    def _iniciarClase( self, parent ):
        """
        Ejecuta constructores de las clases e inicializa variables
        """

        self.parentWindow = parent


        self.navmodel = None
        """
        @ivar: Modelo de navegacion que se asignara a la tabla 
        principal de navegacion
        @type: QSqlQueryModel
        """

        self.navproxymodel = None
        """
        @ivar: = Proxy del modelo de navegacion que filtra al momento 
        de una busqueda
        @type: QSortFilterProxyModel  
        """

        self.detailsmodel = None
        """
        @ivar: Modelo detalle, carga las lineas del documento
        @type: QSqlQueryModel
        """

        #Proxy para el modelo detalle, que filtra al navegar para solo mostrar las lineas relacionadas al documento actual
        self.detailsproxymodel = QSortFilterProxyModel( self )
        self.detailsproxymodel.setSourceModel( self.detailsmodel )

        #Modelo de Edicion
        self.editmodel = None


    def _iniciarInterfaz( self ):
        """
        Realiza Cambios iniciales al formulario
        """
        #FIXME: Porque esto no esta en el designer???
        self.cbcuenta = SearchPanel( None, None, True )
        """
        @ivar: El combo con en el que se cargan las cuentas
        @type: SearcPanel
        """
        self.horizontalLayout_32.addWidget( self.cbcuenta )
        self.actionSave.setVisible( False )
        self.actionCancel.setVisible( False )


    def newDocument( self ):
        """
        activar todos los controles, llena los modelos necesarios, 
        crear el modelo de edidicion
        """
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( u"No se pudo establecer la "\
                                       + "conexión con la base de datos" )

            self.editmodel = MovimientosBancariosModel()
            self.editmodel.autorDoc = self.user.uid
            self.status = False

        except UserWarning as inst:
            logging.error( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(),
                                  unicode( inst ) )
            self.status = True
        except Exception as inst:
            logging.critical( unicode( inst ) )
            print inst
            QMessageBox.critical( self, qApp.organizationName(),
                                  u"Hubo un error al actualizar los datos" )
            self.status = True

        finally:
            if self.database.isOpen():
                self.database.close()


    def setControls( self, status ):
        """
        Cambia el formulario entre modos de edicion y navegacion
        @param status: false = editando        true = navegando
        """
        self.actionPrint.setVisible( status )
        self.dtPicker.setReadOnly( status )
        self.txtobservaciones.setReadOnly( status )

        self.actionSave.setVisible( not status )
        self.actionCancel.setVisible( not status )
        self.tabnavigation.setEnabled( status )
        self.actionNew.setVisible( status )
        self.actionGoFirst.setVisible( status )
        self.actionGoPrevious.setVisible( status )
        self.actionGoNext.setVisible( status )
        self.actionGoLast.setVisible( status )
        self.actionPreview.setVisible( status )

        if status:
            self.swcuenta.setCurrentIndex( 1 )
            self.swconcepto.setCurrentIndex( 1 )
            self.swtipodoc.setCurrentIndex( 1 )
            self.tabledetails.setEditTriggers( 
                                          QAbstractItemView.NoEditTriggers )
        else:
            self.tabWidget.setCurrentIndex( 0 )
            self.txtobservaciones.setPlainText( "" )
            self.swcuenta.setCurrentIndex( 0 )
            self.swconcepto.setCurrentIndex( 0 )
            self.swtipodoc.setCurrentIndex( 0 )
            self.tabledetails.setEditTriggers( 
                          QAbstractItemView.EditKeyPressed |
                          QAbstractItemView.AnyKeyPressed |
                          QAbstractItemView.DoubleClicked )

    def updateModels( self ):
        """
        Recargar todos los modelos
        """
        try:
            if not self.database.isOpen():
                self.database.open()

            self.navmodel = QSqlQueryModel()
            self.navmodel.setQuery( """
            SELECT
                    d.iddocumento,
                    d.fechacreacion as Fecha,
                    CONCAT(cb.banco, ' ',cb.moneda,' [ ', cb.ncuenta,' ]') AS 'Cuenta Bancaria',
                    td.descripcion as 'Tipo Doc',
                    con.descripcion as Concepto,
                    d.Observacion,
                    cb.ncuenta
            FROM documentos d
            JOIN tiposdoc td ON td.idtipodoc=d.idtipodoc
            JOIN cuentasxdocumento cd ON cd.iddocumento = d.iddocumento
            JOIN vw_cuentasbancarias cb ON cb.idcuenta=cd.idcuenta
            LEFT JOIN conceptos con ON con.idconcepto = d.idconcepto
            WHERE td.modulo=%d
            ORDER BY d.iddocumento,d.fechacreacion DESC
                ; """ % constantes.IDCONTABILIDAD )

    #        El modelo que filtra a self.navmodel
            self.navproxymodel = QSortFilterProxyModel()
            self.navproxymodel.setSourceModel( self.navmodel )
            self.navproxymodel.setFilterKeyColumn( -1 )
            self.navproxymodel.setFilterCaseSensitivity ( Qt.CaseInsensitive )

    #        Este es el modelo con los datos de la tabla para navegar
            self.detailsmodel = QSqlQueryModel()
            self.detailsmodel.setQuery( """
            SELECT
                c.iddocumento,
                codigo AS 'Codigo',
                cc.descripcion AS 'Descripcion',
                 monto as 'Monto C$'
            FROM cuentasxdocumento c
            JOIN cuentascontables cc ON cc.idcuenta=c.idcuenta
            JOIN documentos d ON d.iddocumento = c.iddocumento
            JOIN tiposdoc td ON td.idtipodoc = d.idtipodoc AND td.modulo =3
            ORDER BY c.iddocumento,nlinea
            ;""" )

    #        Este es el filtro del modelo anterior
            self.detailsproxymodel = QSortFilterProxyModel()
            self.detailsproxymodel.setSourceModel( self.detailsmodel )

            self.mapper.setSubmitPolicy( QDataWidgetMapper.ManualSubmit )
            self.mapper.setModel( self.navproxymodel )
            self.mapper.addMapping( self.txtobservaciones, OBSERVACION )
            self.mapper.addMapping( self.txtconcepto, CONCEPTO )
            self.mapper.addMapping( self.txtcuenta, CUENTA )
            self.mapper.addMapping( self.txttipodoc, TIPODOC )
            self.mapper.addMapping( self.dtPicker, FECHA )


#        asignar los modelos a sus tablas
            self.tablenavigation.setModel( self.navproxymodel )
            self.tabledetails.setModel( self.detailsproxymodel )

            self.tabledetails.setColumnHidden( IDDOCUMENTO, True )
            self.tablenavigation.setColumnHidden( IDDOCUMENTO, True )
            self.tablenavigation.setColumnHidden( NCUENTA, True )
            self.tablenavigation.resizeColumnsToContents()
#            self.navigate( 'last' )
        except UserWarning as inst:
            logging.error( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(),
                                  unicode( inst ) )
        except Exception as inst:
            logging.critical( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(),
                                  u"Hubo un error al tratar de cargar "\
                                  + "los datos" )
        finally:
            if self.database.isOpen():
                self.database.close
