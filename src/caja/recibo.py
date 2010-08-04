# -*- coding: utf-8 -*-
'''
Created on 25/05/2010

@author: Luis Carlos Mejia
'''
from PyQt4.QtGui import QMainWindow,QDialog, QDataWidgetMapper, QSortFilterProxyModel, QMessageBox, QAbstractItemView, QCompleter
from PyQt4.QtCore import pyqtSignature, pyqtSlot, Qt, QDateTime, SIGNAL, QModelIndex, QTimer
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase

from decimal import Decimal
import functools
from PyQt4.QtSql import  QSqlQuery
from utility.movimientos import movAbonoDeCliente
from utility.base import Base
from ui.Ui_recibo import Ui_frmRecibo
from ui.Ui_dlgrecibo import Ui_dlgRecibo
from document.recibo.recibodelegate import ReciboDelegate
from document.recibo.abonodelegate import AbonoDelegate
from document.recibo.recibomodel import ReciboModel
from document.recibo.abonomodel import AbonoModel,LineaAbono
from utility.moneyfmt import moneyfmt
from utility.reports import frmReportes
from utility.constantes import IDRECIBO,IDRETENCION
#from PyQt4.QtGui import QMainWindow

#controles
IDDOCUMENTO, NDOCIMPRESO, OBSERVACION, TOTAL, FECHA, CONCEPTO, CLIENTE, NRETENCION, TASARETENCION, TOTALRETENCION, OBSERVACIONRET, CONRETENCION = range( 12 )

#table
IDDOCUMENTOT, DESCRIPCION, REFERENCIA, MONTO,MONTODOLAR,IDMONEDA = range( 6 )
IDPAGO=0
TOTALFAC=3
IDRECIBODOC, NFAC, ABONO = range( 3 )
class frmRecibo( Ui_frmRecibo, QMainWindow, Base ):
    """
    Implementacion de la interfaz grafica para entrada compra
    """


    def __init__( self, user, parent ):
        '''
        Constructor
        '''
        super( frmRecibo, self ).__init__( parent )
        self.setupUi( self )
        self.parentWindow = parent
        Base.__init__( self )

        self.__status = True

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
        self.detailsproxymodel = RODetailsModel( self )
        self.detailsproxymodel.setSourceModel( self.detailsmodel )
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#        Este es el modelo con los datos de la con los detalles
        self.abonosmodel = QSqlQueryModel( self )
#        Este es el filtro del modelo anterior
        self.abonosproxymodel = ROAbonosModel( self )
        self.abonosproxymodel.setSourceModel( self.abonosmodel )



        #inicializando el documento
        self.editmodel = None
        self.datosRecibo=None



#        #general events
#        self.connect( self.actionEditCell, SIGNAL( "triggered()" ), self.editCell )
#        self.connect( self.actionDeleteRow, SIGNAL( "triggered()" ), self.removeLine )
#        self.connect( self.actionGoFirst, SIGNAL( "triggered()" ), functools.partial( self.navigate, 'first' ) )
#        self.connect( self.actionGoPrevious, SIGNAL( "triggered()" ), functools.partial( self.navigate, 'previous' ) )
#        self.connect( self.actionGoNext, SIGNAL( "triggered()" ), functools.partial( self.navigate, 'next' ) )
#        self.connect( self.actionGoLast, SIGNAL( "triggered()" ), functools.partial( self.navigate, 'last' ) )

        QTimer.singleShot( 0, self.loadModels )

        # manejador de evento de los radio boton
#        self.connect( self.rbcontado, SIGNAL( "toggled(bool)" ), self.creditocontado)
#        self.connect( self.rbcredito, SIGNAL( "toggled(bool)" ), self.creditocontado )
#
#        QTimer.singleShot( 0, self.loadModels )
#
#
#
#    def creditocontado(self,on):
#        """
#        Asignar el 1 si es al contado, 0 si es al credito
#        """
#        print("hola")
#        if not self.editmodel is None:
#            self.editmodel.escontado = 1 if self.rbcontado.isChecked() else 0
#            print(str(self.editmodel.escontado))


# MANEJO EL EVENTO  DE SELECCION EN EL RADIOBUTTON
    @pyqtSignature( "bool" )
    def on_ckretener_toggled( self, on ):
        """
        """
        self.datosRecibo.retencionAplicada(self,on)

    @pyqtSignature( "" )
    def on_txtobservaciones_textChanged( self ):
        """
        Asignar las observaciones al objeto __document
        """
        if not self.editmodel is None:
            self.editmodel.observaciones = self.txtobservaciones.toPlainText()



    def updateModels( self ):
        """
        Recargar todos los modelos
        """

        try:

            if not QSqlDatabase.database().isOpen():
                QSqlDatabase.database().open()


