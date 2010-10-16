# -*- coding: utf-8 -*-
'''
Created on 25/05/2010
@author: Luis Carlos Mejia
'''
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMainWindow, QDataWidgetMapper, QSortFilterProxyModel, \
QMessageBox, QAbstractItemView, QCompleter, QDialog, qApp
from PyQt4.QtCore import pyqtSlot, Qt, QModelIndex, QTimer, QDate
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase
from decimal import Decimal
from PyQt4.QtSql import  QSqlQuery

from utility.base import Base
from ui.Ui_factura import Ui_frmFactura
from document.factura.facturadelegate import FacturaDelegate
from document.factura.facturamodel import FacturaModel
from utility.moneyfmt import moneyfmt
from recibo import FrmRecibo, dlgRecibo
from utility import constantes

#controles
IDDOCUMENTO, NDOCIMPRESO, CLIENTE, VENDEDOR, SUBTOTAL, IVA, TOTAL, OBSERVACION, FECHA, BODEGA, TASA, TASAIVA, ESTADO, ANULADO, ESCONTADO, TOTALFAC = range( 16 )

#table
IDARTICULO, DESCRIPCION, CANTIDAD, PRECIO, TOTALPROD, IDDOCUMENTOT = range( 6 )
class FrmFactura( Ui_frmFactura, QMainWindow, Base ):
    """
    Implementacion de la interfaz grafica para entrada compra
    """
    web = "facturas.php?doc="
    def __init__( self, parent ):
        '''
        Constructor
        '''
        super( FrmFactura, self ).__init__( parent )
        self.readOnly = True
        self.setupUi( self )
        self.parentWindow = parent
        Base.__init__( self )
        self.__status = True

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
        self.recibo = FrmRecibo(self)  #dlgRecibo( self, True )
        self.recibo.setWindowModality(Qt.WindowModal)
        self.recibo.setWindowFlags(Qt.Dialog)
        self.recibo.parentWindow.removeToolBar(self.recibo.toolBar)
        self.recibo.addToolBar(self.recibo.toolBar)
#        self.recibo.setMaximumHeight(self.recibo.minimumHeight())
        self.toolBar.removeAction( self.actionAnular )
        self.toolBar.addAction( self.actionAnular )


        QTimer.singleShot( 0, self.loadModels )

    def cancel( self ):
        """
        Aca se cancela la edicion del documento
        """
        self.editmodel = None
        self.tablenavigation.setModel( self.navproxymodel )
        self.tabledetails.setModel( self.detailsproxymodel )

        self.readOnly = True
        self.status = True



    def newDocument( self ):
        """
        activar todos los controles, llenar los modelos necesarios, crear el modelo EntradaCompraModel, aniadir una linea a la tabla
        """
        self.readOnly = False
        self.clientesModel = QSqlQueryModel()
        self.existenciaModel = QSqlQueryModel()
        self.vendedoresModel = QSqlQueryModel()
        self.bodegasModel = QSqlQueryModel()


        if not self.updateModels():
