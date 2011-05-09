# -*- coding: utf-8 -*-
#TODO: REFACTOR!!!
#FIXME: Se tiene que insertar el id de la bodega en la anulación
'''
Created on 25/05/2010
@author: Luis Carlos Mejia
'''
from PyQt4.QtCore import pyqtSlot, Qt, QModelIndex, QTimer, QDate, QDateTime
from PyQt4.QtGui import QDataWidgetMapper, QSortFilterProxyModel, QMessageBox, \
    QAbstractItemView, QCompleter, QDialog, qApp, QFormLayout, QVBoxLayout, \
    QDateEdit, QDoubleSpinBox, QLabel, QFrame, QDialogButtonBox, QPlainTextEdit, \
    QComboBox, QGridLayout, QIcon
from PyQt4.QtSql import QSqlQuery, QSqlQueryModel
from decimal import Decimal
from document.factura.facturadelegate import FacturaDelegate, \
    SingleSelectionModel
from document.factura.facturamodel import FacturaModel
from recibo import FrmRecibo, DlgRecibo
from ui.Ui_factura import Ui_frmFactura
from utility import constantes
from utility.base import Base
from utility.moneyfmt import moneyfmt
import logging
from utility.decorators import if_edit_model

#el modelo de la existencia
IDARTICULOEX, DESCRIPCIONEX, PRECIOEX, COSTOEX, EXISTENCIAEX, \
 IDBODEGAEX = range( 6 )

#controles
IDDOCUMENTO, NDOCIMPRESO, CLIENTE, VENDEDOR, SUBTOTAL, IVA, TOTAL, \
OBSERVACION, FECHA, BODEGA, TASA, TASAIVA, ESTADO, ANULADO, \
ESCONTADO, TOTALFAC, ANULABLE, IDBODEGA = range( 18 )

#table
IDARTICULO, DESCRIPCION, CANTIDAD, PRECIO, TOTALPROD, IDDOCUMENTOT = range( 6 )
class FrmFactura( Base, Ui_frmFactura ):
    """
    Implementacion de la interfaz grafica para facturas
    """
    web = "facturas.php?doc="
    def __init__( self, parent ):
        '''
        Constructor
        '''
        super( FrmFactura, self ).__init__( parent )
        self.readOnly = True
        self.recibo = None

        self.clientesModel = QSqlQueryModel()

#       las acciones deberian de estar ocultas
        self.actionSave.setVisible( False )
        self.actionCancel.setVisible( False )
#        El modelo principal
        self.navmodel = QSqlQueryModel( self )
#        El modelo que filtra a self.navmodel
        self.navproxymodel = QSortFilterProxyModel( self )
        self.navproxymodel.setSourceModel( self.navmodel )
        self.navproxymodel.setFilterKeyColumn( -1 )
        self.navproxymodel.setFilterCaseSensitivity ( Qt.CaseInsensitive )