#        El modelo principal

            self.navmodel.setQuery( """
            SELECT
                            padre.iddocumento,
                            padre.ndocimpreso as 'No. Recibo',
                            padre.observacion as 'Recibimos de',
                            padre.total as 'Total C$',
                            DATE(padre.fechacreacion) as 'El dia',
                            c.descripcion as 'En cocepto de',
                            p.nombre as 'Al Cliente',
                            IF(hijo.ndocimpreso IS NULL,'-',hijo.ndocimpreso) as 'No. Retencion',
                            CONCAT(valorcosto,'%') as 'Retencion',
                           IF(hijo.total IS NULL, '-' ,hijo.total)   as 'Total Ret C$',
                           hijo.observacion,
                           IF(hijo.ndocimpreso IS NULL, 0,1)
            FROM documentos padre
            JOIN personas p ON p.idpersona = padre.idpersona
            JOIN conceptos c ON  c.idconcepto=padre.idconcepto
            LEFT JOIN costosxdocumento cd ON cd.iddocumento=padre.iddocumento
            LEFT JOIN  costosagregados ca ON ca.idcostoagregado=cd.idcostoagregado
            LEFT JOIN docpadrehijos ph ON  padre.iddocumento=ph.idpadre
            LEFT JOIN documentos hijo ON hijo.iddocumento=ph.idhijo
            WHERE padre.idtipodoc=18
            ORDER BY CAST(padre.ndocimpreso AS SIGNED)
            ;
            """ )
    #        El modelo que filtra a self.navmodel
            self.navproxymodel = RONavigationModel( self )
            self.navproxymodel.setSourceModel( self.navmodel )
            self.navproxymodel.setFilterKeyColumn( -1 )
            self.navproxymodel.setFilterCaseSensitivity ( Qt.CaseInsensitive )

    #        Este es el modelo con los datos de la tabla para navegar
            self.detailsmodel = QSqlQueryModel( self )
            self.detailsmodel.setQuery( """
                SELECT
                p.recibo as iddocumento,
                CONCAT(tp.descripcion, ' ' , tm.moneda) as 'Tipo de Pago',
                 p.refexterna as 'No. Referencia',
                 monto as 'Monto',
                tp.idtipopago,
                tm.idtipomoneda
            FROM pagos p
            JOIN tiposmoneda tm ON tm.idtipomoneda=p.tipomoneda
            JOIN tipospago tp ON tp.idtipopago=p.tipopago
            ;
            """ )

    #        Este es el filtro del modelo anterior
            self.detailsproxymodel = RODetailsModel( self )
            self.detailsproxymodel.setSourceModel( self.detailsmodel )


# ESTE ES EL MODELO CON LOS DATOS DE Los ABONOS PARA NAVEGAR
            self.abonosmodel = QSqlQueryModel( self )
            self.abonosmodel.setQuery( """
           SELECT
            d.idhijo as idrecibo,
            padre.ndocimpreso,
            d.monto as abono
            FROM docpadrehijos d
            JOIN documentos padre ON d.idpadre=padre.iddocumento
            WHERE padre.idtipodoc=5 and d.monto is not null
;
            """ )

    #        Este es el filtro del modelo anterior
            self.abonosproxymodel = ROAbonosModel( self )
            self.abonosproxymodel.setSourceModel( self.abonosmodel )

## ESTE ES EL MODELO CON LOS DATOS DE LAS FACTURAS PARA NAVEGAR
            self.facturasmodel = QSqlQueryModel( self )
            self.facturasmodel.setQuery( """            
                    SELECT
                iddocumento,
                ndocimpreso,
                Saldo,
                idpersona
            FROM vw_saldofacturas c
            WHERE c.saldo>0
            ORDER BY c.ndocimpreso
            ;
        """ )
            self.facturasproxymodel = ROFacturasModel( self )
            self.facturasproxymodel.setSourceModel( self.facturasmodel )



    #        Este objeto mapea una fila del modelo self.navproxymodel a los controles

            self.mapper.setSubmitPolicy( QDataWidgetMapper.ManualSubmit )
            self.mapper.setModel( self.navproxymodel )
            self.mapper.addMapping( self.lblnrec, NDOCIMPRESO , "text" )
            self.mapper.addMapping( self.lblnreten, NRETENCION , "text" )

            self.mapper.addMapping( self.txtobservaciones, OBSERVACION )
            self.mapper.addMapping( self.dtPicker, FECHA )
            self.mapper.addMapping( self.txtcliente, CLIENTE, "text" )
            self.mapper.addMapping( self.txtconcepto, CONCEPTO, "text" )
            self.mapper.addMapping( self.lbltotalreten, TOTALRETENCION, "text" )
            self.mapper.addMapping( self.txttasaret, TASARETENCION, "text" )
            self.mapper.addMapping( self.lbltotal, TOTAL, "text" )
            self.mapper.addMapping( self.ckretener, CONRETENCION, "checked" )


    #        asignar los modelos a sus tablas
            self.tablenavigation.setModel( self.navproxymodel )
            self.tabledetails.setModel( self.detailsproxymodel )
            self.tableabonos.setModel( self.abonosproxymodel )


#Se utiliza en modo de edicion

            self.tablefacturas.setModel( self.facturasproxymodel )

