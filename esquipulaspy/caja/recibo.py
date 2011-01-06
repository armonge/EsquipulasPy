# -*- coding: utf-8 -*-
'''
Created on 25/05/2010

@author: Luis Carlos Mejia
'''
from PyQt4.QtCore import pyqtSignature, pyqtSlot, Qt, QDateTime, QModelIndex, \
    QTimer
from PyQt4.QtGui import QDialog, QDataWidgetMapper, QSortFilterProxyModel, \
    QMessageBox, QAbstractItemView, QCompleter, qApp
from PyQt4.QtSql import QSqlQueryModel, QSqlQuery, QSqlDatabase
from decimal import Decimal
from document.recibo.abonomodel import AbonoModel, LineaAbono, AbonoDelegate
from document.recibo.recibodelegate import ReciboDelegate
from document.recibo.recibomodel import ReciboModel
from ui.Ui_dlgrecibo import Ui_dlgRecibo
from ui.Ui_recibo import Ui_frmRecibo
from utility import constantes
from utility.base import Base
from utility.moneyfmt import moneyfmt
from utility.movimientos import movAbonoDeCliente
import logging
from utility.decorators import if_edit_model

#from document.recibo.abonodelegate import AbonoDelegate
#from PyQt4.QtGui import QMainWindow

#controles
IDDOCUMENTO, FECHA, NDOCIMPRESO, NOMBRECLIENTE, TOTAL, CONCEPTO, NRETENCION, \
TASARETENCION, TOTALRETENCION, TOTALPAGADO, OBSERVACION, \
CONRETENCION, IDFACTURAS = range( 13 )

#table
IDDOCUMENTOT, DESCRIPCION, REFERENCIA, BANCO, MONTO, \
MONTODOLAR, IDMONEDA = range( 7 )

IDPAGO = 0
TOTALFAC = 3

IDRECIBODOC, NFAC, SALDO, TASAIVA, IDCLIENTE, SALDOFINAL = range( 6 )
class FrmRecibo( Ui_frmRecibo, Base ):
    """
    Implementacion de la interfaz grafica para entrada compra
    """
    web = "recibos.php?doc="

    def __init__( self, parent = None ):
        '''
        Constructor
        '''
        super( FrmRecibo, self ).__init__( parent )



#       las acciones deberian de estar ocultas
        self.frbotones.setVisible( False )
        self.actionSave.setVisible( False )
        self.actionCancel.setVisible( False )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#        El modelo principal
        self.navmodel = QSqlQueryModel( self )
#        El modelo que filtra a self.navmodel
        self.navproxymodel = RONavigationModel( self )
        self.navproxymodel.setSourceModel( self.navmodel )
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++        

#        Este es el modelo con los datos de la con los detalles
        self.detailsmodel = QSqlQueryModel( self )
#        Este es el filtro del modelo anterior
        self.detailsproxymodel = QSortFilterProxyModel( self )
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#        Este es el modelo con los datos de la con los detalles
        self.abonosmodel = QSqlQueryModel( self )
#        Este es el filtro del modelo anterior
        self.abonosproxymodel = QSortFilterProxyModel( self )
        self.abonosproxymodel.setSourceModel( self.abonosmodel )
        self.facturasmodel = QSqlQueryModel( self )
        self.facturasproxymodel = ROFacturasModel( self )
        self.facturasproxymodel.setSourceModel( self.facturasmodel )

        #inicializando el documento
        self.editmodel = None
        self.datosRecibo = None

        self.status = True

        QTimer.singleShot( 0, self.loadModels )

    def agregarFactura( self, i, n ):
#        modelo = cindex.model()
        modelo = self.facturasproxymodel
        self.abonoeditmodel.insertRows( i )
        self.abonoeditmodel.lines[i].idFac = modelo.index( n, 0 ).data()
        self.abonoeditmodel.lines[i].nFac = modelo.index( n, 1 ).data()
        monto = Decimal( modelo.data( modelo.index( n, 2 ), Qt.EditRole ).toString() )

        self.abonoeditmodel.lines[i].tasaIva = Decimal( modelo.data( modelo.index( n, 3 ), Qt.EditRole ).toString() )
        self.abonoeditmodel.lines[i].monto = monto
#        self.abonoeditmodel.lines[i].setMonto( monto)


        self.abonoeditmodel.lines[i].nlinea = n

        self.abonoeditmodel.lines[i].totalFac = monto
        self.tablefacturas.setRowHidden( n, True )

    def cancel( self ):
        """
        Aca se cancela la edicion del documento
        """
        self.status = True

    @property
    def printIdentifier( self ):
        return self.navmodel.record( self.mapper.currentIndex() ).value( "iddocumento" ).toString()

    def newDocument( self ):
        """
        activar todos los controles, llenar los modelos necesarios, crear el modelo EntradaCompraModel, aniadir una linea a la tabla
        """
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( u"No se pudo establecer la conexión"\
                                       + " con la base de datos" )

            self.facturasmodel.setQuery( """          
            SELECT
                s.iddocumento,
                s.ndocimpreso,
                s.Saldo,
                s.tasaiva,
                s.idpersona
            FROM vw_saldofacturas s
            WHERE s.saldo>0 and s.idestado = %d
            ;
        """ % constantes.CONFIRMADO )

            self.tablefacturas.setModel( self.facturasproxymodel )
            self.tablefacturas.setColumnHidden( IDDOCUMENTO, True )
#            self.tablefacturas.setColumnHidden( 3, True )

