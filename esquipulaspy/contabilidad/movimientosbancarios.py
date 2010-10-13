# -*- coding: utf-8 -*-
'''
Created on 25/05/2010

@author: Luis Carlos Mejia
'''
from decimal import Decimal
import functools

from PyQt4.QtGui import QMainWindow, QDialog, QSortFilterProxyModel, QDataWidgetMapper, QAbstractItemView
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase
from PyQt4.QtCore import pyqtSignature, pyqtSlot, QDate, Qt, QTimer

from utility.base import Base
from utility.moneyfmt import moneyfmt
from utility.widgets.searchpanel import SearchPanel

from ui.Ui_dlgmovimientosbancarios import Ui_dlgMovimientosBancarios
from ui.Ui_frmmovimientosbancarios import Ui_frmMovimientosBancarios

from document.movimientosbancarios import MovimientosBancariosModel

IDDOCUMENTO, FECHA, CUENTA, TIPODOC, CONCEPTO, OBSERVACION, NCUENTA = range( 7 )
class FrmMovimientosBancarios( Ui_frmMovimientosBancarios, QMainWindow, Base ):
    def __init__( self, parent ):
        super( FrmMovimientosBancarios, self ).__init__( parent )

        self.setupUi( self )
        self.parentWindow = parent
        Base.__init__( self )


        self.__status = True

        self.cbcuenta = SearchPanel( None, None, True )
        self.horizontalLayout_32.addWidget( self.cbcuenta )


        self.actionSave.setVisible( False )
        self.actionCancel.setVisible( False )
        #        El modelo principal
        self.navmodel = QSqlQueryModel( self )
#        El modelo que filtra a self.navmodel
        self.navproxymodel = None
#        Este es el modelo con los datos de la con los detalles
        self.detailsmodel = QSqlQueryModel( self )
#        Este es el filtro del modelo anterior
        self.detailsproxymodel = RODetailsModel( self )
        self.detailsproxymodel.setSourceModel( self.detailsmodel )
        #inicializando el documento
        self.editmodel = None

        #general events
        self.actionGoFirst.triggered.connect( functools.partial( self.navigate, 'first' ) )
        self.actionGoPrevious.triggered.connect( functools.partial( self.navigate, 'previous' ) )
        self.actionGoNext.triggered.connect( functools.partial( self.navigate, 'next' ) )
        self.actionGoLast.triggered.connect( functools.partial( self.navigate, 'last' ) )

        QTimer.singleShot( 0, self.loadModels )


    def newDocument( self ):
        """
        activar todos los controles, llenar los modelos necesarios, 
        crear el modelo EntradaCompraModel, aniadir una linea a la tabla
        """
        if not QSqlDatabase.database().open():
            raise Exception( u"No se pudo establecer una conexión con la base de datos" )

        self.editmodel = MovimientosBancariosModel( self.user.uid )
        self.editmodel.datos.dateTime = self.dtPicker.dateTime()
        self.editmodel.setConceptos( self.cbconcepto, self.swconcepto )


        self.editmodel.setCuentasBancarias( self.cbcuenta, self.swcuenta )
        self.cbcuenta.currentIndexChanged[int].connect( self.on_cbcuenta_currentIndexChanged )

        self.editmodel.setTiposDoc( self.cbtipodoc, self.swtipodoc )
#        self.tabledetails.setModel(None)
#        self.tabledetails.setModel(self.detailsmodel)
        self.editmodel.setAccountTable( self.tabledetails )
        self.status = False

        if QSqlDatabase.database().isOpen():
            QSqlDatabase.database().close()

    def save( self ):
        if self.editmodel != None:

            self.editmodel.datos.observaciones = self.txtobservaciones.toPlainText()
            if self.editmodel.save():
                self.editmodel = None
                self.updateModels()
                self.status = True

    @pyqtSlot( "QDateTime" )
    def on_dtPicker_dateTimeChanged( self, datetime ):
        """
        Asignar la fecha al objeto __document
        """
        if self.editmodel != None:
            self.editmodel.datos.dateTime = datetime

    @pyqtSignature( "int" )
    def on_cbconcepto_currentIndexChanged( self, index ):
        """
        asignar la concepto al objeto self.editmodel
        """
        self.editmodel.conceptoChanged( index )

    def on_cbcuenta_currentIndexChanged( self, index ):
        """
        asignar la concepto al objeto self.editmodel
        """