# OCULTO LAS COLUMNAS DE LOS ABONOS
            self.tableabonos.setColumnHidden( IDDOCUMENTO, True )


            self.frbotones.setVisible( False )

            self.tabledetails.setColumnHidden( IDPAGO, True )
            self.tabledetails.setColumnHidden( IDMONEDA, True )
            self.tabledetails.setColumnHidden( IDDOCUMENTOT, True )

            self.tablefacturas.setColumnHidden( IDDOCUMENTO, True )
            self.tablefacturas.setColumnHidden( 3, True )

            self.tablenavigation.setColumnHidden( IDDOCUMENTO, True )
            self.tablenavigation.setColumnHidden( OBSERVACIONRET, True )
            self.tablenavigation.setColumnHidden( TOTALRETENCION, True )
            self.tablenavigation.setColumnHidden( CONRETENCION, True )

            self.navigate( 'last' )

        except Exception as inst:
            print inst
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()


    

    def updateLabels( self ):
        
        self.editmodel.asignarTotal(self.abonoeditmodel.total)
         
        self.lbltotal.setText( moneyfmt( self.abonoeditmodel.total, 4, "US$" ) )
        ret=self.datosRecibo.getRetencion
        self.lbltotalreten.setText( moneyfmt( ret, 4, "US$" ) )
        self.lbltotalrecibo.setText( moneyfmt( self.abonoeditmodel.total - ret, 4, "US$" ) )
#        self.tabledetails.resizeColumnsToContents()

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


    @pyqtSlot( )
    def on_actionSave_activated( self ):
        """
        Slot documentation goes here.
        """
        if self.editmodel.valid and self.abonoeditmodel.valid:
            if not QSqlDatabase.database().isOpen():
                QSqlDatabase.database().open()

            if self.editmodel.save( self.abonoeditmodel.lines ):
                QMessageBox.information( None,
                    self.trUtf8( "Llantera Esquipulas" ),
                    self.trUtf8( """El documento se ha guardado con exito""" ) )
                self.editmodel = None
                self.updateModels()
                self.navigate( 'last' )
                self.status = True
            else:
                QMessageBox.critical( None,
                    self.trUtf8( "Llantera Esquipulas" ),
                    self.trUtf8( """Ha ocurrido un error al guardar el documento""" ) )

            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()

        else:
            QMessageBox.warning( None,
                self.trUtf8( "Llantera Esquipulas" ),
                self.trUtf8( """El documento no puede guardarse ya que la información no esta completa""" ),
                QMessageBox.StandardButtons( \
                    QMessageBox.Ok ),
                QMessageBox.Ok )


    @pyqtSlot(  )
    def on_actionPreview_activated( self ):
        """
        Funcion usada para mostrar el reporte de una entrada compra
        """

        report = frmReportes( "entradaslocales.php?doc=%d" % self.navmodel.record( self.mapper.currentIndex() ).value( "iddocumento" ).toInt()[0] , self.datosRecibo.userId, self )

        report.show()

    @pyqtSlot(  )
    def on_actionNew_activated( self ):
        """
        activar todos los controles, llenar los modelos necesarios, crear el modelo EntradaCompraModel, aniadir una linea a la tabla
        """
        if not QSqlDatabase.database().isOpen():
            if not QSqlDatabase.database().open():
                raise Exception( u"No se pudo establecer la conexión con la base de datos" )

            QMessageBox.warning( None,
            "Llantera Esquipulas",
            """Hubo un error al conectarse con la base de datos""",
            QMessageBox.StandardButtons( \
                QMessageBox.Ok ),
            QMessageBox.Ok )
        else:

#            Rellenar el combobox de los CLLIENTES
            self.clientesModel = QSqlQueryModel()
            self.clientesModel.setQuery( """
              SELECT
                    p.idpersona,
                    p.nombre,
                    sum(s.saldo) as SaldoTotal
                    FROM personas p
                    JOIN vw_saldofacturas s ON s.idpersona=p.idpersona
                    WHERE s.saldo>0
                    group by p.idpersona
                    ORDER BY p.nombre
                    ;
            """ )
#Verificar si existen clientes morosos            
            if self.clientesModel.rowCount() == 0:
                QMessageBox.information( None, "Recibo", "No existen clientes morosos" )
                return ""

#            Rellenar el combobox de las CONCEPTOS
            self.conceptosModel = QSqlQueryModel()
            self.conceptosModel.setQuery( """
               SELECT idconcepto, descripcion FROM conceptos c;
            """ )
            if self.conceptosModel.rowCount() == 0:
                QMessageBox.information( None, "Recibo", "No existen conceptos para los recibos, por favor cree uno" )
                return ""
            

            self.cbcliente.setModel( self.clientesModel )
            self.cbcliente.setCurrentIndex( -1 )
            self.cbcliente.setModelColumn( 1 )
            completer = QCompleter()
            completer.setCaseSensitivity( Qt.CaseInsensitive )
            completer.setModel( self.clientesModel )
            completer.setCompletionColumn( 1 )

            
            self.cbconcepto.setModel( self.conceptosModel )
            self.cbconcepto.setModelColumn( 1 )
            completerconcepto = QCompleter()
            completerconcepto.setCaseSensitivity( Qt.CaseInsensitive )
            completerconcepto.setModel( self.conceptosModel )
            completerconcepto.setCompletionColumn( 1 )

            self.editmodel = ReciboModel(self.parentWindow.datosSesion.tipoCambioBanco)
            self.abonoeditmodel = AbonoModel()
            
            self.datosRecibo = DatosRecibo(self.parentWindow.datosSesion)
            self.datosRecibo.cargarRetenciones(self.cbtasaret)
            
            if self.datosRecibo.retencionModel.rowCount()==0:
                QMessageBox.warning( None, "Recibo", u"No existe ninguna tasa de retención. Por favor contacte al administrador del sistema" )
                return ""
            