#        Este es el modelo con los datos de la con los detalles
        self.detailsmodel = QSqlQueryModel( self )
        self.detailsproxymodel = QSortFilterProxyModel( self )
        self.detailsproxymodel.setSourceModel( self.detailsmodel )
        #inicializando el documento
        self.editmodel = None
        self.lblanulado.setHidden( True )
        self.toolBar.removeAction( self.actionAnular )
        self.toolBar.addAction( self.actionAnular )
        self.recibo = None

        self.cargarRecibos()

        self.existenciaModel = QSqlQueryModel()
        self.vendedoresModel = QSqlQueryModel()
        self.bodegasModel = QSqlQueryModel()

        self.anulable = 2
        """
        @ivar: Si la factura actual se puede anular o no
        @type: int
        """

        self.tabledetails.setOrder( 1, 3 )

        self.completer = QCompleter()
        self.completerVendedor = QCompleter()

        QTimer.singleShot( 0, self.loadModels )

    def cargarRecibos( self ):
        self.recibo = FrmRecibo( self )  #dlgRecibo( self, True )
        self.recibo.setWindowModality( Qt.WindowModal )
        self.recibo.setWindowFlags( Qt.Dialog )
        self.recibo.actionNew.setVisible( False )

    def cancel( self ):
        """
        Aca se cancela la edición del documento
        """
        self.editmodel = None
        self.tablenavigation.setModel( self.navproxymodel )
        self.tabledetails.setModel( self.detailsproxymodel )

        self.readOnly = True
        self.status = True



    def newDocument( self ):
        """
        activar todos los controles, llenar los modelos necesarios, 
        crear el modelo FacturaModel, aniadir una linea a la tabla
        """
        self.readOnly = False



        if not self.updateEditModels():
            return

        self.status = False
        self.dtPicker.setDate( self.parentWindow.datosSesion.fecha )

    def updateEditModels( self ):
        """
        Este metodo actualiza los modelos usados en el modo edición
        """
        resultado = False
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( u"No se pudo abrir la conexión "\
                                       + "con la base de datos" )

            self.editmodel = FacturaModel( self.parentWindow.datosSesion )

                #           Cargar el numero de la factura actual
            query = QSqlQuery( """
                        SELECT fnConsecutivo(%d,NULL);
                    """ % constantes.IDFACTURA )
            if not query.exec_():
                raise Exception( "No se pudo obtener el numero de la factura" )
            query.first()
            n = query.value( 0 ).toString()



            self.editmodel.printedDocumentNumber = n

            self.clientesModel.setQuery( """
                        SELECT idpersona , nombre AS cliente 
                        FROM personas
                        WHERE tipopersona = %d
                    """ % constantes.CLIENTE )
            if self.clientesModel.rowCount() == 0:
                raise UserWarning( "No existen clientes en la"\
                                          + " base de datos" )
                return

    #            Rellenar el combobox de los vendedores

            self.vendedoresModel.setQuery( """
                SELECT 
                idpersona, 
                nombre AS Vendedor 
                FROM personas
                WHERE tipopersona = %d
            """ % constantes.VENDEDOR )

    #Verificar si existen clientes            
            if self.vendedoresModel.rowCount() == 0:
                raise UserWarning( "No existen vendedores en la "\
                                      + "base de datos" )

        #Crear el delegado con los articulo y verificar si existen articulos
            self.existenciaModel.setQuery( QSqlQuery( """
            SELECT
                idarticulo,
                descripcion,
                precio,
                ROUND(costo,4) as costo,
                Existencia,
                idbodega
            FROM vw_articulosenbodegas
             WHERE existencia >0
                    """ ) )
            self.proxyexistenciaModel = SingleSelectionModel()
            self.proxyexistenciaModel.setSourceModel( self.existenciaModel )
            self.proxyexistenciaModel.setFilterKeyColumn( IDBODEGAEX )

            if self.proxyexistenciaModel.rowCount() == 0:
                raise UserWarning( "No hay articulos en bodega" )

            delegate = FacturaDelegate( self.proxyexistenciaModel )


    #            Rellenar el combobox de las BODEGAS

            self.bodegasModel.setQuery( """
                     SELECT
                            b.idbodega,
                            b.nombrebodega as Bodega
                    FROM bodegas b
                    JOIN documentos d ON b.idbodega=d.idbodega
                    JOIN docpadrehijos ph ON ph.idpadre =d.iddocumento
                    JOIN documentos k ON ph.idhijo = k.iddocumento AND k.idtipodoc = %d
            JOIN articulosxdocumento ad ON ad.iddocumento=d.iddocumento
            GROUP BY b.idbodega
            HAVING SUM(ad.unidades)>0    
                    """ % constantes.IDKARDEX )

        #Verificar si existen bodegas            
            if self.bodegasModel.rowCount() == 0:
                raise UserWarning( "No existe ninguna bodega "\
                                   + "en la base de datos" )

    #Verificar IVA    
            query = QSqlQuery( """
                    SELECT idcostoagregado, valorcosto 
                    FROM costosagregados c 
                    WHERE idtipocosto = 1 AND activo = 1 
                    ORDER BY idtipocosto;
                    """ )
            query.exec_()
            if not query.size() == 1:
                raise UserWarning( "No fue posible obtener el "\
                                   + "porcentaje del IVA" )


            query.first()


            self.editmodel.ivaId = query.value( 0 ).toInt()[0]
            self.lbltasaiva.setText( ( '0' if self.editmodel.bodegaId != 1 else str( self.editmodel.ivaTasa ) ) + '%' )
            self.editmodel.ivaTasa = Decimal( query.value( 1 ).toString() )


            self.tabledetails.setItemDelegate( delegate )


            self.cbcliente.setModel( self.clientesModel )
            self.cbcliente.setCurrentIndex( -1 )
            self.cbcliente.setFocus()
            self.cbcliente.setModelColumn( 1 )

            self.completer.setCaseSensitivity( Qt.CaseInsensitive )
            self.completer.setModel( self.clientesModel )
            self.completer.setCompletionColumn( 1 )
            self.cbcliente.setCompleter( self.completer )


            self.cbbodega.setModel( self.bodegasModel )
            self.cbbodega.setCurrentIndex( -1 )
            self.cbbodega.setModelColumn( 1 )
            self.completerbodega = QCompleter()
            self.completerbodega.setCaseSensitivity( Qt.CaseInsensitive )
            self.completerbodega.setModel( self.bodegasModel )
            self.completerbodega.setCompletionColumn( 1 )
            self.cbbodega.setCompleter( self.completerbodega )

            self.cbvendedor.setModel( self.vendedoresModel )
            self.cbvendedor.setCurrentIndex( -1 )
            self.cbvendedor.setModelColumn( 1 )

            self.completerVendedor.setCaseSensitivity( Qt.CaseInsensitive )
            self.completerVendedor.setModel( self.vendedoresModel )
            self.completerVendedor.setCompletionColumn( 1 )
            self.cbvendedor.setCompleter( self.completerVendedor )

            self.tabledetails.setModel( self.editmodel )
            self.addLine()
            self.editmodel.dataChanged[QModelIndex, QModelIndex].connect( self.updateLabels )

            self.rbcontado.setChecked( True )
            self.txtobservaciones.setPlainText( "" )

            resultado = True
        except UserWarning as inst:
            logging.error( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(), unicode( inst ) )
        finally:
            if self.database.isOpen():
                self.database.close()
        return resultado

    @property
    def printIdentifier( self ):
        return self.navmodel.record( self.mapper.currentIndex()
                                     ).value( "iddocumento" ).toString()

    def addActionsToToolBar( self ):
        self.actionRefresh = self.createAction( text = "Actualizar",
                                icon = QIcon.fromTheme( 'view-refresh', QIcon( ":/icons/res/view-refresh.png" ) ),
                                 slot = self.refresh,
                                 shortcut = Qt.Key_F5 )

        self.toolBar.addActions( [
            self.actionNew,
            self.actionRefresh,
            self.actionPreview,
            self.actionPrint,
            self.actionSave,
            self.actionCancel,
        ] )
        self.toolBar.addSeparator()
        self.toolBar.addActions( [
            self.actionGoFirst,
            self.actionGoPrevious,
            self.actionGoLast,
            self.actionGoNext,
            self.actionGoLast
        ] )

    def refresh( self ):
        """
        Actualizar los modelos de edición
        """
        if not self.status:
            if QMessageBox.question( self, qApp.organizationName(),
                                      u"Se perderán todos los cambios en la factura. ¿Esta seguro que desea actualizar?", QMessageBox.Yes | QMessageBox.No ) == QMessageBox.No:
                return
            self.updateEditModels()
        else:
            if self.updateModels():
                QMessageBox.information( None, "Factura",
                                     u"Los datos fueron actualizados con éxito" )


    def save( self ):
        """
        Guardar el documento actual
        @rtype: bool
        """
        result = False
        try:
            if not self.valid:
                return False

            if self.editmodel.escontado:
                recibo = DlgRecibo( self )
                if recibo.datosRecibo.retencionValida:
                    if recibo.datosRecibo.retencionModel.rowCount() == 0:
                        raise UserWarning( "No es posible crear un recibo "\
                        + "porque no existen retenciones en la base de datos" )
                else:
                    recibo.ckretener.setChecked( False )
                    recibo.ckretener.setEnabled( False )


                if recibo.exec_() == QDialog.Rejected:

                    return
            else:
                credito = DlgCredito( self )
                if not credito.exec_() == QDialog.Accepted:
                    return

                self.editmodel.fechaTope = credito.dtFechaTope.date()
                self.editmodel.multa = Decimal( str( credito.sbTaxRate.value() ) )

            if QMessageBox.question( self, qApp.organizationName(),
                                     u"¿Esta seguro que desea guardar la factura?",
                                     QMessageBox.Yes | QMessageBox.No ) == QMessageBox.Yes:

                if not self.database.isOpen():
                    if not self.database.open():
                        raise UserWarning( u"No se pudo conectar con la base de datos" )

                self.editmodel.observaciones = self.txtobservaciones.toPlainText()
                if self.editmodel.escontado:
                    recibo.datosRecibo.observaciones = recibo.txtobservaciones.toPlainText()
                if not self.editmodel.save( recibo.datosRecibo if self.editmodel.escontado else None ):
                    raise UserWarning( "No se ha podido guardar la factura" )

                QMessageBox.information( None,
                     qApp.organizationName() ,
                     u"""El documento se ha guardado con éxito""" )

                self.editmodel = None
                self.readOnly = True

                self.updateModels()
                self.cargarRecibos()
                self.navigate( 'last' )
                self.status = True
                result = True
        except UserWarning as inst:
            logging.error( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(), unicode( inst ) )
        except Exception as inst:
            logging.critical( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(),
                                 u"Hubo un error al guardar la factura" )
        finally:
            if self.database.isOpen():
                self.database.close()
        return result