#            Rellenar el combobox de los CLLIENTES
            self.clientesModel = QSqlQueryModel()
            self.clientesModel.setQuery( """
            SELECT
            s.idpersona,
            s.nombre
            FROM vw_saldofacturas s
            WHERE s.idestado = %d
            GROUP BY s.idpersona
            HAVING SUM(s.saldo)>0
            ORDER BY s.nombre
            """ % constantes.CONFIRMADO )
#Verificar si existen clientes morosos            
            if self.clientesModel.rowCount() == 0:
                raise UserWarning( "No existen clientes morosos" )

#            Rellenar el combobox de las CONCEPTOS
            self.conceptosModel = QSqlQueryModel()
            self.conceptosModel.setQuery( """
               SELECT idconcepto, descripcion 
               FROM conceptos c 
               WHERE idtipodoc = %d;
            """ % constantes.IDRECIBO )
            if self.conceptosModel.rowCount() == 0:
                raise UserWarning( "No existen conceptos para los recibos,"\
                                        + " por favor cree uno" )



            self.cbcliente.setModel( self.clientesModel )
            self.cbcliente.setCurrentIndex( -1 )
            self.cbcliente.setModelColumn( 1 )
            completer = QCompleter()
            completer.setCaseSensitivity( Qt.CaseInsensitive )
            completer.setModel( self.clientesModel )
            completer.setCompletionColumn( 1 )


            self.cbconcepto.setModel( self.conceptosModel )
            self.cbconcepto.setCurrentIndex( -1 )
            self.cbconcepto.setModelColumn( 1 )
            completerconcepto = QCompleter()
            completerconcepto.setCaseSensitivity( Qt.CaseInsensitive )
            completerconcepto.setModel( self.conceptosModel )
            completerconcepto.setCompletionColumn( 1 )

            self.datosRecibo = DatosRecibo( self.parentWindow.datosSesion )
            self.editmodel = ReciboModel( self.datosRecibo.lineas, self.datosRecibo.datosSesion.tipoCambioBanco )
            self.abonoeditmodel = AbonoModel( self.datosRecibo.lineasAbonos )


            self.datosRecibo.cargarRetenciones( self.cbtasaret )

            if self.datosRecibo.retencionModel.rowCount() == 0:
                raise UserWarning( u"No existe ninguna tasa de retención."\
                                      + " Por favor contacte al administrador"\
                                      + " del sistema" )
# Asigno el modelo del recibo
            self.datosRecibo.cargarNumeros( self )

            self.tablefacturas.setSelectionMode( QAbstractItemView.SingleSelection )
            self.tablefacturas.setSelectionBehavior( QAbstractItemView.SelectRows )
            self.tableabonos.setModel( self.abonoeditmodel )
            self.tabledetails.setModel( self.editmodel )

# ASIGNO EL DELEGADO A LA TABLA DE LOS PAGO            
            delegate = ReciboDelegate()
            self.tabledetails.setItemDelegate( delegate )


# ASIGNO EL DELEGADO A LA TABLA DE LOS ABONOS
            delegado = AbonoDelegate()
            self.tableabonos.setItemDelegate( delegado )

            self.status = False
            self.frbotones.setVisible( True )
            self.updateFacturasFilter()

            self.abonoeditmodel.dataChanged[QModelIndex, QModelIndex].connect( self.updateLabels )
        except UserWarning as inst:
            logging.error( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(), unicode( inst ) )
        except Exception as inst:
            logging.critical( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(),
                                  u"Hubo un error al tratar de obtener los datos" )
        finally:
            if self.database.isOpen():
                self.database.close()


    def save( self ):
        """
        Slot documentation goes here.
        """
#        self.datosRecibo.lineasAbonos =self.abonoeditmodel.lines
#        self.datosRecibo.lineas = self.editmodel.lines
        self.datosRecibo.observaciones = self.txtobservaciones.toPlainText()
        if self.datosRecibo.valid( self ):
            if QMessageBox.question( self, qApp.organizationName(),
                                 u"¿Esta seguro que desea guardar el recibo?",
                                 QMessageBox.Yes | QMessageBox.No ) == QMessageBox.Yes:
                if not QSqlDatabase.database().isOpen():
                    QSqlDatabase.database().open()


                if self.datosRecibo.save():
                    QMessageBox.information( self,
                        qApp.organizationName() ,
                         u"""El documento se ha guardado con éxito""" )
                    self.editmodel = None
                    self.updateModels()
                    self.navigate( 'last' )
                    self.status = True
                else:
                    QMessageBox.critical( self,
                         qApp.organizationName(),
                         """Ha ocurrido un error al guardar el documento""" )

                if self.database.isOpen():
                    self.database.close()


    @pyqtSlot( bool )
    def on_btnadd_clicked( self, _on ):
        """
        Asignar el contenido al objeto documeto
        """
        cindex = self.tablefacturas.currentIndex()
        if not cindex.model() is None:
            if not self.tablefacturas.isRowHidden( cindex.row() ):
                i = self.abonoeditmodel.rowCount()
                self.agregarFactura( i, cindex.row() )
                self.updateLabels()



    @pyqtSlot( bool )
    def on_btnaddall_clicked( self, _on ):
        """
        Asignar el contenido al objeto documeto
        """
        i = self.abonoeditmodel.rowCount()
        for n in range( self.facturasproxymodel.rowCount() ):
            if not self.tablefacturas.isRowHidden( n ):
                self.agregarFactura( i, n )
                i = i + 1
        self.updateLabels()


    @pyqtSlot( bool )
    def on_btnremove_clicked( self, _on ):
        """
        Asignar el contenido al objeto documeto
        """
        r = self.tableabonos.currentIndex().row()
        if self.abonoeditmodel.rowCount() > 0 and r > -1:
            self.abonoeditmodel.removeRows( r, self.tablefacturas )
            self.updateLabels()

    @pyqtSlot( bool )
    def on_btnremoveall_clicked( self, _on ):
        """
        Asignar el contenido al objeto documeto
        """
        rows = self.abonoeditmodel.rowCount()
        if  rows > 0:
            self.abonoeditmodel.removeRows( 0, self.tablefacturas, rows )
            self.updateLabels()


    @pyqtSlot( int )
    @if_edit_model
    def on_cbcliente_currentIndexChanged( self, index ):
        """
        asignar proveedor al objeto self.editmodel
        """
        self.datosRecibo.clienteId = self.clientesModel.record( index ).value( "idpersona" ).toInt()[0] if index != -1 else - 1
        self.tableabonos.setEnabled( index != -1 )
        self.frbotones.setEnabled( index != -1 )
        self.abonoeditmodel.removeRows( 0, self.tablefacturas,
                                         self.abonoeditmodel.rowCount() )
        self.abonoeditmodel.idcliente = self.datosRecibo.clienteId
        self.updateFacturasFilter()
        self.updateLabels()

    @pyqtSlot( int )
    @if_edit_model
    def on_cbconcepto_currentIndexChanged( self, index ):
        """
        asignar la concepto al objeto self.editmodel
        """
        self.datosRecibo.conceptoId = self.conceptosModel.record( index ).value( "idconcepto" ).toInt()[0]

    @pyqtSlot( int )
    def on_cbtasaret_currentIndexChanged( self, index ):
        """
        asignar la retencion al objeto self.editmodel
        """
        self.datosRecibo.tasaRetencionCambio( self, index )
        if self.ckretener.isEnabled():
            self.updateLabels()