#            QMessageBox.critical(self, qApp.organizationName(), "No fue posible crear una nueva factura")
            return

        self.status = False
        self.dtPicker.setDate( self.parentWindow.datosSesion.fecha )

    @property
    def printIdentifier( self ):
        return self.navmodel.record( self.mapper.currentIndex() ).value( "iddocumento" ).toString()

    def addActionsToToolBar( self ):
        self.actionRefresh = self.createAction( text = "Actualizar", icon = ":/icons/res/view-refresh.png", slot = self.refresh, shortcut = Qt.Key_F5 )

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
        if not self.readOnly:
            if QMessageBox.question( self, qApp.organizationName(),
                                      u"Se perderán todos los cambios en la factura. ¿Esta seguro que desea actualizar?", QMessageBox.Yes | QMessageBox.No ) == QMessageBox.No:
                return

        if self.updateModels():
            QMessageBox.information( None, "Factura",
                                 u"Los datos fueron actualizados con éxito" )


    def save( self ):
        """
        Guardar el documento actual
        """
        if not self.valid:
            return

        recibo = None
        if self.editmodel.escontado:
            recibo = dlgRecibo( self )
            if recibo.datosRecibo.retencionValida:
                if recibo.datosRecibo.retencionModel.rowCount() == 0:
                    QMessageBox.warning( None,
                                     qApp.organizationName(),
                                     """No es posible crear un recibo porque no existen retenciones en la base de datos""",
                                     QMessageBox.StandardButtons( \
                                    QMessageBox.Ok ),
                                    QMessageBox.Ok )
                    return
            else:
                recibo.ckretener.setChecked( False )
                recibo.ckretener.setEnabled( False )

            result = -1
            while result not in ( QDialog.Rejected, QDialog.Accepted ):
                result = recibo.exec_()


            if result == QDialog.Rejected:
                return


        if QMessageBox.question( self, qApp.organizationName(), u"¿Esta seguro que desea guardar la factura?", QMessageBox.Yes | QMessageBox.No ) == QMessageBox.Yes:

            if not QSqlDatabase.database().isOpen():
                QSqlDatabase.database().open()

            self.editmodel.observaciones = self.txtobservaciones.toPlainText()
            if self.editmodel.escontado:
                recibo.datosRecibo.observaciones = recibo.txtobservaciones.toPlainText()
            if self.editmodel.save( recibo.datosRecibo if self.editmodel.escontado else None ):
                QMessageBox.information( None,
                     qApp.organizationName() ,
                     u"""El documento se ha guardado con éxito""" )

                self.editmodel = None
                self.readOnly = True
                self.updateModels()
                self.navigate( 'last' )
                self.status = True
            else:
                QMessageBox.critical( None,
                    qApp.organizationName() ,
                     """Ha ocurrido un error al guardar la factura""" )

            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()




    @pyqtSlot()
    def on_actionAnular_activated( self ):
        if self.anulable == 2:
            QMessageBox.warning( None, "Anular Factura",
                                  u"La factura no puede anularse. Solo las facturas confirmadas o en proceso de autorización pueden anularse" )
        elif self.anulable == 3:
            QMessageBox.warning( None, "Anular Factura",
                                  u"La factura no puede anularse porque no es del día de hoy" )
        elif self.anulable == 4:
            QMessageBox.warning( None, "Anular Factura",
                                  u"La factura no puede anularse porque tiene abonos" )
        elif self.anulable == 5:
            QMessageBox.warning( None, "Anular Factura",
                                  u"La factura no puede anularse porque tiene devoluciones" )
        elif self.anulable == 1:

            doc = self.navmodel.record( self.mapper.currentIndex() ).value( "iddocumento" ).toInt()[0]
            estado = self.navmodel.record( self.mapper.currentIndex() ).value( "idestado" ).toInt()[0]
            total = Decimal( self.navmodel.record( self.mapper.currentIndex() ).value( "totalfac" ).toString() )

            try:
                if not QSqlDatabase.database().isOpen():
                    if not QSqlDatabase.database().open():
                        raise Exception( "NO se pudo abrir la Base de datos" )

                if estado == 3:
                    if QMessageBox.question( self, "Anular factura", u"Esta factura no fue confirmada, ¿Desea eliminarla?", QMessageBox.Yes | QMessageBox.No ) == QMessageBox.Yes:
                        query = QSqlQuery()
                        query.prepare( "CALL `esquipulasdb`.`spEliminarFactura`(:doc)" )
                        query.bindValue( ":doc", doc )
                        if not query.exec_():
                            raise Exception( "No se pudo eliminar el la factura" )

                        QMessageBox.information( None, "Anular Factura", "La factura fue eliminada correctamente" )
                        self.updateModels()
                else:
        #            if QDate.currentDate()!=QDate.fromString(self.navmodel.record( self.mapper.currentIndex() ).value( "Fecha" ).toString(),"dd/MM/yyyy"):
        #                QMessageBox.information( None, u"Anulacion invalida", "Esta factura no se puede anular porque no es del dia actual" )
        #            
        #            elif estado==2:
        #                QMessageBox.information( None, "Anulacion invalida", "Esta factura ya ha sido anulada" )
        #                                
        #                            
        #            elif query.value(0)==str(constantes.IDRECIBO):            
        #                QMessageBox.information( None, "Anulacion invalida", "Esta factura tiene un pago, por lo tanto no se puede anular" )
        #                
        #            else:            
    #            
                    if QMessageBox.question( self, qApp.organizationName(), u"¿Esta seguro que desea anular la factura?", QMessageBox.Yes | QMessageBox.No ) == QMessageBox.Yes:
                        nfac = self.navmodel.record( self.mapper.currentIndex() ).value( "No. Factura" ).toString()
                        anulardialog = Anular( nfac )
                        if anulardialog.conceptosmodel.rowCount() == 0:
                            QMessageBox.warning( None, "Anular Factura", u"No existen conceptos para la anulación" )

                        else:
                            if anulardialog.exec_() == QDialog.Accepted:
                                if anulardialog.cboConceptos.currentIndex() == -1 and anulardialog.txtObservaciones.toPlainText() == "":
                                    QMessageBox.critical( self, qApp.organizationName(), "No ingreso los datos correctos", QMessageBox.Ok )
                                else:

                                    query = QSqlQuery()
                                    if not self.database.transaction():
                                        raise Exception( "No se pudo comenzar la transacción" )

                                    #Cambiar estado Anulado=1 para documento
                                    query.prepare( "UPDATE documentos d SET idestado=%d where iddocumento=%d LIMIT 1" % ( constantes.ANULACIONPENDIENTE, doc ) )
                                    if not query.exec_():
                                        raise Exception( "No se logro cambiar el estado a el documento" )

                                    #Insertar documento anulacion
                                    if not query.prepare( """
                                    INSERT INTO documentos(ndocimpreso,total,fechacreacion,idtipodoc,observacion,idestado)
                                    VALUES(:ndocimpreso,:total,NOW(),:idtipodoc,:observacion,:idestado)""" ):
                                        raise Exception( query.lastError().text() )
                                    query.bindValue( ":ndocimpreso", nfac )
                                    query.bindValue( ":total", total.to_eng_string() )