#FIXME: Hay demasiados if y cosas por el estilo en esta función...deberia de 
#hacerse un refactor
    @pyqtSlot()
    def on_actionAnular_activated( self ):
        if self.anulable == 2:
            QMessageBox.warning( self, qApp.organizationName(),
                                  u"La factura no puede anularse. Solo las"\
                                  + " facturas confirmadas o en proceso de "\
                                  + "autorización pueden anularse" )
        elif self.anulable == 3:
            QMessageBox.warning( self, qApp.organizationName(),
                                  u"La factura no puede anularse porque no "\
                                  + "es del día de hoy" )
        elif self.anulable == 4:
            QMessageBox.warning( self, qApp.organizationName(),
                                  u"La factura no puede anularse porque tiene"\
                                  + " abonos" )
        elif self.anulable == 5:
            QMessageBox.warning( self, qApp.organizationName(),
                                  u"La factura no puede anularse porque tiene"\
                                  + " devoluciones" )
        elif self.anulable == 1:
            currentIndex = self.mapper.currentIndex()
            record = self.navmodel.record( currentIndex )
            doc = record.value( "iddocumento" ).toInt()[0]
            estado = record.value( "idestado" ).toInt()[0]
            total = record.value( "totalfac" ).toString()
            bodega = record.value( IDBODEGA ).toInt()[0]
            if total != "":
                total = Decimal( total )

            query = QSqlQuery()
            try:
                if not self.database.isOpen():
                    if not self.database.open():
                        raise Exception( "NO se pudo abrir la Base de datos" )

                if estado == 3:
                    if QMessageBox.question( self, qApp.organizationName(),
                                              u"Esta factura no fue confirmada,"\
                                              + " ¿Desea eliminarla?",
                                              QMessageBox.Yes | QMessageBox.No ) == QMessageBox.Yes:
                        query = QSqlQuery()
                        query.prepare( "CALL spEliminarFactura(:doc)" )
                        query.bindValue( ":doc", doc )
                        if not query.exec_():
                            raise Exception( "No se pudo eliminar el la factura" )

                        QMessageBox.information( self, qApp.organizationName(),
                                                  "La factura fue eliminada correctamente" )
                        self.updateModels()
                else:
                    if QMessageBox.question( self, qApp.organizationName(),
                                             u"¿Esta seguro que desea anular la factura?",
                                              QMessageBox.Yes | QMessageBox.No ) == QMessageBox.Yes:

                        nfac = self.navmodel.record( self.mapper.currentIndex() ).value( "No. Factura" ).toString()
                        anulardialog = DlgAnular( nfac )
                        if anulardialog.conceptosmodel.rowCount() == 0:
                            QMessageBox.warning( self, qApp.organizationName(),
                                                  u"No existen conceptos para la anulación" )

                        else:
                            if anulardialog.exec_() == QDialog.Accepted:
                                if anulardialog.cboConceptos.currentIndex() == -1 and anulardialog.txtObservaciones.toPlainText() == "":
                                    QMessageBox.critical( self, qApp.organizationName(), "No ingreso los datos correctos", QMessageBox.Ok )
                                else:


                                    if not self.database.transaction():
                                        raise Exception( "No se pudo comenzar la transacción" )

                                    #Cambiar estado Anulado=1 para documento
                                    query.prepare( "UPDATE documentos d SET idestado=%d where iddocumento=%d LIMIT 1" % ( constantes.ANULACIONPENDIENTE, doc ) )
                                    if not query.exec_():
                                        raise Exception( "No se logro cambiar el estado a el documento" )

                                    #Insertar documento anulacion
                                    if not query.prepare( """
                                    INSERT INTO documentos(ndocimpreso,total,fechacreacion,idtipodoc,observacion,idestado, idbodega)
                                    VALUES(:ndocimpreso,:total,NOW(),:idtipodoc,:observacion,:idestado, :idbodega)""" ):
                                        raise Exception( query.lastError().text() )
                                    query.bindValue( ":ndocimpreso", nfac )
                                    query.bindValue( ":total", str( total ) )