# MANEJO EL EVENTO  DE SELECCION EN EL RADIOBUTTON
    @pyqtSlot( bool )
    @if_edit_model
    def on_ckretener_toggled( self, on ):
        """
        """
        self.datosRecibo.aplicarRet = on
        self.cbtasaret.setEnabled( on )
        self.cbtasaret.setCurrentIndex( -1 )

    @pyqtSlot( QDateTime )
    def on_dtPicker_dateTimeChanged( self, datetime ):
        pass

    def removeLine( self ):
        """
        Funcion usada para borrar lineas de la tabla
        """
        index = self.tabledetails.currentIndex()

        if not index.isValid():
            return
        row = index.row()

        self.tabledetails.removeRows( row )
        self.updateLabels()


    def setControls( self, status ):
        """
        @param status: false = editando        true = navegando
        """
        self.actionPrint.setVisible( status )
        self.dtPicker.setReadOnly( True )
#        self.ckretener.setEnabled( ( not status ) )
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
        self.ckretener.setEnabled( False )

        if status:
            self.editmodel = None
            self.frbotones.setVisible( False )
            self.tablenavigation.setModel( self.navproxymodel )
            self.tabledetails.setModel( self.detailsproxymodel )
            self.tableabonos.setModel( self.abonosproxymodel )

            self.tabledetails.setColumnHidden( IDPAGO, True )
            self.tabledetails.setColumnHidden( IDMONEDA, True )
            self.tabledetails.setColumnHidden( IDDOCUMENTOT, True )

            self.swcliente.setCurrentIndex( 1 )
            self.swconcepto.setCurrentIndex( 1 )
            self.swtasaret.setCurrentIndex( 1 )
            self.tabledetails.setEditTriggers( QAbstractItemView.NoEditTriggers )
            self.tableabonos.setEditTriggers( QAbstractItemView.NoEditTriggers )
        else:
            self.tabWidget.setCurrentIndex( 0 )
            self.dtPicker.setDate( self.parentWindow.datosSesion.fecha )
            self.swcliente.setCurrentIndex( 0 )
            self.swconcepto.setCurrentIndex( 0 )
            self.swtasaret.setCurrentIndex( 0 )
            self.txtobservaciones.setPlainText( "" )
            self.lbltotalreten.setText( "US$ 0.0000" )
            self.lbltotal.setText( "US$ 0.0000" )
            self.lbltotalrecibo.setText( "US$ 0.0000" )
            self.cbcliente.setFocus()
            self.ckretener.setChecked( False )
            self.tabledetails.setEditTriggers( QAbstractItemView.EditKeyPressed | QAbstractItemView.AnyKeyPressed | QAbstractItemView.DoubleClicked )
            self.tableabonos.setEditTriggers( QAbstractItemView.EditKeyPressed | QAbstractItemView.AnyKeyPressed | QAbstractItemView.DoubleClicked )
            self.cbcliente.setCurrentIndex( -1 )


        self.tableabonos.setColumnHidden( IDDOCUMENTO, True )

        self.tabledetails.setColumnWidth( DESCRIPCION, 250 )
        self.tabledetails.setColumnWidth( MONTO, 150 )
        self.tabledetails.setColumnWidth( MONTODOLAR, 150 )
        self.tabledetails.setColumnWidth( REFERENCIA, 150 )


    def updateDetailFilter( self, index ):
        self.detailsproxymodel.setFilterKeyColumn( IDDOCUMENTOT )
        iddoc = self.navmodel.record( index ).value( "iddocumento" ).toString()
        self.detailsproxymodel.setFilterRegExp( iddoc )
        self.tablenavigation.selectRow( self.mapper.currentIndex() )