# Asigno el modelo del recibo


            self.datosRecibo.cargarNumeros(self)
            
            self.tablefacturas.setSelectionMode(QAbstractItemView.SingleSelection)
            self.tablefacturas.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.tableabonos.setModel( self.abonoeditmodel )
            self.tableabonos.setColumnHidden(IDDOCUMENTO,True)
            self.tabledetails.setModel( self.editmodel )

# ASIGNO EL DELEGADO A LA TABLA DE LOS PAGO            
            delegate = ReciboDelegate()
            self.tabledetails.setItemDelegate( delegate )
# ASIGNO EL DELEGADO A LA TABLA DE LOS ABONOS
            delegado = AbonoDelegate()
            self.tableabonos.setItemDelegate( delegado )
#            self.addLine()
            
            
            self.status = False
            self.frbotones.setVisible( True )
            self.updateFacturasFilter()
            
            self.connect( self.abonoeditmodel, SIGNAL( "dataChanged(QModelIndex,QModelIndex)" ), self.updateLabels )

        if QSqlDatabase.database().isOpen():
            QSqlDatabase.database().close()

        



    @pyqtSlot(  )
    def on_actionCancel_activated( self ):
        """
        Aca se cancela la edicion del documento
        """
        self.editmodel = None
        self.frbotones.setVisible( False )
        self.tablenavigation.setModel( self.navproxymodel )
        self.tabledetails.setModel( self.detailsproxymodel )
        self.tableabonos.setModel( self.abonosproxymodel )


        self.status = True


    def updateDetailFilter( self, index ):
        self.detailsproxymodel.setFilterKeyColumn( IDDOCUMENTOT )
        iddoc = self.navmodel.record( index ).value( "iddocumento" ).toString()
        self.detailsproxymodel.setFilterRegExp( iddoc )
        self.tablenavigation.selectRow( self.mapper.currentIndex() )