#                                    query.bindValue( ":fechacreacion", QDateTime.currentDateTime().toString('yyyyMMddhhmmss') )
                                    query.bindValue( ":idtipodoc", constantes.IDANULACION )
                                    query.bindValue( ":observacion", anulardialog.txtObservaciones.toPlainText() )
                                    query.bindValue( ":idestado", constantes.PENDIENTE )
                                    query.bindValue( ":idbodega", bodega )

                                    if not query.exec_():
                                        raise Exception( "No se pudo insertar el documento Anulacion" )

                                    insertedId = query.lastInsertId().toString()

                                    if not query.prepare( "INSERT INTO docpadrehijos (idpadre,idhijo) VALUES" +
                                "(:idfac," + insertedId + ")" ):
    #                                "(:usuario," + insertedId + ",0),"
    #                                "(:supervisor," + insertedId + ",1)"):
                                        raise Exception( query.lastError().text() + "No se preparo la relacion de la anulacion con la factura" )

                                    query.bindValue( ":idfac", doc )

                                    if not query.exec_():
                                        raise Exception( "No se pudo insertar la relacion de la Anulacion con la factura" )


                                    if not query.prepare( "INSERT INTO personasxdocumento (idpersona,iddocumento,idaccion) VALUES" \
                                    + "(:usuario," + insertedId + ",:accion)" ):
                                        raise Exception( "No se inserto el usuario y autoriza" )

                                    query.bindValue( ":usuario", self.parentWindow.datosSesion.usuarioId )
                                    query.bindValue ( ":accion", constantes.AUTOR )

                                    if not query.exec_():
                                        raise Exception( "No se pudo Insertar la relacion de la anulacion con el usuario" )


                                    if not self.database.commit():
                                        raise Exception( "No se hizo el commit para la Anulacion" )

                                    QMessageBox.information( self,
                                                             qApp.organizationName(),
                                                             "Factura anulada Correctamente",
                                                             QMessageBox.Ok )
                                    self.updateModels()

            except Exception as inst:
                logging.error( unicode( inst ) )
                logging.error( query.lastError().text() )
                QMessageBox.critical( self, qApp.organizationName(),
                                      unicode( inst ) )
                self.database.rollback()
            except Exception as inst:
                logging.critical( unicode( inst ) )
                logging.critical( query.lastError().text() )
                QMessageBox.critical( self,
                                      qApp.organizationName(),
                                       "Hubo un error al intentar anular "\
                                       + "la factura" )
                self.database.rollback()
            finally:
                if self.database.isOpen():
                    self.database.close()

    @pyqtSlot()
    def on_actionRecibo_activated( self ):
        index = self.mapper.currentIndex()
        record = self.navmodel.record( index )
        self.recibo.remoteProxyModel.setFilterRegExp( "(%s)" % record.value( "iddocumento" ).toString() )
        if self.recibo.remoteProxyModel.rowCount() > 0:
            self.recibo.mapper.setCurrentIndex( 1 )
        if self.recibo.remoteProxyModel.rowCount() != 0:
            self.recibo.mapper.setCurrentIndex( 0 )
            self.recibo.show()


    @pyqtSlot( int )
    def on_cboFiltro_currentIndexChanged( self, index ):
        """
        asignar la bodega al objeto self.editmodel

        """
        self.navproxymodel.setFilterKeyColumn( ANULADO )
        if index == 0:
            self.navproxymodel.setFilterRegExp( "" )
        else:
            self.navproxymodel.setFilterRegExp( "^%d$" % index )

    @pyqtSlot( int )
    @if_edit_model
    def on_cbbodega_currentIndexChanged( self, index ):
        """
        asignar la bodega al objeto self.editmodel
        """
        if self.editmodel.rowCount() > 0 and self.editmodel.lines[0].itemDescription != "":
            self.editmodel.removeRows( 0, self.editmodel.rowCount() )

        self.editmodel.bodegaId = self.bodegasModel.record( index ).value( "idbodega" ).toInt()[0]
        self.proxyexistenciaModel.setFilterRegExp( '^%d$' % self.editmodel.bodegaId )
        self.tabledetails.setColumnHidden( IDARTICULO, True )
        self.updateLabels()



    @pyqtSlot( int )
    @if_edit_model
    def on_cbcliente_currentIndexChanged( self, index ):
        """
        asignar proveedor al objeto self.editmodel
        """
        self.editmodel.clienteId = self.clientesModel.record( index ).value( "idpersona" ).toInt()[0]

    @pyqtSlot( int )
    @if_edit_model
    def on_cbvendedor_currentIndexChanged( self, index ):
        """
        asignar proveedor al objeto self.editmodel
        """
        self.editmodel.vendedorId = self.vendedoresModel.record( index ).value( "idpersona" ).toInt()[0]


    @pyqtSlot( QDateTime )
    def on_dtPicker_dateTimeChanged( self, datetime ):
        pass

    @pyqtSlot( bool )
    @if_edit_model
    def on_rbcontado_toggled( self, on ):
        """
        Asignar las observaciones al objeto editmodel
        """
        self.editmodel.escontado = 1 if on else 0


    def setControls( self, status ):
        """
        @param status: false = editando        true = navegando
        """
        self.actionPrint.setVisible( status )
        self.readOnly = status
        self.txtobservaciones.setReadOnly( status )
        self.rbcontado.setEnabled( ( not status ) )
        self.rbcredito.setEnabled( not status )

        self.actionSave.setVisible( not status )
        self.actionCancel.setVisible( not status )
        self.tabnavigation.setEnabled( status )
        self.actionNew.setVisible( status )
        self.actionGoFirst.setVisible( status )
        self.actionGoPrevious.setVisible( status )
        self.actionGoNext.setVisible( status )
        self.actionGoLast.setVisible( status )
        self.actionPreview.setVisible( status )
        self.actionAnular.setVisible( status )
        self.actionRecibo.setVisible( status )

        if status:
            self.navigate( 'last' )
            self.swcliente.setCurrentIndex( 1 )
            self.swbodega.setCurrentIndex( 1 )
            self.swvendedor.setCurrentIndex( 1 )
            self.tabledetails.setEditTriggers( QAbstractItemView.NoEditTriggers )

            self.tabledetails.removeAction( self.actionDeleteRow )

            self.tablenavigation.setColumnHidden( IDDOCUMENTO, True )
            self.tablenavigation.setColumnHidden( OBSERVACION, True )
            self.tablenavigation.setColumnHidden( SUBTOTAL, True )
            self.tablenavigation.setColumnHidden( IVA, True )
            self.tablenavigation.setColumnHidden( TASAIVA, True )
            self.tablenavigation.setColumnHidden( TASA, True )
            self.tablenavigation.setColumnHidden( ESCONTADO, True )
            self.tablenavigation.setColumnHidden( ANULADO, True )
            self.tablenavigation.setColumnHidden( TOTALFAC, True )
            self.tablenavigation.setColumnHidden( IDBODEGA, True )
            self.tablenavigation.setColumnHidden( ANULABLE, True )


        else:
#            self.btnrecibo.setHidden( True )
            self.tabWidget.setCurrentIndex( 0 )
            self.lblnfac.setText( self.editmodel.printedDocumentNumber )
            self.swcliente.setCurrentIndex( 0 )
            self.swbodega.setCurrentIndex( 0 )
            self.swvendedor.setCurrentIndex( 0 )
            self.lblsubtotal.setText( "0.0000" )
            self.lbliva.setText( "0.0000" )
            self.lbltotal.setText( "0.0000" )
            self.tabledetails.setEditTriggers( QAbstractItemView.AllEditTriggers )
            self.lblanulado.setHidden( True )

            self.tabledetails.addAction( self.actionDeleteRow )

#            self.tabledetails.horizontalHeader().setStretchLastSection(True)

        self.tabledetails.setColumnHidden( IDARTICULO, True )
        self.tabledetails.setColumnHidden( IDDOCUMENTOT, True )


    def updateDetailFilter( self, index ):
        record = self.navmodel.record( index )
        self.lbltasaiva.setText( record.value( "tasaiva" ).toString() + '%' )
        self.lblanulado.setHidden( record.value( "idestado" ).toInt()[0] != constantes.ANULADO )
        self.anulable = record.value( ANULABLE ).toInt()[0]
#        self.actionAnular.setEnabled()
        escontado = record.value( "escontado" ).toBool()
        if escontado:
            self.rbcontado.setChecked( True )

        else:
            self.rbcredito.setChecked( True )