# FILTRO DE LOS ABONOS
        self.abonosproxymodel.setFilterKeyColumn( IDDOCUMENTOT )
        self.abonosproxymodel.setFilterRegExp( iddoc )
        self.tabledetails.resizeColumnsToContents()



    def updateFacturasFilter( self ):
        self.facturasproxymodel.setFilterKeyColumn( IDCLIENTE )
        self.facturasproxymodel.setFilterRegExp( "^" + str( self.datosRecibo.clienteId ) + "$" )


    def updateLabels( self ):
        #Asingar el total al modelo
        totalAbono = self.abonoeditmodel.total

        retener = self.datosRecibo.retencionValida

        if self.cbtasaret.currentIndex() > -1 or ( not self.ckretener.isEnabled() ):
            self.ckretener.setChecked( retener )
        self.ckretener.setEnabled( retener )
        self.cbtasaret.setEnabled( retener )

        ret = self.datosRecibo.obtenerRetencion
        self.editmodel.asignarTotal( totalAbono - ret )
        tasa = self.datosRecibo.datosSesion.tipoCambioBanco

        self.lbltotal.setText( moneyfmt( totalAbono, 4, "US$ " ) )
        self.lbltotal.setToolTip( moneyfmt( totalAbono * tasa, 4, "C$ " ) )

        self.lbltotalreten.setText( moneyfmt( ret, 4, "US$ " ) )
        self.lbltotalreten.setToolTip( moneyfmt( ret * tasa, 4, "C$ " ) )

        self.lbltotalrecibo.setText( moneyfmt( totalAbono - ret, 4, "US$ " ) )
        self.lbltotalrecibo.setToolTip( moneyfmt( ( totalAbono - ret ) * tasa, 4, "C$ " ) )



    def updateModels( self ):
        """
        Recargar todos los modelos
        """
        try:

            if not QSqlDatabase.database().isOpen():
                QSqlDatabase.database().open()
    #        El modelo principal
            query = """
        SELECT
                            padre.iddocumento,
                            DATE(padre.fechacreacion) as 'Fecha',
                            padre.ndocimpreso as 'No. Recibo',
                            p.nombre as 'Cliente',
                            padre.total + IFNULL(hijo.total,0) as 'Total',
                            c.descripcion as 'En cocepto de',
                            IF(hijo.ndocimpreso IS NULL,'-',hijo.ndocimpreso) as 'No. Retencion',
                            IF(ca.valorcosto IS NULL, '-',CONCAT(CAST(ca.valorcosto AS CHAR),'%s')) as 'Retencion',
                            IFNULL(hijo.total,'-') as 'Total Ret C$',
                            padre.total as 'Total Pagado', 
                           padre.observacion ,
                           IF(hijo.iddocumento IS NULL, 0,1) as 'Con Retencion',
                        GROUP_CONCAT('(',fac.iddocumento, ')' SEPARATOR '') as idfacturas
            FROM documentos padre
            JOIN docpadrehijos phfac ON phfac.idhijo = padre.iddocumento
            JOIN documentos fac ON phfac.idpadre = fac.iddocumento AND fac.idtipodoc = %d
            JOIN personasxdocumento pxd ON pxd.iddocumento = padre.iddocumento
            JOIN personas p ON p.idpersona = pxd.idpersona
            JOIN conceptos c ON  c.idconcepto=padre.idconcepto
            LEFT JOIN costosxdocumento cd ON cd.iddocumento=padre.iddocumento
            LEFT JOIN  costosagregados ca ON ca.idcostoagregado=cd.idcostoagregado
            LEFT JOIN docpadrehijos ph ON  padre.iddocumento=ph.idpadre
            LEFT JOIN documentos hijo ON hijo.iddocumento=ph.idhijo
            WHERE padre.idtipodoc=%d
            AND p.tipopersona=%d
            GROUP BY padre.iddocumento
            ORDER BY padre.iddocumento;
            """ % ( '%', constantes.IDFACTURA, constantes.IDRECIBO, constantes.CLIENTE )
    
            self.navmodel.setQuery( query )
    
    # Proxy model que se utilizara desde el formulario de facturacion SOLAMENTE
            self.remoteProxyModel = QSortFilterProxyModel()
            self.remoteProxyModel.setSourceModel( self.navmodel )
            self.remoteProxyModel.setFilterKeyColumn( IDFACTURAS )
            self.remoteProxyModel.setFilterRegExp( '' )
    
    
    
            self.navproxymodel = RONavigationModel( self )
            self.navproxymodel.setSourceModel( self.remoteProxyModel )
            self.navproxymodel.setFilterKeyColumn( -1 )
            self.navproxymodel.setFilterCaseSensitivity ( Qt.CaseInsensitive )
    
    #        Este es el modelo con los datos de la tabla para navegar
    #FIXME: Se el simbolo de la moneda deberia de salir desde la tabla tiposmoneda    
            self.detailsmodel.setQuery( """
                SELECT
                p.iddocumento,
                CONCAT(tp.descripcion, ' ' , tm.moneda) as 'Tipo de Pago',
                 p.refexterna as 'No. Referencia',
                 b.descripcion as Banco,
                 CONCAT(tm.simbolo,' ',FORMAT(monto,4)) as 'Monto',
                 CONCAT('US$ ',FORMAT(monto / IF(p.idtipomoneda=2,1,IFNULL(tc.tasaBanco,tc.tasa)),4)) as 'Monto US$'
            FROM movimientoscaja p
            JOIN documentos d ON d.iddocumento=p.iddocumento AND d.idtipodoc=18
            JOIN tiposcambio tc ON tc.idtc=d.idtipocambio
            JOIN tiposmoneda tm ON tm.idtipomoneda=p.idtipomoneda
            JOIN tiposmovimientocaja tp ON tp.idtipomovimiento=p.idtipomovimiento
            LEFT JOIN bancos b ON b.idbanco = p.idbanco
            ORDER BY p.nlinea
            ;
            """ )
    
    #        Este es el filtro del modelo anterior
            self.detailsproxymodel = QSortFilterProxyModel( self )
            self.detailsproxymodel.setSourceModel( self.detailsmodel )
            self.detailsproxymodel.setFilterKeyColumn( IDDOCUMENTOT )
            self.detailsproxymodel.setFilterRegExp( '^0$' )
    # ESTE ES EL MODELO CON LOS DATOS DE Los ABONOS PARA NAVEGAR
            self.abonosmodel = QSqlQueryModel( self )
            self.abonosmodel.setQuery( """
           SELECT
            d.idhijo as idrecibo,
            padre.ndocimpreso as 'No. Factura',
            CONCAT('US$ ',FORMAT(d.monto,4)) as 'Saldo'
            FROM docpadrehijos d
            JOIN documentos padre ON d.idpadre=padre.iddocumento
            WHERE padre.idtipodoc=%d and d.monto is not null
            ORDER BY d.nlinea
    ;
            """ % constantes.IDFACTURA )
    
    #        Este es el filtro del modelo anterior
            self.abonosproxymodel.setSourceModel( self.abonosmodel )
    
    
    #        Este objeto mapea una fila del modelo self.navproxymodel a los controles
            self.mapper.setSubmitPolicy( QDataWidgetMapper.ManualSubmit )
            self.mapper.setModel( self.navproxymodel )
            self.mapper.addMapping( self.lblnrec, NDOCIMPRESO , "text" )
            self.mapper.addMapping( self.lblnreten, NRETENCION , "text" )
    
            self.mapper.addMapping( self.txtobservaciones, OBSERVACION )
            self.mapper.addMapping( self.dtPicker, FECHA )
            self.mapper.addMapping( self.txtcliente, NOMBRECLIENTE, "text" )
            self.mapper.addMapping( self.txtconcepto, CONCEPTO, "text" )
            self.mapper.addMapping( self.lbltotalreten, TOTALRETENCION, "text" )
            self.mapper.addMapping( self.txttasaret, TASARETENCION, "text" )
            self.mapper.addMapping( self.lbltotal, TOTAL, "text" )
            self.mapper.addMapping( self.lbltotalrecibo, TOTALPAGADO, "text" )
            self.mapper.addMapping( self.ckretener, CONRETENCION, "checked" )
    
            self.tablenavigation.setColumnHidden( 0, True )
            self.tablenavigation.setColumnHidden( TOTALRETENCION, True )
            self.tablenavigation.setColumnHidden( CONRETENCION, True )
            