#                                    query.bindValue( ":fechacreacion", QDateTime.currentDateTime().toString('yyyyMMddhhmmss') )
                                    query.bindValue( ":idtipodoc", constantes.IDANULACION )
                                    query.bindValue( ":observacion", anulardialog.txtObservaciones.toPlainText() )
                                    query.bindValue( ":idestado", constantes.PENDIENTE )

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


                                    if not query.prepare( "INSERT INTO personasxdocumento (idpersona,iddocumento,idaccion) VALUES" +
                                    "(:usuario," + insertedId + ",:accion)" ):
                                        raise Exception( query.lastError().text() + "No se inserto el usuario y autoriza" )

                                    query.bindValue( ":usuario", self.parentWindow.datosSesion.usuarioId )
                                    query.bindValue ( ":accion", constantes.AUTOR )

                                    if not query.exec_():
                                        raise Exception( "No se pudo Insertar la relacion de la anulacion con el usuario" )


                                    if not self.database.commit():
                                        raise Exception( "NO se hizo el commit para la Anulacion" )
                                    QMessageBox.information( self, qApp.organizationName(), "Factura anulada Correctamente", QMessageBox.Ok )
                                    self.updateModels()

            except Exception as inst:
                print inst
                print query.lastError().text()
                self.database.rollback()
            finally:
                if QSqlDatabase.database().isOpen():
                    QSqlDatabase.database().close()

    @pyqtSlot()
    def on_actionRecibo_activated( self ):
        self.recibo.remoteProxyModel.setFilterRegExp("(%s)"%self.navmodel.record( self.mapper.currentIndex() ).value( "iddocumento" ).toString() )
        self.recibo.show()

    @pyqtSlot( "int" )
    def on_cboFiltro_currentIndexChanged( self, index ):
        """
        asignar la bodega al objeto self.editmodel

        """
        self.navproxymodel.setFilterKeyColumn( ANULADO )
        if index == 0:
            self.navproxymodel.setFilterRegExp( "" )
        else:
            self.navproxymodel.setFilterRegExp( "^%d$" % index )

    @pyqtSlot( "int" )
    def on_cbbodega_currentIndexChanged( self, index ):
        """
        asignar la bodega al objeto self.editmodel
        """
        if not self.editmodel is None:
            if self.editmodel.rowCount() > 0 and self.editmodel.lines[0].itemDescription != "":
                for line in self.editmodel.lines:
                    if line.itemId > 0 :
                        self.tabledetails.itemDelegate().filtrados = []
                self.editmodel.removeRows( 0, self.editmodel.rowCount() )
                self.editmodel.insertRow( 0 )

            self.editmodel.bodegaId = self.bodegasModel.record( index ).value( "idbodega" ).toInt()[0]
            self.proxyexistenciaModel.setFilterRegExp( '^%d$' % self.editmodel.bodegaId )
            self.tabledetails.setColumnHidden( IDARTICULO, True )
            self.updateLabels()



    @pyqtSlot( "int" )
    def on_cbcliente_currentIndexChanged( self, index ):
        """
        asignar proveedor al objeto self.editmodel
        """
        if not self.editmodel is None:
            self.editmodel.clienteId = self.clientesModel.record( index ).value( "idpersona" ).toInt()[0]

    @pyqtSlot( "int" )
    def on_cbvendedor_currentIndexChanged( self, index ):
        """
        asignar proveedor al objeto self.editmodel
        """
        if not self.editmodel is None:
            self.editmodel.vendedorId = self.vendedoresModel.record( index ).value( "idpersona" ).toInt()[0]


    @pyqtSlot( "QDateTime" )
    def on_dtPicker_dateTimeChanged( self, datetime ):
        pass