# FILTRO DE LOS ABONOS
        self.abonosproxymodel.setFilterKeyColumn( IDDOCUMENTOT )
        self.abonosproxymodel.setFilterRegExp( iddoc )


    def updateFacturasFilter( self ):
        self.facturasproxymodel.setFilterKeyColumn( 3 )
        self.facturasproxymodel.setFilterRegExp( str( self.datosRecibo.clienteId ) )




    def setControls( self, status ):
        """
        @param status false = editando        true = navegando
        """
        self.dtPicker.setReadOnly( True )
        self.ckretener.setEnabled( ( not status ) )
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
            self.navigate( 'last' )
            self.swcliente.setCurrentIndex( 1 )
            self.swconcepto.setCurrentIndex( 1 )
            self.tabledetails.setEditTriggers( QAbstractItemView.NoEditTriggers )
            self.tableabonos.setEditTriggers( QAbstractItemView.NoEditTriggers )
        else:
            self.tabWidget.setCurrentIndex( 0 )

            self.dtPicker.setDate( self.parentWindow.datosSesion.fecha )
            self.cbcliente.setCurrentIndex(-1)
            self.swcliente.setCurrentIndex( 0 )
            self.swconcepto.setCurrentIndex( 0 )
            self.swtasaret.setCurrentIndex( 0 )
            self.txtobservaciones.setPlainText( "" )
            
            self.lbltotalreten.setText( "0.00" )
            self.lbltotal.setText( "$0.00" )
            self.cbcliente.setFocus()

            self.tabledetails.setEditTriggers( QAbstractItemView.EditKeyPressed | QAbstractItemView.AnyKeyPressed | QAbstractItemView.DoubleClicked )
            self.tableabonos.setEditTriggers( QAbstractItemView.EditKeyPressed | QAbstractItemView.AnyKeyPressed | QAbstractItemView.DoubleClicked )
            
        self.tabledetails.setColumnWidth(DESCRIPCION,250)
        self.tabledetails.setColumnWidth(MONTO,150)
        self.tabledetails.setColumnWidth(MONTODOLAR,150)
        self.tabledetails.setColumnWidth(REFERENCIA,150)
            

    @pyqtSlot( "bool" )
    def on_btnadd_clicked( self, on ):
        """
        Asignar el contenido al objeto documeto
        """
        cindex = self.tablefacturas.currentIndex()
        if not cindex.model() is None:
            if not self.tablefacturas.isRowHidden( cindex.row() ):
                i = self.abonoeditmodel.rowCount()
                self.abonoeditmodel.insertRows( i )

                self.abonoeditmodel.lines[i].idFac = cindex.model().index( cindex.row(), 0 ).data()
                self.abonoeditmodel.lines[i].nFac = cindex.model().index( cindex.row(), 1 ).data()
                self.abonoeditmodel.lines[i].monto = Decimal( cindex.model().data( cindex.model().index( cindex.row(), 2 ), Qt.EditRole ).toString() )
                self.abonoeditmodel.lines[i].totalFac = self.abonoeditmodel.lines[i].monto
                self.abonoeditmodel.lines[i].nlinea = cindex.row()

                self.tablefacturas.setRowHidden( cindex.row(), True )
                self.updateLabels()

    @pyqtSlot( "bool" )
    def on_btnaddall_clicked( self, on ):
        """
        Asignar el contenido al objeto documeto
        """
        i = self.abonoeditmodel.rowCount()
        for n in range( self.facturasproxymodel.rowCount() ):
            if not self.tablefacturas.isRowHidden( n ):
                self.abonoeditmodel.insertRows( i )
                self.abonoeditmodel.lines[i].nFac = self.facturasproxymodel.index( n, 1 ).data()
                self.abonoeditmodel.lines[i].monto = Decimal( self.facturasproxymodel.data( self.facturasproxymodel.index( n, 2 ), Qt.EditRole ).toString() )
                self.abonoeditmodel.lines[i].totalFac = self.abonoeditmodel.lines[i].monto
                self.abonoeditmodel.lines[i].nlinea = n
                self.tablefacturas.setRowHidden( n, True )
                i = i + 1
        self.updateLabels()

    @pyqtSlot( "bool" )
    def on_btnremove_clicked( self, on ):
        """
        Asignar el contenido al objeto documeto
        """
        r = self.tableabonos.currentIndex().row()
        if self.abonoeditmodel.rowCount() > 0 and r > -1:
            self.abonoeditmodel.removeRows( r, self.tablefacturas )
            self.updateLabels()

    @pyqtSlot( "bool" )
    def on_btnremoveall_clicked( self, on ):
        """
        Asignar el contenido al objeto documeto
        """
        rows = self.abonoeditmodel.rowCount()
        if  rows > 0:
            self.abonoeditmodel.removeRows( 0, self.tablefacturas, rows )
            self.updateLabels()
#
#    @pyqtSlot(  )
#    def on_txtpersona_editingFinished( self ):
#        if not  self.__status:
#            self.datos.observaciones = self.txtpersona.text()


    @pyqtSlot( "int" )
    def on_cbcliente_currentIndexChanged( self, index ):
        """
        asignar proveedor al objeto self.editmodel
        """
        if not self.editmodel is None:
            self.datosRecibo.clienteId = self.clientesModel.record( index ).value( "idpersona" ).toInt()[0] if index != -1 else - 1
            self.tableabonos.setEnabled( index != -1 )
            self.frbotones.setEnabled( index != -1 )
            self.abonoeditmodel.removeRows( 0, self.tablefacturas, self.abonoeditmodel.rowCount() )
            self.abonoeditmodel.idcliente = self.datosRecibo.clienteId
            self.updateFacturasFilter()
            self.updateLabels()

    @pyqtSlot( "int" )
    def on_cbconcepto_currentIndexChanged( self, index ):
        """
        asignar la concepto al objeto self.editmodel
        """
        if not self.editmodel is None:
            self.datosRecibo.conceptoId = self.conceptosModel.record( index ).value( "idconcepto" ).toInt()[0]

    @pyqtSlot( "int" )
    def on_cbtasaret_currentIndexChanged( self, index ):
        """
        asignar la retencion al objeto self.editmodel
        """
        if index>-1:
            self.datosRecibo.tasaRetencionCambio(self,index)
        else:
            self.datosRecibo.retencionId

    @pyqtSlot( "QDateTime" )
    def on_dtPicker_dateTimeChanged( self, datetime ):
        pass
    
class dlgRecibo(Ui_dlgRecibo,QDialog):
    def __init__( self,factura,readOnly=False):
        super( dlgRecibo, self ).__init__( factura )
        self.editModel=None
        self.setupUi( self )
        self.readOnly=readOnly        
        self.lbltotal.setText(factura.lblsubtotal.text())
        self.txtcliente.setText(factura.cbcliente.currentText())
        self.setControls(False,factura)
        self.connect( self.buttonBox, SIGNAL( "accepted()" ), self.aceptar )
    
    def aceptar(self):
#        if self.datosRecibo.valid():
            return self.accept()              