#            self.tabledetails.resizeColumnsToContents()

        except Exception as inst:
            pass
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()



class DlgRecibo( Ui_dlgRecibo, QDialog ):
    def __init__( self, factura, readOnly = False ):
        super( DlgRecibo, self ).__init__( factura )
#        self.setModal(True)
        self.editmodel = None
        self.setupUi( self )
        self.readOnly = readOnly
        self.setControls( readOnly, factura )



    def accept( self ):
        if self.readOnly:
            return super( DlgRecibo, self ).accept()

        if self.datosRecibo.valid( self ):
            return super( DlgRecibo, self ).accept()
        else:
            self.setResult( -1 )


    def setControls( self, status, factura ):
        """
        @param status: false = editando        true = navegando
        """
#        self.txtcliente.setReadOnly( status )
        self.ckretener.setEnabled( not status )
        self.txtobservaciones.setReadOnly( status )
        self.readOnly = status
        self.lbltotal.setText( factura.lbltotal.text() )
        if status:
            self.tabledetails.setEditTriggers( QAbstractItemView.NoEditTriggers )
            self.swtasaret.setCurrentIndex( 1 )
            self.buttonBox.buttons()[1].setHidden( True )
        else:
            self.txtcliente.setText( factura.cbcliente.currentText() )
            self.totalFactura = Decimal( 0 )
            self.lbltotal.setText( factura.lbltotal.text() )
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open():
                    raise Exception( u"No se pudo establecer la conexión con la base de datos" )

                QMessageBox.warning( None,
                qApp.organizationName(),
                """Hubo un error al conectarse con la base de datos""",
                QMessageBox.StandardButtons( \
                    QMessageBox.Ok ),
                QMessageBox.Ok )
            else:
                self.datosRecibo = DatosRecibo( factura.editmodel.datosSesion )
                self.datosRecibo.cargarNumeros( self )
                self.datosRecibo.cargarRetenciones( self.cbtasaret )
                delegado = ReciboDelegate()

            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()

            self.editmodel = ReciboModel( self.datosRecibo.lineas, self.datosRecibo.datosSesion.tipoCambioBanco )
            self.editmodel.insertRow( 0 )
            linea = self.editmodel.lines[0]
            linea.pagoId = 0
            linea.monedaId = 0
            linea.pagoDescripcion = ""
            linea.nref = ""
            linea.monto = factura.editmodel.total
            linea.montoDolar = factura.editmodel.total
            index = self.editmodel.index( 0, MONTO )
            self.editmodel.dataChanged.emit( index, index )

            self.lblfecha.setText( self.datosRecibo.datosSesion.fecha.toString( "dd/MM/yyyy" ) )

            self.tabledetails.setModel( self.editmodel )
            self.tabledetails.setColumnHidden( IDPAGO, True )