#            self.recibo.setHidden(True)

        self.detailsproxymodel.setFilterKeyColumn( IDDOCUMENTOT )
        self.detailsproxymodel.setFilterRegExp( record.value( "iddocumento" ).toString() )
        self.tablenavigation.selectRow( self.mapper.currentIndex() )

    def updateLabels( self ):
        self.lblsubtotal.setText( moneyfmt( self.editmodel.subtotal, 4, "US$ " ) )
        self.lbliva.setText( moneyfmt( self.editmodel.IVA, 4, "US$ " ) )
        self.lbltotal.setText( moneyfmt( self.editmodel.total, 4, "US$ " ) )
        self.lbltasaiva.setText( str( self.editmodel.ivaTasa ) + '%' )
        self.tabledetails.resizeColumnsToContents()

    def updateModels( self ):
        """
        Recargar todos los modelos
        """
        resultado = False
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( u"No se pudo establecer la "\
                                       + "conexión con la base de datos" )


    #        El modelo principal

            query = """
            SELECT
            
                    d.iddocumento,
                    d.ndocimpreso as 'No. Factura',
                    GROUP_CONCAT(IF(pxd.idaccion=%d,p.nombre,"") SEPARATOR '') as Cliente,
                    GROUP_CONCAT(IF(pxd.idaccion=%d,p.nombre,"") SEPARATOR '') as Vendedor,
                    CONCAT('US$ ',FORMAT(ROUND(d.total / (1+ IF(valorcosto IS NULL,0,valorcosto/100)),4),4))  as subtotal,
                    CONCAT('US$ ',FORMAT(d.total- ROUND(d.total / (1+ IF(valorcosto IS NULL,0,valorcosto/100)),4),4))  as iva,
                    CONCAT('US$ ',FORMAT(d.Total,4)) as Total,
                    d.observacion,
                    d.fechacreacion as Fecha,
                    b.nombrebodega as Bodega,
                    tc.tasa as 'Tipo de Cambio Oficial',
                    valorcosto as tasaiva,
                    ed.descripcion as Estado,
                    d.idestado,
                    d.escontado,
                    d.total as totalfac,
                    fnFacturaAnulable(d.iddocumento,d.idtipodoc,%d,%d,%d,%d) as anulable,
                    b.idbodega
                FROM documentos d
                JOIN estadosdocumento ed ON ed.idestado = d.idestado
                JOIN bodegas b ON b.idbodega=d.idbodega
                JOIN tiposcambio tc ON tc.idtc=d.idtipocambio
                JOIN personasxdocumento pxd ON pxd.iddocumento=d.iddocumento
                JOIN personas p ON p.idpersona=pxd.idpersona
                LEFT JOIN costosxdocumento cd ON cd.iddocumento=d.iddocumento
                LEFT JOIN costosagregados ca ON ca.idcostoagregado=cd.idcostoagregado
                WHERE d.idtipodoc=%d
                GROUP BY d.iddocumento
                ORDER BY CAST(IF(ndocimpreso='S/N',0,d.ndocimpreso) AS SIGNED)
                ;
            """ % ( constantes.CLIENTE,
                    constantes.VENDEDOR,
                    constantes.IDRECIBO,
                    constantes.IDNC,
                    constantes.CONFIRMADO,
                    constantes.PENDIENTE,
                    constantes.IDFACTURA )
            self.navmodel.setQuery( query )



    #        Este es el modelo con los datos de la tabla para navegar
            self.detailsmodel.setQuery( u"""
                SELECT
                    ad.idarticulo,
                    ad.descripcion as 'Descripción',
                    -a.unidades as Unidades,
                    CONCAT('US$ ',FORMAT(a.precioventa,4)) as 'Precio Unit.',
                    CONCAT('US$ ',FORMAT(-a.unidades*a.precioventa,4)) as 'Total',
                    a.iddocumento
                FROM articulosxdocumento a
                JOIN vw_articulosdescritos ad on a.idarticulo=ad.idarticulo
                WHERE a.precioventa IS NOT NULL
                ;
            """ )

    #        Este objeto mapea una fila del modelo self.navproxymodel a los controles

            self.mapper.setSubmitPolicy( QDataWidgetMapper.ManualSubmit )

            self.mapper.setModel( self.navproxymodel )
            self.mapper.addMapping( self.lblnfac, NDOCIMPRESO , "text" )
            self.mapper.addMapping( self.txtobservaciones, OBSERVACION )
            self.mapper.addMapping( self.txtcliente, CLIENTE, "text" )
            self.mapper.addMapping( self.txtvendedor, VENDEDOR, "text" )
            self.mapper.addMapping( self.txtbodega, BODEGA, "text" )
            self.mapper.addMapping( self.lbltotal, TOTAL, "text" )
            self.mapper.addMapping( self.lblsubtotal, SUBTOTAL, "text" )
            self.mapper.addMapping( self.lbliva, IVA, "text" )
            self.mapper.addMapping( self.dtPicker, FECHA )

    #        asignar los modelos a sus tablas

            self.tablenavigation.setModel( self.navproxymodel )
            self.tabledetails.setModel( self.detailsproxymodel )






            resultado = True
        except UserWarning as inst:
            logging.error( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(),
                                  unicode( inst ) )
            self.status = True
        except Exception as inst:
            logging.critical( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(),
                                  u"Hubo un error al actualizar los datos" )
            self.status = True
        finally:
            if self.database.isOpen():
                self.database.close()


        return resultado


    @property
    def valid( self ):
        """
        Un documento es valido cuando 
        self.printedDocumentNumber != ""
        self.providerId !=0
        self.validLines >0
        self.ivaId !=0
        self.uid != 0
        self.warehouseId != 0
        """
        if int( self.editmodel.datosSesion.usuarioId ) == 0:
            raise Exception( "No existe el usuario" )
        elif int( self.editmodel.clienteId ) == 0:
            QMessageBox.warning( self, qApp.organizationName(),
                                  "Por favor elija el cliente" )
            self.cbcliente.setFocus()
        elif int( self.editmodel.vendedorId ) == 0:
            QMessageBox.warning( self, qApp.organizationName(),
                                 "Por favor elija el vendedor" )
            self.cbvendedor.setFocus()
        elif int( self.editmodel.bodegaId ) == 0:
            QMessageBox.warning( self, qApp.organizationName(),
                                  "Por favor elija la bodega" )
            self.cbbodega.setFocus()
        elif int( self.editmodel.validLines ) == 0:
            QMessageBox.warning( self, qApp.organizationName(),
                              "Por favor complete la información de los artículos comprados" )
        else:
            return True
        return False