# MANEJO EL EVENTO  DE SELECCION EN EL RADIOBUTTON
    @pyqtSlot( "bool" )
    def on_rbcontado_toggled( self, on ):
        """
        Asignar las observaciones al objeto __qdocument
        """
        if not self.editmodel is None:
            self.editmodel.escontado = 1 if on else 0
#        else:
#            self.btnrecibo.setHidden(not on)


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
        if status:
            self.navigate( 'last' )
            self.swcliente.setCurrentIndex( 1 )
            self.swbodega.setCurrentIndex( 1 )
            self.swvendedor.setCurrentIndex( 1 )
            self.tabledetails.setEditTriggers( QAbstractItemView.NoEditTriggers )
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
            self.tabledetails.setEditTriggers( QAbstractItemView.EditKeyPressed
                                               | QAbstractItemView.AnyKeyPressed | QAbstractItemView.DoubleClicked )
            self.lblanulado.setHidden( True )

#            self.tabledetails.horizontalHeader().setStretchLastSection(True)

        self.tabledetails.setColumnHidden( IDARTICULO, True )
        self.tabledetails.setColumnHidden( IDDOCUMENTOT, True )

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

    def updateDetailFilter( self, index ):
        self.lbltasaiva.setText( self.navmodel.record( index ).value( "tasaiva" ).toString() + '%' )
        self.lblanulado.setHidden( self.navmodel.record( index ).value( "idestado" ).toInt()[0] != constantes.ANULADO )
        self.anulable = self.navmodel.record( index ).value( "anulable" ).toInt()[0]
#        self.actionAnular.setEnabled()
        self.dtPicker.setDate( QDate.fromString( self.navmodel.record( index ).value( "Fecha" ).toString(), "dd/MM/yyyy" ) )
        escontado = self.navmodel.record( index ).value( "escontado" ).toBool()
        if escontado:
            self.rbcontado.setChecked( True )

        else:
            self.rbcredito.setChecked( True )