#        self.btnguardar.setEnabled(True)
        self.editmodel.cuentaBancariaChanged( 
                     self.tabledetails, index, self.dtPicker,
                     self.cbconcepto, self.cbtipodoc )

    @pyqtSignature( "int" )
    def on_cbtipodoc_currentIndexChanged( self, index ):
        """
        asignar la concepto al objeto self.editmodel
        """
        self.editmodel.tipoDocChanged( self.cbconcepto, index )

    def setControls( self, status ):
        """
        @param status: false = editando        true = navegando
        """
        self.actionPrint.setVisible( status )
        self.dtPicker.setReadOnly( status )
        self.dtPicker.setMinimumDate( QDate( 1772, 1, 1 ) )
        self.dtPicker.setMaximumDate( QDate( 7999, 12, 31 ) )
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
#            self.navigate( 'last' )
            self.swcuenta.setCurrentIndex( 1 )
            self.swconcepto.setCurrentIndex( 1 )
            self.swtipodoc.setCurrentIndex( 1 )
            self.tabledetails.setEditTriggers( QAbstractItemView.NoEditTriggers )
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

    def updateDetailFilter( self, index ):
        self.detailsproxymodel.setFilterKeyColumn( IDDOCUMENTO )
        fecha = QDate.fromString( self.navmodel.record( 
                                   self.mapper.currentIndex() ).value( "Fecha" ).toString(),
                                    "dd/MM/yyyy" )
        self.dtPicker.setDate( fecha )
        self.detailsproxymodel.setFilterRegExp( 
                                   self.navmodel.record( index ).value( "iddocumento" ).toString() )
        self.tablenavigation.selectRow( self.mapper.currentIndex() )

    def updateModels( self ):
        """
        Recargar todos los modelos
        """
        try:
            if not QSqlDatabase.database().isOpen():
                QSqlDatabase.database().open()

            self.navmodel.setQuery( """
            SELECT
                    d.iddocumento,
                    DATE_FORMAT(d.fechacreacion,'%d/%m/%Y') as Fecha,
                    CONCAT(cb.banco, ' ',cb.moneda,' [ ', cb.ncuenta,' ]') as 'Cuenta Bancaria',
                    td.descripcion as 'Tipo Doc',
                    con.descripcion as Concepto,
                    d.Observacion,
                    cb.ncuenta
            FROM documentos d
            JOIN tiposdoc td ON td.idtipodoc=d.idtipodoc
            JOIN cuentasxdocumento cd ON cd.iddocumento = d.iddocumento
            JOIN vw_cuentasbancarias cb ON cb.idcuenta=cd.idcuenta
            LEFT JOIN conceptos con ON con.idconcepto = d.idconcepto
            WHERE td.modulo=3
            ORDER BY d.iddocumento,d.fechacreacion DESC
                ;
            """ )

    #        El modelo que filtra a self.navmodel
            self.navproxymodel = QSortFilterProxyModel( self )
            self.navproxymodel.setSourceModel( self.navmodel )
            self.navproxymodel.setFilterKeyColumn( -1 )
            self.navproxymodel.setFilterCaseSensitivity ( Qt.CaseInsensitive )
    #        Este es el modelo con los datos de la tabla para navegar
            self.detailsmodel = QSqlQueryModel( self )
            self.detailsmodel.setQuery( u"""
            SELECT
                c.iddocumento,
                Codigo AS 'Código',
                cc.descripcion AS 'Descripción',
                 monto as 'Monto C$'
            FROM cuentasxdocumento c
            JOIN cuentascontables cc ON cc.idcuenta=c.idcuenta
            JOIN documentos d ON d.iddocumento = c.iddocumento
            JOIN tiposdoc td ON td.idtipodoc = d.idtipodoc AND td.modulo =3
            ORDER BY c.iddocumento,nlinea
            ;
            """ )
    #        Este es el filtro del modelo anterior
            self.detailsproxymodel = RODetailsModel( self )
            self.detailsproxymodel.setSourceModel( self.detailsmodel )

            self.mapper.setSubmitPolicy( QDataWidgetMapper.ManualSubmit )
            self.mapper.setModel( self.navproxymodel )
            self.mapper.addMapping( self.txtobservaciones, OBSERVACION )
            self.mapper.addMapping( self.txtconcepto, CONCEPTO )
            self.mapper.addMapping( self.txtcuenta, CUENTA )
            self.mapper.addMapping( self.txttipodoc, TIPODOC )

