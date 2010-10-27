# -*- coding: utf-8 -*-
'''
Created on 03/07/2010

@author: MARCOS
'''
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot, Qt, QDateTime, QTimer, QDate
from PyQt4.QtGui import QSortFilterProxyModel, QMessageBox, QCompleter, \
    QDataWidgetMapper, QStyledItemDelegate, QDoubleSpinBox, qApp, QDialog
from PyQt4.QtSql import QSqlQueryModel, QSqlQuery
from decimal import Decimal, InvalidOperation
from document.cheque.chequemodel import ChequeModel
from ui.Ui_cheques import Ui_frmCheques
from utility import constantes
from utility.accountselector import AccountsSelectorDelegate, \
    AccountsSelectorLine
from utility.base import Base
from utility.moneyfmt import moneyfmt
from utility.widgets.searchpanel import SearchPanel
import logging
from utility.decorators import if_edit_model





IDDOCUMENTO, NCHEQUE, CUENTABANCARIA, NOMBRE, FECHA, CONCEPTO, \
TOTAL, SUBTOTAL, IVA, TOTALRET, TIPOCAMBIO, TASARETENCION, \
ESTADO, IDESTADO, TOTALCHEQUE = range( 15 )
#accounts model
IDDOC, IDCUENTA, CODIGO, DESCRIPCION, MONTO = range( 5 )
class FrmCheques( Ui_frmCheques, Base ):
    """
    Implementacion de la interfaz grafica para Cheques
    """
    web = "cheques.php?doc="
    def __init__( self, parent ):
        '''
        Constructor
        '''
        super( FrmCheques, self ).__init__( parent )


        self.navmodel = QSqlQueryModel( self )
        self.navproxymodel = QSortFilterProxyModel( self )
        self.navproxymodel.setSourceModel( self.navmodel )

        self.accountsModel = QSqlQueryModel()
        self.accountsProxyModel = ROAccountsModel( self )
        self.accountsProxyModel.setSourceModel( self.accountsModel )

        #        El modelo que filtra a self.navmodel
        self.navproxymodel.setFilterKeyColumn( -1 )
        self.navproxymodel.setFilterCaseSensitivity ( Qt.CaseInsensitive )
        self.editmodel = None

        self.status = True
        #las acciones deberian de estar ocultas

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


        QTimer.singleShot( 0, self.loadModels )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def updateDetailFilter( self, index ):
        record = self.navmodel.record( index )
        self.accountsProxyModel.setFilterKeyColumn( IDDOCUMENTO )
        self.accountsProxyModel.setFilterRegExp( 
                                record.value( "iddocumento" ).toString() )
        self.tablenavigation.selectRow( self.mapper.currentIndex() )
        self.actionAnular.setEnabled( record.value( "idestado" ).toInt()[0] == constantes.CONFIRMADO )
        