#        self.setWindowFlags(Qt.WindowTitleHint | Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)
    def save(self):
        self.datosRecibo.observaciones = self.txtobservaciones.toPlainText()
        self.datosRecibo.lines = self.editModel.lines
        linea = LineaAbono()
        self.datosRecibo.lineasAbonos.append()
        self.datosRecibo.save()
        
    def setControls( self, status,factura ):
        """
        @param status false = editando        true = navegando
        """
        self.txtcliente.setReadOnly( status )
        self.ckretener.setEnabled(not status)
        self.txtobservaciones.setReadOnly( status )
        self.readOnly=status
        
        if status:
            self.tabledetails.setEditTriggers( QAbstractItemView.NoEditTriggers )
        else:
#            self.lblnrec.setText( "" )
            self.editModel = ReciboModel(self.datosRecibo.datosSesion.tipoCambioBanco)
            
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open():
                    raise Exception( u"No se pudo establecer la conexión con la base de datos" )
    
                QMessageBox.warning( None,
                "Llantera Esquipulas",
                """Hubo un error al conectarse con la base de datos""",
                QMessageBox.StandardButtons( \
                    QMessageBox.Ok ),
                QMessageBox.Ok )
            else:        
                self.datosRecibo = DatosRecibo(factura.editmodel.datosSesion)
                self.datosRecibo.cargarNumeros(self.lblnrec, self.lblnreten)
                self.datosRecibo.cargarRetenciones(self.cbtasaret)
                delegado = ReciboDelegate()    
                
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()

            self.editModel = ReciboModel()
            self.editModel.insertRow(0)
            linea = self.editModel.lines[0]
            linea.pagoId = 0
            linea.monedaId = 0
            linea.pagoDescripcion = ""
            linea.nref = ""
            linea.monto = factura.editmodel.total
            index= self.editModel.index(0,MONTO)
            self.editModel.emit( SIGNAL( "dataChanged(QModelIndex, QModelIndex)" ), index, index )
            
            self.tabledetails.setModel(self.editModel)
            self.tabledetails.setColumnHidden(IDPAGO,True)
            self.tabledetails.setColumnHidden(IDMONEDA,True)
            self.tabledetails.setColumnWidth(DESCRIPCION,200)
            
            self.tabledetails.setItemDelegate(delegado)
            self.tabledetails.setEditTriggers( QAbstractItemView.EditKeyPressed | QAbstractItemView.AnyKeyPressed | QAbstractItemView.DoubleClicked )
     
    
#    @pyqtSlot()
#    def on_txtpersona_editingFinished( self ):    
#        if not  self.readOnly:
#            self.datosRecibo.observaciones = self.txtpersona.text()
            
# MANEJO EL EVENTO  DE SELECCION EN EL RADIOBUTTON
    @pyqtSignature( "bool" )
    def on_ckretener_toggled( self, on ):
        """
        """
        self.datosRecibo.retencionAplicada(self,on)
  
        
    @pyqtSlot( "int" )
    def on_cbtasaret_currentIndexChanged( self, index ):
        """
        asignar la retencion al objeto self.editmodel
        """
        self.datosRecibo.tasaRetencionCambio(self,index)
        
    def updateLabels( self ):
        if not self.readOnly:
            self.lbltotalreten.setText( moneyfmt( self.datosRecibo.getRetencion, 4, "US$" ) )
            self.lbltotalrecibo.setText(moneyfmt(self.datosRecibo.totalPagado))
            self.tabledetails.resizeColumnsToContents()
        
class DatosRecibo(object):
    def __init__(self,datosSesion):
        object.__init__(self)
    
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
        tmpsubtotal = sum( [linea.monto for linea in self.lineas if linea.valid] )
        return tmpsubtotal if tmpsubtotal > 0 else Decimal( 0 )
    
    @property
    def totalPagado( self ):
        """
    
        """
        total = self.total
        return total * (1- (( self.retencionTasa / Decimal( 100 ) )  if self.aplicarRet else 0))
    
    
        
    @property
    def valid( self ):
        """
        Un documento es valido cuando 
        self.printedDocumentNumber != ""
        self.providerId !=0
        self.validLines >0
        self.__idIVA !=0
        self.uid != 0
        self.warehouseId != 0 
        """
        if  self.printedDocumentNumber == "":
            print( "No existe numero de doc impreso" )
        elif int( self.clienteId ) == 0:
            print( "No existe un cliente seleccionado" )
        elif int( self.validLines ) < 1:
            print( "No Hay ninguna linea no valida" )
        elif int( self.retencionId ) == 0:
            print( "No hay tasa de retencion" )
        elif int( self.uid ) == 0:
            print( "No hay un usuario" )
        elif int( self.conceptoId ) == 0:
            print( "No hay un concepto" )
        elif self.idtc == 0:
            print( "no hay un tipo de cambio para la fecha" + self.datetime )
        else:
            return True
        return False

    @property
    def getRetencion( self ):
        return ( self.total * ( self.retencionTasa / Decimal( 100 ) ) ) if self.aplicarRet else Decimal(0)
    
    @property
    def validLines( self ):
        """
        la cantidad de lineas validas que hay en el documento
        """
        foo = 0
        for line in self.lineas:
            if line.valid:foo += 1
        return foo
    
    def save( self ):
        """
        Este metodo guarda el documento actual en la base de datos
        """

        if not self.valid:
            raise Exception( "El documento a salvar no es valido" )

        query = QSqlQuery()

        try:

            if not QSqlDatabase.database().transaction():
                raise Exception( u"No se pudo comenzar la transacción" )