#            self.tabledetails.setColumnHidden(IDMONEDA,True)



            self.tabledetails.setColumnWidth( DESCRIPCION, 200 )
            self.tabledetails.setItemDelegate( delegado )
            self.tabledetails.setEditTriggers( QAbstractItemView.EditKeyPressed | QAbstractItemView.AnyKeyPressed | QAbstractItemView.DoubleClicked )
            self.swtasaret.setCurrentIndex( 0 )
            self.datosRecibo.clienteId = factura.editmodel.clienteId
            self.datosRecibo.conceptoId = 1

            linea = LineaAbono( self )
            linea.idFac = 1
            linea.tasaIva = factura.editmodel.ivaTasa
            linea.monto = factura.editmodel.total
            self.totalFactura = factura.editmodel.total
            self.editmodel.total = self.totalFactura

            self.datosRecibo.lineasAbonos.append( linea )


    @pyqtSignature( "bool" )
    def on_ckretener_toggled( self, on ):
        """
        """
        if self.editmodel != None:
            self.datosRecibo.aplicarRet = on
            self.cbtasaret.setEnabled( on )
            self.cbtasaret.setCurrentIndex( -1 )

    @pyqtSlot( "int" )
    def on_cbtasaret_currentIndexChanged( self, index ):
        """
        asignar la retencion al objeto self.editmodel
        """
        if self.editmodel != None:
            self.datosRecibo.tasaRetencionCambio( self, index )
            if self.ckretener.isEnabled():
                self.updateLabels()

#    def updateLabels( self ):
#        if not self.readOnly:
#            self.lbltotalreten.setText( moneyfmt( self.datosRecibo.obtenerRetencion, 4, "US$" ) )
#            self.lbltotalrecibo.setText(moneyfmt(self.datosRecibo.totalPagado))
##            self.tabledetails.resizeColumnsToContents()
    def updateLabels( self ):
        #Asingar el total al modelo
        totalAbono = self.totalFactura

        retener = self.datosRecibo.retencionValida

        if self.cbtasaret.currentIndex() > -1 or ( not self.ckretener.isEnabled() ):
            self.ckretener.setChecked( retener )
        self.ckretener.setEnabled( retener )

        ret = self.datosRecibo.obtenerRetencion
        self.editmodel.asignarTotal( totalAbono - ret )
        tasa = self.datosRecibo.datosSesion.tipoCambioBanco

        self.lbltotal.setText( moneyfmt( totalAbono, 4, "US$ " ) )
        self.lbltotal.setToolTip( moneyfmt( totalAbono * tasa, 4, "C$ " ) )

        self.lbltotalreten.setText( moneyfmt( ret, 4, "US$ " ) )
        self.lbltotalreten.setToolTip( moneyfmt( ret * tasa, 4, "C$ " ) )

        self.lbltotalrecibo.setText( moneyfmt( totalAbono - ret, 4, "US$ " ) )
        self.lbltotalrecibo.setToolTip( moneyfmt( ( totalAbono - ret ) * tasa, 4, "C$ " ) )