#        if record.value( "caret.valorcosto" )>Decimal(0.00):
#            print "tiene retencion"
#        
    def updateModels( self ):
    #inicializando el documento
    #El modelo principal
    #FIXME Revisar escape del %
    #TODO:REVISAR BIEN

        self.navmodel.setQuery( u"""
        SELECT padre.iddocumento,
            padre.ndocimpreso as 'No. Cheque',
            cb.descripcion as 'Cuenta Bancaria',
            p.nombre as Cliente,
            DATE(padre.fechacreacion) as 'Fecha',
            c.descripcion as 'En concepto de',
            IF (tm.simbolo="C$",CONCAT(tm.simbolo,FORMAT(padre.total*tc.tasa,4)),CONCAT(tm.simbolo,FORMAT(padre.total,4))) as Total,
            
            IF (tm.simbolo="C$",ROUND(padre.total*tc.tasa/ (1+ IF(ca.valorcosto IS NULL,0,ca.valorcosto/100))),ROUND(padre.total/ (1+ IF(ca.valorcosto IS NULL,0,ca.valorcosto/100)))) as subtotal,
            
            IF (tm.simbolo="C$",CONCAT(tm.simbolo,FORMAT(tc.tasa*padre.total-(tc.tasa*padre.total/(1+ IF(ca.valorcosto IS NULL,0,ca.valorcosto/100))),4)),CONCAT(tm.simbolo,FORMAT(padre.total-(padre.total/(1+ IF(ca.valorcosto IS NULL,0,ca.valorcosto/100))),4))) as iva,
                       
            IF(hijo.total IS NULL, CONCAT(tm.simbolo,'0.0000') ,CONCAT(tm.simbolo,hijo.total))   as 'Total Ret C$',
            tc.tasa as TipoCambio,
            caret.valorcosto as 'retencion',
            ed.descripcion AS Estado,
            padre.idestado,
            IF (tm.simbolo="C$",padre.total*tc.tasa,padre.total) as TotalCheque
            FROM documentos padre
            JOIN estadosdocumento ed ON ed.idestado = padre.idestado
            JOIN tiposcambio tc on padre.idtipocambio=tc.idtc
            JOIN personasxdocumento pxd ON padre.iddocumento=pxd.iddocumento
            JOIN personas p ON p.idpersona=pxd.idpersona
            JOIN conceptos c ON  c.idconcepto=padre.idconcepto
            
            LEFT JOIN costosxdocumento cd ON cd.iddocumento=padre.iddocumento
            LEFT JOIN  costosagregados ca ON ca.idcostoagregado=cd.idcostoagregado
            LEFT JOIN docpadrehijos ph ON  padre.iddocumento=ph.idpadre
            LEFT JOIN documentos hijo ON hijo.iddocumento=ph.idhijo
            
            LEFT JOIN costosxdocumento cdret ON cdret.iddocumento=hijo.iddocumento
            LEFT JOIN  costosagregados caret ON caret.idcostoagregado=cdret.idcostoagregado            
            
            JOIN cuentasxdocumento cuentasdoc on cuentasdoc.iddocumento=padre.iddocumento
            JOIN cuentascontables cb ON cb.idcuenta=cuentasdoc.idcuenta
            JOIN cuentasbancarias cbank on cb.idcuenta=cbank.idcuentacontable
            JOIN tiposmoneda tm on tm.idtipomoneda=cbank.idtipomoneda 
            WHERE padre.idtipodoc= %d AND p.tipopersona = %d
            GROUP BY padre.iddocumento
            ORDER BY CAST(IF(padre.ndocimpreso="S/N",0, padre.ndocimpreso )AS SIGNED)
        """ % ( constantes.IDCHEQUE,
                constantes.PROVEEDOR ) )