class DlgCredito( QDialog ):
    def __init__( self, parent = None ):
        super( DlgCredito, self ).__init__( parent )

        self.dtFechaTope = QDateEdit( QDate.currentDate().addDays( 1 ) )
        self.dtFechaTope.setMinimumDate( QDate.currentDate().addDays( 1 ) )
        """
        @ivar: Este widget tiene la fecha tope en la que puede 
            pagarse el credito
        @type: QDateEdit
        """
        self.sbTaxRate = QDoubleSpinBox()
        """
        @ivar: Este widget contiene la tasa de multa que se
            le aplicara a este credito
        @typ: QDoubleSpinBox
        """

        self.setupUi()

    def setupUi( self ):
        vertical_layout = QVBoxLayout( self )

        form_layout = QFormLayout()

        self.dtFechaTope.setCalendarPopup( True )
        self.sbTaxRate.setSuffix( '%' )

        form_layout.addRow( u"<b>Fecha Tope</b>", self.dtFechaTope )
        form_layout.addRow( u"<b>Tasa de multa</b>", self.sbTaxRate )

        buttonbox = QDialogButtonBox( QDialogButtonBox.Ok |
                                      QDialogButtonBox.Cancel )

        vertical_layout.addLayout( form_layout )
        vertical_layout.addWidget( buttonbox )

        buttonbox.accepted.connect( self.accept )
        buttonbox.rejected.connect( self.reject )