#INSERTAR RECIBO
            query.prepare( """
            INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,idusuario,anulado, idpersona, observacion,total,escontado,idtipocambio,idconcepto) 
            VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:idusuario,:anulado,:idpersona,:observacion,:total,:escontado,:idtc,:concepto)
            """ )
            query.bindValue( ":ndocimpreso", self.printedDocumentNumber )
            query.bindValue( ":fechacreacion", self.datetime.toString( 'yyyyMMddhhmmss' ) )
            query.bindValue( ":idtipodoc", self.__documentType )
            query.bindValue( ":idusuario", self.datosSesion.usuarioId )
            query.bindValue( ":anulado", 0 )
            query.bindValue( ":idpersona", self.clienteId )
            query.bindValue( ":observacion", self.observaciones )
            query.bindValue( ":total", self.total.to_eng_string() )
            query.bindValue( ":escontado", self.escontado )
            query.bindValue( ":idtc", self.datosSesion.tipoCambioId )
            query.bindValue( ":concepto", self.conceptoId )
            
            if not query.exec_():
                raise Exception( "No se pudo insertar el recibo" )
            insertedId = query.lastInsertId().toInt()[0]


#INSERTAR LA RELACION CON LA SESION DE CAJA            
            query.prepare( """
                INSERT INTO docpadrehijos (idpadre,idhijo)
                VALUES (:idsesion,:idrecibo)
                """ )

            query.bindValue( ":idsesion", self.sesion )
            query.bindValue( ":idrecibo", insertedId )

            if not query.exec_():
                raise Exception( "No se Inserto la relacion entre la sesion de caja y el recibo" )


#INSERTAR LOS TIPOS DE PAGO
            i = 0
            for linea in self.lineas:
                if linea.valid:
                    linea.save( insertedId, i )
                    i = i + 1
#INSERTAR los abonos
            
            for l in self.lineasAbonos:
                if l.valid:
                    l.save( insertedId )

#VERIFICO SI se aplicara la retencion                     
            if self.aplicarRet :

#INSERTAR EL DOCUMENTO RETENCION            
                query.prepare( """
                INSERT INTO documentos (ndocimpreso,fechacreacion,idtipodoc,idusuario,anulado, idpersona, observacion,total,escontado,idtipocambio,idconcepto) 
                VALUES ( :ndocimpreso,:fechacreacion,:idtipodoc,:idusuario,:anulado,:idpersona,:observacion,:total,:escontado,:idtc,:concepto)
                """ )
                query.bindValue( ":ndocimpreso", self.retencionNumero )
                query.bindValue( ":fechacreacion", self.datetime )
                query.bindValue( ":idtipodoc", 19 )
                query.bindValue( ":idusuario", self.uid )
                query.bindValue( ":anulado", 0 )
                query.bindValue( ":idpersona", self.clienteId )
                query.bindValue( ":observacion", self.observacionesRet )
                query.bindValue( ":total", self.getRetencion.to_eng_string() )
                query.bindValue( ":escontado", self.escontado )
                query.bindValue( ":idtc", self.idtc )
                query.bindValue( ":concepto", self.conceptoId )
                if not query.exec_():
                    raise Exception( "No se Inserto la retencion" )

                idret = query.lastInsertId().toInt()[0]

                query.prepare( """
                INSERT INTO docpadrehijos (idpadre,idhijo)
                VALUES (:idrecibo,:idretencion)
                """ )

                query.bindValue( ":idrecibo", insertedId )
                query.bindValue( ":idretencion", idret )

                if not query.exec_():
                    raise Exception( "No se Inserto la relacion entre la retencion y el recibo" )


# INSERTAR EL ID DEL COSTO RETENCION                
                query.prepare( """
                INSERT INTO costosxdocumento (iddocumento, idcostoagregado) VALUES( :iddocumento, :idcostoagregado )
                """ )
                query.bindValue( ":iddocumento", insertedId )
                query.bindValue( ":idcostoagregado", self.retencionid )
                if not query.exec_():
                    raise Exception( "el costo Retencion  NO SE INSERTO" )


            #manejar las cuentas contables
            movAbonoDeCliente( insertedId, self.total * self.tc, self.getRetencion * self.tc )

            if not QSqlDatabase.database().commit():
                raise Exception( "No se pudo hacer commit" )
        except Exception as inst:
            print  query.lastError().databaseText()
            print inst.args
            QSqlDatabase.database().rollback()
            return False

        return True

    def cargarRetenciones(self,cbtasaret):
#            Rellenar el combobox de las retenciones
            self.retencionModel = QSqlQueryModel()
            self.retencionModel.setQuery( """
                    SELECT 
                        idcostoagregado, 
                        FORMAT(valorcosto,0) as tasa
                    FROM costosagregados 
                    WHERE 
                    (idtipocosto=10 OR idtipocosto = 8) AND 
                    activo=1 
                    ORDER BY valorcosto desc; 
                    """ )

            cbtasaret.setModel( self.retencionModel )
            cbtasaret.setModelColumn( 1 )

    def cargarNumeros(self,recibo):