#            self.recibo.setHidden(True)

        self.detailsproxymodel.setFilterKeyColumn( IDDOCUMENTOT )
#        print self.navmodel.record( index ).value( "iddocumento" ).toString() 
        self.detailsproxymodel.setFilterRegExp( self.navmodel.record( index ).value( "iddocumento" ).toString() )
        self.tablenavigation.selectRow( self.mapper.currentIndex() )

    def updateLabels( self ):
        self.lblsubtotal.setText( moneyfmt( self.editmodel.subtotal, 4, "US$ " ) )
        self.lbliva.setText( moneyfmt( self.editmodel.IVA, 4, "US$ " ) )
        self.lbltotal.setText( moneyfmt( self.editmodel.total, 4, "US$ " ) )
        self.lbltasaiva.setText( ( '0' if self.editmodel.bodegaId <> 1 else str( self.editmodel.ivaTasa ) ) + '%' )
        self.tabledetails.resizeColumnsToContents()

    def updateModels( self ):
        """
        Recargar todos los modelos
        """

        try:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open():
                    QMessageBox.warning( None,
                    qApp.organizationName(),
                    """Hubo un error al conectarse con la base de datos""",
                    QMessageBox.StandardButtons( \
                        QMessageBox.Ok ),
                    QMessageBox.Ok )
                    raise Exception( u"No se pudo establecer la conexión con la base de datos" )

            if self.readOnly:
#        El modelo principal

                query ="""
                SELECT
                        d.iddocumento,
                        d.ndocimpreso as 'No. Factura',
                        GROUP_CONCAT(IF(pxd.idaccion=%d,p.nombre,"") SEPARATOR '') as Cliente,
                        GROUP_CONCAT(IF(pxd.idaccion=%d,p.nombre,"") SEPARATOR '') as Vendedor,
                        CONCAT('US$ ',FORMAT(ROUND(d.total / (1+ IF(valorcosto IS NULL,0,valorcosto/100)),4),4))  as subtotal,
                        CONCAT('US$ ',FORMAT(d.total- ROUND(d.total / (1+ IF(valorcosto IS NULL,0,valorcosto/100)),4),4))  as iva,
                        CONCAT('US$ ',FORMAT(d.Total,4)) as Total,
                        d.observacion,
                        %s as Fecha,
                        b.nombrebodega as Bodega,
                        tc.tasa as 'Tipo de Cambio Oficial',
                        valorcosto as tasaiva,
                        ed.descripcion as Estado,
                        d.idestado,
                        d.escontado,
                        d.total as totalfac,
                        fnFacturaAnulable(d.iddocumento,d.idtipodoc,%d,%d,%d,%d) as anulable
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
                """ % ( constantes.CLIENTE, constantes.VENDEDOR, "DATE_FORMAT(d.fechacreacion,'%d/%m/%Y')", constantes.IDRECIBO, constantes.IDNC, constantes.CONFIRMADO, constantes.PENDIENTE, constantes.IDFACTURA ) 
                print query  
                self.navmodel.setQuery( query)
                


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