class DatosRecibo( object ):
    def __init__( self, datosSesion ):
        object.__init__( self )

        self.__documentType = 18
        self.clienteId = 0
        self.observaciones = ""
        self.aplicarRet = True

        self.lineas = []
        self.lineasAbonos = []
        self.numeroImpreso = ''

        self.conceptoId = 0
        self.datosSesion = datosSesion
        self.retencionId = 0
        self.retencionTasa = Decimal( 0 )
        self.retencionNumeroImpreso = ''


    @property
    def total( self ):
        """
        """
        tmpsubtotal = sum( [linea.monto for linea in self.lineasAbonos] )
        return tmpsubtotal if tmpsubtotal > 0 else Decimal( 0 )

    @property
    def subtotal( self ):
        """
        """
        tmpsubtotal = sum( [linea.subMonto for linea in self.lineasAbonos] )
        return tmpsubtotal if tmpsubtotal > 0 else Decimal( 0 )

    @property
    def totalPagado( self ):
        """
    
        """
        return self.total - self.obtenerRetencion




    def valid( self, recibo ):
        """
        Un documento es valido cuando 
        self.printedDocumentNumber != ""
        self.providerId !=0
        self.validLines >0
        self.__idIVA !=0
        self.uid != 0
        self.warehouseId != 0 
        """

        if int( self.clienteId ) == 0:
            try:
                recibo.cbcliente.setFocus()
            except:
                pass
            QMessageBox.information( None, "Guardar Recibo", "No existe un cliente seleccionado" )
        elif int( self.conceptoId ) == 0:
            try:
                recibo.cbconcepto.setFocus()
            except:
                pass
            QMessageBox.information( None, "Guardar Recibo", "No hay un concepto" )
        elif self.aplicarRet and int( self.retencionId ) == 0:
                recibo.cbtasaret.setFocus()
                QMessageBox.information( None, "Guardar Recibo", "No hay tasa de retencion" )
        elif self.datosSesion.tipoCambioBanco == 0:
            QMessageBox.information( None, "Guardar Recibo", "no hay un tipo de cambio para la fecha" + self.datosSesion.fecha )
        elif int( self.datosSesion.usuarioId ) == 0:
            raise Exception( "No hay un usuario" )
        elif  self.printedDocumentNumber == "":
            raise Exception( "No existe numero de doc impreso" )
        else:
            foo = 0
            for line in self.lineas:
                foo += 1
                if not line.valid:
                    recibo.tabledetails.selectRow( foo - 1 )
                    QMessageBox.information( None, "Guardar Recibo", u"La linea " + str( foo ) + u" de los pagos esta incompleta. " + line.error )
                    return False
            if len( self.lineasAbonos ) == 0:
                QMessageBox.information( None, "Guardar Recibo", u"Por favor elija al menos una factura a la que se realizará el abono" )
                return False

            foo = 0
            for line in self.lineasAbonos:
                foo += 1

                if not line.valid:
                    QMessageBox.information( None, "Guardar Recibo", u"La linea " + str( foo ) + u" de las facturas abonadas no es válida" )
                    return False


            return True
        return False

    @property
    def retencionValida( self ):
        subtotal = self.subtotal
        subtotalC = subtotal * self.datosSesion.tipoCambioBanco
        return subtotalC > 1000

    @property
    def obtenerRetencion( self ):
        if self.aplicarRet:

            if not self.retencionValida:
                self.aplicarRet = False
                self.retencionId = 0
                return Decimal( 0 )
            else:
                return ( self.subtotal * ( self.retencionTasa / Decimal( 100 ) ) )
        else:
            return Decimal( 0 )

    @property
    def obtenerGanancia( self ):
        total = self.total
        retencion = self.obtenerRetencion
        return Decimal( str( round( ( total + retencion ) * ( self.datosSesion.tipoCambioBanco - self.datosSesion.tipoCambioOficial ), 4 ) ) )

    @property
    def validLines( self ):
        """
        la cantidad de lineas validas que hay en el documento
        """
        foo = 0
        for line in self.lineas:
            if line.valid:foo += 1
        return foo

    def save( self, sinFactura = True ):
        """
        Este metodo guarda el documento actual en la base de datos
        """

        if not self.valid:
            raise Exception( "El documento a salvar no es valido" )

        query = QSqlQuery()

        try:

            if sinFactura:
                if not QSqlDatabase.database().transaction():
                    raise Exception( u"No se pudo comenzar la transacción" )

            fechaCreacion = self.datosSesion.fecha.toString( 'yyyyMMdd' ) + QDateTime.currentDateTime().toString( "hhmmss" )
    #INSERTAR RECIBO
            query.prepare( """
            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc, observacion,total,idtipocambio,idconcepto,idcaja) 
            VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:observacion,:total,:idtc,:concepto,:caja)
            """ )
            query.bindValue( ":ndocimpreso", self.printedDocumentNumber )
            query.bindValue( ":fechacreacion", fechaCreacion )
            query.bindValue( ":idtipodoc", self.__documentType )
            query.bindValue( ":observacion", self.observaciones )
            totalPagado = self.totalPagado
            query.bindValue( ":total", totalPagado.to_eng_string() )

            query.bindValue( ":idtc", self.datosSesion.tipoCambioId )
            query.bindValue( ":concepto", self.conceptoId )
            query.bindValue( ":caja", self.datosSesion.cajaId )

            if not query.exec_():
                raise Exception( "No se pudo insertar el recibo" )
            insertedId = query.lastInsertId().toString()


    #INSERTAR LA RELACION CON LA SESION DE CAJA            
            query.prepare( """
                INSERT INTO docpadrehijos (idpadre,idhijo)
                VALUES (:idsesion,:idrecibo)
                """ )

            query.bindValue( ":idsesion", self.datosSesion.sesionId )
            query.bindValue( ":idrecibo", insertedId )

            if not query.exec_():
                raise Exception( "No se Inserto la relacion entre la sesion de caja y el recibo" )


    #INSERTAR LA RELACION CON El USUARIO y EL CLIENTE

            query.prepare( 
                "INSERT INTO personasxdocumento (iddocumento,idpersona,idaccion) VALUES" +
                "(" + insertedId + ",:iduser,:autor),"
                "(" + insertedId + ",:idcliente,:cliente)"
                )

            query.bindValue( ":iduser", self.datosSesion.usuarioId )
            query.bindValue( ":autor", constantes.AUTOR )
            query.bindValue( ":idcliente", self.clienteId )
            query.bindValue( ":usuario", constantes.CLIENTE )


            if not query.exec_():
                raise Exception( "No se Inserto la relacion entre el recibo y las personas" )

    #INSERTAR LOS TIPOS DE PAGO

            if len( self.lineas ) == 0:
                raise Exception( "Deben existir pagos" )

            i = 1
            for linea in self.lineas:
    #                    print insertedId + "-" + str(linea.pagoId) + "-" + str(linea.monedaId)
                linea.save( insertedId, i )
                i = i + 1
    #INSERTAR los abonos
            i = 0

            if len( self.lineasAbonos ) == 0:
                raise Exception( "Deben existir abonos" )

            for l in self.lineasAbonos:
                l.save( insertedId, i )
                i = i + 1

    #VERIFICO SI se aplicara la retencion                     
            if self.aplicarRet :

    #INSERTAR EL DOCUMENTO RETENCION CON EL TOTAL EN NEGATIVO, PORQUE ESTA SALIENDO DE CAJA            
                query.prepare( """
                INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,total,idtipocambio,idconcepto) 
                VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:total,:idtc,:concepto)
                """ )
                query.bindValue( ":ndocimpreso", self.retencionNumeroImpreso )
                query.bindValue( ":fechacreacion", fechaCreacion )
                query.bindValue( ":idtipodoc", constantes.IDRETENCION )
                query.bindValue( ":total", self.obtenerRetencion.to_eng_string() )
                query.bindValue( ":idtc", self.datosSesion.tipoCambioId )
                query.bindValue( ":concepto", self.conceptoId )
                if not query.exec_():
                    raise Exception( "No se Inserto la retencion" )

                idret = query.lastInsertId().toString()

                query.prepare( "INSERT INTO docpadrehijos (idpadre,idhijo) VALUES" +
                "(:idsesion," + idret + ")," +
                "(:idrecibo," + idret + ")" )

                query.bindValue( ":idsesion", self.datosSesion.sesionId )
                query.bindValue( ":idrecibo", insertedId )

                if not query.exec_():
                    raise Exception( "No se Inserto la relacion entre la retencion y el recibo" )


    # INSERTAR EL ID DEL COSTO RETENCION                
                query.prepare( """
                INSERT INTO costosxdocumento (iddocumento, idcostoagregado) VALUES( :iddocumento, :idcostoagregado )
                """ )
                query.bindValue( ":iddocumento", insertedId )
                query.bindValue( ":idcostoagregado", self.retencionId )
                if not query.exec_():
                    raise Exception( "el costo Retencion  NO SE INSERTO" )


            #manejar las cuentas contables
            tasa = self.datosSesion.tipoCambioOficial
            movAbonoDeCliente( insertedId, self.total * tasa, self.obtenerRetencion * tasa, self.obtenerGanancia )

            if sinFactura:
                if not QSqlDatabase.database().commit():
                    raise Exception( "No se pudo hacer commit" )
        except Exception as inst:
            QSqlDatabase.database().rollback()
            return False

        return True

    def cargarRetenciones( self, cbtasaret ):