#            Cargar el numero de el Recibo actual
        idrec= str(IDRECIBO)
        idret = str(IDRETENCION)
        query = QSqlQuery( "CALL spConsecutivo(" + idrec +",null)")
        if not query.exec_():
            print( query.lastError().text() )
        query.first()
        n = query.value( 0 ).toString()
        print n
        recibo.lblnrec.setText( n )
        self.printedDocumentNumber = n

        query = QSqlQuery( "CALL spConsecutivo(" + idret +",null)")
        if not query.exec_():
            print( query.lastError().text() )
        query.first()
        n = query.value( 0 ).toString()
        recibo.lblnreten.setText( n )        
        self.retencionNumeroImpreso = n                
                

    def tasaRetencionCambio(self,recibo,index):
        self.retencionId = self.retencionModel.record(index).value( "idcostoagregado" ).toInt()[0]
        value =self.retencionModel.record( index ).value( "tasa" ).toString()
        self.retencionTasa = Decimal( value if value!="" else 0 )
        recibo.updateLabels()
        
    def retencionAplicada(self,recibo,on):
        recibo.cbtasaret.setCurrentIndex(-1)
        recibo.cbtasaret.setEnabled(on)
        self.aplicarRet = on    
        recibo.updateLabels()
            
        
class RONavigationModel( QSortFilterProxyModel ):
    """
    basicamente le da formato a la salida de mapper
    """
    def data( self, index, role = Qt.DisplayRole ):
        """
        Esta funcion redefine data en la clase base, es el metodo que se utiliza para mostrar los datos del modelo
        """
        value = QSortFilterProxyModel.data( self, index, role )
        if value.isValid() and role in ( Qt.EditRole, Qt.DisplayRole ):
            if index.column() == TOTAL :
                return moneyfmt( Decimal( value.toString() ), 2, "$" )
        return value

class RODetailsModel( QSortFilterProxyModel ):
    """
    El modelo que maneja la tabla en la que se previsualizan los os,
    basicamente esta creado para darle formato al total y al MONTO
    """
    def __init__( self, dbcursor = None ):
        super( QSortFilterProxyModel, self ).__init__()

    def columnCount( self, index = QModelIndex() ):
        return 6

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
#            if orientation == Qt.Horizontal:
#                return Qt.AlignLeft | Qt.AlignVCenter
            return Qt.AlignHCenter | Qt.AlignVCenter
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if  section == DESCRIPCION:
                return u"Descripción"
            elif section == MONTO:
                return "Monto"
            elif section == MONTODOLAR:
                return u"Monto US$"
            elif section == REFERENCIA:
                return "Referencia"
        return int( section + 1 )


    def data( self, index, role = Qt.DisplayRole ):
        """
        Esta funcion redefine data en la clase base, es el metodo que se utiliza para mostrar los datos del modelo
        """
        value = QSortFilterProxyModel.data( self, index, role )
        if value.isValid() and role == Qt.DisplayRole:
            if index.column() == MONTO:
                return moneyfmt( Decimal( value.toString() ), 2, "US$" )
        return value

class ROAbonosModel( QSortFilterProxyModel ):
    """
    El modelo que maneja la tabla en la que se previsualizan los os,
    basicamente esta creado para darle formato al total y al MONTO
    """
    def __init__( self, dbcursor = None ):
        super( QSortFilterProxyModel, self ).__init__()

    def columnCount( self, index = QModelIndex() ):
        return 3

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
            elif section == ABONO:
                return "Monto"
        return int( section + 1 )


    def data( self, index, role = Qt.DisplayRole ):
        """
        Esta funcion redefine data en la clase base, es el metodo que se utiliza para mostrar los datos del modelo
        """
        value = QSortFilterProxyModel.data( self, index, role )
        if value.isValid() and role == Qt.DisplayRole:
            if index.column() == ABONO:
                return moneyfmt( Decimal( value.toString() ), 4, "US$" )
        return value

class ROFacturasModel( QSortFilterProxyModel ):
    """
    El modelo que maneja la tabla en la que se previsualizan los os,
    basicamente esta creado para darle formato al total y al MONTO
    """
    def __init__( self, dbcursor = None ):
        super( QSortFilterProxyModel, self ).__init__()

    def columnCount( self, index = QModelIndex() ):
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
            elif section == ABONO:
                return "Saldo"
        return int( section + 1 )


    def data( self, index, role = Qt.DisplayRole ):
        """
        Esta funcion redefine data en la clase base, es el metodo que se utiliza para mostrar los datos del modelo
        """
        value = QSortFilterProxyModel.data( self, index, role )
        if value.isValid() and role == Qt.DisplayRole:
            if index.column() == ABONO:
                return moneyfmt( Decimal( value.toString() ), 4, "$" )
        return value