#
#                self.mapper.addMapping( self.recibo.lbltotal, TOTAL, "text" )
#                self.mapper.addMapping( self.recibo.txtcliente, CLIENTE, "text" )
#                self.mapper.addMapping( self.recibo.lblfecha, FECHA, "text" )

        #        asignar los modelos a sus tablas

                self.tablenavigation.setModel( self.navproxymodel )
                self.tabledetails.setModel( self.detailsproxymodel )

                self.tablenavigation.setColumnHidden( IDDOCUMENTO, True )
                self.tablenavigation.setColumnHidden( OBSERVACION, True )
                self.tablenavigation.setColumnHidden( SUBTOTAL, True )
                self.tablenavigation.setColumnHidden( IVA, True )
                self.tablenavigation.setColumnHidden( TASAIVA, True )
                self.tablenavigation.setColumnHidden( TASA, True )
                self.tablenavigation.setColumnHidden( ESCONTADO, True )
                self.tablenavigation.setColumnHidden( ANULADO, True )
                self.tablenavigation.setColumnHidden( TOTALFAC, True )

            else:

        #            Rellenar el combobox de los CLLIENTES 
                self.editmodel = FacturaModel( self.parentWindow.datosSesion )

            #           Cargar el numero de la factura actual
                query = QSqlQuery( """
                            SELECT fnConsecutivo(5,NULL);
                        """ )
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
                    QMessageBox.information( None, "Factura", "No existen clientes en la base de datos" )
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
                    QMessageBox.information( None, "Factura", "No existen vendedores en la base de datos" )
                    return

            #Crear el delegado con los articulo y verificar si existen articulos
                self.existenciaModel.setQuery( QSqlQuery( """
                            SELECT
                    idarticulo,
                    descripcion,
                    precio,
                    costodolar,
                    ROUND(costo,4) as costo,
                    Existencia,
                    idbodega
                FROM vw_articulosenbodegas
                 WHERE existencia >0
                        """ ) )
                self.proxyexistenciaModel = QSortFilterProxyModel()
                self.proxyexistenciaModel.setSourceModel( self.existenciaModel )
                self.proxyexistenciaModel.setFilterKeyColumn( 6 )

                delegate = FacturaDelegate( self.proxyexistenciaModel )
                if delegate.proxymodel.rowCount() == 0:
                    QMessageBox.information( None, "Factura", "No hay articulos en existencia" )
                    return

        #            Rellenar el combobox de las BODEGAS

                self.bodegasModel.setQuery( """
                         SELECT
                                b.idbodega,
                                b.nombrebodega as Bodega
                        FROM bodegas b
                        JOIN documentos d ON b.idbodega=d.idbodega
                        JOIN docpadrehijos ph ON ph.idpadre =d.iddocumento
                        JOIN documentos k ON ph.idhijo = k.iddocumento AND k.idtipodoc = 27
                JOIN articulosxdocumento ad ON ad.iddocumento=d.iddocumento
                GROUP BY b.idbodega
                HAVING SUM(ad.unidades)>0    
                        """ )

            #Verificar si existen bodegas            
                if self.bodegasModel.rowCount() == 0:
                            QMessageBox.information( None, "Factura", "No existe ninguna bodega en la base de datos" )
                            return

        #Verificar IVA    
                query = QSqlQuery( """
                        SELECT idcostoagregado, valorcosto 
                        FROM costosagregados c 
                        WHERE idtipocosto = 1 AND activo = 1 
                        ORDER BY idtipocosto;
                        """ )
                query.exec_()
                if not query.size() == 1:
                    QMessageBox.information( None, "Factura", "No fue posible obtener el porcentaje del IVA" )
                    return
                query.first()


                self.editmodel.ivaId = query.value( 0 ).toInt()[0]
                self.lbltasaiva.setText( ( '0' if self.editmodel.bodegaId <> 1 else str( self.editmodel.ivaTasa ) ) + '%' )
                self.editmodel.ivaTasa = Decimal( query.value( 1 ).toString() )


                self.tabledetails.setItemDelegate( delegate )


                self.cbcliente.setModel( self.clientesModel )
                self.cbcliente.setCurrentIndex( -1 )
                self.cbcliente.setFocus()
                self.cbcliente.setModelColumn( 1 )
                self.completer = QCompleter()
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
                self.completerVendedor = QCompleter()
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
        except Exception as inst:
            print inst
            self.status = True
            resultado = False
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()

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
            QMessageBox.warning( None, "Factura Incompleta", "Por favor elija el cliente" )
            self.cbcliente.setFocus()
        elif int( self.editmodel.vendedorId ) == 0:
            QMessageBox.warning( None, "Factura Incompleta", "Por favor elija el vendedor" )
            self.cbvendedor.setFocus()
        elif int( self.editmodel.bodegaId ) == 0:
            QMessageBox.warning( None, "Factura Incompleta", "Por favor elija la bodega" )
            self.cbbodega.setFocus()
        elif int( self.editmodel.validLines ) == 0:
            QMessageBox.warning( None, "Factura Incompleta", "Algunas filas de la factura estan incompletas" )
        else:
            return True
        return False