#        El modelo que filtra a self.navmodel


        self.tablenavigation.resizeColumnsToContents()

        #Este es el modelo para las cuentas





        self.accountsModel.setQuery( """
        SELECT
            c.iddocumento, 
            c.idcuenta,
            cc.codigo as Codigo,
            cc.descripcion as Nombre,
            c.monto as Monto
        FROM cuentasxdocumento c 
        JOIN documentos d ON c.iddocumento = d.iddocumento
        JOIN cuentascontables cc ON cc.idcuenta = c.idcuenta
        WHERE d.idtipodoc = %d
        ORDER BY nlinea
        """ % ( constantes.IDCHEQUE ) )


        self.mapper.setSubmitPolicy( QDataWidgetMapper.ManualSubmit )
        self.mapper.setModel( self.navproxymodel )
        self.mapper.addMapping( self.lblncheque, NCHEQUE, "text" )
        self.mapper.addMapping( self.dtPicker, FECHA, "date" )
        self.mapper.addMapping( self.lblbeneficiario, NOMBRE, "text" )
        self.mapper.addMapping( self.total, TOTAL, "text" )
        self.mapper.addMapping( self.lblconcepto, CONCEPTO, "text" )
        self.mapper.addMapping( self.retencion, TOTALRET, "text" )
        self.mapper.addMapping( self.lbltipocambio, TIPOCAMBIO, "text" )
        self.mapper.addMapping( self.subtotal, SUBTOTAL )
        self.mapper.addMapping( self.iva, IVA, "text" )
        self.mapper.addMapping( self.lblcuenta, CUENTABANCARIA, "text" )
        self.mapper.addMapping( self.lblretencion, TASARETENCION, "text" )
        self.tablenavigation.setModel( self.navproxymodel )
        self.tabledetails.setModel( self.accountsProxyModel )

        self.tabledetails.setColumnHidden( IDCUENTA, True )
        self.tabledetails.setColumnHidden( IDDOC, True )
        self.tablenavigation.setColumnHidden( TIPOCAMBIO, True )
        self.tablenavigation.setColumnHidden( SUBTOTAL, True )
        self.tablenavigation.setColumnHidden( IVA, True )
        self.tablenavigation.setColumnHidden( IDDOCUMENTO, True )
        self.tablenavigation.setColumnHidden( CONCEPTO, True )
        self.tablenavigation.setColumnHidden( CONCEPTO, True )
        self.tablenavigation.setColumnHidden( IDESTADO, True )
        self.tablenavigation.setColumnHidden( TOTALCHEQUE, True )

        self.tablenavigation.resizeColumnsToContents()
    def addActionsToToolBar( self ):
        self.actionAnular = self.createAction( text = "Anular",
                                               icon = ":/icons/res/edit-delete.png",
                                               slot = self.anular )

        self.toolBar.addActions( [
            self.actionNew,
            self.actionPreview,
            self.actionPrint,
            self.actionSave,
            self.actionCancel,
            self.actionAnular
        ] )
        self.toolBar.addSeparator()
        self.toolBar.addActions( [
            self.actionGoFirst,
            self.actionGoPrevious,
            self.actionGoLast,
            self.actionGoNext,
            self.actionGoLast
        ] )


    def setControls( self, status ):
        """
        @param status: false = editando        true = navegando
        """
        self.actionPrint.setVisible( status )
        self.dtPicker.setReadOnly( status )
        self.subtotal.setReadOnly( status )
        self.txtobservaciones.setReadOnly( status )

        self.actionGoFirst.setVisible( status )
        self.actionGoPrevious.setVisible( status )
        self.actionGoNext.setVisible( status )
        self.actionGoLast.setVisible( status )
        self.actionAnular.setVisible( status )

        self.actionSave.setVisible( not status )
        self.actionCancel.setVisible( not status )
        self.actionNew.setVisible( status )
        self.actionPreview.setVisible( status )
        self.ckretencion.setEnabled( not status )
        self.ckIva.setEnabled( not status )
        self.conceptowidget.setCurrentIndex( 1 if not status else 0 )
        self.beneficiariowidget.setCurrentIndex( 1 if not status else 0 )
        self.cuentawidget.setCurrentIndex( 1 if not status else 0 )

        if not status:
            self.total.setText( "0.0" )
            self.subtotal.setValue( 0 )
            self.iva.setText( "0.0" )
            self.retencion.setText( "0.0" )
            self.txtobservaciones.setPlainText( "" )
            self.editmodel.uid = self.user.uid
            self.tabledetails.addAction( self.actionDeleteRow )
        else:
            self.tabledetails.removeAction( self.actionDeleteRow )
            
    def deleteRow( self ):
        """
        Funcion usada para borrar lineas de la tabla
        """
        index = self.tabledetails.currentIndex()

        if not index.isValid():
            return
        row = index.row()

        self.editmodel.removeRows( row, 1 )

        
    @pyqtSlot( bool )
    @if_edit_model
    def on_ckretencion_toggled( self, on ):
        """
        """

        if on :
            self.retencionwidget.setCurrentIndex( 1 )
            self.editmodel.hasretencion = True
        else:
            self.retencionwidget.setCurrentIndex( 0 )
            self.cboretencion.setCurrentIndex( -1 )
            self.editmodel.hasretencion = False
        #self.cboretencion.    

    @pyqtSlot( bool )
    @if_edit_model
    def on_ckIva_toggled( self, on ):
        """
        """
        #Verificar IVA    
        query = QSqlQuery( """
                SELECT idcostoagregado, valorcosto 
                FROM costosagregados c 
                WHERE idtipocosto = 1 AND activo = 1 
                ORDER BY idtipocosto;
                """ )
        query.exec_()
        if not query.size() == 1:
            QMessageBox.information( self,
                                     qApp.organizationName(),
                                     "No fue posible obtener el porcentaje "\
                                     + "del IVA" )
        if on :
            self.editmodel.hasiva = True
            query.first()
            self.editmodel.ivaId = query.value( 0 ).toInt()[0]

        else:
            self.editmodel.hasiva = False

        self.updateTotals()

    @pyqtSlot( int )
    @if_edit_model
    def on_cboconcepto_currentIndexChanged( self, index ):
        self.editmodel.conceptoId = self.conceptosmodel.record( index ).value( "idconcepto" ).toInt()[0]

    @pyqtSlot( int )
    @if_edit_model
    def on_cbocuenta_currentIndexChanged( self, index ):
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( "Hubo un error al conectarse con la base de datos" )

            self.editmodel.setData( self.editmodel.index(  0, 2 ),
                            [self.cuentabancaria.record( index ).value( "idcuentacontable" ).toInt()[0],
                             self.cuentabancaria.record( index ).value( "codigo" ).toString(),
                             self.cuentabancaria.record( index ).value( "descripcion" ).toString()] )
            self.accountseditdelegate.accounts.setFilterRegExp( "[^%d]" % self.cuentabancaria.record( index ).value( "idcuentacontable" ).toInt()[0] )

            self.editmodel.moneda = self.cuentabancaria.record( index ).value( "IDMONEDA" ).toInt()[0]
            self.editmodel.simbolo = self.cuentabancaria.record( index ).value( "simbolo" ).toString()
            # Cargar el numero del cheque actual
            if index > -1:
                query = QSqlQuery( """
                CALL spConsecutivo(12,""" + self.cuentabancaria.record( index ).value( "idcuentacontable" ).toString() + ")" )
                if not query.exec_():
                    raise UserWarning( "No se pudo obtener el numero consecutivo del cheque" )
                query.first()
                n = query.value( 0 ).toString()

                self.lblncheque.setText( n )
                self.editmodel.printedDocumentNumber = n

                self.editmodel.setData( self.editmodel.index( 0, 3 ), self.editmodel.totalCordobas )
                self.updateTotals()

        except UserWarning as inst:
            logging.error( inst )
            QMessageBox.critical( self, qApp.organizationName(), unicode( inst ) )
        except Exception as inst:
            logging.critical( inst )

    @pyqtSlot( int )
    @if_edit_model
    def on_cboretencion_currentIndexChanged( self, index ):
        self.editmodel.retencionId = self.retencionModel.record( index ).value( "idcostoagregado" ).toInt()[0]
        self.editmodel.retencionPorcentaje = Decimal( self.cboretencion.currentText() ) if self.cboretencion.currentText() != "" else 0
        self.updateTotals()

    @pyqtSlot( int )
    @if_edit_model
    def on_cbobeneficiario_currentIndexChanged( self, index ):
        self.editmodel.proveedorId = self.proveedoresmodel.record( index ).value( "idpersona" ).toInt()[0]

    @pyqtSlot( float )
    @if_edit_model
    def on_subtotal_valueChanged( self, _index ):
        self.updateTotals()


    def updateTotals( self ):
        self.editmodel.subtotal = Decimal( str( self.subtotal.value() ) )
        self.editmodel.setData( 
                               self.editmodel.index( 0, 3 ),
                               self.editmodel.totalCordobas.quantize( 
                                                     Decimal( '0.0001' ) ) )
        if self.editmodel.moneda == constantes.IDCORDOBAS:

            self.total.setText( moneyfmt( self.editmodel.totalCordobas,
                                          4,
                                          self.editmodel.simbolo ) )
            self.iva.setText( moneyfmt( self.editmodel.iva,
                                        4,
                                        self.editmodel.simbolo ) )
            self.retencion.setText( moneyfmt( self.editmodel.retencion,
                                              4,
                                              self.editmodel.simbolo ) )

            self.total.setToolTip( moneyfmt( self.editmodel.totalDolares,
                                             4,
                                             "US$" ) )
            self.iva.setToolTip( moneyfmt( self.editmodel.iva,
                                           4,
                                           "US$" ) )
            self.retencion.setToolTip( moneyfmt( self.editmodel.retencion,
                                                 4,
                                                 "US$" ) )

        elif self.editmodel.moneda == constantes.IDDOLARES:
            self.total.setText( moneyfmt( self.editmodel.totalDolares,
                                          4,
                                          "US$" ) )
            self.iva.setText( moneyfmt( self.editmodel.iva,
                                        4,
                                        "US$" ) )
            self.retencion.setText( moneyfmt( self.editmodel.retencion,
                                              4,
                                              "US$" ) )

            self.total.setToolTip( moneyfmt( self.editmodel.totalCordobas,
                                             4,
                                             "C$" ) )
            self.iva.setToolTip( moneyfmt( self.editmodel.iva,
                                           4,
                                           "C$" ) )
            self.retencion.setToolTip( moneyfmt( self.editmodel.retencion,
                                                 4,
                                                 "C$" ) )

    def cancel( self ):
        """
        Aca se cancela la edicion del documento
        """
        self.editmodel = None
        self.tablenavigation.setModel( self.navproxymodel )
        self.tabledetails.setModel( self.accountsProxyModel )
        self.tabledetails.setColumnHidden( IDCUENTA, True )

        self.status = True
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( u"No se pudo establecer la conexión con la base de datos" )

            self.updateModels()
            self.navigate( 'last' )
        except UserWarning as inst:
                QMessageBox.warning( self,
                                     qApp.organizationName(),
                                     inst )
                logging.critical( unicode( inst ) )
                self.status = True

                    



    @property
    def printIdentifier( self ):
        self.navmodel.record( self.mapper.currentIndex() ).value( "iddocumento" ).toString()

    def newDocument( self ):
        """
        activar todos los controles, llenar los modelos necesarios, 
        crear el modelo ChequeModel
        """
        self.tabWidget.setCurrentIndex( 0 )
        query = QSqlQuery()
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( u"No se pudo establecer la conexión "\
                                       + "con la base de datos" )

            #Crea modelo para edicion            
            self.editmodel = ChequeModel()

            #Sacar valor porcentaje del IVA
            query = QSqlQuery( """SELECT 
                valorcosto
            FROM costosagregados c 
            WHERE activo=1 AND idtipocosto=%d
            """ % ( constantes.IVA ) )
            if not query.exec_():
                raise UserWarning( "No se pudo ejecutar la consulta para"\
                                   + " obtener los valores de los impuestos" )
            elif not query.size() > 0:
                raise UserWarning( "No se pudieron obtener los valores"\
                                   + " de los impuestos" )
            query.first()
            self.editmodel.ivaRate = Decimal( query.value( 0 ).toString() )

            self.dtPicker.setDateTime( QDateTime.currentDateTime() )
            self.lbltipocambio.setText( str( self.editmodel.exchangeRate ) )


    #        Crea un edit delegate para las cuentas
            self.accountseditdelegate = ChequesFiltroDelegate( QSqlQuery( """
            SELECT c.idcuenta, c.codigo, c.descripcion 
            FROM cuentascontables c 
            JOIN cuentascontables p ON c.padre = p.idcuenta AND p.padre != 1
            WHERE c.padre != 1 AND c.idcuenta != 22
            """ ) )
            self.tabledetails.setItemDelegate( self.accountseditdelegate )
            self.tabledetails.setModel( self.editmodel )


    #            Rellenar el combobox de las retenciones
            self.retencionModel = QSqlQueryModel()
            self.retencionModel.setQuery( """             
                    SELECT
                        idcostoagregado, 
                        FORMAT(valorcosto,0) as tasa 
                    FROM costosagregados 
                    WHERE idtipocosto IN (%d,%d) AND 
                    activo=1 
                    ORDER BY valorcosto desc; 
                    """ % ( constantes.RETENCIONPROFESIONALES,
                            constantes.RETENCIONFUENTE ) )

            self.cboretencion.setModel( self.retencionModel )
            self.cboretencion.setCurrentIndex( -1 )
            self.cboretencion.setModelColumn( 1 )


    #       Rellenar el combobox de los PROVEEDORES
            self.proveedoresmodel = QSqlQueryModel()
            self.proveedoresmodel.setQuery( """
              SELECT
                    p.idpersona,
                    p.nombre,
                    p.activo
                    FROM personas p
                    where p.tipopersona=2
                    group by p.idpersona
                    ORDER BY p.nombre
                    ;
            """ )

            self.proveedoresfiltro = QSortFilterProxyModel()
            self.proveedoresfiltro.setSourceModel( self.proveedoresmodel )
            self.proveedoresfiltro.setFilterKeyColumn( 1 )
    #        self.proveedoresfiltro.setFilterRegExp("0")
            self.cbobeneficiario.setModel( self.proveedoresfiltro )
            self.cbobeneficiario.setCurrentIndex( -1 )
            self.cbobeneficiario.setModelColumn( 1 )

            completer = QCompleter()
            completer.setCaseSensitivity( Qt.CaseInsensitive )
            completer.setModel( self.proveedoresmodel )
            completer.setCompletionColumn( 1 )

    #       Rellenar el combobox de los conceptos
            self.conceptosmodel = QSqlQueryModel()
            self.conceptosmodel.setQuery( """
              SELECT idconcepto,descripcion 
              FROM conceptos c;
            """ )
            self.cboconcepto.setModel( self.conceptosmodel )
            self.cboconcepto.setCurrentIndex( -1 )
            self.cboconcepto.setModelColumn( 1 )

            completer = QCompleter()
            completer.setCaseSensitivity( Qt.CaseInsensitive )
            completer.setModel( self.conceptosmodel )
            completer.setCompletionColumn( 1 )

            self.cuentabancaria = QSqlQueryModel()
            #self.status = False
    #            Rellenar el combobox de las CONCEPTOS

            self.cuentabancaria.setQuery( """
               SELECT 
                   idcuentacontable,
                   cc.codigo,
                   CONCAT(cc.descripcion,"  Moneda: ",tm.moneda) as Descripcion,
                   tm.moneda as Moneda,
                   tm.simbolo as simbolo,
                   tm.idtipomoneda as IDMONEDA
               FROM cuentasbancarias c 
               JOIN cuentascontables cc ON cc.idcuenta=c.idcuentacontable
               JOIN tiposmoneda tm ON tm.idtipomoneda=c.idtipomoneda;
            """ )


            line = AccountsSelectorLine()
            record = self.cuentabancaria.record( self.cbocuenta.currentIndex() )
            line.itemId = record.value( "idcuentacontable" ).toInt()[0]
            line.code = record.value( "codigo" ).toString()
            line.name = record.value( "descripcion" ).toString()
            line.amount = self.subtotal.value()

            self.editmodel.insertRow( 0 )
            self.editmodel.lines[0] = line

            self.cbocuenta.setModel( self.cuentabancaria )
            self.cbocuenta.setCurrentIndex( -1 )
            self.cbocuenta.setModelColumn( 2 )

            self.tabledetails.resizeColumnsToContents()
            self.tabledetails.setColumnHidden( 0, True )


            completercuenta = QCompleter()
            completercuenta.setCaseSensitivity( Qt.CaseInsensitive )
            completercuenta.setModel( self.cuentabancaria )
            completercuenta.setCompletionColumn( 1 )





            self.lblretencion.setText( "" )

            self.status = False
        except UserWarning as inst:
            logging.error( unicode( inst ) )
            QMessageBox.warning( self,
                                 qApp.organizationName(),
                                 unicode( inst ) )
            self.status = True
        except Exception as inst:
            QMessageBox.warning( self,
                                 qApp.organizationName(),
                                 u"No se pudo iniciar la creación "\
                                 + "del nuevo cheque" )
            logging.critical( unicode( inst ) )
            self.status = True
        finally:
            if self.database.isOpen():
                self.database.close()



    @pyqtSlot( QDateTime )
    def on_dtPicker_dateTimeChanged( self, datetime ):
        """
        Asignar la fecha al objeto __document
        """
        if self.editmodel is not None:
            super( FrmCheques, self ).on_dtPicker_dateTimeChanged( datetime )
            self.lbltipocambio.setText( str( self.editmodel.exchangeRate ) )

    @pyqtSlot()
    def anular( self ):
        record = self.navmodel.record( self.mapper.currentIndex() )
        """
        @var: El elemento actual en el navmodel
        @type: QSqlRecord
        """
        
        doc = record.value( "iddocumento" ).toInt()[0]
        total = Decimal( record.value( "TotalCheque" ).toString() )
        
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise Exception( "NO se pudo abrir la Base de datos" )
            
            if QMessageBox.question( self,
                 qApp.organizationName(),
                 u"¿Esta seguro que desea anular el cheque?",
                 QMessageBox.Yes | QMessageBox.No ) == QMessageBox.Yes:

                anulardialog = Anular( self.navmodel.record( self.mapper.currentIndex() ).value( "No. Cheque" ).toString() )
                if anulardialog.conceptosmodel.rowCount() == 0:
                    QMessageBox.warning( self,
                                         qApp.organizationName(),
                                         u"No existen conceptos para la anulación" )
                else:
                    if anulardialog.exec_() == QDialog.Accepted:
                        if anulardialog.cboConceptos.currentIndex() == -1 and anulardialog.txtObservaciones.toPlainText() == "":
                            QMessageBox.critical( self,
                                                  qApp.organizationName(),
                                                  "Por favor rellene todos los campos" )
                        else:
                            query = QSqlQuery()
                            if not self.database.transaction():
                                raise Exception( "No se pudo comenzar la transacción" )
                            #
                            query = QSqlQuery( """
                                SELECT fnConsecutivo(%d,NULL);
                                """ % constantes.IDANULACION)
                            if not query.exec_():
                                raise Exception( "No se pudo obtener el numero de la factura" )
                            query.first()
                            n = query.value( 0 ).toString()
                            #Insertar documento anulacion
                            if not query.prepare( """
                            INSERT INTO documentos(ndocimpreso,total,fechacreacion,idtipodoc,observacion,idestado)
                            VALUES(:ndocimpreso,:total,:fechacreacion,:idtipodoc,:observacion,:idestado)""" ):
                                raise Exception( query.lastError().text() )
                            
                            query.bindValue( ":ndocimpreso", n )
                            query.bindValue( ":total", total.to_eng_string() )
                            query.bindValue( ":fechacreacion", QDate.currentDate() )
                            query.bindValue( ":idtipodoc", constantes.IDANULACION )
                            query.bindValue( ":observacion", anulardialog.txtObservaciones.toPlainText() )
                            query.bindValue( ":idestado", constantes.CONFIRMADO )
            
                            if not query.exec_():
                                raise Exception( "No se pudo insertar el documento Anulacion" )

                            idanulacion = query.lastInsertId().toString()
                            
                            query.prepare( "CALL spEliminarCheque(:doc,:anulado,:idcheque,:idretencion)" )
                            query.bindValue( ":doc", idanulacion )
                            query.bindValue( ":idcheque", doc )
                            query.bindValue( ":anulado", constantes.ANULADO)
                            query.bindValue( ":idretencion", constantes.IDRETENCION)
                            if not query.exec_():
                                raise UserWarning( "No se pudo Anular el Cheque" )                         
                            
            
                            if not query.prepare( "INSERT INTO docpadrehijos (idpadre,idhijo) VALUES" +
                        "(:idcheque," + idanulacion + ")" ):
            #                                "(:usuario," + insertedId + ",0),"
            #                                "(:supervisor," + insertedId + ",1)"):
                                raise Exception( query.lastError().text() + "No se preparo la relacion de la anulacion con el Cheque" )
            
                            query.bindValue( ":idcheque", doc )
            
                            if not query.exec_():
                                raise Exception( "No se pudo insertar la relacion de la Anulacion con el Cheque" )
            
            
                            if not query.prepare( "INSERT INTO personasxdocumento (idpersona,iddocumento,idaccion) VALUES" +
                            "(:usuario," + idanulacion + ",:accion)" ):
                                raise Exception( query.lastError().text() + "No se inserto el usuario y autoriza" )
            
                            query.bindValue( ":usuario", self.user.uid )
                            query.bindValue ( ":accion", constantes.AUTOR )
            
                            if not query.exec_():
                                raise Exception( "No se pudo Insertar la relacion de la anulacion con el usuario" )
            
            
                            if not self.database.commit():
                                raise Exception( "NO se hizo el commit para la Anulacion" )
                            QMessageBox.information( self,
                                                     qApp.organizationName(),
                                                     "Cheque anulado Correctamente",
                                                     QMessageBox.Ok )
                            self.updateModels()
        except UserWarning as inst:
            logging.error(unicode(inst))
            logging.error(query.lastError().text())
            self.database.rollback()
            QMessageBox.critical(self,
                                qApp.organizationName(),
                                unicode(inst))
        except Exception as inst:
            logging.critical( unicode( inst ) )
            logging.critical( query.lastError().text() )
            self.database.rollback()
        finally:
            if self.database.isOpen():
                self.database.close()


    def save( self ):
        """
        Guardar el documento actual
        """
        query = QSqlQuery( """
        SELECT
            cc.idcuenta,
            SUM(IFNULL(monto,0)) monto
        FROM cuentascontables cc
        LEFT JOIN cuentascontables ch ON cc.idcuenta = ch.padre
        LEFT JOIN cuentasxdocumento cxd ON cc.idcuenta = cxd.idcuenta
        WHERE cc.idcuenta = %d""" % ( 
                     self.cuentabancaria.record( 
                        self.cbocuenta.currentIndex()
                         ).value( "idcuentacontable" ).toInt()[0] ) )
        query.exec_()
        query.first()
        totalcuenta = query.value( 1 ).toString()
        if Decimal( str( self.subtotal.value() ) ) > Decimal( totalcuenta ):
            QMessageBox.warning( self,
                                 qApp.organizationName(),
                                 "No existe suficiente saldo para crear"\
                                 + " el cheque" )

        if QMessageBox.question( self,
                                 qApp.organizationName(),
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
                    QMessageBox.warning( self,
                                         qApp.organizationName() ,
                                         self.editmodel.validError )
                except AttributeError:
                    QMessageBox.warning( self,
                                         qApp.organizationName() ,
                                         u"El documento no puede guardarse ya "\
                                         + "que la información no esta completa" )


class ROAccountsModel( QSortFilterProxyModel ):
    def __init__( self, _dbcursor = None ):
        super( QSortFilterProxyModel, self ).__init__()
    def data( self, index, role = Qt.DisplayRole ):
        """
        Esta funcion redefine data en la clase base, es
        el metodo que se utiliza para mostrar los datos del modelo
        """
        value = QSortFilterProxyModel.data( self, index, role )
        if value.isValid() and role == Qt.DisplayRole:
            if index.column() == MONTO:
                try:
                    return moneyfmt( Decimal( value.toString() ), 4, "C$" )
                except InvalidOperation:
                    return Decimal( 0 )
        return value


class ChequesFiltroDelegate( AccountsSelectorDelegate ):
    def __init__( self, query ):
        super( ChequesFiltroDelegate, self ).__init__( query )
        self.__accounts = self.accounts
        self.accounts = QSortFilterProxyModel()
        self.accounts.setDynamicSortFilter( True )
        self.accounts.setSourceModel( self.__accounts )
        self.accounts.setFilterKeyColumn( 0 )

    def setModelData( self, editor, model, index ):

        if index.column() in ( 1, 2 ):
            model.setData( index, [
                       self.accounts.index( editor.currentIndex(), 0 ).data(),
                       self.accounts.index( editor.currentIndex(), 1 ).data(),
                       self.accounts.index( editor.currentIndex(), 2 ).data()
                       ] )
            try:
                index = self.accounts.mapToSource( 
                              self.accounts.index( editor.currentIndex(), 0 ) )
                del self.__accounts.items[index.row()]
            except IndexError:
                pass
        else:
            QStyledItemDelegate.setModelData( self, editor, model, index )

    def createEditor( self, parent, _option, index ):

        if index.column() in ( 1, 2 ):
            if index.data() != "":
                self.__accounts.items.append( [
                                         index.model().lines[index.row()].itemId,
                                         index.model().lines[index.row()].code,
                                         index.model().lines[index.row()].name
                                         ] )
            sp = SearchPanel( self.accounts, parent )
            sp.setColumn( index.column() )
            return sp
        elif index.column() == 3:
            doublespinbox = QDoubleSpinBox( parent )
            doublespinbox.setMinimum( -1000000 )
            doublespinbox.setMaximum( 1000000 )
            doublespinbox.setDecimals( 4 )

            return doublespinbox

class Anular( QDialog ):
    def __init__( self , numero, parent = None ):
        super( Anular, self ).__init__( parent )

        self.setupUi()


        #QtCore.QMetaObject.connectSlotsByName(self)

        self.conceptosmodel = QSqlQueryModel()
        self.conceptosmodel.setQuery( """
        SELECT idconcepto,descripcion
        FROM conceptos c
        WHERE idtipodoc = %d
        ;
        """ % constantes.IDANULACION )
        self.cboConceptos.setModel( self.conceptosmodel )
        self.cboConceptos.setCurrentIndex( -1 )
        self.cboConceptos.setModelColumn( 1 )
        self.numero = numero

        self.lblnCheque2.setText( str( self.numero ) )
        self.buttonBox.accepted.connect( self.accept )
        self.buttonBox.rejected.connect( self.reject )


    def setupUi( self ):
        self.setObjectName( "frmAnulaciones" )
        self.setWindowTitle( "Seleccione la Cheque a anular" )
        self.resize( 485, 300 )
        self.gridLayout = QtGui.QGridLayout( self )
        self.gridLayout.setObjectName( "gridLayout" )
        self.lblnCheque = QtGui.QLabel( self )
        self.lblnCheque.setObjectName( "lblnCheque" )
        self.lblnCheque.setText( "# Cheque" )
        self.gridLayout.addWidget( self.lblnCheque, 0, 0, 1, 1 )
        self.lblnCheque2 = QtGui.QLabel( self )
        self.lblnCheque2.setFrameShape( QtGui.QFrame.Box )
        self.lblnCheque2.setText( "" )
        self.lblnCheque2.setObjectName( "lblnCheque2" )
        self.gridLayout.addWidget( self.lblnCheque2, 0, 1, 1, 1 )
        self.lblconcepto = QtGui.QLabel( self )
        self.lblconcepto.setObjectName( "lblconcepto" )
        self.lblconcepto.setText( "Concepto" )
        self.gridLayout.addWidget( self.lblconcepto, 1, 0, 1, 1 )
        self.cboConceptos = QtGui.QComboBox( self )
        self.cboConceptos.setObjectName( "cboConceptos" )
        self.gridLayout.addWidget( self.cboConceptos, 1, 1, 1, 1 )
        self.lblobservaciones = QtGui.QLabel( self )
        self.lblobservaciones.setObjectName( "lblobservaciones" )
        self.lblobservaciones.setText( "Observaciones" )
        self.gridLayout.addWidget( self.lblobservaciones, 2, 0, 1, 1 )
        self.txtObservaciones = QtGui.QPlainTextEdit( self )
        self.txtObservaciones.setObjectName( "txtObservaciones" )
        self.gridLayout.addWidget( self.txtObservaciones, 3, 1, 1, 1 )
        self.buttonBox = QtGui.QDialogButtonBox( self )
        self.buttonBox.setOrientation( QtCore.Qt.Horizontal )
        self.buttonBox.setStandardButtons( 
                  QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok )
        self.buttonBox.setObjectName( "buttonBox" )
        self.gridLayout.addWidget( self.buttonBox, 4, 0, 1, 2 )