#        asignar los modelos a sus tablas
            self.tablenavigation.setModel( self.navproxymodel )
            self.tabledetails.setModel( self.detailsproxymodel )
#
#
#
            self.tabledetails.setColumnHidden( IDDOCUMENTO, True )
#
            self.tablenavigation.setColumnHidden( IDDOCUMENTO, True )
            self.tablenavigation.setColumnHidden( NCUENTA, True )
            self.tablenavigation.resizeColumnsToContents()
            self.navigate( 'last' )

        except Exception as inst:
            print inst
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close

class dlgMovimientosBancarios( QDialog, Ui_dlgMovimientosBancarios ):

    def __init__( self, padre ):
        super( dlgMovimientosBancarios, self ).__init__( padre )

        self.setupUi( self )
        if not QSqlDatabase.database().open():
            raise Exception( u"No se pudo establecer una conexión con la base de datos" )


        self.editmodel = MovimientosBancariosModel( padre.user.uid )
        self.editmodel.idCuentaBanco = padre.editmodel.idCuentaContable
        self.editmodel.datos.delBanco = 1
        fecha = padre.editmodel.fechaConciliacion
        self.editmodel.datos.dateTime = fecha
        self.dtPicker.setMinimumDate( QDate( fecha.year(), fecha.month(), 1 ) )
        self.dtPicker.setMaximumDate( fecha )
        self.dtPicker.setDate( fecha )
        self.txtcuenta.setText( padre.txtbanco.text() + " " + padre.txtmoneda.text() + " [" + padre.txtcuentabanco.text() + "]" )

        lineaModel = self.editmodel.editmodel
        lineaModel.insertRows( 0 )
        lineaModel.lines[0].itemId = self.editmodel.idCuentaBanco
        lineaModel.lines[0].code = padre.txtcuenta.text()
        lineaModel.lines[0].name = padre.txtcuenta.toolTip()
        self.swcuenta.setCurrentIndex( 1 )

        self.editmodel.setConceptos( self.cbconcepto )
        self.cbconcepto.setEnabled( True )

        self.editmodel.setTiposDoc( self.cbtipodoc )
        self.cbtipodoc.setEnabled( True )
        self.editmodel.setAccountTable( self.tabledetails )

        self.buttonBox.accepted.connect( self.agregar )
        self.buttonBox.rejected.connect( self.reject )

        if QSqlDatabase.database().isOpen():
            QSqlDatabase.database().close()

    @pyqtSlot( "QDateTime" )
    def on_dtPicker_dateTimeChanged( self, datetime ):
        """
        Asignar la fecha al objeto __document
        """
        if self.editmodel != None:
            self.editmodel.datos.dateTime = datetime

    @pyqtSignature( "int" )
    def on_cbtipodoc_currentIndexChanged( self, index ):
        """
        asignar la concepto al objeto self.editmodel
        """
        self.editmodel.tipoDocChanged( self.cbconcepto, index )

    def on_cbcuenta_currentIndexChanged( self, index ):
        """
        asignar la concepto al objeto self.editmodel
        """
#        self.btnguardar.setEnabled(True)
        self.editmodel.cuentaBancariaChanged( self.tabledetails, index, self.dtPicker, self.cbconcepto, self.cbtipodoc )

    @pyqtSignature( "int" )
    def on_cbconcepto_currentIndexChanged( self, index ):
        """
        asignar la concepto al objeto self.editmodel
        """
        self.editmodel.conceptoChanged( index )

    def agregar( self ):
        self.editmodel.datos.observaciones = self.txtobservaciones.toPlainText()
        self.editmodel.datos.total = self.editmodel.editmodel.lines[0].amount
        if self.editmodel.valid:
            self.accept()


class RODetailsModel( QSortFilterProxyModel ):
    """
    El modelo que maneja la tabla en la que se previsualizan los datos,
    basicamente esta creado para darle formato al monto
    """
    def data( self, index, role = Qt.DisplayRole ):
        """
        Esta funcion redefine data en la clase base, es el metodo que se utiliza para mostrar los datos del modelo
        """
        value = QSortFilterProxyModel.data( self, index, role )


        if index.column() == 3 and role == Qt.DisplayRole:
            return moneyfmt( Decimal( value.toString() ), 4, "C$ " )
        return value