#class RONavigationModel( QSortFilterProxyModel ):
#    """
#    basicamente le da formato a la salida de mapper
#    """
#    def data( self, index, role = Qt.DisplayRole ):
#        """
#        Esta funcion redefine data en la clase base, es el metodo que se utiliza para mostrar los datos del modelo
#        """
#        value = QSortFilterProxyModel.data( self, index, role )
#        if value.isValid() and role in ( Qt.EditRole, Qt.DisplayRole):
#            if index.column() in ( SUBTOTAL, IVA, TOTAL ):
#                return moneyfmt( Decimal( value.toString() ), 4, "US$" )
#            elif index.column() == ANULADO:
#                if role == Qt.DisplayRole:
#                    return "Anulada" if value.toInt()[0]==1 else ""
#                
#        return value
#
#class RODetailsModel( QSortFilterProxyModel ):
#    """
#    El modelo que maneja la tabla en la que se previsualizan los os,
#    basicamente esta creado para darle formato al total y al precio
#    """
#    def __init__( self, dbcursor = None ):
#        super( QSortFilterProxyModel, self ).__init__()
#
#    def columnCount( self, index = QModelIndex() ):
#        return 5
#
#    def headerData( self, section, orientation, role = Qt.DisplayRole ):
#        if role == Qt.TextAlignmentRole:
#            if orientation == Qt.Horizontal:
#                return int( Qt.AlignLeft | Qt.AlignVCenter )
#            return int( Qt.AlignRight | Qt.AlignVCenter )
#        if role != Qt.DisplayRole:
#            return None
#        if orientation == Qt.Horizontal:
#            if  section == DESCRIPCION:
#                return u"Descripción"
#            elif section == PRECIO:
#                return "Precio"
#            elif section == TOTALPROD:
#                return "TOTAL"
#            elif section == CANTIDAD:
#                return "Cantidad"
#        return int( section + 1 )
#
#    def data( self, index, role = Qt.DisplayRole ):
#        """
#        Esta funcion redefine data en la clase base, es el metodo que se utiliza para mostrar los datos del modelo
#        """
#        value = QSortFilterProxyModel.data( self, index, role )
#        if value.isValid() and role == Qt.DisplayRole:
#            if index.column() in ( TOTALPROD, PRECIO ):
#                return moneyfmt( Decimal( value.toString() ), 4, "US$" )
#        return value



#TODO: Que tipo de conceptos se deberian de mostrar aca?
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

        self.lblnfactura2.setText( str( self.numero ) )
        self.buttonBox.accepted.connect( self.accept )
        self.buttonBox.rejected.connect( self.reject )


    def setupUi( self ):
        self.setObjectName( "frmAnulaciones" )
        self.setWindowTitle( "Seleccione la factura a anular" )
        self.resize( 485, 300 )
        self.gridLayout = QtGui.QGridLayout( self )
        self.gridLayout.setObjectName( "gridLayout" )
        self.lblnfactura = QtGui.QLabel( self )
        self.lblnfactura.setObjectName( "lblnfactura" )
        self.lblnfactura.setText( "# Factura" )
        self.gridLayout.addWidget( self.lblnfactura, 0, 0, 1, 1 )
        self.lblnfactura2 = QtGui.QLabel( self )
        self.lblnfactura2.setFrameShape( QtGui.QFrame.Box )
        self.lblnfactura2.setText( "" )
        self.lblnfactura2.setObjectName( "lblnfactura2" )
        self.gridLayout.addWidget( self.lblnfactura2, 0, 1, 1, 1 )
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
        self.buttonBox.setStandardButtons( QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok )
        self.buttonBox.setObjectName( "buttonBox" )
        self.gridLayout.addWidget( self.buttonBox, 4, 0, 1, 2 )
