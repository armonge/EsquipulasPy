# -*- coding: utf-8 -*-
#TODO: Refactor, esta clase deberia de poder separse en una base y 2 clases 
#derivadas, una de estaas heredando de Base y la otra de QDialog
'''
Created on 25/05/2010
@author: Luis Carlos Mejia
'''
from PyQt4.QtCore import Qt, QTimer, pyqtSlot, QDateTime
from PyQt4.QtGui import QSortFilterProxyModel, QAbstractItemView, \
    QDataWidgetMapper, QMessageBox, qApp, QCompleter
from PyQt4.QtSql import QSqlQueryModel, QSqlQuery
from document.movimientosbancarios import MovimientosBancariosModel
from ui.Ui_frmmovimientosbancarios import Ui_frmMovimientosBancarios
from utility import constantes
from utility.accountselector import AccountsSelectorDelegate
from utility.base import Base
from utility.decorators import if_edit_model
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
        self.cbcuenta = SearchPanel( None, None, True )
        self.cbcuenta.lineEdit().setAlignment( Qt.AlignHCenter )
        self.cbcuenta.currentIndexChanged[int].connect( self.on_cbcuenta_currentIndexChanged )
        """
        @ivar: El combo con en el que se cargan las cuentas
        @type: SearcPanel
        """
        self.horizontalLayout_32.addWidget( self.cbcuenta )
        self.actionSave.setVisible( False )
        self.actionCancel.setVisible( False )
        self.cbconcepto.view().setMinimumHeight( 60 )
        self.dtPicker.setDateTime( QDateTime.currentDateTime() )

    @pyqtSlot( QDateTime )
    @if_edit_model
    def on_dtPicker_dateTimeChanged( self, datetime ):
        self.editmodel.fechaDoc = datetime

    @pyqtSlot( int )
    @if_edit_model
    def on_cbcuenta_currentIndexChanged( self, index ):
        self.editmodel.setData( self.editmodel.index( 0, 2 ),
                            [self.cuentasModel.record( index ).value( "idcuentacontable" ).toInt()[0],
                             self.cuentasModel.record( index ).value( "codigo" ).toString(),
                             self.cuentasModel.record( index ).value( "Cuenta Contable" ).toString()] )
#        self.accountseditdelegate.accounts.setFilterRegExp( "[^%d]" % self.cuentabancaria.record( index ).value( "idcuentacontable" ).toInt()[0] )

    def updateDetailFilter( self, _index ):
        self.detailsproxymodel.setFilterKeyColumn( IDDOCUMENTO )
        iddoc = self.navmodel.record( _index ).value( "iddocumento" ).toString()
        self.detailsproxymodel.setFilterRegExp( iddoc )

    def save( self ):
        self.editmodel.observacionesDoc = self.txtobservaciones.toPlainText()
        self.editmodel.lineasDoc = self.editmodel.lines
        self.editmodel.totalDoc = self.editmodel.lineasDoc[0].amount
        Base.save( self, True )

    @pyqtSlot( int )
    @if_edit_model
    def on_cbconcepto_currentIndexChanged( self, index ):
        """
        asignar la concepto al objeto self.editmodel
        """
        self.editmodel.conceptoId = self.conceptosModel.record( index ).value( "idconcepto" ).toInt()[0]

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
            self.editmodel.tipoDoc = constantes.IDDEPOSITO

            self.cuentasModel = QSqlQueryModel()
            self.cuentasModel.setQuery( """
            SELECT
                c.idcuentacontable,
                cc.codigo,
                cc.descripcion as 'Cuenta Contable',
                CONCAT(c.ctabancaria, ' [ ' , b.descripcion, ' - ', tm.simbolo, ' ]') as 'Cuenta Bancaria'
            FROM cuentasbancarias c
            JOIN bancos b ON b.idbanco = c.idbanco
            JOIN tiposmoneda tm ON tm.idtipomoneda= c.idtipomoneda
            JOIN cuentascontables cc ON cc.idcuenta = c.idcuentacontable
            ;
            """ )
            if self.cuentasModel.rowCount() == 0:
                raise UserWarning( "No existen cuentas bancarias en la base de datos,"\
                                        + " por favor cree una" )


            self.cbcuenta.setModelColumn(3)            
            self.cbcuenta.setModel(self.cuentasModel)
            self.cbcuenta.setCurrentIndex(-1)
            self.cbcuenta.tabla.setColumnHidden(0,True)
            #self.cbcuenta.tabla.setColumnHidden(1,True)
            #self.cbcuenta.tabla.setColumnHidden(2,True)
            
            self.txttipodoc.setText("Deposito")
            

            #            Rellenar el combobox de las CONCEPTOS
            self.conceptosModel = QSqlQueryModel()
            self.conceptosModel.setQuery( """
               SELECT idconcepto, descripcion 
               FROM conceptos c 
               WHERE idtipodoc = %d;
            """ % constantes.IDDEPOSITO )
            if self.conceptosModel.rowCount() == 0:
                raise UserWarning( "No existen conceptos para los depositos, por favor cree uno" )

            self.cbconcepto.setModel( self.conceptosModel )

            self.cbconcepto.setModel( self.conceptosModel )
            self.cbconcepto.setCurrentIndex( -1 )
            self.cbconcepto.setModelColumn( 1 )
            completerconcepto = QCompleter()
            completerconcepto.setCaseSensitivity( Qt.CaseInsensitive )
            completerconcepto.setModel( self.conceptosModel )
            completerconcepto.setCompletionColumn( 1 )

            self.editmodel.insertRow( 1 )
            self.editmodel.insertRow( 1 )
            self.editmodel.fechaDoc = QDateTime.currentDateTime()
            self.editmodel.autorId = self.user.uid
                #        Crea un edit delegate para las cuentas
            self.cuentasDelegate = AccountsSelectorDelegate( QSqlQuery( """
            SELECT c.idcuenta, c.codigo, c.descripcion
            FROM cuentascontables c
            WHERE c.idcuenta in (4,5,6)
            """ ) )
            self.tabledetails.setItemDelegate( self.cuentasDelegate )
            self.tabledetails.setModel( self.editmodel )

            self.tabledetails.setModel( self.editmodel )
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
#            self.swtipodoc.setCurrentIndex( 0 )
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
            self.detailsproxymodel.setFilterKeyColumn( IDDOCUMENTO )

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