#            Rellenar el combobox de las retenciones
            self.retencionModel = QSqlQueryModel()
            self.retencionModel.setQuery( """
                    SELECT 
                        idcostoagregado, 
                        FORMAT(valorcosto,0) as tasa
                    FROM costosagregados 
                    WHERE 
                    (idtipocosto=%d OR idtipocosto =%d) AND 
                    activo=1 
                    ORDER BY valorcosto desc; 
                    """ % ( constantes.RETENCIONPROFESIONALES, constantes.RETENCIONFUENTE ) )

            cbtasaret.setModel( self.retencionModel )
            cbtasaret.setModelColumn( 1 )
            cbtasaret.setCurrentIndex( -1 )
            self.retencionId = 0

    def cargarNumeros( self, recibo ):
#            Cargar el numero de el Recibo actual
        idrec = str( constantes.IDRECIBO )
        idret = str( constantes.IDRETENCION )
        query = QSqlQuery( "CALL spConsecutivo(" + idrec + ",null)" )
        if not query.exec_():
            print( query.lastError().text() )
        query.first()
        n = query.value( 0 ).toString()

        recibo.lblnrec.setText( n )
        self.printedDocumentNumber = n

        query = QSqlQuery( "CALL spConsecutivo(" + idret + ",null)" )
        if not query.exec_():
            print( query.lastError().text() )
        query.first()
        n = query.value( 0 ).toString()
        recibo.lblnreten.setText( n )
        self.retencionNumeroImpreso = n


    def tasaRetencionCambio( self, _recibo, index ):
        self.retencionId = self.retencionModel.record( index ).value( "idcostoagregado" ).toInt()[0]
        value = self.retencionModel.record( index ).value( "tasa" ).toString()
        self.retencionTasa = Decimal( value if value != "" else 0 )



class RONavigationModel( QSortFilterProxyModel ):
    """
    basicamente le da formato a la salida de mapper
    """
    def data( self, index, role = Qt.DisplayRole ):
        """
        Esta funcion redefine data en la clase base, es el metodo que se utiliza para mostrar los datos del modelo
        """
        value = QSortFilterProxyModel.data( self, index, role )
        if value.isValid() and role in ( Qt.EditRole, Qt.DisplayRole , Qt.TextAlignmentRole ):
            if index.column() in ( TOTAL, TOTALPAGADO, TOTALRETENCION ) :
                if role in ( Qt.EditRole, Qt.DisplayRole ):
                    value = value.toString()
                    return moneyfmt( Decimal( value if value != "-" else 0 ), 4, "US$" )
                elif role == Qt.TextAlignmentRole:
                    return Qt.AlignHCenter | Qt.AlignVCenter

        return value

class ROFacturasModel( QSortFilterProxyModel ):
    """
    El modelo que maneja la tabla en la que se previsualizan los os,
    basicamente esta creado para darle formato al total y al MONTO
    """
    def __init__( self, _dbcursor = None ):
        super( ROFacturasModel, self ).__init__()

    def columnCount( self, _index = QModelIndex() ):
        return 4

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int( Qt.AlignLeft | Qt.AlignVCenter )
            return int( Qt.AlignRight | Qt.AlignVCenter )
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if  section == NFAC:
                return u"No. Factura"
            elif section == SALDO:
                return "Saldo"
            elif section == TASAIVA:
                return "Tasa Iva"
        return int( section + 1 )


    def data( self, index, role = Qt.DisplayRole ):
        """
        Esta funcion redefine data en la clase base, es el metodo que se utiliza para mostrar los datos del modelo
        """
        value = QSortFilterProxyModel.data( self, index, role )
        if value.isValid() and role == Qt.DisplayRole:
            if index.column() == SALDO:
                return moneyfmt( Decimal( value.toString() ), 4, "US$ " )
        return value