#TODO: Que tipo de conceptos se deberian de mostrar aca?
class DlgAnular( QDialog ):
    def __init__( self , numero, parent = None ):
        super( DlgAnular, self ).__init__( parent )

        self.cboConceptos = QComboBox( self )
        self.cboConceptos.setObjectName( "cboConceptos" )

        self.txtObservaciones = QPlainTextEdit( self )
        self.txtObservaciones.setObjectName( "txtObservaciones" )
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

        self.lblnfactura2.setText( str( self.numero ) )



    def setupUi( self ):
        self.setObjectName( "frmAnulaciones" )
        self.setWindowTitle( "Seleccione la factura a anular" )
        self.resize( 485, 300 )
        gridLayout = QGridLayout( self )
        gridLayout.setObjectName( "gridLayout" )
        lblnfactura = QLabel( self )
        lblnfactura.setObjectName( "lblnfactura" )
        lblnfactura.setText( "# Factura" )
        gridLayout.addWidget( lblnfactura, 0, 0, 1, 1 )
        self.lblnfactura2 = QLabel( self )
        self.lblnfactura2.setFrameShape( QFrame.Box )
        self.lblnfactura2.setText( "" )
        self.lblnfactura2.setObjectName( "lblnfactura2" )
        gridLayout.addWidget( self.lblnfactura2, 0, 1, 1, 1 )
        lblconcepto = QLabel( self )
        lblconcepto.setObjectName( "lblconcepto" )
        lblconcepto.setText( "Concepto" )
        gridLayout.addWidget( lblconcepto, 1, 0, 1, 1 )


        gridLayout.addWidget( self.cboConceptos, 1, 1, 1, 1 )
        lblobservaciones = QLabel( self )
        lblobservaciones.setObjectName( "lblobservaciones" )
        lblobservaciones.setText( "Observaciones" )
        gridLayout.addWidget( lblobservaciones, 2, 0, 1, 1 )


        gridLayout.addWidget( self.txtObservaciones, 3, 1, 1, 1 )
        buttonBox = QDialogButtonBox( self )
        buttonBox.setOrientation( Qt.Horizontal )
        buttonBox.setStandardButtons( QDialogButtonBox.Cancel |
                                      QDialogButtonBox.Ok )
        buttonBox.setObjectName( "buttonBox" )
        gridLayout.addWidget( buttonBox, 4, 0, 1, 2 )

        buttonBox.accepted.connect( self.accept )
        buttonBox.rejected.connect( self.reject )
